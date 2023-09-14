from contextlib import nullcontext as does_not_raise
from pathlib import Path

import pytest

from ansys.optislang.core import Optislang, examples
from ansys.optislang.core.io import File, FileOutputFormat, RegisteredFile
from ansys.optislang.core.node_types import AddinType, NodeType
from ansys.optislang.core.tcp.base_nodes import (
    Edge,
    TcpNodeProxy,
    TcpParametricSystemProxy,
    TcpRootSystemProxy,
    TcpSlotProxy,
    TcpSystemProxy,
)
from ansys.optislang.core.tcp.managers import CriteriaManager, ParameterManager, ResponseManager

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
    osl.timeout = 20
    return osl


# region TEST NODE
def test_node_initialization(optislang: Optislang):
    """Test `Node` initialization."""
    optislang.open(file_path=calculator_w_parameters)
    project = optislang.project
    root_system = project.root_system
    node = root_system.get_nodes()[0]
    assert isinstance(node, TcpNodeProxy)
    optislang.dispose()


def test_node_properties(optislang: Optislang):
    """Test properties of the instance of `Node` class."""
    optislang.open(file_path=calculator_w_parameters)
    project = optislang.project
    root_system = project.root_system
    node = root_system.get_nodes()[0]
    assert isinstance(node, TcpNodeProxy)
    assert isinstance(node.uid, str)
    assert isinstance(node.type, NodeType)
    assert isinstance(node.type.id, str)
    assert isinstance(node.type.subtype, AddinType)
    optislang.dispose()


def test_node_queries(optislang: Optislang):
    """Test get methods of the instance of `Node` class."""
    optislang.open(file_path=calculator_w_parameters)
    project = optislang.project
    root_system = project.root_system
    node: TcpNodeProxy = root_system.find_nodes_by_name("Calculator")[0]

    ancestors = node.get_ancestors()
    assert len(ancestors) == 1
    assert isinstance(ancestors[0], TcpRootSystemProxy)

    connections = node.get_connections()
    assert len(connect_nodes) == 2
    for connection in connections:
        assert isinstance(connection, Edge)

    exists = node.exists()
    assert exists
    assert isinstance(exists, bool)

    info = node._get_info()
    assert isinstance(info, dict)

    name = node.get_name()
    assert isinstance(name, str)
    assert name == "Calculator"

    parent_name = node.get_parent_name()
    assert isinstance(name, str)

    parent = node.get_parent()
    assert isinstance(parent, TcpRootSystemProxy)
    assert parent_name == parent.get_name()

    properties = node.get_properties()
    assert isinstance(properties, dict)

    stop_after_execution_property = node.get_property("StopAfterExecution")
    assert isinstance(stop_after_execution_property, bool)

    reg_files = node.get_registered_files()
    assert len(reg_files) == 1
    assert isinstance(reg_files[0], RegisteredFile)

    res_files = node.get_result_files()
    assert len(res_files) == 1
    assert isinstance(res_files[0], RegisteredFile)

    states_ids = node.get_states_ids()
    assert len(states_ids) == 1
    assert isinstance(states_ids[0], str)

    slots = node.get_slots()
    assert len(slots) == 8
    for slot in slots:
        assert isinstance(slot, TcpSlotProxy)

    status = node.get_status()
    assert isinstance(status, str)

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


def test_get_ancestors(optislang: Optislang):
    """Test `get_ancestors` method on nested systems."""
    optislang.open(file_path=nested_systems)
    project = optislang.project
    root_system = project.root_system
    system_in_sensitivity: TcpParametricSystemProxy = root_system.find_nodes_by_name(
        "System_inSensitivity", 2
    )[0]
    calculator_in_system: TcpNodeProxy = system_in_sensitivity.find_nodes_by_name(
        "Calculator_inSystem"
    )[0]
    ancestors = calculator_in_system.get_ancestors()
    assert len(ancestors) == 3
    assert isinstance(ancestors[0], TcpRootSystemProxy)
    assert isinstance(ancestors[1], TcpParametricSystemProxy)
    assert isinstance(ancestors[2], TcpSystemProxy)


def test_set_property(optislang: Optislang, tmp_path: Path):
    """Test `set_property` method."""
    optislang.open(calculator_w_parameters)
    optislang.save_as(tmp_path / "test_set_property.opf")
    root_system = optislang.project.root_system
    node: TcpNodeProxy = root_system.find_nodes_by_name("Calculator")[0]
    # enum prop
    set_enum_property = {
        "enum": ["read_and_write_mode", "classic_reevaluate_mode"],
        "value": "classic_reevaluate_mode",
    }
    node.set_property("ReadMode", set_enum_property)
    assert node.get_property("ReadMode") == set_enum_property

    # bool prop
    set_bool_property = True
    node.set_property("StopAfterExecution", set_bool_property)
    assert node.get_property("StopAfterExecution") == set_bool_property

    # int prop
    set_int_property = 2
    node.set_property("ExecutionOptions", set_int_property)
    assert node.get_property("ExecutionOptions") == set_int_property

    optislang.dispose()


