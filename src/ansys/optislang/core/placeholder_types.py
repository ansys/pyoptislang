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

"""Contains definitions for placeholder types and user levels."""

from __future__ import annotations

from enum import Enum
from typing import NamedTuple, Optional, Any, Union


class PlaceholderType(Enum):
    """Provides supported placeholder types."""

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


class UserLevel(Enum):
    """Provides supported user levels for placeholders."""

    COMPUTATION_ENGINEER = "computation_engineer"
    FLOW_ENGINEER = "flow_engineer"


class PlaceholderInfo(NamedTuple):
    """Information about a placeholder returned by get_placeholder method.
    
    Attributes
    ----------
    placeholder_id : str
        The placeholder identifier (mapped from C++ 'name' field).
    user_level : UserLevel
        The user level for the placeholder.
    type : PlaceholderType
        The placeholder type.
    description : str
        Description of the placeholder.
    range : str
        Range specification for the placeholder.
    value : Optional[Any]
        Current value of the placeholder (if set).
    expression : Optional[str]
        Expression associated with the placeholder (if it's a macro).
    """
    placeholder_id: str
    user_level: UserLevel
    type: PlaceholderType
    description: str
    range: str
    value: Optional[Any] = None
    expression: Optional[str] = None
