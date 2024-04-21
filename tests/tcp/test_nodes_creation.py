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

import pytest

from ansys.optislang.core import Optislang, node_types
from ansys.optislang.core.osl_server import OslVersion
from ansys.optislang.core.tcp.nodes import System

pytestmark = pytest.mark.local_osl

NODE_TYPES_MODULE = dir(node_types)
NODE_TYPES = [
    node_type
    for node_type in NODE_TYPES_MODULE
    if not (
        callable(getattr(node_types, node_type))
        or node_type.startswith("__")
        or node_type == "annotations"
    )
]


@pytest.fixture()
def optislang(scope="function", autouse=False) -> Optislang:
    """Create instance of Optislang class.

    Returns
    -------
    Optislang:
        Connects to the optiSLang application and provides an API to control it.
    """
    osl = Optislang(ini_timeout=60)
    osl.timeout = 20
    yield osl
    osl.dispose()


def test_all_nodes_creation(optislang: Optislang):
    """Test creation of all available nodes."""
    if optislang.osl_version < OslVersion(24, 1, 2, 0):
        pytest.skip(f"Not compatible with {optislang.osl_version_string}")

    rs = optislang.application.project.root_system
    rs.delete_children_nodes()
    for node_type in NODE_TYPES:
        print(f"Creating {eval('node_types.' + node_type)}")
        node = rs.create_node(type_=eval("node_types." + node_type))
        nodes_in_rs = rs.get_nodes()
        assert node.uid == nodes_in_rs[0].uid
        assert node.type == nodes_in_rs[0].type
        node.delete()


def test_create_node_in_system(optislang: Optislang):
    """Test creation of node inside a system."""
    rs = optislang.application.project.root_system
    sens: System = rs.create_node(type_=node_types.Sensitivity)
    node = sens.create_node(type_=node_types.CalculatorSet)

    nodes_in_rs = rs.get_nodes()
    assert sens.uid == nodes_in_rs[0].uid
    assert sens.type == nodes_in_rs[0].type

    nodes_in_sens = sens.get_nodes()
    assert node.uid == nodes_in_sens[0].uid
    assert node.type == nodes_in_sens[0].type

    sens.delete_children_nodes()
    empty_tuple = sens.get_nodes()
    assert len(empty_tuple) == 0
