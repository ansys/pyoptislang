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

from typing import cast

import pytest

from ansys.optislang.core import Optislang, node_types
from ansys.optislang.core.osl_server import OslVersion
from ansys.optislang.core.tcp.nodes import System

pytestmark = pytest.mark.local_osl


@pytest.fixture()
def optislang(scope="function", autouse=False) -> Optislang:
    """Create instance of Optislang class.

    Returns
    -------
    Optislang:
        Connects to the optiSLang application and provides an API to control it.
    """
    osl = Optislang(ini_timeout=90)
    osl.timeout = 60
    yield osl
    osl.dispose()


def test_all_nodes_creation(optislang: Optislang):
    """Test creation of all available nodes."""
    if optislang.osl_version < OslVersion(24, 1, 2, 0):
        pytest.skip(f"Not compatible with {optislang.osl_version_string}")

    rs = optislang.application.project.root_system
    rs.delete_children_nodes()

    for node_group in optislang.osl_server.get_available_nodes().values():
        if node_group == "builtin_nodes" or node_group == "integration_plugins":
            for node in node_group:
                print(f"Creating node {node}")
                node = rs.create_node(type_=node_types.get_node_type_from_str(node))
                nodes_in_rs = rs.get_nodes()
                assert node.uid == nodes_in_rs[0].uid
                assert node.type == nodes_in_rs[0].type
                node.delete()


def test_create_node_in_system(optislang: Optislang):
    """Test creation of node inside a system."""
    assert optislang.application.project
    rs = optislang.application.project.root_system
    sens = cast(System, rs.create_node(type_=node_types.Sensitivity))
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
