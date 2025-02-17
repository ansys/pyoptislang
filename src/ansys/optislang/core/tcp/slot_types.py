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
from typing import cast

from ansys.optislang.core.slot_types import SlotTypeHint


class SlotTypeHintTCP(Enum):
    """Provides supported slots type strings specifically for oSL TCP API."""

    UNDEFINED = "Undefined"
    BOOL = "Bool"
    INTEGER = "Integer"
    UNSIGNED_INTEGER = "Unsigned Integer"
    UNSIGNED_INTEGER_VECTOR = "Unsigned Integer Vector"
    REAL = "Real"
    STRING = "String"
    STRING_LIST = "String List"
    VARIANT = "Variant"
    PATH = "Path"
    PARAMETER = "Parameter"
    PARAMETER_SET = "Parameter Set"
    PARAMETER_MANAGER = "Parameter Manager"
    DESIGN = "Design"
    DESIGN_POINT = "Designpoint"
    DESIGN_CONTAINER = "Design Container"
    BOOL_VECTOR = "Bool Vector"
    CRITERION = "Criterion"
    CRITERION_SEQUENCE = "Criterion Sequence"
    DESIGN_ENTRY = "Designentry"
    RUN_INFO_META = "Runinfo Meta"
    RUN_INFO = "Runinfo"
    DESIGN_POINTS = "Designpoints"

    @classmethod
    def from_str(cls, string: str) -> SlotTypeHintTCP:
        """Convert string to an instance of the ``SlotTypeHintTCP`` class.

        Parameters
        ----------
        string: str
            String to be converted.

        Returns
        -------
        SlotTypeHintTCP
            Instance of the ``SlotTypeHintTCP`` class.

        Raises
        ------
        TypeError
            Raised when an invalid type of ``string`` is given.
        ValueError
            Raised when an invalid value of ``string`` is given.
        """
        return cast(SlotTypeHintTCP, cls._value2member_map_[string])

    def to_slot_type(self) -> SlotTypeHint:
        """Convert instance of the ``SlotTypeHintTCP`` class to general SlotTypeHint.

        Returns
        -------
        SlotTypeHint
            Instance of the ``SlotTypeHint`` class.
        """
        return SlotTypeHint[self.name]
