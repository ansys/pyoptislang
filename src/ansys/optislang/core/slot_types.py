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

"""Contains definitions for node slot types."""

from __future__ import annotations

from enum import Enum


class SlotTypeHint(Enum):
    """Provides supported slots types."""

    UNDEFINED = 0
    BOOL = 1
    INTEGER = 2
    UNSIGNED_INTEGER = 3
    UNSIGNED_INTEGER_VECTOR = 4
    REAL = 5
    STRING = 6
    STRING_LIST = 7
    VARIANT = 8
    PATH = 9
    PARAMETER = 10
    PARAMETER_SET = 11
    PARAMETER_MANAGER = 12
    DESIGN = 13
    DESIGN_POINT = 14
    DESIGN_CONTAINER = 15
    BOOL_VECTOR = 16
    CRITERION = 17
    CRITERION_SEQUENCE = 18
    DESIGN_ENTRY = 19
    RUN_INFO_META = 20
    RUN_INFO = 21
    DESIGN_POINTS = 22
