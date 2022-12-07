from contextlib import nullcontext as does_not_raise
import os
from pathlib import Path
import socket
import time

import pytest

from ansys.optislang.core import OslServerProcess, examples
from ansys.optislang.core.project_parametric import Design, ParameterManager
import ansys.optislang.core.tcp_osl_server as tos

_host = socket.gethostbyname(socket.gethostname())
_port = 5310


_msg = '{ "What": "SYSTEMS_STATUS_INFO" }'
parametric_project = examples.get_files("calculator_with_params")[1]

pytestmark = pytest.mark.local_osl


@pytest.fixture(scope="function", autouse=True)
def osl_server_process():
    time.sleep(2)
    # Will be executed before each test
    osl_server_process = OslServerProcess(shutdown_on_finished=False)
    osl_server_process.start()
    time.sleep(5)
    return osl_server_process


@pytest.fixture(scope="function", autouse=False)
def tcp_client() -> tos.TcpClient:
    """Create TcpClient.

    Returns
    -------
    TcpOslServer:
        Class which provides access to optiSLang server using plain TCP/IP communication protocol.
    """
    return tos.TcpClient()


@pytest.fixture(scope="function", autouse=False)
def tcp_osl_server() -> tos.TcpOslServer:
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
    tcp_osl_server = tos.TcpOslServer(host=_host, port=_port)
    tcp_osl_server.set_timeout(timeout=10)
    return tcp_osl_server


# TcpClient
def test_connect_and_disconnect(osl_server_process: OslServerProcess, tcp_client: tos.TcpClient):
    "Test ``connect``."
    with does_not_raise() as dnr:
        tcp_client.connect(host=_host, port=_port)
        tcp_client.disconnect()
        osl_server_process.terminate()
    assert dnr is None


def test_send_msg(osl_server_process: OslServerProcess, tcp_client: tos.TcpClient):
    "Test ``send_msg`"
    with does_not_raise() as dnr:
        tcp_client.connect(host=_host, port=_port)
        tcp_client.send_msg(_msg)
        tcp_client.disconnect()
        osl_server_process.terminate()
    assert dnr is None


@pytest.mark.parametrize("path_type", [str, Path])
def test_send_file(
    osl_server_process: OslServerProcess,
    tcp_client: tos.TcpClient,
    tmp_path: Path,
    path_type,
):
    "Test ``send_file``"
    file_path = tmp_path / "testfile.txt"
    if path_type == str:
        file_path = str(file_path)
    elif path_type != Path:
        assert False

    with open(file_path, "w") as testfile:
        testfile.write(_msg)
    with does_not_raise() as dnr:
        tcp_client.connect(host=_host, port=_port)
        tcp_client.send_file(file_path)
        tcp_client.disconnect()
        osl_server_process.terminate()
    assert dnr is None


def test_receive_msg(osl_server_process: OslServerProcess, tcp_client: tos.TcpClient):
    "Test ``receive_msg``."
    tcp_client.connect(host=_host, port=_port)
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
    file_path = tmp_path / "testfile.txt"
    received_path = tmp_path / "received.txt"
    if path_type == str:
        file_path = str(file_path)
        received_path = str(received_path)
    elif path_type != Path:
        assert False

    with open(file_path, "w") as testfile:
        testfile.write(_msg)
    tcp_client.connect(host=_host, port=_port)
    tcp_client.send_file(file_path)
    with does_not_raise() as dnr:
        tcp_client.receive_file(received_path)
    assert os.path.isfile(received_path)
    tcp_client.disconnect()
    osl_server_process.terminate()
    assert dnr is None


# TcpOslServer
def test_get_server_info(tcp_osl_server: tos.TcpOslServer):
    """Test ``_get_server_info``."""
    server_info = tcp_osl_server._get_server_info()
    tcp_osl_server.shutdown()
    assert isinstance(server_info, dict)
    assert bool(server_info)


def test_get_basic_project_info(tcp_osl_server: tos.TcpOslServer):
    """Test ``_get_basic_project_info``."""
    basic_project_info = tcp_osl_server._get_basic_project_info()
    tcp_osl_server.shutdown()
    assert isinstance(basic_project_info, dict)
    assert bool(basic_project_info)


def test_get_osl_version_string(osl_server_process, tcp_osl_server):
    """Test ``get_osl_version_string``."""
    version = tcp_osl_server.get_osl_version_string()
    tcp_osl_server.shutdown()
    assert isinstance(version, str)
    assert bool(version)


