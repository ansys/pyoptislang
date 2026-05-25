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

from contextlib import closing
import logging
import os
from pathlib import Path
import socket
import tempfile
import time
import uuid

import pytest

from ansys.optislang.core import OslServerProcess, errors
from ansys.optislang.core.communication_channels import CommunicationChannel
from ansys.optislang.core.node_types import NodeType
from ansys.optislang.core.osl_server import OslVersion
from ansys.optislang.core.placeholder_types import PlaceholderType, UserLevel
import ansys.optislang.core.tcp.osl_server as tos

_host = "127.0.0.1"


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


_msg = '{ "What": "SYSTEMS_STATUS_INFO" }'

pytestmark = pytest.mark.local_osl


def create_osl_server_process(shutdown_on_finished=False, project_path=None) -> OslServerProcess:
    port = find_free_port()
    with tempfile.TemporaryDirectory() as temp_dir:
        server_info_file = Path(temp_dir) / "osl_server_info.ini"
        osl_server_process = OslServerProcess(
            shutdown_on_finished=shutdown_on_finished,
            project_path=project_path,
            port_range=(port, port),
            server_info=server_info_file,
            enable_tcp_server=True,
            listener=("127.0.0.1", 56789) if shutdown_on_finished else None,
        )
        osl_server_process.start()

        start_timeout = 180
        start = time.time()
        while not os.path.exists(server_info_file):
            osl_process_exit_code = osl_server_process.wait_for_finished(timeout=0.1)
            if osl_process_exit_code is not None:
                raise RuntimeError(
                    f"optiSLang Process start failed (returncode: {osl_process_exit_code})."
                )
            if time.time() - start > start_timeout:
                break

        if os.path.exists(server_info_file):
            return osl_server_process
        osl_server_process.terminate()
        raise TimeoutError("optiSLang Process start timed out after {}s".format(start_timeout))


@pytest.fixture(scope="function", autouse=False)
def osl_server_process():
    # Will be executed before each test
    return create_osl_server_process(shutdown_on_finished=True)


@pytest.fixture(scope="function", autouse=False)
def tcp_listener():
    return tos.TcpOslListener(
        port_range=(49152, 65535),
        timeout=60,
        name="GeneralListener",
        uid=str(uuid.uuid4()),
        logger=logging.getLogger(__name__),
        communication_channel=CommunicationChannel.TCP,
    )


@pytest.fixture(scope="function", autouse=False)
def tcp_client() -> tos.TcpClient:
    """Create TcpClient.

    Returns
    -------
    TcpOslServer:
        Class which provides access to optiSLang server using plain TCP/IP communication protocol.
    """
    return tos.TcpClient()


def create_tcp_osl_server(osl_server_process: OslServerProcess) -> tos.TcpOslServer:
    """Create TcpOslServer.

    Parameters
    ----------
    Tuple (host: str, port: int)
        host: A string representation of an IPv4/v6 address or domain name of running optiSLang
            server.
        port: A numeric port number of running optiSLang server.

    Returns
    -------
    TcpOslServer:
        Class which provides access to optiSLang server using plain TCP/IP communication protocol.
    """
    tcp_osl_server = tos.TcpOslServer(host=_host, port=osl_server_process.port_range[0])
    tcp_osl_server.timeout = 60
    return tcp_osl_server


# region FunctionsAttributeRegister
def test_functions_attribute_register():
    functions_attribute_register = tos.FunctionsAttributeRegister(
        1, lambda value: isinstance(value, (int, float))
    )
    assert functions_attribute_register.default_value == 1
    functions_attribute_register.default_value = 10
    assert functions_attribute_register.default_value == 10

    with pytest.raises(ValueError):
        functions_attribute_register.register("invalid", "string")

    functions_attribute_register.register("test1", 20)
    functions_attribute_register.register("test2", 30)
    assert functions_attribute_register.get_value("test1") == 20
    assert functions_attribute_register.get_value("dont_exist") == 10

    functions_attribute_register.unregister("test1")
    assert functions_attribute_register.get_value("test1") == 10
    assert functions_attribute_register.is_registered("test2")
    assert not functions_attribute_register.is_registered("test1")
    functions_attribute_register.unregister_all()
    assert not functions_attribute_register.is_registered("test2")


# endregion


# region TcpClient
def test_client_properties(osl_server_process: OslServerProcess, tcp_client: tos.TcpClient):
    "Test ``local_address`` and ``remote_address``."
    tcp_client.connect(host=_host, port=osl_server_process.port_range[0])
    ra = tcp_client.remote_address
    assert isinstance(ra, tuple)
    assert isinstance(ra[0], str)
    assert isinstance(ra[1], int)
    la = tcp_client.local_address
    assert isinstance(la, tuple)
    assert isinstance(la[0], str)
    assert isinstance(la[1], int)
    tcp_client.disconnect()
    osl_server_process.terminate()


def test_connect_and_disconnect(osl_server_process: OslServerProcess, tcp_client: tos.TcpClient):
    "Test ``connect``."
    tcp_client.connect(host=_host, port=osl_server_process.port_range[0])
    tcp_client.disconnect()
    osl_server_process.terminate()


def test_tcpclient_properties(osl_server_process: OslServerProcess, tcp_client: tos.TcpClient):
    "Test clients properties."
    tcp_client.connect(host=_host, port=osl_server_process.port_range[0])
    remote_address = tcp_client.remote_address
    assert isinstance(remote_address, tuple)
    assert isinstance(remote_address[0], str)
    assert isinstance(remote_address[1], int)
    local_address = tcp_client.local_address
    assert isinstance(local_address, tuple)
    assert isinstance(local_address[0], str)
    assert isinstance(local_address[1], int)
    tcp_client.disconnect()
    osl_server_process.terminate()


