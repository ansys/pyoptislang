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


class SerializationMode(str, Enum):
    """Serialization mode for setting values."""

    DEFAULT = "default"
    VALUE_WRAPPER = "value-wrapper"
    PATH_DICT = "path-dict"
    PATH_STR = "path-str"


def _coerce_serialization_mode(value: Optional[SerializationMode]) -> SerializationMode:
    """Validate and normalize ``SerializationMode`` input."""
    if value is None:
        return SerializationMode.DEFAULT

    if isinstance(value, SerializationMode):
        return value

    valid_values = [mode.value for mode in SerializationMode]
    raise TypeError(
        f"Unsupported serialization mode '{value}'. "
        f"Expected SerializationMode, one of: {valid_values}."
    )


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
        """Instance of a setting property with an optional assigned value.

        Parameters
        ----------
        prop: SettingProperty[T]
            Property definition metadata
        """
        self._prop = prop
        self._value: T | None = None

    @property
    def name(self) -> str:
        """Name of the setting property.

        Returns
        -------
        str
            Name of the setting property
        """
        return self._prop.name

    @property
    def value(self) -> T:
        """Value of the setting instance.

        Returns
        -------
        T
            Current value of the setting instance
        """
        return self._value

    @value.setter
    def value(self, v: T):
        """Set the value of the setting instance.

        Parameters
        ----------
        v: T
            New value to assign to the setting instance
        """
        self._prop.validator(v)
        self._value = v

    def _serialize_value(self, serializer: SettingsSerializer) -> Any:
        """Serialize this setting instance value for transport.

        This method applies the setting's value transform and then delegates
        serialization to the provided serializer.
        """
        transformed = self._prop.transform(self._value)
        return serializer.serialize(self._prop, transformed)


class SettingProperty(Generic[T]):
    """Base descriptor for a setting property."""

    def __init__(
        self,
        name: str,
        default: Any = None,
        *,
        validator: Optional[Callable[[Any], None]] = None,
        transform: Optional[Callable[[Any], Any]] = None,
        serialization_mode: SerializationMode = SerializationMode.DEFAULT,
    ):
        """Initialize the setting property.

        Parameters
        ----------
        name: str
            Name of the setting property
        default: Any, optional
            Default value of the setting property
        validator: Callable[[Any], None], optional
            Function to validate the value
        transform: Callable[[Any], Any], optional
            Function to transform the value before serialization
        serialization_mode: SerializationMode, optional
            Mode to use during serialization. ``SerializationMode.DEFAULT``
            means no special serializer treatment.
        """
        self.name = name
        self.default = default
        self.validator = validator or (lambda x: x)
        self.transform = transform or (lambda x: x)
        self.serialization_mode = _coerce_serialization_mode(serialization_mode)

    def __call__(self: SettingProperty[T], *args: Any) -> SettingInstance[T]:
        """Create a setting instance and optionally assign an initial value.

        Examples
        --------
        ``prop()`` creates an empty instance.
        ``prop(value)`` creates an instance with ``value`` already assigned.
        """
        if len(args) > 1:
            raise TypeError(f"Expected at most one value for '{self.name}', got {len(args)}")

        instance = SettingInstance(self)
        if len(args) == 1:
            instance.value = args[0]
        return instance

    def __set_name__(self, owner, attr_name: str):
        """Set the name of the attribute in the owner class."""
        self.attr_name = attr_name
        self.private_name = f"_{attr_name}"

    def __get__(self, instance, owner) -> T:
        """Get the value of the setting property from the instance."""
        if instance is None:
            return self

        if hasattr(instance, self.private_name):
            return getattr(instance, self.private_name, self.default)

        return self.default

    def __set__(self, instance, value):
        """Set the value of the setting property on the instance."""
        self.validator(value)
        value = self.transform(value)
        setattr(instance, self.private_name, value)


class TypedSetting(SettingProperty[T]):
    """Property that enforces a specific type for its value."""

    def __init__(self, name, type_, default=None, **kwargs):
        """Initialize a typed setting property.

        Parameters
        ----------
        name : str
            Name of the setting property.
        type_ : type
            Expected type of the setting property's value.
        default : Any, optional
            Default value of the setting property.
        **kwargs : Any
            Additional keyword arguments passed to the base class.
        """
        self.type_ = type_

        def validator(value):
            if value is not None and not isinstance(value, type_):
                raise TypeError(f"{name} must be {type_}, got {type(value)}.")

        super().__init__(name, default=default, validator=validator, **kwargs)


