from contextlib import nullcontext as does_not_raise

import pytest

from ansys.optislang.core import Optislang, examples
from ansys.optislang.core.nodes import Node, ParametricSystem, RootSystem, System
from ansys.optislang.core.project_parametric import ParameterManager

pytestmark = pytest.mark.local_osl
single_node = examples.get_files("calculator_with_params")[1][0]
nested_systems = examples.get_files("nested_systems")[1][0]
connect_nodes = examples.get_files("nodes_connection")[1][0]


@pytest.fixture()
def optislang(scope="function", autouse=False) -> Optislang:
    """Create instance of Optislang class.

    Returns
    -------
    Optislang:
        Connects to the optiSLang application and provides an API to control it.
    """
    osl = Optislang()
    osl.set_timeout(20)
    return osl


# TEST NODE
def test_node_initialization(optislang: Optislang):
    """Test `Node` initialization."""
    optislang.open(file_path=single_node)
    project = optislang.project
    root_system = project.root_system
    node = root_system.get_nodes()[0]
    assert isinstance(node, Node)
    optislang.dispose()


def test_node_properties(optislang: Optislang):
    """Test properties of the instance of `Node` class."""
    optislang.open(file_path=single_node)
    project = optislang.project
    root_system = project.root_system
    node = root_system.get_nodes()[0]
    assert isinstance(node, Node)
    assert isinstance(node.uid, str)
    optislang.dispose()


def test_node_queries(optislang: Optislang):
    """Test get methods of the instance of `Node` class."""
    optislang.open(file_path=single_node)
    project = optislang.project
    root_system = project.root_system
    node = root_system.find_nodes_by_name("Calculator")[0]

    info = node._get_info()
    assert isinstance(info, dict)

    name = node.get_name()
    assert isinstance(name, str)
    assert name == "Calculator"

    parent_name = node.get_parent_name()
    assert isinstance(name, str)

    parent = node.get_parent()
    assert isinstance(parent, RootSystem)
    assert parent_name == parent.get_name()

    properties = node.get_properties()
    assert isinstance(properties, dict)

    status = node.get_status()
    assert isinstance(status, str)

    type = node.get_type()
    assert isinstance(type, str)
    assert type == "CalculatorSet"

    with does_not_raise() as dnr:
        print(node)
    assert dnr is None

    optislang.dispose()


# TEST SYSTEM
def test_find_node_by_uid(optislang: Optislang):
    """Test `find_node_by_uid`."""
    optislang.open(file_path=nested_systems)
    project = optislang.project
    root_system = project.root_system

    # level 1
    level0_node = root_system.find_node_by_uid(
        uid="8854b2c4-fd8a-4e07-839e-1f36553e2d40", search_depth=1
    )
    assert isinstance(level0_node, Node)
    with does_not_raise() as dnr:
        print(level0_node)
    assert dnr is None

    level0_system = root_system.find_node_by_uid(
        uid="a8375c1f-0e39-4901-aa29-56d88f693b54", search_depth=1
    )
    assert isinstance(level0_system, System)
    with does_not_raise() as dnr:
        print(level0_system)
    assert dnr is None

    higher_level = root_system.find_node_by_uid(
        uid="051ba887-cd72-4fe1-a676-2d75a8a843e9", search_depth=1
    )
    assert higher_level is None

    # level 2
    level1_node = root_system.find_node_by_uid(
        uid="051ba887-cd72-4fe1-a676-2d75a8a843e9", search_depth=2
    )
    assert isinstance(level1_node, Node)

    higher_level = root_system.find_node_by_uid(
        uid="ab7d50e2-b031-4c75-b701-fd9fcadf779c", search_depth=2
    )
    assert higher_level is None

    # level 3
    level2_node = root_system.find_node_by_uid(
        uid="ab7d50e2-b031-4c75-b701-fd9fcadf779c", search_depth=3
    )
    assert isinstance(level2_node, Node)

    higher_level = root_system.find_node_by_uid(
        uid="161992fc-d1ee-487f-8bab-0b9897e641e8", search_depth=3
    )
    assert higher_level is None

    # level 4
    level3_node = root_system.find_node_by_uid(
        uid="161992fc-d1ee-487f-8bab-0b9897e641e8", search_depth=4
    )
    assert isinstance(level3_node, Node)

    optislang.dispose()


def test_find_node_by_name(optislang: Optislang):
    """Test `find_node_by_name`."""
    optislang.open(file_path=nested_systems)
    project = optislang.project
    root_system = project.root_system

    # level 1
    level0_node = root_system.find_nodes_by_name(name="Calculator", search_depth=1)[0]
    assert isinstance(level0_node, Node)

    level0_system = root_system.find_nodes_by_name(name="System", search_depth=1)[0]
    assert isinstance(level0_system, System)

    higher_level = root_system.find_nodes_by_name(name="Calculator_inSystem", search_depth=1)
    assert isinstance(higher_level, tuple)
    assert len(higher_level) == 0

    # level 2
    level1_node = root_system.find_nodes_by_name(name="Calculator_inSensitivity", search_depth=2)[0]
    assert isinstance(level1_node, Node)

    higher_level = root_system.find_nodes_by_name(
        name="System_inSystem_inSensitivity", search_depth=2
    )
    assert isinstance(higher_level, tuple)
    assert len(higher_level) == 0

    # level 3
    level2_nodes = root_system.find_nodes_by_name(name="Calculator_inSystem", search_depth=3)
    assert len(level2_nodes) == 2

    # level 4
    level3_nodes = root_system.find_nodes_by_name(name="Calculator_inSystem", search_depth=4)
    assert len(level3_nodes) == 3

    optislang.dispose()


# TEST PARAMETRIC SYSTEM
def test_get_parameter_manager(optislang: Optislang):
    """Test initialization and __str__ methods of both `ParametricSystem` and `ParameterManager`."""
    optislang.open(file_path=nested_systems)
    project = optislang.project
    root_system = project.root_system
    parametric_system: ParametricSystem = root_system.find_nodes_by_name("Parametric System")[0]
    with does_not_raise() as dnr:
        print(parametric_system)
        parameter_manager = parametric_system.parameter_manager
        print(parameter_manager)
        assert isinstance(parameter_manager, ParameterManager)
    optislang.dispose()
    assert dnr is None