def test_send_msg(osl_server_process: OslServerProcess, tcp_client: tos.TcpClient):
    "Test ``send_msg`"
    tcp_client.connect(host=_host, port=osl_server_process.port_range[0])
    tcp_client.send_msg(_msg)
    tcp_client.disconnect()
    osl_server_process.terminate()


@pytest.mark.parametrize("path_type", [str, Path])
def test_send_file(
    osl_server_process: OslServerProcess,
    tcp_client: tos.TcpClient,
    tmp_path: Path,
    path_type,
):
    "Test ``send_file``"
    file_path = path_type(tmp_path / "testfile.txt")

    with open(file_path, "w") as testfile:
        testfile.write(_msg)
    tcp_client.connect(host=_host, port=osl_server_process.port_range[0])
    tcp_client.send_file(file_path)
    tcp_client.disconnect()
    osl_server_process.terminate()


def test_receive_msg(osl_server_process: OslServerProcess, tcp_client: tos.TcpClient):
    "Test ``receive_msg``."
    tcp_client.connect(host=_host, port=osl_server_process.port_range[0])
    tcp_client.send_msg(_msg)
    msg = tcp_client.receive_msg()
    tcp_client.disconnect()
    osl_server_process.terminate()
    assert isinstance(msg, str)


@pytest.mark.parametrize("path_type", [str, Path])
def test_receive_file(
    osl_server_process: OslServerProcess,
    tcp_client: tos.TcpClient,
    tmp_path: Path,
    path_type,
):
    "Test ``receive_file`"
    file_path = path_type(tmp_path / "testfile.txt")
    received_path = path_type(tmp_path / "received.txt")

    with open(file_path, "w") as testfile:
        testfile.write(_msg)
    tcp_client.connect(host=_host, port=osl_server_process.port_range[0])
    tcp_client.send_file(file_path)
    tcp_client.receive_file(received_path)
    assert os.path.isfile(received_path)
    tcp_client.disconnect()
    osl_server_process.terminate()


# endregion


# region TcpListener
def test_is_initialized(osl_server_process: OslServerProcess, tcp_listener: tos.TcpOslListener):
    """Test `is_initialized`."""
    assert tcp_listener.is_initialized()
    tcp_listener.dispose()
    osl_server_process.terminate()


def test_listener_properties(
    osl_server_process: OslServerProcess, tcp_listener: tos.TcpOslListener
):
    """Test `name`, `uid`, `timeout`, `host_addresses`, `port`, `refresh_listener..`."""
    assert isinstance(tcp_listener.uid, str)
    new_uid = str(uuid.uuid4())
    tcp_listener.uid = new_uid
    assert tcp_listener.uid == new_uid
    name = tcp_listener.name
    assert isinstance(name, str)
    assert name == "GeneralListener"

    assert isinstance(tcp_listener.timeout, (float, int))
    assert tcp_listener.timeout == 60
    tcp_listener.timeout = 15
    assert tcp_listener.timeout == 15

    assert isinstance(tcp_listener.host_addresses, list)
    assert all(isinstance(elem, str) for elem in tcp_listener.host_addresses)
    assert isinstance(tcp_listener.port, int)
    refresh = tcp_listener.refresh_listener_registration
    assert isinstance(refresh, bool)
    assert refresh == False
    tcp_listener.refresh_listener_registration = True
    new_refresh = tcp_listener.refresh_listener_registration
    assert isinstance(new_refresh, bool)
    assert new_refresh == True
    tcp_listener.dispose()
    osl_server_process.terminate()


def test_add_clear_callback(osl_server_process: OslServerProcess, tcp_listener: tos.TcpOslListener):
    """Test add and clear callback."""
    tcp_listener.add_callback(print, "print-this")
    tcp_listener.clear_callbacks()
    tcp_listener.dispose()
    osl_server_process.terminate()


def test_start_stop_listening(
    osl_server_process: OslServerProcess, tcp_listener: tos.TcpOslListener
):
    """Test add and clear callback."""
    tcp_listener.start_listening()
    assert tcp_listener.is_listening()
    tcp_listener.stop_listening()
    assert not tcp_listener.is_listening()
    tcp_listener.dispose()
    osl_server_process.terminate()


# endregion


# region TcpOslServer


