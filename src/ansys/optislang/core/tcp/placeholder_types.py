# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""Contains definitions for placeholder types and user levels for TCP API."""

from __future__ import annotations

from enum import Enum

from ansys.optislang.core.placeholder_types import PlaceholderType, UserLevel


class PlaceholderTypeTCP(Enum):
    """Provides supported placeholder type strings specifically for oSL TCP API."""

    UNKNOWN = "unknown"
    STRING = "string"
    SPLIT_PATH = "split_path"
    RELATIVE_SPLIT_PATH = "relative_split_path"
    PATH = "path"
    UINT = "uint"
    INT = "int"
    STRING_LIST = "string_list"
    REAL = "real"
    BOOL = "bool"
    PROVIDED_PATH = "provided_path"

    @classmethod
    def from_str(cls, string: str) -> PlaceholderTypeTCP:
        """Convert string to an instance of the ``PlaceholderTypeTCP`` class.

        Parameters
        ----------
        string: str
            String representation of the enum to be converted.

        Returns
        -------
        PlaceholderTypeTCP
            Instance of the ``PlaceholderTypeTCP`` class.

        Raises
        ------
        TypeError
            Raised when an invalid type of ``string`` is given.
        ValueError
            Raised when an invalid value of ``string`` is given.
        """
        if not isinstance(string, str):
            raise TypeError(f"String was expected, but `{type(string)}` was given.")
        try:
            return cls(string)
        except ValueError as exc:
            raise ValueError(f"{string} is not a valid {cls.__name__}") from exc

    def to_placeholder_type(self) -> PlaceholderType:
        """Convert instance of the ``PlaceholderTypeTCP`` class to general PlaceholderType.

        Returns
        -------
        PlaceholderType
            Instance of the ``PlaceholderType`` class.
        """
        return PlaceholderType[self.name]


class UserLevelTCP(Enum):
    """Provides supported user level strings specifically for oSL TCP API."""

    COMPUTATION_ENGINEER = "computation_engineer"
    FLOW_ENGINEER = "flow_engineer"

    @classmethod
    def from_str(cls, string: str) -> UserLevelTCP:
        """Convert string to an instance of the ``UserLevelTCP`` class.

        Parameters
        ----------
        string: str
            String representation of the enum to be converted.

        Returns
        -------
        UserLevelTCP
            Instance of the ``UserLevelTCP`` class.

        Raises
        ------
        TypeError
            Raised when an invalid type of ``string`` is given.
        ValueError
            Raised when an invalid value of ``string`` is given.
        """
        if not isinstance(string, str):
            raise TypeError(f"String was expected, but `{type(string)}` was given.")
        try:
            return cls(string)
        except ValueError as exc:
            raise ValueError(f"'{string}' is not a valid {cls.__name__}") from exc

    def to_user_level(self) -> UserLevel:
        """Convert instance of the ``UserLevelTCP`` class to general UserLevel.

        Returns
        -------
        UserLevel
            Instance of the ``UserLevel`` class.
        """
        return UserLevel[self.name]