def test_get_osl_version(tcp_osl_server):
    """Test ``get_osl_version``."""
    major_version, minor_version, maintenance_version, revision = tcp_osl_server.get_osl_version()
    tcp_osl_server.shutdown()
    assert isinstance(major_version, int)
    assert isinstance(minor_version, int)
    assert isinstance(maintenance_version, int) or maintenance_version == None
    assert isinstance(revision, int) or revision == None


def test_get_project_description(osl_server_process, tcp_osl_server):
    """Test ``get_project_description``."""
    project_description = tcp_osl_server.get_project_description()
    tcp_osl_server.shutdown()
    assert isinstance(project_description, str)
    assert not bool(project_description)


def test_get_project_location(tcp_osl_server: tos.TcpOslServer):
    """Test ``get_project_location``."""
    project_location = tcp_osl_server.get_project_location()
    tcp_osl_server.shutdown()
    assert isinstance(project_location, Path)
    assert bool(project_location)


def test_get_project_name(tcp_osl_server: tos.TcpOslServer):
    """Test ``get_project_name``."""
    project_name = tcp_osl_server.get_project_name()
    tcp_osl_server.shutdown()
    assert isinstance(project_name, str)
    assert bool(project_name)


def test_get_project_status(tcp_osl_server: tos.TcpOslServer):
    """Test ``get_get_project_status``."""
    project_status = tcp_osl_server.get_project_status()
    tcp_osl_server.shutdown()
    assert isinstance(project_status, str)
    assert bool(project_status)


def test_get_working_dir(tcp_osl_server: tos.TcpOslServer):
    """Test ``get_working_dir``."""
    working_dir = tcp_osl_server.get_working_dir()
    tcp_osl_server.shutdown()
    assert isinstance(working_dir, Path)
    assert bool(working_dir)


# not implemented
def test_new(tcp_osl_server: tos.TcpOslServer):
    """Test ``new``."""
    with pytest.raises(NotImplementedError):
        tcp_osl_server.new()
    tcp_osl_server.shutdown()


# not implemented
def test_open(tcp_osl_server: tos.TcpOslServer):
    """Test ``open``."""
    with pytest.raises(NotImplementedError):
        tcp_osl_server.open("string", False, False, False)
    tcp_osl_server.shutdown()


def test_reset(tcp_osl_server: tos.TcpOslServer):
    """Test ``reset``."""
    with does_not_raise() as dnr:
        tcp_osl_server.reset()
    tcp_osl_server.shutdown()
    assert dnr is None


@pytest.mark.parametrize("path_type", [str, Path])
def test_run_python_file(tcp_osl_server: tos.TcpOslServer, tmp_path: Path, path_type):
    """Test ``run_python_file``."""
    cmd = """
a = 5
b = 10
result = a + b
print(result)
"""
    cmd_path = tmp_path / "commands.txt"
    if path_type == str:
        cmd_path = str(cmd_path)
    elif path_type != Path:
        assert False

    with open(cmd_path, "w") as f:
        f.write(cmd)
    run_file = tcp_osl_server.run_python_file(file_path=cmd_path)
    tcp_osl_server.shutdown()
    assert isinstance(run_file, tuple)


def test_run_python_script(tcp_osl_server: tos.TcpOslServer):
    """Test ``run_python_script``."""
    cmd = """
a = 5
b = 10
result = a + b
print(result)
"""
    run_script = tcp_osl_server.run_python_script(script=cmd)
    tcp_osl_server.shutdown()
    assert isinstance(run_script, tuple)


# not implemented
def test_save(tcp_osl_server: tos.TcpOslServer):
    """Test ``save``."""
    with pytest.raises(NotImplementedError):
        tcp_osl_server.save()
    tcp_osl_server.shutdown()


# not implemented
def test_save_as(tcp_osl_server: tos.TcpOslServer):
    """Test ``save_as``."""
    with pytest.raises(NotImplementedError):
        tcp_osl_server.save_as("string", False, False, False)
    tcp_osl_server.shutdown()


def test_save_copy(tmp_path: Path, tcp_osl_server: tos.TcpOslServer):
    """Test ``save_copy``."""
    copy_path = tmp_path / "test_save_copy.opf"
    tcp_osl_server.save_copy(copy_path)
    tcp_osl_server.shutdown()
    assert os.path.isfile(copy_path)


