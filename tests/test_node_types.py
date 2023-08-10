from __future__ import annotations

from contextlib import nullcontext as does_not_raise
from typing import TYPE_CHECKING, Any

import pytest

from ansys.optislang.core.node_types import AddinType, NodeType

if TYPE_CHECKING:
    from enum import Enum


# region TEST ENUMERATION METHODS:
def enumeration_test_method(enumeration_class: Enum, enumeration_name: str) -> Enum:
    """Test instance creation, method `from_str` and spelling."""
    mixed_name = ""
    for index, char in enumerate(enumeration_name):
        if index % 2 == 1:
            mixed_name += char.lower()
        else:
            mixed_name += char
    try:
        enumeration_from_str = enumeration_class.from_str(string=mixed_name)
    except:
        assert False
    assert isinstance(enumeration_from_str, enumeration_class)
    assert isinstance(enumeration_from_str.name, str)
    assert enumeration_from_str.name == enumeration_name
    return enumeration_from_str


def from_str_invalid_inputs_method(
    enumeration_class: Enum, invalid_value: str, invalid_value_type: float
):
    """Test passing incorrect inputs to enuration classes `from_str` method."""
    with pytest.raises(TypeError):
        enumeration_class.from_str(invalid_value_type)

    with pytest.raises(ValueError):
        enumeration_class.from_str(invalid_value)


@pytest.mark.parametrize(
    "addin_type, name",
    [
        (AddinType, "BUILT_IN"),
        (AddinType, "ALGORITHM_PLUGIN"),
        (AddinType, "INTEGRATION_PLUGIN"),
        (AddinType, "PYTHON_BASED_ALGORITHM_PLUGIN"),
        (AddinType, "PYTHON_BASED_INTEGRATION_PLUGIN"),
        (AddinType, "PYTHON_BASED_MOP_NODE_PLUGIN"),
        (AddinType, "PYTHON_BASED_NODE_PLUGIN"),
    ],
)
def test_design_flow(addin_type: AddinType, name: str):
    """Test `AddinType`."""
    enumeration_test_method(enumeration_class=addin_type, enumeration_name=name)


@pytest.mark.parametrize(
    "enumeration_class, invalid_value, invalid_value_type",
    [
        (AddinType, "invalid", 1),
    ],
)
def test_invalid_inputs(enumeration_class: Enum, invalid_value: str, invalid_value_type: Any):
    from_str_invalid_inputs_method(
        enumeration_class=enumeration_class,
        invalid_value=invalid_value,
        invalid_value_type=invalid_value_type,
    )


# endregion


# region TEST CLASSES
def test_node_type():
    """Test initialization and properties of `NodeType` class."""
    node_type = NodeType(id="name", subtype=AddinType.BUILT_IN)
    assert isinstance(node_type.id, str)
    assert isinstance(node_type.subtype, AddinType)
    assert node_type.id == "name"
    assert node_type.subtype == AddinType.BUILT_IN
    node_type_eq = NodeType(id="name", subtype=AddinType.BUILT_IN)
    node_type_neq1 = NodeType(id="another_name", subtype=AddinType.BUILT_IN)
    node_type_neq2 = NodeType(id="name", subtype=AddinType.ALGORITHM_PLUGIN)
    assert node_type == node_type_eq
    assert not node_type == node_type_neq1
    assert not node_type == node_type_neq2
    with does_not_raise() as dnr:
        print(node_type)
    assert dnr is None


# endregion
