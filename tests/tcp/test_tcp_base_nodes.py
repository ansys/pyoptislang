from pathlib import Path

import pytest

from ansys.optislang.core import Optislang
from ansys.optislang.core.io import File, FileOutputFormat, RegisteredFile
from ansys.optislang.core.node_types import AddinType, NodeType
from ansys.optislang.core.tcp.base_nodes import (
    Edge,
    TcpInnerInputSlotProxy,
    TcpInnerOutputSlotProxy,
    TcpInputSlotProxy,
    TcpNodeProxy,
    TcpOutputSlotProxy,
    TcpParametricSystemProxy,
    TcpRootSystemProxy,
    TcpSystemProxy,
)
from ansys.optislang.core.tcp.managers import CriteriaManager, ParameterManager, ResponseManager

pytestmark = pytest.mark.local_osl


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


# region TEST NODE
def test_node_initialization(optislang: Optislang, tmp_example_project):
    """Test `Node` initialization."""
    optislang.application.open(file_path=tmp_example_project("calculator_with_params"))
    project = optislang.project
    root_system = project.root_system
    node = root_system.get_nodes()[0]
    assert isinstance(node, TcpNodeProxy)


def test_node_properties(optislang: Optislang, tmp_example_project):
    """Test properties of the instance of `Node` class."""
    optislang.application.open(file_path=tmp_example_project("calculator_with_params"))
    project = optislang.project
    root_system = project.root_system
    node = root_system.get_nodes()[0]
    assert isinstance(node, TcpNodeProxy)
    assert isinstance(node.uid, str)
    assert isinstance(node.type, NodeType)
    assert isinstance(node.type.id, str)
    assert isinstance(node.type.subtype, AddinType)


def test_node_queries(optislang: Optislang, tmp_example_project):
    """Test get methods of the instance of `Node` class."""
    optislang.application.open(file_path=tmp_example_project("calculator_with_params"))
    project = optislang.project
    root_system = project.root_system
    node: TcpNodeProxy = root_system.find_nodes_by_name("Calculator")[0]

    ancestors = node.get_ancestors()
    assert len(ancestors) == 1
    assert isinstance(ancestors[0], TcpRootSystemProxy)

    connections = node.get_connections()
    assert len(connections) == 4
    for connection in connections:
        assert isinstance(connection, Edge)

    exists = node.exists()
    assert exists
    assert isinstance(exists, bool)

    info = node._get_info()
    assert isinstance(info, dict)

    input_slots = node.get_input_slots()
    assert len(input_slots) == 5
    for slot in input_slots:
        assert isinstance(slot, TcpInputSlotProxy)

    name = node.get_name()
    assert isinstance(name, str)
    assert name == "Calculator"

    output_slots = node.get_output_slots()
    assert len(output_slots) == 5
    for slot in output_slots:
        assert isinstance(slot, TcpOutputSlotProxy)

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

    status = node.get_status()
    assert isinstance(status, str)

    print(node)


def test_control(optislang: Optislang, tmp_example_project):
    """Test control methods of the instance of `Node` class."""
    optislang.application.open(file_path=tmp_example_project("calculator_with_params"))
    project = optislang.project
    root_system = project.root_system
    node = root_system.find_nodes_by_name("Calculator")[0]

    for command in ["start", "restart", "stop_gently", "stop", "reset"]:
        output = node.control(command, wait_for_completion=False)
        assert output is None
        output = node.control(command, timeout=3)
        assert isinstance(output, bool)


def test_get_ancestors(optislang: Optislang, tmp_example_project):
    """Test `get_ancestors` method on nested systems."""
    optislang.application.open(file_path=tmp_example_project("nested_systems"))
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

    calculator_in_parametric_system = root_system.find_nodes_by_name(
        "Calculator_inParametricSystem", 2
    )[0]
    ancestors = calculator_in_parametric_system.get_ancestors()
    assert len(ancestors) == 2
    assert isinstance(ancestors[0], TcpRootSystemProxy)
    assert isinstance(ancestors[1], TcpParametricSystemProxy)


def test_set_property(optislang: Optislang, tmp_example_project):
    """Test `set_property` method."""
    optislang.application.open(file_path=tmp_example_project("calculator_with_params"))
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


# endregion


# region TEST SYSTEM
def test_find_node_by_uid(optislang: Optislang, tmp_example_project):
    """Test `find_node_by_uid`."""
    optislang.application.open(file_path=tmp_example_project("nested_systems"))
    project = optislang.project
    root_system = project.root_system

    # level 1
    level0_node = root_system.find_node_by_uid(
        uid="8854b2c4-fd8a-4e07-839e-1f36553e2d40", search_depth=1
    )
    assert isinstance(level0_node, TcpNodeProxy)
    print(level0_node)

    level0_system = root_system.find_node_by_uid(
        uid="a8375c1f-0e39-4901-aa29-56d88f693b54", search_depth=1
    )
    assert isinstance(level0_system, TcpSystemProxy)
    print(level0_system)

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


def test_find_node_by_name(optislang: Optislang, tmp_example_project):
    """Test `find_node_by_name`."""
    optislang.application.open(file_path=tmp_example_project("nested_systems"))
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


# endregion


# region TEST PARAMETRIC SYSTEM
def test_managers(optislang: Optislang, tmp_example_project):
    """Test initialization and __str__ methods of both `ParametricSystem` and `ParameterManager`."""
    optislang.application.open(file_path=tmp_example_project("nested_systems"))
    project = optislang.project
    root_system = project.root_system
    parametric_system: TcpParametricSystemProxy = root_system.find_nodes_by_name(
        "Parametric System"
    )[0]
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


def test_get_inner_slots(optislang: Optislang, tmp_example_project):
    """Test `get_inner_[input, output]_slots`."""
    optislang.application.open(file_path=tmp_example_project("nested_systems"))
    project = optislang.project
    root_system = project.root_system
    parametric_system: TcpParametricSystemProxy = root_system.find_nodes_by_name(
        "Parametric System"
    )[0]
    inner_input_slots = parametric_system.get_inner_input_slots()
    assert isinstance(inner_input_slots[0], TcpInnerInputSlotProxy)
    inner_output_slots = parametric_system.get_inner_output_slots()
    assert isinstance(inner_output_slots[0], TcpInnerOutputSlotProxy)


def test_get_omdb_files(optislang: Optislang, tmp_example_project):
    """Test `get_omdb_files()` method."""
    optislang.application.open(file_path=tmp_example_project("omdb_files"))
    optislang.timeout = 30
    optislang.application.project.reset()
    optislang.application.project.start()
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


def test_save_designs_as(tmp_path: Path, tmp_example_project):
    """Test `save_designs_as` method."""
    optislang = Optislang(project_path=tmp_example_project("omdb_files"))
    optislang.timeout = 30
    optislang.application.project.reset()
    optislang.application.project.start()

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


# endregion