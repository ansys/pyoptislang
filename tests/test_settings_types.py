# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from pathlib import Path

import pytest

from ansys.optislang.core.io import AbsolutePath
from ansys.optislang.core.settings.enums import AutoSaveMode
from ansys.optislang.core.settings.types import (
    ChoiceSetting,
    EnumSetting,
    ModelSetting,
    PathSetting,
    SerializationMode,
    SettingModel,
    SettingProperty,
    SettingsSerializer,
    TypedSetting,
)
from ansys.optislang.core.tcp.settings import TcpSerializer


class _MockedSerializer(SettingsSerializer):
    def __init__(self):
        self.calls = []

    def serialize(self, prop, value):
        self.calls.append((prop.name, value))
        return {"name": prop.name, "value": value}


def test_setting_property_call_creates_setting_instance_and_validates_argument_count():
    prop = SettingProperty("my_setting")

    assert prop.serialization_mode == SerializationMode.DEFAULT

    empty = prop()
    assert empty.name == "my_setting"
    assert empty.value is None

    initialized = prop(123)
    assert initialized.name == "my_setting"
    assert initialized.value == 123

    with pytest.raises(TypeError, match="Expected at most one value"):
        prop(1, 2)


def test_setting_instance_serialize_value_applies_transform_before_serializer():
    prop = SettingProperty("value", transform=lambda x: x + 1)
    instance = prop(41)
    serializer = _MockedSerializer()

    serialized = instance._serialize_value(serializer)

    assert serialized == {"name": "value", "value": 42}
    assert serializer.calls == [("value", 42)]


def test_tcp_serializer_default_mode_has_no_special_wrapping():
    prop = SettingProperty("plain")
    serializer = TcpSerializer()

    serialized = serializer.serialize(prop, 7)

    assert serialized == 7


def test_setting_model_descriptor_default_access_and_modified_flag():
    class _Model(SettingModel):
        count = TypedSetting("count", int, 5)

    model = _Model()
    assert model.count == 5
    assert model.is_modified() is False

    model.count = 6
    assert model.count == 6
    assert model.is_modified() is True


def test_typed_setting_rejects_invalid_type():
    class _Model(SettingModel):
        count = TypedSetting("count", int)

    model = _Model()
    with pytest.raises(TypeError, match="count must be"):
        model.count = "not-int"


def test_choice_setting_validates_options_and_uses_value_wrapper_style():
    class _Model(SettingModel):
        mode = ChoiceSetting("mode", ["a", "b"], default="a")

    model = _Model()
    assert model.mode == "a"
    assert _Model.mode.serialization_mode == SerializationMode.VALUE_WRAPPER

    model.mode = "b"
    assert model.mode == "b"

    with pytest.raises(ValueError, match="must be one of"):
        model.mode = "c"


def test_enum_setting_normalizes_default_and_assigned_values():
    class _Model(SettingModel):
        auto_save_mode = EnumSetting("AutoSaveMode", AutoSaveMode, AutoSaveMode.NO_AUTO_SAVE)

    model = _Model()
    assert model.auto_save_mode == "no_auto_save"

    model.auto_save_mode = AutoSaveMode.AS_ACTOR_FINISHED
    assert model.auto_save_mode == "as_actor_finished"

    model.auto_save_mode = "as_algo_iteration_finished"
    assert model.auto_save_mode == "as_algo_iteration_finished"


def test_enum_setting_rejects_invalid_value():
    class _Model(SettingModel):
        auto_save_mode = EnumSetting("AutoSaveMode", AutoSaveMode)

    model = _Model()
    with pytest.raises(ValueError, match="must be"):
        model.auto_save_mode = "invalid"


def test_path_setting_transforms_to_absolute_path_and_validates_input_type():
    class _Model(SettingModel):
        path = PathSetting("path")

    model = _Model()
    model.path = Path("my_folder") / "my_file.txt"
    assert isinstance(model.path, AbsolutePath)

    with pytest.raises(TypeError, match="must be str, Path or OptislangPath"):
        model.path = 123


def test_path_setting_serialization_dict_and_string_modes():
    dict_prop = PathSetting("path", export_mode=SerializationMode.PATH_DICT)
    str_prop = PathSetting("path", export_mode=SerializationMode.PATH_STR)
    absolute_path = AbsolutePath(Path("folder") / "file.txt")

    dict_serialized = dict_prop.serialize(absolute_path)
    str_serialized = str_prop.serialize(absolute_path)

    assert isinstance(dict_serialized, dict)
    assert "path" in dict_serialized
    assert str_serialized == str(absolute_path)


def test_path_setting_rejects_non_enum_export_mode():
    with pytest.raises(TypeError, match="Expected SerializationMode"):
        PathSetting("path", export_mode="dict")


def test_model_setting_lazy_instantiation_and_type_validation():
    class _Child(SettingModel):
        value = TypedSetting("value", int, 1)

    class _Parent(SettingModel):
        child = ModelSetting("child", _Child)

    parent = _Parent()
    assert hasattr(parent, "_child") is False

    child = parent.child
    assert isinstance(child, _Child)
    assert hasattr(parent, "_child") is True
    assert parent.child._parent_property is _Parent.child

    with pytest.raises(TypeError, match="child must be instance of"):
        parent.child = object()


def test_setting_model_iter_settings_includes_base_and_derived_descriptors():
    class _Base(SettingModel):
        base_prop = TypedSetting("base_prop", int, 1)

    class _Derived(_Base):
        derived_prop = TypedSetting("derived_prop", int, 2)

    names = [name for name, _ in _Derived._iter_settings()]
    assert names == ["base_prop", "derived_prop"]


def test_setting_model_serialize_supports_modified_only_and_nested_models():
    class _Child(SettingModel):
        count = TypedSetting("count", int, 0)

    class _Parent(SettingModel):
        mode = ChoiceSetting("mode", ["off", "on"], default="off")
        child = ModelSetting("child", _Child)

    parent = _Parent()
    serializer = TcpSerializer()

    assert parent.serialize(serializer=serializer, modified_only=True) == {}

    parent.mode = "on"
    assert parent.serialize(serializer=serializer, modified_only=True) == {"mode": {"value": "on"}}

    parent.child.count = 3
    assert parent.serialize(serializer=serializer, modified_only=True) == {
        "mode": {"value": "on"},
        "child": {"count": 3},
    }
