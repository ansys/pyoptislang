from contextlib import nullcontext as does_not_raise
import sys

import pytest

from ansys.optislang.core import PY3, encoding

defenc = sys.getdefaultencoding()
test_string = "my_test_str"

if PY3:
    text_type = str
    binary_type = bytes
    test_text_type = test_string
    test_binary_type = str.encode(test_string)
else:
    if defenc == "ascii":
        defenc = "utf-8"
    text_type = unicode
    binary_type = str
    test_text_type = unicode(test_string, defenc)
    test_binary_type = test_string


@pytest.mark.parametrize(
    "input, expected", [(test_text_type, text_type), (test_binary_type, binary_type)]
)
def test_safe_decode(input, expected):
    "Test ``safe_decode``."
    tmp = encoding.safe_decode(input)
    assert isinstance(input, expected)


def test_to_ascii_safe():
    "Test ``to_ascii_safe``."
    with does_not_raise() as dnr:
        encoding.to_ascii_safe(test_text_type)
    assert dnr is None


def test_force_bytes():
    """Test ``force_bytes``."""
    tmp = encoding.force_bytes(test_text_type)
    assert isinstance(tmp, bytes)


def test_force_text():
    """Test ``force_text``."""
    tmp = encoding.force_text(test_binary_type)
    assert isinstance(tmp, str)
