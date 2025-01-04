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

import sys

import pytest

from ansys.optislang.core import encoding

defenc = sys.getdefaultencoding()
test_string = "my_test_str"

if sys.version_info[0] >= 3:
    text_type = str
    binary_type = bytes
    test_text_type = test_string
    test_binary_type = bytes(test_string, "utf-8")
else:
    if defenc == "ascii":
        defenc = "utf-8"
    text_type = unicode
    binary_type = str
    test_text_type = unicode(test_string, defenc)
    test_binary_type = test_string


@pytest.mark.parametrize(
    "input, expected", [(test_text_type, text_type), (test_binary_type, text_type)]
)
def test_safe_decode(input, expected):
    "Test ``safe_decode``."
    decoded = encoding.safe_decode(input)
    assert isinstance(decoded, expected)


def test_to_ascii_safe():
    "Test ``to_ascii_safe``."
    encoding.to_ascii_safe(test_text_type)


def test_force_bytes():
    """Test ``force_bytes``."""
    forced_bytes = encoding.force_bytes(test_text_type)
    assert isinstance(forced_bytes, bytes)


def test_force_text():
    """Test ``force_text``."""
    forced_text = encoding.force_text(test_binary_type)
    assert isinstance(forced_text, str)
