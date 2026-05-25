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

from pathlib import Path

import pytest

from ansys.optislang.core import Optislang
from ansys.optislang.core.nodes import InputSlot, OutputSlot, SlotType
from ansys.optislang.core.osl_server import OslVersion
from ansys.optislang.core.slot_types import SlotTypeHint
from ansys.optislang.core.tcp.nodes import (
    Edge,
    TcpNodeProxy,
    TcpParametricSystemProxy,
    TcpRootSystemProxy,
    TcpSlotProxy,
)

pytestmark = pytest.mark.local_osl


@pytest.fixture()
def optislang(tmp_example_project, scope="function", autouse=False) -> Optislang:
    """Create instance of Optislang class.

    Returns
    -------
    Optislang:
        Connects to the optiSLang application and provides an API to control it.
    """
    osl = Optislang(project_path=tmp_example_project("nodes_connection"), ini_timeout=90)
    osl.timeout = 60
    yield osl
    osl.dispose()


def test_tcp_slot_proxy_properties(optislang: Optislang):
    """Test `TcpSlotProxy` properties."""
    rs: TcpRootSystemProxy = optislang.project.root_system
    sens: TcpParametricSystemProxy = rs.find_nodes_by_name("Sensitivity")[0]
    random_slot = sens.get_input_slots()[0]
    print(random_slot)
    assert isinstance(random_slot.name, str)
    assert isinstance(random_slot.node, TcpNodeProxy)
    assert isinstance(random_slot.type, SlotType)
    assert isinstance(random_slot.type_hint, SlotTypeHint)


def test_tcp_slot_queries(optislang: Optislang):
    """Test `TcpSlotProxy` properties."""
    rs: TcpRootSystemProxy = optislang.project.root_system
    calc: TcpNodeProxy = rs.find_nodes_by_name("Calculator")[0]
    output_slot: TcpSlotProxy = calc.get_output_slots(name="ODesign")[0]
    connections = output_slot.get_connections()
    assert len(connections) == 1
    assert isinstance(connections[0], Edge)
    assert isinstance(output_slot.get_type_hint(), SlotTypeHint)


def test_edge(optislang: Optislang):
    """Test `Edge` properties."""
    root_system: TcpRootSystemProxy = optislang.project.root_system
    calculator = root_system.find_nodes_by_name("Calculator")[0]
    edge = calculator.get_connections()[0]
    assert isinstance(edge, Edge)
    print(edge)
    assert isinstance(edge.from_slot, OutputSlot)
    assert isinstance(edge.to_slot, InputSlot)
    assert edge.exists()


def test_connect_nodes(optislang: Optislang, tmp_path: Path):
    """Test connecting nodes, obtaining connections and disconnecting slot."""
    rs: TcpRootSystemProxy = optislang.project.root_system
    a: TcpNodeProxy = rs.find_nodes_by_name("A")[0]
    b: TcpNodeProxy = rs.find_nodes_by_name("B")[0]
    calc: TcpNodeProxy = rs.find_nodes_by_name("Calculator")[0]
    sens: TcpParametricSystemProxy = rs.find_nodes_by_name("Sensitivity")[0]
    calc_i: TcpNodeProxy = sens.find_nodes_by_name("Calculator")[0]

    a_output = a.get_output_slots(name="OVar")[0]
    b_output = b.get_output_slots(name="OVar")[0]
    calc_inputA = calc.get_input_slots(name="A")[0]
    calc_inputB = calc.get_input_slots(name="B")[0]
    calc_inputRS = calc.get_input_slots(name="IDesign")[0]

    sens_inner_output = sens.get_inner_output_slots(name="IODesign")[0]
    sens_inner_input = sens.get_inner_input_slots(name="IIDesign")[0]
    sens_output = sens.get_output_slots(name="OReferenceDesign")[0]
    calc_i_output = calc_i.get_output_slots(name="ODesign")[0]
    calc_i_input = calc_i.get_input_slots(name="IDesign")[0]

    rs_output = rs.get_inner_output_slots(name="IODesign")[0]
    rs_input = rs.get_inner_input_slots(name="IIDesign")[0]

    a_output.connect_to(calc_inputA)
    calc_inputB.connect_from(b_output)
    sens_inner_output.connect_to(calc_i_input)
    calc_i_output.connect_to(sens_inner_input)
    rs_output.connect_to(calc_inputRS)
    sens_output.connect_to(rs_input)

    assert len(calc.get_connections()) == 4
    assert len(calc.get_connections(slot_type=SlotType.INPUT)) == 3
    assert len(calc.get_connections(slot_name="B")) == 1

    a_output.disconnect()
    assert len(calc.get_connections()) == 3

    assert len(calc_i.get_connections()) == 2
    calc_i_input.disconnect()
    assert len(calc_i.get_connections()) == 1


def test_disconnect_nodes(optislang: Optislang, tmp_path: Path):
    """Test disconnecting nodes."""
    if optislang.osl_version < OslVersion(24, 1, 0, 0):
        pytest.skip(f"Not compatible with {optislang.osl_version_string}")

    rs: TcpRootSystemProxy = optislang.project.root_system
    a: TcpNodeProxy = rs.find_nodes_by_name("A")[0]
    b: TcpNodeProxy = rs.find_nodes_by_name("B")[0]
    calc: TcpNodeProxy = rs.find_nodes_by_name("Calculator")[0]
    sens: TcpParametricSystemProxy = rs.find_nodes_by_name("Sensitivity")[0]
    calc_i: TcpNodeProxy = sens.find_nodes_by_name("Calculator")[0]

    a_output = a.get_output_slots(name="OVar")[0]
    b_output = b.get_output_slots(name="OVar")[0]
    calc_inputA = calc.get_input_slots(name="A")[0]
    calc_inputB = calc.get_input_slots(name="B")[0]
    calc_inputRS = calc.get_input_slots(name="IDesign")[0]

    sens_inner_output = sens.get_inner_output_slots(name="IODesign")[0]
    sens_inner_input = sens.get_inner_input_slots(name="IIDesign")[0]
    sens_output = sens.get_output_slots(name="OReferenceDesign")[0]
    calc_i_output = calc_i.get_output_slots(name="ODesign")[0]
    calc_i_input = calc_i.get_input_slots(name="IDesign")[0]

    rs_output = rs.get_inner_output_slots(name="IODesign")[0]
    rs_input = rs.get_inner_input_slots(name="IIDesign")[0]

    a_output.connect_to(calc_inputA)
    calc_inputB.connect_from(b_output)
    sens_inner_output.connect_to(calc_i_input)
    calc_i_output.connect_to(sens_inner_input)
    rs_output.connect_to(calc_inputRS)
    sens_output.connect_to(rs_input)

    assert len(calc.get_connections()) == 4
    assert len(calc.get_connections(slot_type=SlotType.INPUT)) == 3
    assert len(calc.get_connections(slot_name="B")) == 1

    assert len(calc_i.get_connections()) == 2

    a_output.disconnect(calc_inputA)
    sens_inner_output.disconnect(calc_i_input)

    assert len(calc.get_connections()) == 3
    assert len(calc_i.get_connections()) == 1
