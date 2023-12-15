import pytest

from ansys.optislang.core import Optislang, node_types
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
    osl = Optislang()
    osl.timeout = 20
    yield osl
    osl.dispose()


def test_all_nodes_creation(optislang: Optislang):
    """Test creation of all available nodes."""
    rs = optislang.application.project.root_system
    rs.delete_children_nodes()
    for node_type in NODE_TYPES:
        if node_type in [
            "AMOP",
            "ARSM",
            "AlgorithmSystemPlugin",
            "BASS",
            "CustomAlgorithm",
            "DXAMO",
            "DPF",
            "DXMISQP",
            "DXASO",
            "DXUPEGO",
            "EA",
            "PIBO",
        ]:
            continue
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
