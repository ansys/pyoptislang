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

from __future__ import annotations

import pytest

from ansys.optislang.core.node_types import AddinType, NodeType


@pytest.mark.parametrize(
    "name",
    [
        "BUILT_IN",
        "ALGORITHM_PLUGIN",
        "INTEGRATION_PLUGIN",
        "PYTHON_BASED_ALGORITHM_PLUGIN",
        "PYTHON_BASED_INTEGRATION_PLUGIN",
        "PYTHON_BASED_MOP_NODE_PLUGIN",
        "PYTHON_BASED_NODE_PLUGIN",
    ],
)
def test_design_flow(name: str):
    """Test `AddinType`."""
    mixed_name = ""
    for index, char in enumerate(name):
        if index % 2 == 1:
            mixed_name += char.lower()
        else:
            mixed_name += char

    enumeration_from_str = AddinType.from_str(string=mixed_name)

    assert isinstance(enumeration_from_str, AddinType)
    assert isinstance(enumeration_from_str.name, str)
    assert enumeration_from_str.name == name


def test_invalid_inputs():
    """Test passing incorrect inputs to enuration classes `from_str` method."""
    with pytest.raises(TypeError):
        AddinType.from_str(1)

    with pytest.raises(ValueError):
        AddinType.from_str("invalid")


def test_node_type_class():
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
    assert node_type != "foo"
