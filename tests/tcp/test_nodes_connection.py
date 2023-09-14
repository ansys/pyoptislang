from __future__ import annotations

from contextlib import nullcontext as does_not_raise
from pathlib import Path

import pytest

from ansys.optislang.core import Optislang, examples
from ansys.optislang.core.base_nodes import InputSlot, OutputSlot, SlotType
from ansys.optislang.core.tcp.base_nodes import (
    Edge,
    TcpNodeProxy,
    TcpParametricSystemProxy,
    TcpRootSystemProxy,
    TcpSlotProxy,
)

pytestmark = pytest.mark.local_osl
connect_nodes = examples.get_files("nodes_connection")[1][0]


@pytest.fixture()
def optislang(scope="function", autouse=False) -> Optislang:
    """Create instance of Optislang class.

    Returns
    -------
    Optislang:
        Connects to the optiSLang application and provides an API to control it.
    """
    osl = Optislang(project_path=connect_nodes)
    osl.timeout = 20
    return osl


def test_tcp_slot_proxy_properties(optislang: Optislang):
    """Test `TcpSlotProxy` properties."""
    rs: TcpRootSystemProxy = optislang.project.root_system
    sens: TcpParametricSystemProxy = rs.find_nodes_by_name("Sensitivity")[0]
    random_slot = sens.get_slots()[0]
    with does_not_raise() as dnr:
        print(random_slot)
    assert isinstance(random_slot.name, str)
    assert isinstance(random_slot.node, TcpNodeProxy)
    assert isinstance(random_slot.type, SlotType)
    assert isinstance(random_slot.type_hint, str)
    optislang.dispose()


def test_tcp_slot_queries(optislang: Optislang):
    """Test `TcpSlotProxy` properties."""
    rs: TcpRootSystemProxy = optislang.project.root_system
    calc: TcpNodeProxy = rs.find_nodes_by_name("Calculator")[0]
    output_slot: TcpSlotProxy = calc.get_slots(type_=SlotType.OUTPUT, name="ODesign")[0]
    connections = output_slot.get_connections()
    assert len(connections) == 1
    assert isinstance(connections[0], Edge)
    assert isinstance(output_slot.get_type_hint(), str)
    optislang.dispose()


def test_edge(optislang: Optislang):
    """Test `Edge` properties."""
    root_system: TcpRootSystemProxy = optislang.project.root_system
    calculator = root_system.find_nodes_by_name("Calculator")[0]
    edge = calculator.get_connections()[0]
    assert isinstance(edge, Edge)
    with does_not_raise() as dnr:
        print(edge)
    assert isinstance(edge.from_slot, OutputSlot)
    assert isinstance(edge.to_slot, InputSlot)
    assert edge.exists()
    optislang.dispose()


def test_connect_nodes(optislang: Optislang, tmp_path: Path):
    """Test connecting nodes, obtaining connections and disconnecting slot."""
    optislang.save_as(file_path=tmp_path / "test_connect_nodes.opf")
    rs: TcpRootSystemProxy = optislang.project.root_system
    a: TcpNodeProxy = rs.find_nodes_by_name("A")[0]
    b: TcpNodeProxy = rs.find_nodes_by_name("B")[0]
    calc: TcpNodeProxy = rs.find_nodes_by_name("Calculator")[0]
    sens: TcpParametricSystemProxy = rs.find_nodes_by_name("Sensitivity")[0]
    calc_i: TcpNodeProxy = sens.find_nodes_by_name("Calculator")[0]

    a_output = a.get_slots(type_=SlotType.OUTPUT, name="OVar")[0]
    b_output = b.get_slots(type_=SlotType.OUTPUT, name="OVar")[0]
    calc_inputA = calc.get_slots(type_=SlotType.INPUT, name="A")[0]
    calc_inputB = calc.get_slots(type_=SlotType.INPUT, name="B")[0]
    calc_inputRS = calc.get_slots(type_=SlotType.INPUT, name="IDesign")[0]

    sens_inner_output = sens.get_slots(type_=SlotType.INNER_OUTPUT, name="IODesign")[0]
    sens_inner_input = sens.get_slots(type_=SlotType.INNER_INPUT, name="IIDesign")[0]
    sens_output = sens.get_slots(type_=SlotType.OUTPUT, name="OReferenceDesign")[0]
    calc_i_output = calc_i.get_slots(type_=SlotType.OUTPUT, name="ODesign")[0]
    calc_i_input = calc_i.get_slots(type_=SlotType.INPUT, name="IDesign")[0]

    rs_output = rs.get_slots(type_=SlotType.INNER_OUTPUT, name="IODesign")[0]
    rs_input = rs.get_slots(type_=SlotType.INNER_INPUT, name="IIDesign")[0]

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
    optislang.dispose()
