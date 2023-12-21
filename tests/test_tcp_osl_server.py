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
import ansys.optislang.core.tcp_osl_server as tos

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


# TcpClient
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


# TcpListener
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


# TcpOslServer

# def test_close(osl_server_process: OslServerProcess):
#     tcp_osl_server = create_tcp_osl_server(osl_server_process)
#     with does_not_raise() as dnr:
#         tcp_osl_server.close()
#         tcp_osl_server.new()
#         tcp_osl_server.dispose()
#     assert dnr is None


def test_osl_version_properties(osl_server_process: OslServerProcess):
    """Test ``osl_version`` and ``osl_version_string``."""
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
    assert timeouts_register.default_value == 10

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


def test_evaluate_design(tmp_path: Path, tmp_example_project):
    "Test ``evaluate_design``."
    osl_server_process = create_osl_server_process(
        shutdown_on_finished=False, project_path=tmp_example_project("calculator_with_params")
    )
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    tcp_osl_server.save_copy(file_path=tmp_path / "test_evaluate_design.opf")
    tcp_osl_server.reset()
    result = tcp_osl_server.evaluate_design({"a": 5, "b": 10})
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert isinstance(result, list)
    assert isinstance(result[0], dict)


@pytest.mark.parametrize(
    "uid, expected",
    [
        ("3577cb69-15b9-4ad1-a53c-ac8af8aaea82", dict),
        ("3577cb69-15b9-4ad1-a53c-ac8af8aaea83", errors.OslCommandError),
    ],
)
def test_get_actor_info(uid, expected, tmp_example_project):
    """Test ``get_actor_info``."""
    osl_server_process = create_osl_server_process(
        shutdown_on_finished=False, project_path=tmp_example_project("calculator_with_params")
    )
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    if expected == errors.OslCommandError:
        with pytest.raises(expected):
            info = tcp_osl_server.get_actor_info(uid)
    else:
        info = tcp_osl_server.get_actor_info(uid)
        assert isinstance(info, expected)
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


@pytest.mark.parametrize(
    "uid, expected",
    [
        ("3577cb69-15b9-4ad1-a53c-ac8af8aaea82", dict),
        ("3577cb69-15b9-4ad1-a53c-ac8af8aaea83", errors.OslCommandError),
    ],
)
def test_get_actor_properties(uid, expected, tmp_example_project):
    """Test ``get_actor_properties``."""
    osl_server_process = create_osl_server_process(
        shutdown_on_finished=False, project_path=tmp_example_project("calculator_with_params")
    )
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    if expected == errors.OslCommandError:
        with pytest.raises(expected):
            properties = tcp_osl_server.get_actor_properties(uid)
    else:
        properties = tcp_osl_server.get_actor_properties(uid)
        assert isinstance(properties, expected)
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


@pytest.mark.parametrize(
    "uid, expected",
    [
        ("3577cb69-15b9-4ad1-a53c-ac8af8aaea82", dict),
        ("3577cb69-15b9-4ad1-a53c-ac8af8aaea83", errors.OslCommandError),
    ],
)
def test_get_actor_states(uid, expected, tmp_example_project):
    """Test ``get_actor_states``."""
    osl_server_process = create_osl_server_process(
        shutdown_on_finished=False, project_path=tmp_example_project("calculator_with_params")
    )
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    if expected == errors.OslCommandError:
        with pytest.raises(expected):
            states = tcp_osl_server.get_actor_states(uid)
    else:
        states = tcp_osl_server.get_actor_states(uid)
        print(states)
        assert isinstance(states, expected)
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


@pytest.mark.parametrize(
    "uid, expected",
    [
        ("3577cb69-15b9-4ad1-a53c-ac8af8aaea82", dict),
        ("3577cb69-15b9-4ad1-a53c-ac8af8aaea83", errors.OslCommandError),
    ],
)
def test_get_actor_status_info(uid, expected, tmp_example_project):
    """Test ``get_actor_status_info``."""
    osl_server_process = create_osl_server_process(
        shutdown_on_finished=False, project_path=tmp_example_project("calculator_with_params")
    )
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    if expected == errors.OslCommandError:
        with pytest.raises(expected):
            status_info = tcp_osl_server.get_actor_status_info(uid, "0")
    else:
        status_info = tcp_osl_server.get_actor_status_info(uid, "0")
        assert isinstance(status_info, expected)
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


