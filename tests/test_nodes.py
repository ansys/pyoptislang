from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

from ansys.optislang.core.nodes import (
    DesignFlow,
    NodeClassType,
    RegisteredLocationType,
    SamplingType,
    SlotType,
)

if TYPE_CHECKING:
    from enum import Enum


# TEST ENUMERATION METHODS:
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
    "design_flow, name",
    [
        (DesignFlow, "NONE"),
        (DesignFlow, "RECEIVE"),
        (DesignFlow, "SEND"),
        (DesignFlow, "RECEIVE_SEND"),
    ],
)
def test_design_flow(design_flow: DesignFlow, name: str):
    """Test `DesignFlow`."""
    enumeration_test_method(enumeration_class=design_flow, enumeration_name=name)


@pytest.mark.parametrize(
    "node_class_type, name",
    [
        (NodeClassType, "NODE"),
        (NodeClassType, "SYSTEM"),
        (NodeClassType, "PARAMETRIC_SYSTEM"),
        (NodeClassType, "ROOT_SYSTEM"),
        (NodeClassType, "INTEGRATION_NODE"),
    ],
)
def test_node_class_type(node_class_type: NodeClassType, name: str):
    """Test `NodeClassType`."""
    enumeration_test_method(enumeration_class=node_class_type, enumeration_name=name)


@pytest.mark.parametrize(
    "registered_location_type, name",
    [
        (RegisteredLocationType, "INPUT_SLOT"),
        (RegisteredLocationType, "INTERNAL_VARIABLE"),
        (RegisteredLocationType, "OUTPUT_SLOT"),
        (RegisteredLocationType, "PARAMETER"),
        (RegisteredLocationType, "RESPONSE"),
    ],
)
def test_registered_location_type(registered_location_type: RegisteredLocationType, name: str):
    """Test `RegisteredLocationType`."""
    enumeration_test_method(enumeration_class=registered_location_type, enumeration_name=name)


@pytest.mark.parametrize(
    "sampling_type, name",
    [
        (SamplingType, "CENTERPOINT"),
        (SamplingType, "FULLFACTORIAL"),
        (SamplingType, "AXIAL"),
        (SamplingType, "STARPOINTS"),
        (SamplingType, "KOSHAL"),
        (SamplingType, "CENTRALCOMPOSITE"),
        (SamplingType, "MIXEDTERMS"),
        (SamplingType, "LATINHYPER"),
        (SamplingType, "LATINHYPERDETEMINISTIC"),
        (SamplingType, "OPTIMIZEDLATINHYPER"),
        (SamplingType, "ORTHOLATINHYPERDETEMINISTIC"),
        (SamplingType, "SOBOLSEQUENCES"),
        (SamplingType, "PLAINMONTECARLO"),
        (SamplingType, "DOPTIMAL"),
        (SamplingType, "DOPTIMALLINEAR"),
        (SamplingType, "DOPTIMALQUADRATIC"),
        (SamplingType, "DOPTIMALQUADRATICNOMIXED"),
        (SamplingType, "KOSHALLINEAR"),
        (SamplingType, "KOSHALQUADRATIC"),
        (SamplingType, "FEKETE"),
        (SamplingType, "BOXBEHNKEN"),
        (SamplingType, "FULLCOMBINATORIAL"),
        (SamplingType, "ADVANCEDLATINHYPER"),
    ],
)
def test_sampling_type(sampling_type: SamplingType, name: str):
    """Test `SamplingType`."""
    enumeration_test_method(enumeration_class=sampling_type, enumeration_name=name)


@pytest.mark.parametrize(
    "slot_type, name, direction",
    [
        (SlotType, "INPUT", "receiving"),
        (SlotType, "OUTPUT", "sending"),
        (SlotType, "INNER_INPUT", "receiving"),
        (SlotType, "INNER_OUTPUT", "sending"),
    ],
)
def test_slot_type(slot_type: SlotType, name: str, direction: str):
    """Test `SlotType`."""
    output = enumeration_test_method(enumeration_class=slot_type, enumeration_name=name)
    assert slot_type.to_dir_str(output) == direction


@pytest.mark.parametrize(
    "enumeration_class, invalid_value, invalid_value_type",
    [
        (DesignFlow, "invalid", 1),
        (NodeClassType, "invalid", 1),
        (RegisteredLocationType, "invalid", 1),
        (SlotType, "invalid", 1),
    ],
)
def test_invalid_inputs(enumeration_class: Enum, invalid_value: str, invalid_value_type: Any):
    from_str_invalid_inputs_method(
        enumeration_class=enumeration_class,
        invalid_value=invalid_value,
        invalid_value_type=invalid_value_type,
    )