def test_tcp_osl_properties(osl_server_process: OslServerProcess):
    """Test `host`, `port` and `timeout` properties of `TcpOslServer` class."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    assert isinstance(tcp_osl_server.host, str)
    assert isinstance(tcp_osl_server.port, int)

    osl_version = tcp_osl_server.osl_version
    assert len(osl_version) == 4
    assert isinstance(osl_version[0], int)
    assert isinstance(osl_version[1], int)
    assert isinstance(osl_version[2], int)
    assert isinstance(osl_version[3], int)
    osl_version_string = tcp_osl_server.osl_version_string
    assert isinstance(osl_version_string, str)

    assert isinstance(tcp_osl_server.timeout, (int, float))
    assert tcp_osl_server.timeout == 60
    tcp_osl_server.timeout = 20
    assert tcp_osl_server.timeout == 20

    assert not tcp_osl_server.is_remote

    with pytest.raises(ValueError):
        tcp_osl_server.timeout = -5
    with pytest.raises(ValueError):
        tcp_osl_server.timeout = "5"
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_max_request_attempts_register(osl_server_process: OslServerProcess):
    """Test `max_request_attempts_register`."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    max_request_attempts_register = tcp_osl_server.max_request_attempts_register
    assert max_request_attempts_register.default_value == 2

    with pytest.raises(ValueError):
        max_request_attempts_register.register("invalid_value", "s")

    with pytest.raises(ValueError):
        max_request_attempts_register.register("invalid_value", -1)

    with pytest.raises(ValueError):
        max_request_attempts_register.register("invalid_value", True)

    with pytest.raises(ValueError):
        max_request_attempts_register.register("invalid_value", (1, 0))

    max_request_attempts_register.register("valid_value1", 4)
    max_request_attempts_register.register(tcp_osl_server.__class__.add_criterion, 3)
    assert max_request_attempts_register.is_registered("valid_value1")
    assert max_request_attempts_register.is_registered(tcp_osl_server.__class__.add_criterion)
    assert max_request_attempts_register.is_registered("add_criterion")
    assert max_request_attempts_register.get_value("valid_value1") == 4
    assert max_request_attempts_register.get_value("add_criterion") == 3
    assert max_request_attempts_register.get_value(tcp_osl_server.__class__.add_criterion) == 3

    # overwrite
    max_request_attempts_register.get_value("evaluate_design") == 1
    max_request_attempts_register.register("evaluate_design", 3)
    assert max_request_attempts_register.get_value("evaluate_design") == 3

    max_request_attempts_register.unregister("valid_value1")
    assert (
        max_request_attempts_register.get_value("valid_value1")
        == max_request_attempts_register.default_value
    )
    assert not max_request_attempts_register.is_registered("valid_value1")

    max_request_attempts_register.unregister_all()
    assert not max_request_attempts_register.is_registered("valid_value2")
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_timeouts_register(osl_server_process: OslServerProcess):
    """Test `timeouts_register`."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    timeouts_register = tcp_osl_server.timeouts_register
    # note: method `create_tcp_osl_server` modifies timeout, default is `30` otherwise
    assert timeouts_register.default_value == 60

    with pytest.raises(ValueError):
        timeouts_register.register("invalid_value", "s")

    with pytest.raises(ValueError):
        timeouts_register.register("invalid_value", -1)

    with pytest.raises(ValueError):
        timeouts_register.register("invalid_value", True)

    with pytest.raises(ValueError):
        timeouts_register.register("invalid_value", (1, 0))

    timeouts_register.register("valid_value1", 8.0)
    timeouts_register.register("valid_value2", None)
    timeouts_register.register(tcp_osl_server.__class__.add_criterion, 15)
    assert timeouts_register.is_registered("valid_value1")
    assert timeouts_register.is_registered("valid_value2")
    assert timeouts_register.is_registered(tcp_osl_server.__class__.add_criterion)
    assert timeouts_register.is_registered("add_criterion")
    assert timeouts_register.get_value("valid_value1") == 8
    assert timeouts_register.get_value("valid_value2") is None
    assert timeouts_register.get_value("add_criterion") == 15
    assert timeouts_register.get_value(tcp_osl_server.__class__.add_criterion) == 15

    # overwrite
    timeouts_register.get_value("evaluate_design") is None
    timeouts_register.register("evaluate_design", 1000)
    assert timeouts_register.get_value("evaluate_design") == 1000

    timeouts_register.unregister("valid_value1")
    assert timeouts_register.get_value("valid_value1") == timeouts_register.default_value
    assert not timeouts_register.is_registered("valid_value1")

    timeouts_register.unregister_all()
    assert not timeouts_register.is_registered("valid_value2")

    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_add_remove_set_criterion(osl_server_process: OslServerProcess):
    """Test ``add_criterion``, ``remove_criterion/a``, ``set_criterion_property``."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    root_system_uid = (
        tcp_osl_server.get_full_project_tree_with_properties()
        .get("projects", [{}])[0]
        .get("system", {})
        .get("uid", None)
    )
    if not root_system_uid:
        assert False
    name = "my_crit_1"
    expression = "1+1"
    criterion_type = "greaterequal"
    limit = "-1*5"
    tcp_osl_server.add_criterion(
        uid=root_system_uid,
        criterion_type=criterion_type,
        expression=expression,
        name=name,
        limit=limit,
    )
    tcp_osl_server.add_criterion(
        uid=root_system_uid,
        criterion_type="max",
        expression="1+1",
        name="my_crit_2",
    )
    criterion_dict = tcp_osl_server.get_criterion(uid=root_system_uid, name=name)
    assert criterion_dict.get(name)
    assert criterion_dict[name]["expression"] == expression
    assert criterion_dict[name]["type"]["value"] == criterion_type
    assert criterion_dict[name]["limit"] == limit

    tcp_osl_server.set_criterion_property(
        uid=root_system_uid, criterion_name="my_crit_2", name="expression", value="2+2"
    )
    criterion_dict = tcp_osl_server.get_criterion(uid=root_system_uid, name="my_crit_2")
    assert criterion_dict["my_crit_2"]["expression"] == "2+2"

    tcp_osl_server.remove_criterion(uid=root_system_uid, name="my_crit_2")
    assert len(tcp_osl_server.get_criteria(root_system_uid)) == 1

    tcp_osl_server.remove_criteria(root_system_uid)
    assert len(tcp_osl_server.get_criteria(root_system_uid)) == 0

    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


# def test_close(osl_server_process: OslServerProcess):
#     tcp_osl_server = create_tcp_osl_server(osl_server_process)
#     tcp_osl_server.close()
#     tcp_osl_server.new()
#     tcp_osl_server.dispose()


