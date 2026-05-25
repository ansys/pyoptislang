# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

from ansys.optislang.core.nodes import DesignFlow, NodeClassType, SamplingType, SlotType

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
    "name",
    [
        "NONE",
        "RECEIVE",
        "SEND",
        "RECEIVE_SEND",
    ],
)
def test_design_flow(name: str):
    """Test `DesignFlow`."""
    enumeration_test_method(enumeration_class=DesignFlow, enumeration_name=name)


@pytest.mark.parametrize(
    "name",
    [
        "NODE",
        "SYSTEM",
        "PARAMETRIC_SYSTEM",
        "ROOT_SYSTEM",
        "INTEGRATION_NODE",
        "PROXY_SOLVER",
    ],
)
def test_node_class_type(name: str):
    """Test `NodeClassType`."""
    enumeration_test_method(enumeration_class=NodeClassType, enumeration_name=name)


@pytest.mark.parametrize(
    "name",
    [
        "CENTERPOINT",
        "FULLFACTORIAL",
        "AXIAL",
        "STARPOINTS",
        "KOSHAL",
        "CENTRALCOMPOSITE",
        "MIXEDTERMS",
        "LATINHYPER",
        "LATINHYPERDETEMINISTIC",
        "OPTIMIZEDLATINHYPER",
        "ORTHOLATINHYPERDETEMINISTIC",
        "SOBOLSEQUENCES",
        "PLAINMONTECARLO",
        "DOPTIMAL",
        "DOPTIMALLINEAR",
        "DOPTIMALQUADRATIC",
        "DOPTIMALQUADRATICNOMIXED",
        "KOSHALLINEAR",
        "KOSHALQUADRATIC",
        "FEKETE",
        "BOXBEHNKEN",
        "FULLCOMBINATORIAL",
        "ADVANCEDLATINHYPER",
    ],
)
def test_sampling_type(name: str):
    """Test `SamplingType`."""
    enumeration_test_method(enumeration_class=SamplingType, enumeration_name=name)


@pytest.mark.parametrize(
    "name, direction",
    [
        ("INPUT", "receiving"),
        ("OUTPUT", "sending"),
        ("INNER_INPUT", "receiving"),
        ("INNER_OUTPUT", "sending"),
    ],
)
def test_slot_type(name: str, direction: str):
    """Test `SlotType`."""
    output = enumeration_test_method(enumeration_class=SlotType, enumeration_name=name)
    assert SlotType.to_dir_str(output) == direction


@pytest.mark.parametrize(
    "enumeration_class, invalid_value, invalid_value_type",
    [
        (DesignFlow, "invalid", 1),
        (NodeClassType, "invalid", 1),
        (SlotType, "invalid", 1),
    ],
)
def test_invalid_inputs(enumeration_class: Enum, invalid_value: str, invalid_value_type: Any):
    from_str_invalid_inputs_method(
        enumeration_class=enumeration_class,
        invalid_value=invalid_value,
        invalid_value_type=invalid_value_type,
    )