# endregion


# region TEST SYSTEM
def test_find_node_by_uid(optislang: Optislang):
    """Test `find_node_by_uid`."""
    optislang.open(file_path=nested_systems)
    project = optislang.project
    root_system = project.root_system

    # level 1
    level0_node = root_system.find_node_by_uid(
        uid="8854b2c4-fd8a-4e07-839e-1f36553e2d40", search_depth=1
    )
    assert isinstance(level0_node, TcpNodeProxy)
    with does_not_raise() as dnr:
        print(level0_node)
    assert dnr is None

    level0_system = root_system.find_node_by_uid(
        uid="a8375c1f-0e39-4901-aa29-56d88f693b54", search_depth=1
    )
    assert isinstance(level0_system, TcpSystemProxy)
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
    assert isinstance(level1_node, TcpNodeProxy)

    higher_level = root_system.find_node_by_uid(
        uid="ab7d50e2-b031-4c75-b701-fd9fcadf779c", search_depth=2
    )
    assert higher_level is None

    # level 3
    level2_node = root_system.find_node_by_uid(
        uid="ab7d50e2-b031-4c75-b701-fd9fcadf779c", search_depth=3
    )
    assert isinstance(level2_node, TcpNodeProxy)

    higher_level = root_system.find_node_by_uid(
        uid="161992fc-d1ee-487f-8bab-0b9897e641e8", search_depth=3
    )
    assert higher_level is None

    # level 4
    level3_node = root_system.find_node_by_uid(
        uid="161992fc-d1ee-487f-8bab-0b9897e641e8", search_depth=4
    )
    assert isinstance(level3_node, TcpNodeProxy)

    optislang.dispose()


def test_find_node_by_name(optislang: Optislang):
    """Test `find_node_by_name`."""
    optislang.open(file_path=nested_systems)
    project = optislang.project
    root_system = project.root_system

    # level 1
    level0_node = root_system.find_nodes_by_name(name="Calculator", search_depth=1)[0]
    assert isinstance(level0_node, TcpNodeProxy)

    level0_system = root_system.find_nodes_by_name(name="System", search_depth=1)[0]
    assert isinstance(level0_system, TcpSystemProxy)

    higher_level = root_system.find_nodes_by_name(name="Calculator_inSystem", search_depth=1)
    assert isinstance(higher_level, tuple)
    assert len(higher_level) == 0

    # level 2
    level1_node = root_system.find_nodes_by_name(name="Calculator_inSensitivity", search_depth=2)[0]
    assert isinstance(level1_node, TcpNodeProxy)

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


# endregion


# region TEST PARAMETRIC SYSTEM
def test_get_managers(optislang: Optislang):
    """Test initialization and __str__ methods of both `ParametricSystem` and managers."""
    optislang.open(file_path=nested_systems)
    project = optislang.project
    root_system = project.root_system
    parametric_system: TcpParametricSystemProxy = root_system.find_nodes_by_name(
        "Parametric System"
    )[0]
    with does_not_raise() as dnr:
        print(parametric_system)
        parameter_manager = parametric_system.parameter_manager
        assert isinstance(parameter_manager, ParameterManager)
        print(parameter_manager)

        criteria_manager = parametric_system.criteria_manager
        assert isinstance(criteria_manager, CriteriaManager)
        print(criteria_manager)

        response_manager = parametric_system.response_manager
        assert isinstance(response_manager, ResponseManager)
        print(response_manager)

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

    sensitivity: TcpParametricSystemProxy = root_system.find_nodes_by_name("Sensitivity")[0]
    s_omdb_file = sensitivity.get_omdb_files()
    assert len(s_omdb_file) > 0
    assert isinstance(s_omdb_file[0], File)

    most_inner_sensitivity: TcpParametricSystemProxy = root_system.find_nodes_by_name(
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

    sensitivity: TcpParametricSystemProxy = root_system.find_nodes_by_name("Sensitivity")[0]
    s_hids = sensitivity.get_states_ids()
    s_file = sensitivity.save_designs_as(s_hids[0], "FirstDesign", FileOutputFormat.CSV, tmp_path)
    assert isinstance(s_file, File)
    assert s_file.exists
    assert s_file.path.suffix == ".csv"

    most_inner_sensitivity: TcpParametricSystemProxy = root_system.find_nodes_by_name(
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


# endregion