@pytest.mark.parametrize(
    "uid, feature_name, expected",
    [
        ("3577cb69-15b9-4ad1-a53c-ac8af8aaea82", "can_finalize", bool),
        ("3577cb69-15b9-4ad1-a53c-ac8af8aaea82", "invalid_input", errors.OslCommandError),
        ("3577cb69-15b9-4ad1-a53c-ac8af8aaea83", "can_finalize", errors.OslCommandError),
    ],
)
def test_get_actor_supports(uid, feature_name, expected, tmp_example_project):
    """Test ``get_actor_status_info``."""
    osl_server_process = create_osl_server_process(
        shutdown_on_finished=False, project_path=tmp_example_project("calculator_with_params")
    )
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    if expected == errors.OslCommandError:
        with pytest.raises(expected):
            status_info = tcp_osl_server.get_actor_supports(uid, feature_name)
    else:
        status_info = tcp_osl_server.get_actor_supports(uid, feature_name)
        assert isinstance(status_info, expected)
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_get_full_project_status_info(osl_server_process: OslServerProcess):
    """Test ``get_full_project_status_info``."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    status_info = tcp_osl_server.get_full_project_status_info()
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert isinstance(status_info, dict)
    assert bool(status_info)


def test_get_full_project_tree(osl_server_process: OslServerProcess):
    """Test ``get_full_project_tree``."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    project_tree = tcp_osl_server.get_full_project_tree()
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert isinstance(project_tree, dict)
    assert bool(project_tree)


def test_get_full_project_tree_with_properties(osl_server_process: OslServerProcess):
    """Test `get_full_project_tree_with_properties`."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    project_tree = tcp_osl_server.get_full_project_tree_with_properties()
    assert isinstance(project_tree, dict)
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


@pytest.mark.parametrize(
    "uid, hid, slot_name, expected",
    [
        ("3577cb69-15b9-4ad1-a53c-ac8af8aaea82", "0", "OVar", dict),
        ("3577cb69-15b9-4ad1-a53c-ac8af8aaea82", "invalid", "OVar", errors.OslCommandError),
        ("3577cb69-15b9-4ad1-a53c-ac8af8aaea82", "0", "invalid", errors.OslCommandError),
        ("3577cb69-15b9-4ad1-a53c-ac8af8aaea83", "0", "OVar", errors.OslCommandError),
    ],
)
def test_get_input_slot_value(uid, hid, slot_name, expected, tmp_example_project):
    """Test ``get_input_slot_value``."""
    osl_server_process = create_osl_server_process(
        shutdown_on_finished=False, project_path=tmp_example_project("calculator_with_params")
    )
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    if expected == errors.OslCommandError:
        with pytest.raises(expected):
            input_slot_value = tcp_osl_server.get_input_slot_value(uid, hid, slot_name)
    else:
        input_slot_value = tcp_osl_server.get_input_slot_value(uid, hid, slot_name)
        assert isinstance(input_slot_value, expected)
        assert bool(input_slot_value)
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


@pytest.mark.parametrize(
    "uid, hid, slot_name, expected",
    [
        ("3577cb69-15b9-4ad1-a53c-ac8af8aaea82", "0", "var", dict),
        ("3577cb69-15b9-4ad1-a53c-ac8af8aaea82", "invalid", "var", errors.OslCommandError),
        ("3577cb69-15b9-4ad1-a53c-ac8af8aaea82", "0", "invalid", errors.OslCommandError),
        ("3577cb69-15b9-4ad1-a53c-ac8af8aaea83", "0", "var", errors.OslCommandError),
    ],
)
def test_get_output_slot_value(uid, hid, slot_name, expected, tmp_example_project):
    """Test ``get_output_slot_value``."""
    osl_server_process = create_osl_server_process(
        shutdown_on_finished=False, project_path=tmp_example_project("calculator_with_params")
    )
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    if expected == errors.OslCommandError:
        with pytest.raises(expected):
            output_slot_value = tcp_osl_server.get_output_slot_value(uid, hid, slot_name)
    else:
        output_slot_value = tcp_osl_server.get_output_slot_value(uid, hid, slot_name)
        assert isinstance(output_slot_value, expected)
        assert bool(output_slot_value)
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_get_project_tree_systems(osl_server_process: OslServerProcess):
    """Test `get_project_tree_systems`."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    project_tree_systems = tcp_osl_server.get_project_tree_systems()
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert isinstance(project_tree_systems, dict)
    assert bool(dict)


