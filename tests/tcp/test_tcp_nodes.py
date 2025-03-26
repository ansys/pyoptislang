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

import pytest

from ansys.optislang.core import Optislang
from ansys.optislang.core.io import File, RegisteredFile
from ansys.optislang.core.node_types import AddinType, NodeType, Sensitivity, optislang_node
from ansys.optislang.core.osl_server import OslVersion
from ansys.optislang.core.tcp.managers import (
    CriteriaManager,
    DesignManager,
    ParameterManager,
    ResponseManager,
)
from ansys.optislang.core.tcp.nodes import (
    DesignFlow,
    Edge,
    ExecutionOption,
    TcpInnerInputSlotProxy,
    TcpInnerOutputSlotProxy,
    TcpInputSlotProxy,
    TcpIntegrationNodeProxy,
    TcpNodeProxy,
    TcpOutputSlotProxy,
    TcpParametricSystemProxy,
    TcpRootSystemProxy,
    TcpSystemProxy,
)

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
        output = node.control(command, timeout=60)
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


def test_node_execution_options(optislang: Optislang, tmp_example_project):
    """Test `set_execution_options` and `get_execution_options` methods."""
    optislang.application.open(file_path=tmp_example_project("calculator_with_params"))
    root_system = optislang.project.root_system
    node: TcpNodeProxy = root_system.find_nodes_by_name("Calculator")[0]

    execution_options_list = [
        ExecutionOption.INACTIVE,
        ExecutionOption.ACTIVE,
        ExecutionOption.STARTING_POINT,
        ExecutionOption.ACTIVE | ExecutionOption.STARTING_POINT,
        ExecutionOption.END_POINT,
        ExecutionOption.ACTIVE | ExecutionOption.END_POINT,
        ExecutionOption.SAVE_POINT,
        ExecutionOption.ACTIVE | ExecutionOption.SAVE_POINT,
        ExecutionOption.RECYCLE_RESULTS,
        ExecutionOption.ACTIVE | ExecutionOption.RECYCLE_RESULTS,
    ]

    for execution_options in execution_options_list:
        node.set_execution_options(execution_options)
        recv_execution_options = node.get_execution_options()
        assert execution_options == recv_execution_options


# endregion


# region TEST INTEGRATION_NODE


def test_register_location(optislang: Optislang):
    """Test `register_location` and `get_registered_locations`."""
    root_system = optislang.application.project.root_system
    sensitivity: TcpParametricSystemProxy = root_system.create_node(type_=Sensitivity)
    integration_node: TcpIntegrationNodeProxy = sensitivity.create_node(
        type_=optislang_node,
        design_flow=DesignFlow.RECEIVE_SEND,
    )
    # input slot
    actual_name = integration_node.register_location_as_input_slot(
        location="input_slot_1",
        name="input_slot_1",
        reference_value=10,
    )
    input_slots = integration_node.get_registered_input_slots()
    assert len(input_slots) == 1
    assert isinstance(input_slots[0], dict)
    assert actual_name == "input_slot_1"

    # internal variable
    actual_name = integration_node.register_location_as_internal_variable(
        location={"expression": "10", "id": "variable_1"},
        name="variable_1",
        reference_value=10,
    )
    internal_variables = integration_node.get_internal_variables()
    assert len(internal_variables) == 1
    assert isinstance(internal_variables[0], dict)
    assert actual_name == "variable_1"

    # output slot
    actual_name = integration_node.register_location_as_output_slot(
        location="output_slot_1",
        name="output_slot_1",
        reference_value=10,
    )
    output_slots = integration_node.get_registered_output_slots()
    assert len(output_slots) == 1
    assert isinstance(output_slots[0], dict)
    assert actual_name == "output_slot_1"

    # parameter
    actual_name = integration_node.register_location_as_parameter(
        location="parameter_1",
        name="parameter1",
        reference_value=10,
    )
    parameters = integration_node.get_registered_parameters()
    assert len(parameters) == 1
    assert isinstance(parameters[0], dict)
    assert actual_name == "parameter1"

    # response
    actual_name = integration_node.register_location_as_response(
        location="response_1",
        name="response_1",
        reference_value=10,
    )

    responses = integration_node.get_registered_responses()
    assert len(responses) == 1
    assert isinstance(responses[0], dict)
    assert actual_name == "response_1"


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

    design_manager = parametric_system.design_manager
    assert isinstance(design_manager, DesignManager)


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
    if optislang.osl_version < OslVersion(24, 1, 0, 0):
        pytest.skip(f"Not compatible with {optislang.osl_version_string}")

    optislang.application.open(file_path=tmp_example_project("omdb_files"))
    optislang.timeout = 60
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


# endregion
