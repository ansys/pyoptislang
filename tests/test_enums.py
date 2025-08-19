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

import pytest

from ansys.optislang.core.placeholder_types import PlaceholderType, UserLevel
from ansys.optislang.core.slot_types import SlotTypeHint
from ansys.optislang.core.tcp.placeholder_types import PlaceholderTypeTCP, UserLevelTCP
from ansys.optislang.core.tcp.slot_types import SlotTypeHintTCP


def test_slot_type_enum_from_str():
    with pytest.raises(TypeError):
        SlotTypeHintTCP.from_str(string=42).to_slot_type()

    with pytest.raises(ValueError):
        SlotTypeHintTCP.from_str(string="INVALID").to_slot_type()

    assert SlotTypeHintTCP.from_str(string="String List").to_slot_type() == SlotTypeHint.STRING_LIST


def test_placeholder_type_enum_from_str():
    with pytest.raises(TypeError):
        PlaceholderTypeTCP.from_str(string=42).to_placeholder_type()

    with pytest.raises(ValueError):
        PlaceholderTypeTCP.from_str(string="INVALID").to_placeholder_type()

    assert (
        PlaceholderTypeTCP.from_str(string="provided_path").to_placeholder_type()
        == PlaceholderType.PROVIDED_PATH
    )


def test_user_level_type_enum_from_str():
    with pytest.raises(TypeError):
        UserLevelTCP.from_str(string=42).to_user_level()

    with pytest.raises(ValueError):
        UserLevelTCP.from_str(string="INVALID").to_user_level()

    assert (
        UserLevelTCP.from_str(string="computation_engineer").to_user_level()
        == UserLevel.COMPUTATION_ENGINEER
    )
