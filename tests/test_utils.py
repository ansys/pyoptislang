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