def test_get_project_tree_systems_with_properties(osl_server_process: OslServerProcess):
    """Test `get_project_tree_systems_with_properties`."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    project_tree_systems = tcp_osl_server.get_project_tree_systems_with_properties()
    assert isinstance(project_tree_systems, dict)
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_get_server_info(osl_server_process: OslServerProcess):
    """Test ``get_server_info``."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    server_info = tcp_osl_server.get_server_info()
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert isinstance(server_info, dict)
    assert bool(server_info)


def test_get_basic_project_info(osl_server_process: OslServerProcess):
    """Test ``get_basic_project_info``."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    basic_project_info = tcp_osl_server.get_basic_project_info()
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert isinstance(basic_project_info, dict)
    assert bool(basic_project_info)


def test_get_project_description(osl_server_process: OslServerProcess):
    """Test ``get_project_description``."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    project_description = tcp_osl_server.get_project_description()
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert isinstance(project_description, str)
    assert not bool(project_description)


def test_get_project_location(osl_server_process: OslServerProcess):
    """Test ``get_project_location``."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    project_location = tcp_osl_server.get_project_location()
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert isinstance(project_location, Path)
    assert bool(project_location)


def test_get_project_name(osl_server_process: OslServerProcess):
    """Test ``get_project_name``."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    project_name = tcp_osl_server.get_project_name()
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert isinstance(project_name, str)
    assert bool(project_name)


def test_get_project_status(osl_server_process: OslServerProcess):
    """Test ``get_get_project_status``."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    project_status = tcp_osl_server.get_project_status()
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert isinstance(project_status, str)
    assert bool(project_status)


def test_get_server_is_alive(osl_server_process: OslServerProcess):
    """Test ``get_server_is_alive``."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    is_alive = tcp_osl_server.get_server_is_alive()
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert isinstance(is_alive, bool)


def test_get_set_timeout(osl_server_process: OslServerProcess):
    """Test ``get_set_timeout``."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    timeout = tcp_osl_server.timeout
    assert isinstance(timeout, (int, float))
    assert timeout == 10
    tcp_osl_server.timeout = 15
    new_timeout = tcp_osl_server.timeout
    assert isinstance(new_timeout, (int, float))
    assert new_timeout == 15
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_get_systems_status_info(osl_server_process: OslServerProcess):
    """Test `get_project_tree_systems_with_properties`."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    systems_status_info = tcp_osl_server.get_systems_status_info()
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert isinstance(systems_status_info, dict)
    assert bool(dict)


def test_get_working_dir(osl_server_process: OslServerProcess):
    """Test ``get_working_dir``."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    working_dir = tcp_osl_server.get_working_dir()
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert isinstance(working_dir, Path)
    assert bool(working_dir)


def test_new(osl_server_process: OslServerProcess, tmp_path: Path):
    """Test ``new``."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    tcp_osl_server.new()
    assert tcp_osl_server.get_project_name() == "Unnamed project"
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
    assert tcp_osl_server.get_project_name() == "calculator"
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
    cmd = """
a = 5
b = 10
result = a + b
print(result)
"""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    run_script = tcp_osl_server.run_python_script(script=cmd)
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert isinstance(run_script, tuple)


def test_save(osl_server_process: OslServerProcess):
    """Test ``save``."""
    tcp_osl_server = create_tcp_osl_server(osl_server_process)
    file_path = tcp_osl_server.get_project_location()
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
    tcp_osl_server.save_as(file_path=arg_path)
    assert file_path.is_file()
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


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
    tcp_osl_server.save_copy(arg_path)
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert copy_path.is_file()


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
#     with does_not_raise() as dnr:
#         tcp_osl_server.stop_gently()
#     tcp_osl_server.shutdown()
#     assert dnr is None


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