class ChoiceSetting(SettingProperty[T]):
    """Property that restricts its value to a predefined set of options."""

    def __init__(self, name: str, options: list[T], default: T = None, **kwargs):
        """Initialize a choice setting property.

        Parameters
        ----------
        name : str
            Name of the setting property.
        options : list[T]
            List of valid options for the setting property's value.
        default : T, optional
            Default value of the setting property.
        **kwargs : Any
            Additional keyword arguments passed to the base class.
        """
        self.options = list(options)
        self.type_hint = Literal[tuple(options)]

        def validator(value):
            if value is not None and value not in options:
                raise ValueError(f"{name} must be one of {options}, got {value}")

        super().__init__(
            name,
            default=default,
            validator=validator,
            serialization_mode=SerializationMode.VALUE_WRAPPER,
            **kwargs,
        )


class EnumSetting(SettingProperty[E], Generic[E]):
    """Property that restricts its value to a specific Enum type.

    Notes
    -----
    - The EnumSetting class is designed to accept either an instance of the Enum
    or a string that matches one of the Enum's values.
    - The value is transformed to a lowercase string representation
    of the Enum name for serialization.
    """

    def __init__(self, name: str, enum_cls: type[E], default=None, **kwargs):
        """Initialize an enum setting property.

        Parameters
        ----------
        name : str
            Name of the setting property.
        enum_cls : type[E]
            Enum class defining the valid options for the setting property's value.
        default : E, optional
            Default value of the setting property.
        **kwargs : Any
            Additional keyword arguments passed to the base class.
        """
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
            serialization_mode=SerializationMode.VALUE_WRAPPER,
            **kwargs,
        )


class PathSetting(SettingProperty[Union[str, Path, OptislangPath]]):
    """Property that represents a file system path.

    Notes
    -----
    - The PathSetting class is designed to accept a string, a Path object,
    or an OptislangPath object as its value.
    - The value is transformed to an AbsolutePath for serialization.
    - The export_mode parameter controls whether the serialized output is a dictionary or a string.
    """

    def __init__(
        self,
        name: str,
        *,
        export_mode: SerializationMode = SerializationMode.PATH_DICT,
        **kwargs,
    ):
        """Initialize a path setting property.

        Parameters
        ----------
        name : str
            Key used in the exported dictionary
        export_mode : SerializationMode, optional
            Path export mode.
        """
        self.export_mode = _coerce_serialization_mode(export_mode)
        if self.export_mode not in (SerializationMode.PATH_DICT, SerializationMode.PATH_STR):
            raise ValueError(
                "PathSetting export_mode must be "
                "SerializationMode.PATH_DICT or SerializationMode.PATH_STR."
            )

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

        super().__init__(
            name,
            validator=validator,
            transform=transform,
            serialization_mode=self.export_mode,
            **kwargs,
        )

    def serialize(self, value):
        if value is None:
            return None

        if self.export_mode == SerializationMode.PATH_DICT:
            return value.to_dict()
        else:
            return str(value)


class SettingModel:
    """Base class for a model containing multiple settings.

    Notes
    -----
    - The SettingModel class is designed to be subclassed to define specific models
    with various settings.
    - It provides mechanisms for lazy instantiation of nested models, type validation,
    and serialization of settings.
    """

    def __init__(self):
        """Initialize the SettingModel instance."""
        self._modified = False

    def __setattr__(self, name, value):
        """Set an attribute on the SettingModel instance."""
        cls = type(self)
        prop = getattr(cls, name, None)

        if isinstance(prop, SettingProperty):
            prop.__set__(self, value)
            object.__setattr__(self, "_modified", True)
            return
        object.__setattr__(self, name, value)

    @classmethod
    def _iter_settings(cls):
        """Iterate over all setting properties defined in the class and its base classes."""
        for base in reversed(cls.__mro__):
            for name, attr in base.__dict__.items():
                if isinstance(attr, SettingProperty):
                    yield name, attr

    def is_modified(self):
        """Check if any setting in the model has been modified."""
        return getattr(self, "_modified", False)

    def serialize(self, serializer: SettingsSerializer, *, modified_only: bool = False):
        """Serialize the settings model to a dictionary."""
        properties = {}

        for attr_name, prop in self._iter_settings():

            if modified_only and not hasattr(self, prop.private_name):
                continue

            value = getattr(self, attr_name)

            if isinstance(value, SettingModel):
                properties[prop.name] = value.serialize(
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
        """Initialize a model setting property.

        Parameters
        ----------
        name : str
            Name of the setting property.
        model_cls : type[T]
            Class of the nested SettingModel.
        default_factory : Callable[[], T], optional
            Factory function to create a default instance of the model.
        force_all : bool, optional
            If True, all settings in the nested model will be serialized,
            even if they are not modified.
        **kwargs : Any
            Additional keyword arguments passed to the base class.
        """

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
        """Get the nested SettingModel instance from the parent instance."""
        if instance is None:
            return self

        # do not create model unless accessed
        value = getattr(instance, self.private_name, None)

        if value is None:
            value = self.default_factory()
            value._parent_property = self
            setattr(instance, self.private_name, value)

        return value
