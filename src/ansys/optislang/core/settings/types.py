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

"""Contains base settings classes."""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Generic, Literal, Optional, TypeVar, Union

from ansys.optislang.core.io import AbsolutePath, OptislangPath

T = TypeVar("T")
E = TypeVar("E", bound=Enum)


class SettingsSerializer(ABC):
    """Abstract interface for settings serialization.

    Responsible for converting normalized property values
    into a transport-specific representation (e.g. TCP).
    """

    @abstractmethod
    def serialize(self, prop, value: Any) -> Any:
        """Serialize a single property value.

        Parameters
        ----------
        prop: SettingProperty
            Property definition metadata
        value: Any
            Validated and normalized value

        Returns
        -------
        Any
            Transport specific representation of the value
        """
        pass


class SettingInstance(Generic[T]):

    def __init__(self, prop: SettingProperty[T]):
        self._prop = prop
        self._value: T | None = None

    @property
    def name(self) -> str:
        return self._prop.name

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, v: T):
        self._prop.validator(v)
        self._value = v

    def prepare(self, serializer: SettingsSerializer):
        transformed = self._prop.transform(self._value)
        return self._prop.name, serializer.serialize(self._prop, transformed)


class SettingProperty(Generic[T]):

    def __init__(
        self,
        name: str,
        default: Any = None,
        *,
        validator: Optional[Callable[[Any], None]] = None,
        transform: Optional[Callable[[Any], Any]] = None,
        serialization_style: Optional[str] = None,
    ):
        self.name = name
        self.default = default
        self.validator = validator or (lambda x: x)
        self.transform = transform or (lambda x: x)
        self.serialization_style = serialization_style

    def __call__(self: SettingProperty[T]) -> SettingInstance[T]:
        return SettingInstance(self)

    def __set_name__(self, owner, attr_name: str):
        self.attr_name = attr_name
        self.private_name = f"_{attr_name}"

    def __get__(self, instance, owner) -> T:
        if instance is None:
            return self

        if hasattr(instance, self.private_name):
            return getattr(instance, self.private_name, self.default)

        return self.default

    def __set__(self, instance, value):
        self.validator(value)
        value = self.transform(value)
        setattr(instance, self.private_name, value)


class TypedSetting(SettingProperty[T]):

    def __init__(self, name, type_, default=None, **kwargs):
        def validator(value):
            if value is not None and not isinstance(value, type_):
                raise TypeError(f"{name} must be {type_}, got {type(value)}.")

        super().__init__(name, default=default, validator=validator, **kwargs)


class ChoiceSetting(SettingProperty[T]):

    def __init__(self, name: str, options: list[T], default: T = None, **kwargs):
        self.options = list(options)
        self.type_hint = Literal[tuple(options)]

        def validator(value):
            if value is not None and value not in options:
                raise ValueError(f"{name} must be one of {options}, got {value}")

        super().__init__(
            name,
            default=default,
            validator=validator,
            serialization_style="value-wrapper",
            **kwargs,
        )


class EnumSetting(SettingProperty[E], Generic[E]):

    def __init__(self, name: str, enum_cls: type[E], default=None, **kwargs):
        self.enum_cls = enum_cls
        self.options = [e.value for e in enum_cls]

        def validator(value):
            if value is None:
                return
            if isinstance(value, enum_cls):
                return
            if value in self.options:
                return
            raise ValueError(f"{name} must be {list(enum_cls)} or matching value, got {value}")

        def transform(value):
            if value is None:
                return None

            if isinstance(value, enum_cls):
                return value.name.lower()

            if isinstance(value, str):
                return value.lower()

            raise TypeError(f"{name} must be {enum_cls} or str, got {value}")

        super().__init__(
            name,
            default=(
                default.name.lower()
                if isinstance(default, enum_cls)
                else default.lower() if isinstance(default, str) else default
            ),
            validator=validator,
            transform=transform,
            serialization_style="value-wrapper",
            **kwargs,
        )


class PathSetting(SettingProperty[Union[str, Path, OptislangPath]]):

    def __init__(self, name: str, *, export_mode: str = "dict", **kwargs):
        """
        Parameters
        ----------
        name : str
            Key used in the exported dictionary
        export_mode : str, optional
            ["dict" or "str"], by default "dict"
        """
        self.export_mode = export_mode

        def transform(value: Optional[Union[str, Path, OptislangPath]]):
            if value is None:
                return None
            if isinstance(value, OptislangPath):
                return value
            return AbsolutePath(value)

        def validator(value):
            if value is None:
                return
            if not isinstance(value, (str, Path, OptislangPath)):
                raise TypeError(f"{name} must be str, Path or OptislangPath, got {type(value)}")

        super().__init__(name, validator=validator, transform=transform, **kwargs)

    def serialize(self, value):
        if value is None:
            return None

        if self.export_mode == "dict":
            return value.to_dict()
        else:
            return str(value)


class SettingModel:

    def __init__(self):
        self._modified = False

    def __setattr__(self, name, value):
        cls = type(self)
        prop = getattr(cls, name, None)

        if isinstance(prop, SettingProperty):
            prop.__set__(self, value)
            object.__setattr__(self, "_modified", True)
            return
        object.__setattr__(self, name, value)

    @classmethod
    def _iter_settings(cls):
        for base in reversed(cls.__mro__):
            for name, attr in base.__dict__.items():
                if isinstance(attr, SettingProperty):
                    yield name, attr

    def is_modified(self):
        return getattr(self, "_modified", False)

    def to_dict(self, serializer: SettingsSerializer, *, modified_only: bool = False):
        properties = {}

        for attr_name, prop in self._iter_settings():

            if modified_only and not hasattr(self, prop.private_name):
                continue

            value = getattr(self, attr_name)

            if isinstance(value, SettingModel):
                properties[prop.name] = value.to_dict(
                    serializer=serializer, modified_only=modified_only
                )
                continue
            properties[prop.name] = serializer.serialize(prop, value)

        return properties


class ModelSetting(SettingProperty[T]):
    """Property representing nested SettingModel."""

    def __init__(
        self,
        name: str,
        model_cls: type[T],
        *,
        default_factory=None,
        force_all: bool = True,
        **kwargs,
    ):
        self.model_cls = model_cls
        self.default_factory = default_factory or model_cls
        self.force_all = force_all

        def validator(value):
            if value is None:
                return
            if not isinstance(value, model_cls):
                raise TypeError(f"{name} must be instance of {model_cls.__name__}")

        super().__init__(name, default=None, validator=validator, **kwargs)

    def __get__(self, instance, owner):
        if instance is None:
            return self

        # do not create model unless accessed
        value = getattr(instance, self.private_name, None)

        if value is None:
            value = self.default_factory()
            value._parent_property = self
            setattr(instance, self.private_name, value)

        return value
