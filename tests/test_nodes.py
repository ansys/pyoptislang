from contextlib import nullcontext as does_not_raise
from pathlib import Path

import pytest

from ansys.optislang.core import Optislang, examples
from ansys.optislang.core.io import File, FileOutputFormat, RegisteredFile
from ansys.optislang.core.nodes import Node, ParametricSystem, RootSystem, System
from ansys.optislang.core.project_parametric import ParameterManager

pytestmark = pytest.mark.local_osl
calculator_w_parameters = examples.get_files("calculator_with_params")[1][0]
nested_systems = examples.get_files("nested_systems")[1][0]
connect_nodes = examples.get_files("nodes_connection")[1][0]
omdb_files = examples.get_files("omdb_files")[1][0]


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
    optislang.open(file_path=calculator_w_parameters)
    project = optislang.project
    root_system = project.root_system
    node = root_system.get_nodes()[0]
    assert isinstance(node, Node)
    optislang.dispose()


def test_node_properties(optislang: Optislang):
    """Test properties of the instance of `Node` class."""
    optislang.open(file_path=calculator_w_parameters)
    project = optislang.project
    root_system = project.root_system
    node = root_system.get_nodes()[0]
    assert isinstance(node, Node)
    assert isinstance(node.uid, str)
    optislang.dispose()


def test_node_queries(optislang: Optislang):
    """Test get methods of the instance of `Node` class."""
    optislang.open(file_path=calculator_w_parameters)
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

    reg_files = node.get_registered_files()
    assert len(reg_files) == 1
    assert isinstance(reg_files[0], RegisteredFile)

    res_files = node.get_result_files()
    assert len(res_files) == 1
    assert isinstance(res_files[0], RegisteredFile)

    states_ids = node.get_states_ids()
    assert len(states_ids) == 1
    assert isinstance(states_ids[0], str)

    status = node.get_status()
    assert isinstance(status, str)

    type = node.get_type()
    assert isinstance(type, str)
    assert type == "CalculatorSet"

    with does_not_raise() as dnr:
        print(node)
    assert dnr is None

    optislang.dispose()


def test_control(optislang: Optislang):
    """Test control methods of the instance of `Node` class."""
    optislang.open(file_path=calculator_w_parameters)
    project = optislang.project
    root_system = project.root_system
    node = root_system.find_nodes_by_name("Calculator")[0]

    for command in ["start", "restart", "stop_gently", "stop", "reset"]:
        output = node.control(command, wait_for_completion=False)
        assert isinstance(output, None)
        output = node.control(command, timeout=3)
        assert isinstance(output, bool)

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


def test_get_omdb_files(tmp_path: Path):
    """Test `get_omdb_files()` method."""
    optislang = Optislang(project_path=omdb_files)
    optislang.set_timeout(30)
    optislang.reset()
    optislang.start()
    project = optislang.project
    root_system = project.root_system

    sensitivity: ParametricSystem = root_system.find_nodes_by_name("Sensitivity")[0]
    s_omdb_file = sensitivity.get_omdb_files()
    assert len(s_omdb_file) > 0
    assert isinstance(s_omdb_file[0], File)

    most_inner_sensitivity: ParametricSystem = root_system.find_nodes_by_name(
        "MostInnerSensitivity", search_depth=3
    )[0]
    mis_omdb_file = most_inner_sensitivity.get_omdb_files()
    assert len(mis_omdb_file) > 0
    assert isinstance(mis_omdb_file[0], File)
    optislang.dispose()


def test_save_designs_as(tmp_path: Path):
    """Test `save_designs_as` method."""
    optislang = Optislang(project_path=omdb_files)
    optislang.set_timeout(30)
    optislang.reset()
    optislang.start()
    project = optislang.project
    root_system = project.root_system

    sensitivity: ParametricSystem = root_system.find_nodes_by_name("Sensitivity")[0]
    s_hids = sensitivity.get_states_ids()
    s_file = sensitivity.save_designs_as(s_hids[0], "FirstDesign", FileOutputFormat.CSV, tmp_path)
    assert isinstance(s_file, File)
    assert s_file.exists
    assert s_file.path.suffix == ".csv"

    most_inner_sensitivity: ParametricSystem = root_system.find_nodes_by_name(
        "MostInnerSensitivity", 3
    )[0]
    mis_hids = most_inner_sensitivity.get_states_ids()
    mis_file = most_inner_sensitivity.save_designs_as(mis_hids[0], "InnerDesign")
    assert isinstance(mis_file, File)
    assert mis_file.exists
    assert mis_file.path.suffix == ".json"
    mis_file.path.unlink()
    assert not mis_file.exists

    optislang.dispose()
