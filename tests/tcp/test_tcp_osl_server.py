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
import ansys.optislang.core.tcp.osl_server as tos

_host = socket.gethostbyname(socket.gethostname())


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
        )
        osl_server_process.start()

        start_timeout = 60
        start = time.time()
        while not os.path.exists(server_info_file):
            time.sleep(0.1)
            if time.time() - start > start_timeout:
                break

        if os.path.exists(server_info_file):
            return osl_server_process
        osl_server_process.terminate()
        raise TimeoutError("optiSLang Process start timed out after {}s".format(start_timeout))


@pytest.fixture(scope="function", autouse=False)
def osl_server_process():
    # Will be executed before each test
    return create_osl_server_process(shutdown_on_finished=False)


@pytest.fixture(scope="function", autouse=False)
def tcp_listener():
    return tos.TcpOslListener(
        port_range=(49152, 65535),
        timeout=30,
        name="GeneralListener",
        host="127.0.0.1",
        uid=str(uuid.uuid4()),
        logger=logging.getLogger(__name__),
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
    tcp_osl_server.timeout = 10
    return tcp_osl_server


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
    """Test `name`, `uid`, `timeout`, `host`, `port`, `refresh_listener..`."""
    assert isinstance(tcp_listener.uid, str)
    new_uid = str(uuid.uuid4())
    tcp_listener.uid = new_uid
    assert tcp_listener.uid == new_uid
    name = tcp_listener.name
    assert isinstance(name, str)
    assert name == "GeneralListener"
    timeout = tcp_listener.timeout
    assert isinstance(timeout, (float, int))
    assert timeout == 30
    tcp_listener.timeout = 15
    new_timeout = tcp_listener.timeout
    assert isinstance(new_timeout, (float, int))
    assert new_timeout == 15
    assert isinstance(tcp_listener.host, str)
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
    assert isinstance(tcp_osl_server.timeout, (int, float))
    assert tcp_osl_server.timeout == 10
    tcp_osl_server.timeout = 20
    assert isinstance(tcp_osl_server.timeout, (int, float))
    assert tcp_osl_server.timeout == 20
    with pytest.raises(ValueError):
        tcp_osl_server.timeout = -5
    with pytest.raises(TypeError):
        tcp_osl_server.timeout = "5"
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


# def test_close(osl_server_process: OslServerProcess):
#     tcp_osl_server = create_tcp_osl_server(osl_server_process)
#     with does_not_raise() as dnr:
#         tcp_osl_server.close()
#         tcp_osl_server.new()
#         tcp_osl_server.dispose()
#     assert dnr is None


def test_connect_nodes(tmp_path: Path, tmp_example_project):
    """Test `connect_nodes` method."""
    osl_server_process = create_osl_server_process(
        shutdown_on_finished=False, project_path=tmp_example_project("connect_nodes")
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


def test_disconnect_slot(tmp_path: Path, tmp_example_project):
    "Test ``disconnect_slot`` command."
    osl_server_process = create_osl_server_process(
        shutdown_on_finished=False, project_path=tmp_example_project("calculator_with_params")
    )
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    osl_version = tcp_osl_server.osl_version
    assert len(osl_version) == 4
    assert isinstance(osl_version[0], int)
    assert isinstance(osl_version[1], int)
    assert isinstance(osl_version[2], int)
    assert isinstance(osl_version[3], int)
    osl_version_string = tcp_osl_server.osl_version_string
    assert isinstance(osl_version_string, str)
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_evaluate_design(tmp_path: Path, tmp_example_project):
    "Test ``evaluate_design``."
    osl_server_process = create_osl_server_process(
        shutdown_on_finished=False, project_path=tmp_example_project("calculator_with_params")
    )
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    tcp_osl_server.save_copy(file_path=tmp_path / "test_evaluate_design.opf")
    tcp_osl_server.reset()
    result = tcp_osl_server.evaluate_design({"a": 5, "b": 10})
    assert isinstance(result, list)
    assert isinstance(result[0], dict)
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_get_actor_queries(tmp_example_project):
    """Test `get_actor_` - `info`, `properties`,`states`, `status_info`, `supports` queries."""
    osl_server_process = create_osl_server_process(
        shutdown_on_finished=False, project_path=tmp_example_project("calculator_with_params")
    )
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    UID = "3577cb69-15b9-4ad1-a53c-ac8af8aaea82"
    INVALID_UID = "3577cb69-15b9-4ad1-a53c-ac8af8aaea83"
    # info
    info = tcp_osl_server.get_actor_info(UID)
    assert isinstance(info, dict)
    with pytest.raises(errors.OslCommandError):
        info = tcp_osl_server.get_actor_info(INVALID_UID)
    # properties
    properties = tcp_osl_server.get_actor_properties(UID)
    assert isinstance(properties, dict)
    with pytest.raises(errors.OslCommandError):
        properties = tcp_osl_server.get_actor_properties(INVALID_UID)
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
        shutdown_on_finished=False, project_path=tmp_example_project("calculator_with_params")
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
        shutdown_on_finished=False, project_path=tmp_example_project("calculator_with_params")
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
        shutdown_on_finished=False, project_path=tmp_example_project("calculator_with_params")
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


def test_set_actor_property(tmp_path: Path, tmp_example_project):
    osl_server_process = create_osl_server_process(
        shutdown_on_finished=False, project_path=tmp_example_project("calculator_with_params")
    )
    tcp_osl_server = create_tcp_osl_server(osl_server_process)

    UID = "3577cb69-15b9-4ad1-a53c-ac8af8aaea82"
    # enum prop
    set_enum_property = {
        "enum": ["read_and_write_mode", "classic_reevaluate_mode"],
        "value": "classic_reevaluate_mode",
    }
    tcp_osl_server.set_actor_property(UID, "ReadMode", set_enum_property)
    read_mode = tcp_osl_server.get_actor_properties(UID).get("properties", {}).get("ReadMode")
    assert read_mode == set_enum_property

    # bool prop
    set_bool_property = True
    tcp_osl_server.set_actor_property(UID, "StopAfterExecution", set_bool_property)
    stop_after_exec = (
        tcp_osl_server.get_actor_properties(UID).get("properties", {}).get("StopAfterExecution")
    )
    assert stop_after_exec == set_bool_property

    # int prop
    set_int_property = 2
    tcp_osl_server.set_actor_property(UID, "ExecutionOptions", set_int_property)
    exec_options = (
        tcp_osl_server.get_actor_properties(UID).get("properties", {}).get("ExecutionOptions")
    )
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


def test_get_project_uid(osl_server_process: OslServerProcess):
    """Test `project_uid`."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    uid = tcp_osl_server.get_project_uid()
    assert isinstance(uid, str)
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


# endregion
