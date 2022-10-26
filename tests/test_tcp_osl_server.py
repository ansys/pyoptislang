from contextlib import nullcontext as does_not_raise
import os
import time

import pytest

from ansys.optislang.core import OslServerProcess, examples
from ansys.optislang.core.project_parametric import Design, ParameterManager
import ansys.optislang.core.tcp_osl_server as tos

_host = "127.0.0.1"
_port = 5310
_msg = '{ "What": "SYSTEMS_STATUS_INFO" }'
parametric_project = examples.get_files("calculator_with_params")[1]

pytestmark = pytest.mark.local_osl


@pytest.fixture(scope="session", autouse=True)
def osl_server_process():
    # Will be executed before the first test
    osl = OslServerProcess()
    osl.start()
    time.sleep(3)
    yield osl
    # Will be executed after the last test
    osl.terminate()


@pytest.fixture
def tcp_client() -> tos.TcpClient:
    """Create TcpClient.

    Returns
    -------
    TcpOslServer:
        Class which provides access to optiSLang server using plain TCP/IP communication protocol.
    """
    client = tos.TcpClient()
    client.connect(host=_host, port=_port)
    return client


@pytest.fixture
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
    return tos.TcpOslServer(host=_host, port=_port)


## TcpClient
def test_connect(tcp_client):
    "Test ``connect``."
    client = tos.TcpClient()
    with does_not_raise() as dnr:
        client.connect(host=_host, port=_port)
    assert dnr is None


def test_disconnect(tcp_client):
    "Test ``disconnect``"
    client = tcp_client
    with does_not_raise() as dnr:
        client.disconnect()
    assert dnr is None


def test_send_msg(tcp_client):
    "Test ``send_msg`"
    client = tcp_client
    with does_not_raise() as dnr:
        client.send_msg(_msg)
    assert dnr is None


def test_send_file(tcp_client, tmp_path):
    "Test ``send_file`"
    client = tcp_client
    file_path = os.path.join(tmp_path, "testfile.txt")
    with open(file_path, "w") as testfile:
        testfile.write(_msg)
    with does_not_raise() as dnr:
        client.send_file(file_path)
    assert dnr is None


def test_receive_msg(tcp_client):
    "Test ``receive_msg``."
    client = tcp_client
    client.send_msg(_msg)
    msg = client.receive_msg()
    assert isinstance(msg, str)


def test_receive_file(tcp_client, tmp_path):
    "Test ``receive_file`"
    client = tcp_client
    file_path = os.path.join(tmp_path, "testfile.txt")
    with open(file_path, "w") as testfile:
        testfile.write(_msg)
    client.send_file(file_path)
    with does_not_raise() as dnr:
        client.receive_file(os.path.join(tmp_path, "received.txt"))
    assert dnr is None


## TcpOslServer
def test_get_server_info(tcp_osl_server):
    """Test ``_get_server_info``."""
    server_info = tcp_osl_server._get_server_info()
    assert isinstance(server_info, dict)
    assert bool(server_info)


def test_get_basic_project_info(tcp_osl_server):
    """Test ``_get_basic_project_info``."""
    server = tcp_osl_server
    basic_project_info = server._get_basic_project_info()
    assert isinstance(basic_project_info, dict)
    assert bool(basic_project_info)


def test_get_osl_version(tcp_osl_server):
    """Test ``get_osl_version``."""
    server = tcp_osl_server
    version = server.get_osl_version()
    assert isinstance(version, str)
    assert bool(version)


def test_get_project_description(tcp_osl_server):
    """Test ``get_project_description``."""
    server = tcp_osl_server
    project_description = server.get_project_description()
    assert isinstance(project_description, str)
    assert not bool(project_description)


def test_get_project_location(tcp_osl_server):
    """Test ``get_project_location``."""
    server = tcp_osl_server
    project_location = server.get_project_location()
    assert isinstance(project_location, str)
    assert bool(project_location)


def test_get_project_name(tcp_osl_server):
    """Test ``get_project_name``."""
    server = tcp_osl_server
    project_name = server.get_project_name()
    assert isinstance(project_name, str)
    assert bool(project_name)


def test_get_project_status(tcp_osl_server):
    """Test ``get_get_project_status``."""
    server = tcp_osl_server
    project_status = server.get_project_status()
    assert isinstance(project_status, str)
    assert bool(project_status)


def test_get_working_dir(tcp_osl_server):
    """Test ``get_working_dir``."""
    server = tcp_osl_server
    working_dir = server.get_working_dir()
    assert isinstance(working_dir, str)
    assert bool(working_dir)


# not implemented
def test_new(tcp_osl_server):
    """Test ``new``."""
    server = tcp_osl_server
    with pytest.raises(NotImplementedError):
        server.new()


# not implemented
def test_open(tcp_osl_server):
    """Test ``open``."""
    server = tcp_osl_server
    with pytest.raises(NotImplementedError):
        server.open("string", False, False, False)


def test_reset(tcp_osl_server):
    """Test ``reset``."""
    server = tcp_osl_server
    with does_not_raise() as dnr:
        server.reset()
    assert dnr is None


def test_run_python_file(tcp_osl_server, tmp_path):
    """Test ``run_python_file``."""
    server = tcp_osl_server
    cmd = """
a = 5
b = 10
result = a + b
print(result)
"""
    cmd_path = os.path.join(tmp_path, "commands.txt")
    with open(cmd_path, "w") as f:
        f.write(cmd)
    run_file = server.run_python_file(file_path=cmd_path)
    assert isinstance(run_file, tuple)


def test_run_python_script(tcp_osl_server):
    """Test ``run_python_script``."""
    server = tcp_osl_server
    cmd = """
a = 5
b = 10
result = a + b
print(result)
"""
    run_script = server.run_python_script(script=cmd)
    assert isinstance(run_script, tuple)


# not implemented
def test_save(tcp_osl_server):
    """Test ``save``."""
    server = tcp_osl_server
    with pytest.raises(NotImplementedError):
        server.save()


# not implemented
def test_save_as(tcp_osl_server):
    """Test ``save_as``."""
    server = tcp_osl_server
    with pytest.raises(NotImplementedError):
        server.save_as("string", False, False, False)


def test_save_copy(tmp_path, tcp_osl_server):
    """Test ``save_copy``."""
    server = tcp_osl_server
    copy_path = os.path.join(tmp_path, "test_save_copy.opf")
    server.save_copy(copy_path)
    assert os.path.isfile(copy_path)


def test_start(tcp_osl_server):
    """Test ``start``."""
    server = tcp_osl_server
    with does_not_raise() as dnr:
        server.start()
    assert dnr is None


def test_stop(tcp_osl_server):
    """Test ``stop``."""
    server = tcp_osl_server
    with does_not_raise() as dnr:
        server.stop()
    assert dnr is None


def test_stop_gently(tcp_osl_server):
    """Test ``stop_gently``."""
    server = tcp_osl_server
    with does_not_raise() as dnr:
        server.stop_gently()
    assert dnr is None


def test_shutdown(tcp_osl_server):
    """Test ``shutdown``."""
    server = tcp_osl_server
    with does_not_raise() as dnr:
        server.shutdown()
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