def test_start(tcp_osl_server: tos.TcpOslServer):
    """Test ``start``."""
    with does_not_raise() as dnr:
        tcp_osl_server.start()
    tcp_osl_server.shutdown()
    assert dnr is None


def test_stop(tcp_osl_server: tos.TcpOslServer):
    """Test ``stop``."""
    with does_not_raise() as dnr:
        tcp_osl_server.stop()
    tcp_osl_server.shutdown()
    assert dnr is None


# def test_stop_gently(tcp_osl_server: tos.TcpOslServer):
#     """Test ``stop_gently``."""
#     with does_not_raise() as dnr:
#         tcp_osl_server.stop_gently()
#     tcp_osl_server.shutdown()
#     assert dnr is None


def test_shutdown(tcp_osl_server: tos.TcpOslServer):
    """Test ``shutdown``."""
    with does_not_raise() as dnr:
        tcp_osl_server.shutdown()
    assert dnr is None


# #######################################################################
# TODO: TEST properly with implemented `open` method or remake all tests
#       so that OslServer opens parametric_project.
# #######################################################################


def test_get_nodes_dict(tcp_osl_server):
    "Test ``get_nodes_dict``."
    node_dict = tcp_osl_server.get_nodes_dict()
    assert isinstance(node_dict, dict)
    # assert node_dict[0]['name'] == 'Calculator'
    tcp_osl_server.shutdown()


def test_get_parameter_manager(tcp_osl_server):
    "Test ``get_parameter_manager``."
    par_manager = tcp_osl_server.get_parameter_manager()
    assert isinstance(par_manager, ParameterManager)
    tcp_osl_server.shutdown()


def test_get_parameters_list(tcp_osl_server):
    "Test ``get_parameters_list``."
    params = tcp_osl_server.get_parameters_list()
    assert isinstance(params, list)
    # assert len(params) > 0
    # assert set(['a', 'b']) == set(params)
    tcp_osl_server.shutdown()


def test_create_design(tcp_osl_server):
    "Test ``create_design``."
    inputs = {"a": 5, "b": 10}
    design = tcp_osl_server.create_design(inputs)
    tcp_osl_server.shutdown()

    assert isinstance(design, Design)
    assert isinstance(design.parameters["a"], (int, float))
    design.set_parameter("a", 10)
    assert design.parameters["a"] == 10
    design.set_parameters({"b": 20, "c": 30})
    assert design.parameters["c"] == 30
    direct_design = Design(inputs={"a": 5, "b": 10})
    assert isinstance(direct_design, Design)
    assert isinstance(direct_design.parameters["b"], (int, float))


def test_evaluate_design(tcp_osl_server):
    "Test ``evaluate_design``."
    design = Design(inputs={"a": 5, "b": 10})
    assert design.status == "IDLE"
    assert design.id == "NOT ASSIGNED"
    result = tcp_osl_server.evaluate_design(design)
    tcp_osl_server.shutdown()

    assert isinstance(result, tuple)
    assert isinstance(result[0], dict)
    assert isinstance(result[1], dict)
    # assert design.status == 'SUCCEEDED'
    assert isinstance(design.responses, dict)
    # assert design.responses['c'] == 15
    assert isinstance(design.criteria, dict)


def test_evaluate_multiple_designs(tcp_osl_server):
    designs = [
        Design(inputs={"a": 1, "b": 2}),
        Design(inputs={"a": 3, "b": 4}),
        Design(inputs={"a": 5, "b": 6}),
        Design(inputs={"e": 7, "f": 8}),
    ]
    results = tcp_osl_server.evaluate_multiple_designs(designs)
    tcp_osl_server.shutdown()

    for result in results:
        assert isinstance(result, tuple)
        assert isinstance(result[0], dict)
        assert isinstance(result[1], dict)
        # assert 'b' in result[0]
        # assert 'c' in result[1]


def test_validate_design():
    tcp_osl_server = tos.TcpOslServer(host=_host, port=_port, project_path=parametric_project)
    designs = [
        Design(inputs={"a": 1, "b": 2}),
        Design(inputs={"e": 3, "f": 4}),
        Design(inputs={"a": 5, "g": 6}),
    ]
    for design in designs:
        result = tcp_osl_server.validate_design(design)
        print(result)
        assert isinstance(result[0], str)
        assert isinstance(result[1], bool)
        assert isinstance(result[2], list)

    tcp_osl_server.shutdown()