def test_connect_nodes(tmp_example_project):
    """Test `connect_nodes` method."""
    osl_server_process = create_osl_server_process(
        shutdown_on_finished=True, project_path=tmp_example_project("nodes_connection")
    )
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    variable_uid = "b8b8b48f-b806-4382-9777-f03ceb5dccc0"
    calculator_uid = "e63ce638-ec33-47cf-ba02-2d83771678fa"

    tcp_osl_server.connect_nodes(
        from_actor_uid=variable_uid, from_slot="OVar", to_actor_uid=calculator_uid, to_slot="A"
    )
    info = tcp_osl_server.get_actor_info(calculator_uid)
    assert len(info["connections"]) == 1
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_create_remove_node(osl_server_process: OslServerProcess):
    """Test `create_node` and `remove_node` methods."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    tree = tcp_osl_server.get_full_project_tree()
    assert len(tree["projects"][0]["system"]["nodes"]) == 0

    uid = tcp_osl_server.create_node(type_="CalculatorSet")
    new_tree = tcp_osl_server.get_full_project_tree()
    assert len(new_tree["projects"][0]["system"]["nodes"]) == 1

    tcp_osl_server.remove_node(uid)
    empty_tree = tcp_osl_server.get_full_project_tree()
    assert len(empty_tree["projects"][0]["system"]["nodes"]) == 0
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_disconnect_slot(tmp_example_project):
    "Test ``disconnect_slot`` command."
    osl_server_process = create_osl_server_process(
        shutdown_on_finished=True, project_path=tmp_example_project("calculator_with_params")
    )
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    UID = "3577cb69-15b9-4ad1-a53c-ac8af8aaea82"
    INPUT_SLOT_NAME = "OVar"
    OUTPUT_SLOT_NAME = "var"

    # input slot
    tcp_osl_server.disconnect_slot(UID, INPUT_SLOT_NAME, "sdInputs")
    # output slot
    tcp_osl_server.disconnect_slot(UID, OUTPUT_SLOT_NAME, "sdOutputs")

    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_evaluate_design(tmp_example_project):
    "Test ``evaluate_design``."
    osl_server_process = create_osl_server_process(
        shutdown_on_finished=True, project_path=tmp_example_project("calculator_with_params")
    )
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    tcp_osl_server.reset()
    result = tcp_osl_server.evaluate_design({"a": 5, "b": 10})
    assert isinstance(result, list)
    assert isinstance(result[0], dict)
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_get_actor_queries(tmp_example_project):
    """Test `get_actor_` - `info`, `properties`,`states`, `status_info`, `supports` queries."""
    osl_server_process = create_osl_server_process(
        shutdown_on_finished=True, project_path=tmp_example_project("calculator_with_params")
    )
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    UID = "3577cb69-15b9-4ad1-a53c-ac8af8aaea82"
    INVALID_UID = "3577cb69-15b9-4ad1-a53c-ac8af8aaea83"
    # info
    info = tcp_osl_server.get_actor_info(UID)
    assert isinstance(info, dict)
    with pytest.raises(errors.OslCommandError):
        info = tcp_osl_server.get_actor_info(INVALID_UID)
    # internal variables
    internal_variables = tcp_osl_server.get_actor_internal_variables(uid=UID)
    assert len(internal_variables) == 3
    assert isinstance(internal_variables[0], dict)
    with pytest.raises(errors.OslCommandError):
        internal_variables = tcp_osl_server.get_actor_internal_variables(uid=INVALID_UID)
    # properties
    properties = tcp_osl_server.get_actor_properties(UID)
    assert isinstance(properties, dict)
    with pytest.raises(errors.OslCommandError):
        properties = tcp_osl_server.get_actor_properties(INVALID_UID)
    # registered input slots
    registered_input_slots = tcp_osl_server.get_actor_registered_input_slots(uid=UID)
    assert isinstance(registered_input_slots, list)
    assert len(registered_input_slots) == 0
    with pytest.raises(errors.OslCommandError):
        tcp_osl_server.get_actor_registered_input_slots(uid=INVALID_UID)
    # registered output slots
    registered_output_slots = tcp_osl_server.get_actor_registered_output_slots(uid=UID)
    assert len(registered_output_slots) == 1
    assert isinstance(registered_output_slots[0], dict)
    with pytest.raises(errors.OslCommandError):
        tcp_osl_server.get_actor_registered_output_slots(uid=INVALID_UID)
    # registered parameters
    registered_parameters = tcp_osl_server.get_actor_registered_parameters(uid=UID)
    assert isinstance(registered_parameters, list)
    assert len(registered_parameters) == 0
    with pytest.raises(errors.OslCommandError):
        tcp_osl_server.get_actor_registered_parameters(uid=INVALID_UID)
    # registered responses
    registered_responses = tcp_osl_server.get_actor_registered_responses(uid=UID)
    assert len(registered_responses) == 2
    assert isinstance(registered_responses[0], dict)
    with pytest.raises(errors.OslCommandError):
        tcp_osl_server.get_actor_registered_responses(uid=INVALID_UID)
    # states
    states = tcp_osl_server.get_actor_states(UID)
    assert isinstance(states, dict)
    with pytest.raises(errors.OslCommandError):
        states = tcp_osl_server.get_actor_states(INVALID_UID)
    # status_info
    status_info = tcp_osl_server.get_actor_status_info(UID, "0")
    assert isinstance(status_info, dict)
    with pytest.raises(errors.OslCommandError):
        status_info = tcp_osl_server.get_actor_status_info(INVALID_UID, "0")
    with pytest.raises(errors.OslCommandError):
        status_info = tcp_osl_server.get_actor_status_info(UID, "1")
    # supports
    supports = tcp_osl_server.get_actor_supports(UID, "can_finalize")
    assert isinstance(supports, bool)
    with pytest.raises(errors.OslCommandError):
        supports = tcp_osl_server.get_actor_supports(INVALID_UID, "can_finalize")
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_get_available_locations(tmp_example_project):
    """Test `get_available_[input/output]_locations``."""
    osl_server_process = create_osl_server_process(
        shutdown_on_finished=True, project_path=tmp_example_project("omdb_files")
    )
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    tcp_osl_server.reset()
    tcp_osl_server.start()
    properties = tcp_osl_server.get_full_project_tree_with_properties()
    omdb_uid = tcp_osl_server.create_node(
        type_="optislang_omdb", integration_type="python_based_integration_plugin"
    )
    omdb_path = Path(properties["projects"][0]["working_dir"]) / r"Sensitivity/Sensitivity.omdb"
    path_value = {
        "path": {
            "base_path_mode": {"value": "ABSOLUTE_PATH"},
            "split_path": {
                "head": "",
                "tail": str(omdb_path),
            },
        }
    }
    tcp_osl_server.set_actor_property(omdb_uid, "Path", path_value)

    tcp_osl_server.load(omdb_uid)
    input_locations = tcp_osl_server.get_available_input_locations(omdb_uid)
    assert len(input_locations) == 1
    assert isinstance(input_locations[0], dict)
    output_locations = tcp_osl_server.get_available_output_locations(omdb_uid)
    assert len(output_locations) == 1
    assert isinstance(output_locations[0], dict)
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_get_available_nodes(osl_server_process: OslServerProcess):
    """Test ``get_available_nodes`` query."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    with pytest.deprecated_call():
        available_nodes = tcp_osl_server.get_available_nodes()
    assert len(available_nodes) > 0
    key, value = next(iter(available_nodes.items()))
    assert isinstance(key, str)
    assert isinstance(value, list)
    builtins = available_nodes["builtin_nodes"]
    assert len(builtins) > 0
    assert isinstance(builtins[0], str)
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_get_available_node_types(osl_server_process: OslServerProcess):
    """Test ``get_available_nodes`` query."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    available_nodes = tcp_osl_server.get_available_node_types()
    assert len(available_nodes) > 0
    available_node = next(iter(available_nodes))
    assert isinstance(available_node, NodeType)
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_get_criteria(tmp_example_project):
    """Test ``get_criterion/a``."""
    osl_server_process = create_osl_server_process(
        shutdown_on_finished=True, project_path=tmp_example_project("calculator_with_params")
    )
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    root_system_uid = (
        tcp_osl_server.get_full_project_tree_with_properties()
        .get("projects", [{}])[0]
        .get("system", {})
        .get("uid", None)
    )
    criterion = tcp_osl_server.get_criterion(uid=root_system_uid, name="obj_c")
    assert isinstance(criterion, dict)
    criteria = tcp_osl_server.get_criteria(uid=root_system_uid)
    assert len(criteria) == 1
    assert isinstance(criteria[0], dict)
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_get_doe_size(tmp_example_project):
    """Test ``get_doe_size``."""
    osl_server_process = create_osl_server_process(
        shutdown_on_finished=True, project_path=tmp_example_project("omdb_files")
    )
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    UID = "011097b5-380d-4726-a0d0-128ddee83a7a"
    doe_size = tcp_osl_server.get_doe_size(
        uid=UID, sampling_type="latinhyper", num_discrete_levels=1
    )
    assert isinstance(doe_size, int)
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_get_project_queries(osl_server_process: OslServerProcess):
    """Test queries below related to active project.

    ``get_basic_project_info``, ``get_full_project_status_info``, ``get_full_project_tree``,
    ``get_full_project_tree_wit_properties``, ``get_project_systems``,
    ``get_project_systems_with_properties``, ``get_systems_status_info``
    """
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    # basic_project_info
    basic_project_info = tcp_osl_server.get_basic_project_info()
    assert isinstance(basic_project_info, dict)
    assert bool(basic_project_info)
    # full project status info
    status_info = tcp_osl_server.get_full_project_status_info()
    assert isinstance(status_info, dict)
    assert bool(status_info)
    # full project tree
    project_tree = tcp_osl_server.get_full_project_tree()
    assert isinstance(project_tree, dict)
    assert bool(project_tree)
    # full project tree with properties
    project_tree_with_properties = tcp_osl_server.get_full_project_tree_with_properties()
    assert isinstance(project_tree_with_properties, dict)
    # project tree systems
    project_tree_systems = tcp_osl_server.get_project_tree_systems()
    assert isinstance(project_tree_systems, dict)
    assert bool(dict)
    # project tree system with properties
    project_tree_systems_with_properties = tcp_osl_server.get_project_tree_systems_with_properties()
    assert isinstance(project_tree_systems_with_properties, dict)
    # systems_status_info
    systems_status_info = tcp_osl_server.get_systems_status_info()
    assert isinstance(systems_status_info, dict)
    assert bool(dict)
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_get_hpc_licensing_forwarded_environment(tmp_example_project):
    """Test ``get_hpc_licensing_forwarded_environment``."""
    osl_server_process = create_osl_server_process(
        shutdown_on_finished=True, project_path=tmp_example_project("calculator_with_params")
    )
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    hpc_licensing = tcp_osl_server.get_hpc_licensing_forwarded_environment(
        "3577cb69-15b9-4ad1-a53c-ac8af8aaea82"
    )
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert isinstance(hpc_licensing, dict)


def test_get_input_slot_value(tmp_example_project):
    """Test ``get_input_slot_value``."""
    osl_server_process = create_osl_server_process(
        shutdown_on_finished=True, project_path=tmp_example_project("calculator_with_params")
    )
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    UID = "3577cb69-15b9-4ad1-a53c-ac8af8aaea82"
    HID = "0"
    SLOT_NAME = "OVar"
    input_slot_value = tcp_osl_server.get_input_slot_value(UID, HID, SLOT_NAME)
    assert isinstance(input_slot_value, dict)
    assert bool(input_slot_value)
    with pytest.raises(errors.OslCommandError):
        input_slot_value = tcp_osl_server.get_input_slot_value("invalid", HID, SLOT_NAME)
    with pytest.raises(errors.OslCommandError):
        input_slot_value = tcp_osl_server.get_input_slot_value(UID, "invalid", SLOT_NAME)
    with pytest.raises(errors.OslCommandError):
        input_slot_value = tcp_osl_server.get_input_slot_value(UID, HID, "invalid")
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_get_output_slot_value(tmp_example_project):
    """Test ``get_output_slot_value``."""
    osl_server_process = create_osl_server_process(
        shutdown_on_finished=True, project_path=tmp_example_project("calculator_with_params")
    )
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    UID = "3577cb69-15b9-4ad1-a53c-ac8af8aaea82"
    HID = "0"
    SLOT_NAME = "var"
    output_slot_value = tcp_osl_server.get_output_slot_value(UID, HID, SLOT_NAME)
    assert isinstance(output_slot_value, dict)
    assert bool(output_slot_value)
    with pytest.raises(errors.OslCommandError):
        output_slot_value = tcp_osl_server.get_output_slot_value("invalid", HID, SLOT_NAME)
    with pytest.raises(errors.OslCommandError):
        output_slot_value = tcp_osl_server.get_output_slot_value(UID, "invalid", SLOT_NAME)
    with pytest.raises(errors.OslCommandError):
        output_slot_value = tcp_osl_server.get_output_slot_value(UID, HID, "invalid")
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_get_server_queries(osl_server_process: OslServerProcess):
    """Test ``get_server_info`` and ``get_server_is_alive``."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    # server_info
    server_info = tcp_osl_server.get_server_info()
    assert isinstance(server_info, dict)
    assert bool(server_info)
    # server is alive
    is_alive = tcp_osl_server.get_server_is_alive()
    assert isinstance(is_alive, bool)
    assert is_alive
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_new(osl_server_process: OslServerProcess, tmp_path: Path):
    """Test ``new``."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    tcp_osl_server.new()
    project_name = tcp_osl_server.get_basic_project_info().get("projects", [{}])[0].get("name")
    assert project_name == "Unnamed project"
    tcp_osl_server.save_as(file_path=tmp_path / "newProject.opf")
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


@pytest.mark.parametrize("path_type", [str, Path])
def test_open(osl_server_process: OslServerProcess, tmp_example_project, path_type):
    """Test ``open``."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    project = tmp_example_project("simple_calculator")
    assert project.is_file()
    if path_type == str:
        project = str(project)
    tcp_osl_server.open(project)
    project_name = tcp_osl_server.get_basic_project_info().get("projects", [{}])[0].get("name")
    project_name == "calculator"
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_register_location(osl_server_process: OslServerProcess):
    """Test ``register_location_as_[...]`` and ``get_registered_[...]``."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    sensitivity_uid = tcp_osl_server.create_node(type_="Sensitivity")
    integration_uid = tcp_osl_server.create_node(
        type_="optislang_node",
        integration_type="integration_plugin",
        parent_uid=sensitivity_uid,
        design_flow="RECEIVE_SEND",
    )

    # input slot
    actual_name = tcp_osl_server.register_location_as_input_slot(
        uid=integration_uid,
        location="input_slot_1",
        name="input_slot_1",
        reference_value=10,
    )
    input_slots = tcp_osl_server.get_actor_registered_input_slots(uid=integration_uid)
    assert len(input_slots) == 1
    assert isinstance(input_slots[0], dict)
    assert actual_name == "input_slot_1"

    #  internal variable
    actual_name = tcp_osl_server.register_location_as_internal_variable(
        uid=integration_uid,
        location={"expression": "10", "id": "variable_1"},
        name="internal_variable_1",
        reference_value=10,
    )
    internal_variables = tcp_osl_server.get_actor_internal_variables(uid=integration_uid)

    # output slot
    actual_name = tcp_osl_server.register_location_as_output_slot(
        uid=integration_uid,
        location="output_slot_1",
        name="output_slot_1",
        reference_value=10,
    )
    output_slots = tcp_osl_server.get_actor_registered_output_slots(uid=integration_uid)
    assert len(output_slots) == 1
    assert isinstance(output_slots[0], dict)
    assert actual_name == "output_slot_1"

    # parameter
    actual_name = tcp_osl_server.register_location_as_parameter(
        uid=integration_uid,
        location="parameter_1",
        name="parameter1",
        reference_value=10,
    )
    parameters = tcp_osl_server.get_actor_registered_parameters(uid=integration_uid)
    assert len(parameters) == 1
    assert isinstance(parameters[0], dict)
    assert actual_name == "parameter1"

    # response
    actual_name = tcp_osl_server.register_location_as_response(
        uid=integration_uid,
        location="response_1",
        name="response_1",
        reference_value=10,
    )

    responses = tcp_osl_server.get_actor_registered_responses(uid=integration_uid)
    assert len(responses) == 1
    assert isinstance(responses[0], dict)
    assert actual_name == "response_1"

    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_reset(osl_server_process: OslServerProcess):
    """Test ``reset``."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    tcp_osl_server.reset()
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


@pytest.mark.parametrize("path_type", [str, Path])
def test_run_python_file(
    osl_server_process: OslServerProcess,
    tmp_path: Path,
    path_type,
):
    """Test ``run_python_file``."""
    cmd = """
a = 5
b = 10
result = a + b
print(result)
"""
    cmd_path = path_type(tmp_path / "commands.txt")

    with open(cmd_path, "w") as f:
        f.write(cmd)
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    run_file = tcp_osl_server.run_python_file(file_path=cmd_path)
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert isinstance(run_file, tuple)


def test_run_python_script(osl_server_process: OslServerProcess):
    """Test ``run_python_script``."""
    cmd = "a = 5\nb = 10\nresult = a + b\nprint(result)"
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    run_script = tcp_osl_server.run_python_script(script=cmd)
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert isinstance(run_script, tuple)


def test_save(osl_server_process: OslServerProcess):
    """Test ``save``."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    file_path = Path(
        tcp_osl_server.get_basic_project_info().get("projects", [{}])[0].get("location")
    )
    assert file_path.is_file()
    mod_time = os.path.getmtime(str(file_path))
    tcp_osl_server.save()
    save_time = os.path.getmtime(str(file_path))
    assert mod_time != save_time
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


@pytest.mark.parametrize("path_type", [str, Path])
def test_save_as(
    osl_server_process: OslServerProcess,
    tmp_path: Path,
    path_type,
):
    """Test ``save_as``."""
    file_path = tmp_path / "test_save.opf"
    arg_path = path_type(file_path)

    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    old_wdir = Path(
        tcp_osl_server.get_basic_project_info().get("projects", [{}])[0].get("working_dir", None)
    )
    old_loc = Path(tcp_osl_server.get_basic_project_info().get("projects", [{}])[0].get("location"))

    tcp_osl_server.save_as(file_path=arg_path)

    new_wdir = Path(
        tcp_osl_server.get_basic_project_info().get("projects", [{}])[0].get("working_dir", None)
    )
    new_loc = Path(tcp_osl_server.get_basic_project_info().get("projects", [{}])[0].get("location"))
    assert new_wdir != old_wdir
    assert new_loc != old_loc

    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()

    assert file_path.is_file()


@pytest.mark.parametrize("path_type", [str, Path])
def test_save_copy(
    osl_server_process: OslServerProcess,
    tmp_path: Path,
    path_type,
):
    """Test ``save_copy``."""
    copy_path = tmp_path / "test_save_copy.opf"
    arg_path = path_type(copy_path)

    tcp_osl_server = create_tcp_osl_server(osl_server_process)

    if tcp_osl_server.osl_version < OslVersion(24, 1, 0, 0):
        pytest.skip(f"Not compatible with {tcp_osl_server.osl_version_string}")

    old_wdir = Path(
        tcp_osl_server.get_basic_project_info().get("projects", [{}])[0].get("working_dir", None)
    )
    old_loc = Path(tcp_osl_server.get_basic_project_info().get("projects", [{}])[0].get("location"))

    tcp_osl_server.save_copy(arg_path)

    new_wdir = Path(
        tcp_osl_server.get_basic_project_info().get("projects", [{}])[0].get("working_dir", None)
    )
    new_loc = Path(tcp_osl_server.get_basic_project_info().get("projects", [{}])[0].get("location"))
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert copy_path.is_file()
    assert new_wdir == old_wdir
    assert new_loc == old_loc


def test_set_actor_property(tmp_example_project):
    osl_server_process = create_osl_server_process(
        shutdown_on_finished=True, project_path=tmp_example_project("calculator_with_params")
    )
    tcp_osl_server = create_tcp_osl_server(osl_server_process)

    UID = "3577cb69-15b9-4ad1-a53c-ac8af8aaea82"
    # enum prop
    set_enum_property = {
        "enum": ["read_and_write_mode", "classic_reevaluate_mode"],
        "value": "classic_reevaluate_mode",
    }
    tcp_osl_server.set_actor_property(UID, "ReadMode", set_enum_property)
    read_mode = tcp_osl_server.get_actor_properties(UID).get("ReadMode")
    assert read_mode == set_enum_property

    # bool prop
    set_bool_property = True
    tcp_osl_server.set_actor_property(UID, "StopAfterExecution", set_bool_property)
    stop_after_exec = tcp_osl_server.get_actor_properties(UID).get("StopAfterExecution")
    assert stop_after_exec == set_bool_property

    # int prop
    set_int_property = 2
    tcp_osl_server.set_actor_property(UID, "ExecutionOptions", set_int_property)
    exec_options = tcp_osl_server.get_actor_properties(UID).get("ExecutionOptions")
    assert exec_options == set_int_property

    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_start(osl_server_process: OslServerProcess):
    """Test ``start``."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    tcp_osl_server.start()
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_stop(osl_server_process: OslServerProcess):
    """Test ``stop``."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    tcp_osl_server.stop()
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


# def test_stop_gently(osl_server_process: OslServerProcess):
#     """Test ``stop_gently``."""
#     tcp_osl_server = create_tcp_osl_server(osl_server_process)
#     tcp_osl_server.stop_gently()
#     tcp_osl_server.shutdown()


def test_shutdown(osl_server_process: OslServerProcess):
    """Test ``shutdown``."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_force_shutdown_local_process():
    """Test ``_force_shutdown_local_process``."""
    tcp_osl_server = tos.TcpOslServer()
    tcp_osl_server._force_shutdown_local_process()
    tcp_osl_server.dispose()


# endregion


def test_get_placeholder_ids(osl_server_process: OslServerProcess):
    """Test get_placeholder_ids method."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    if tcp_osl_server.osl_version < OslVersion(26, 1, 0, 0):
        pytest.skip(f"Not compatible with {tcp_osl_server.osl_version_string}")

    # Get placeholder IDs (should return empty list for new project)
    placeholder_ids = tcp_osl_server.get_placeholder_ids()

    # Verify the result
    assert isinstance(placeholder_ids, list)

    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_create_placeholder(osl_server_process: OslServerProcess):
    """Test create_placeholder method."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    if tcp_osl_server.osl_version < OslVersion(26, 1, 0, 0):
        pytest.skip(f"Not compatible with {tcp_osl_server.osl_version_string}")

    # Create a placeholder with minimal arguments
    placeholder_id = tcp_osl_server.create_placeholder(value=42.5)

    # Verify the result
    assert isinstance(placeholder_id, str)
    assert len(placeholder_id) > 0

    # Verify placeholder was created by checking IDs list
    placeholder_ids = tcp_osl_server.get_placeholder_ids()
    assert placeholder_id in placeholder_ids

    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_create_placeholder_with_all_options(osl_server_process: OslServerProcess):
    """Test create_placeholder method with all optional parameters."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    if tcp_osl_server.osl_version < OslVersion(26, 1, 0, 0):
        pytest.skip(f"Not compatible with {tcp_osl_server.osl_version_string}")

    # Create a placeholder with all arguments
    placeholder_id = tcp_osl_server.create_placeholder(
        value=100.0,
        placeholder_id="full_param",
        overwrite=True,
        user_level=UserLevel.COMPUTATION_ENGINEER,
        description="Full test parameter",
        range_="[0,1000]",
        type_=PlaceholderType.REAL,
        expression="x*10",
    )

    # Verify the result
    assert placeholder_id == "full_param"

    # Verify placeholder was created
    placeholder_ids = tcp_osl_server.get_placeholder_ids()
    assert "full_param" in placeholder_ids

    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_get_placeholder(osl_server_process: OslServerProcess):
    """Test get_placeholder method."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    if tcp_osl_server.osl_version < OslVersion(26, 1, 0, 0):
        pytest.skip(f"Not compatible with {tcp_osl_server.osl_version_string}")

    # First create a placeholder
    placeholder_id = tcp_osl_server.create_placeholder(
        value="test_value", placeholder_id="test_param"
    )

    # Get the placeholder
    placeholder_info = tcp_osl_server.get_placeholder(placeholder_id)

    # Verify the result
    assert hasattr(placeholder_info, "placeholder_id")
    assert placeholder_info.placeholder_id == placeholder_id

    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_set_placeholder_value(osl_server_process: OslServerProcess):
    """Test set_placeholder_value method."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    if tcp_osl_server.osl_version < OslVersion(26, 1, 0, 0):
        pytest.skip(f"Not compatible with {tcp_osl_server.osl_version_string}")

    # First create a placeholder
    placeholder_id = tcp_osl_server.create_placeholder(value="initial_value")

    # Set different types of values
    tcp_osl_server.set_placeholder_value(placeholder_id, "new_string_value")
    tcp_osl_server.set_placeholder_value(placeholder_id, 42.5)
    tcp_osl_server.set_placeholder_value(placeholder_id, True)

    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_rename_placeholder(osl_server_process: OslServerProcess):
    """Test rename_placeholder method."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    if tcp_osl_server.osl_version < OslVersion(26, 1, 0, 0):
        pytest.skip(f"Not compatible with {tcp_osl_server.osl_version_string}")

    # First create a placeholder
    old_id = tcp_osl_server.create_placeholder(value="test_value", placeholder_id="old_param")

    # Rename the placeholder
    tcp_osl_server.rename_placeholder(old_id, "new_param")

    # Verify the placeholder was renamed
    placeholder_ids = tcp_osl_server.get_placeholder_ids()
    assert "new_param" in placeholder_ids
    assert "old_param" not in placeholder_ids

    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_remove_placeholder(osl_server_process: OslServerProcess):
    """Test remove_placeholder method."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    if tcp_osl_server.osl_version < OslVersion(26, 1, 0, 0):
        pytest.skip(f"Not compatible with {tcp_osl_server.osl_version_string}")

    # First create a placeholder
    placeholder_id = tcp_osl_server.create_placeholder(
        value="test_value", placeholder_id="to_be_removed"
    )

    # Verify it was created
    placeholder_ids = tcp_osl_server.get_placeholder_ids()
    assert placeholder_id in placeholder_ids

    # Remove the placeholder
    tcp_osl_server.remove_placeholder(placeholder_id)

    # Verify it was removed
    placeholder_ids_after = tcp_osl_server.get_placeholder_ids()
    assert placeholder_id not in placeholder_ids_after

    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_create_placeholder_from_actor_property(osl_server_process: OslServerProcess):
    """Test create_placeholder_from_actor_property method."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    if tcp_osl_server.osl_version < OslVersion(26, 1, 0, 0):
        pytest.skip(f"Not compatible with {tcp_osl_server.osl_version_string}")

    # Create a node first
    node_uid = tcp_osl_server.create_node(type_="CalculatorSet")

    # Create placeholder from actor property (default create_as_expression=False)
    placeholder_id = tcp_osl_server.create_placeholder_from_actor_property(
        actor_uid=node_uid, property_name="RetryEnable"
    )

    # Verify the result
    assert isinstance(placeholder_id, str)
    assert len(placeholder_id) > 0

    # Verify placeholder was created
    placeholder_ids = tcp_osl_server.get_placeholder_ids()
    assert placeholder_id in placeholder_ids

    # Create placeholder from actor property with create_as_expression=True
    expression_placeholder_id = tcp_osl_server.create_placeholder_from_actor_property(
        actor_uid=node_uid, property_name="RetryEnable", create_as_expression=True
    )

    # Verify the expression placeholder result
    assert isinstance(expression_placeholder_id, str)
    assert len(expression_placeholder_id) > 0
    assert expression_placeholder_id != placeholder_id  # Should be different IDs

    # Verify both placeholders were created
    updated_placeholder_ids = tcp_osl_server.get_placeholder_ids()
    assert placeholder_id in updated_placeholder_ids
    assert expression_placeholder_id in updated_placeholder_ids

    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_assign_unassign_placeholder(osl_server_process: OslServerProcess):
    """Test assign_placeholder and unassign_placeholder methods."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    if tcp_osl_server.osl_version < OslVersion(26, 1, 0, 0):
        pytest.skip(f"Not compatible with {tcp_osl_server.osl_version_string}")

    # Create a node and placeholder
    node_uid = tcp_osl_server.create_node(type_="CalculatorSet")
    placeholder_id = tcp_osl_server.create_placeholder(
        type_=PlaceholderType.BOOL, value=True, placeholder_id="assign_test"
    )

    # Assign placeholder to actor property
    tcp_osl_server.assign_placeholder(
        actor_uid=node_uid, property_name="RetryEnable", placeholder_id=placeholder_id
    )

    # Unassign placeholder from actor property
    tcp_osl_server.unassign_placeholder(actor_uid=node_uid, property_name="RetryEnable")

    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


# endregion
