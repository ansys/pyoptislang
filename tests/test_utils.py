# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
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

from enum import Enum

import pytest

from ansys.optislang.core import utils


def test_enum_from_str():
    class MyEnum(Enum):
        ONE = 0
        TWO = 1

    with pytest.raises(TypeError):
        utils.enum_from_str(123, MyEnum)
        utils.enum_from_str("ONE", list)

    with pytest.raises(ValueError):
        utils.enum_from_str("THREE", MyEnum)

    assert utils.enum_from_str("one", MyEnum) == MyEnum.ONE
    assert utils.enum_from_str("ONE", MyEnum) == MyEnum.ONE
    assert utils.enum_from_str("ONX", MyEnum, ["X", "E"]) == MyEnum.ONE
