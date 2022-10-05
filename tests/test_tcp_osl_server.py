from contextlib import nullcontext as does_not_raise
import os
import time

import pytest

from ansys.optislang.core import OslServerProcess
import ansys.optislang.core.tcp_osl_server as tos

_host = "127.0.0.1"
_port = 5310
_msg = '{ "What": "SYSTEMS_STATUS_INFO" }'

pytestmark = pytest.mark.local_osl


@pytest.fixture(scope="function", autouse=True)
def osl_server_process():
    # Will be executed before the first test
    osl_server_process = OslServerProcess()
    osl_server_process.start()
    time.sleep(3)
    return osl_server_process


@pytest.fixture(scope="function", autouse=False)
def tcp_client() -> tos.TcpClient:
    """Create TcpClient.

    Returns
    -------
    TcpOslServer:
        Class which provides access to optiSLang server using plain TCP/IP communication protocol.
    """
    client = tos.TcpClient()
    return client


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
    tcp_osl_server.set_timeout(timeout=3)
    return tcp_osl_server


## TcpClient
def test_connect_and_disconnect(osl_server_process, tcp_client):
    "Test ``connect``."
    with does_not_raise() as dnr:
        tcp_client.connect(host=_host, port=_port)
        tcp_client.disconnect()
        osl_server_process.terminate()
    assert dnr is None


def test_send_msg(osl_server_process, tcp_client):
    "Test ``send_msg`"
    with does_not_raise() as dnr:
        tcp_client.connect(host=_host, port=_port)
        tcp_client.send_msg(_msg)
        tcp_client.disconnect()
        osl_server_process.terminate()
    assert dnr is None


def test_send_file(osl_server_process, tcp_client, tmp_path):
    "Test ``send_file`"
    file_path = os.path.join(tmp_path, "testfile.txt")
    with open(file_path, "w") as testfile:
        testfile.write(_msg)
    with does_not_raise() as dnr:
        tcp_client.connect(host=_host, port=_port)
        tcp_client.send_file(file_path)
        tcp_client.disconnect()
        osl_server_process.terminate()
    assert dnr is None


def test_receive_msg(osl_server_process, tcp_client):
    "Test ``receive_msg``."
    tcp_client.connect(host=_host, port=_port)
    tcp_client.send_msg(_msg)
    msg = tcp_client.receive_msg()
    tcp_client.disconnect()
    osl_server_process.terminate()
    assert isinstance(msg, str)


def test_receive_file(osl_server_process, tcp_client, tmp_path):
    "Test ``receive_file`"
    file_path = os.path.join(tmp_path, "testfile.txt")
    with open(file_path, "w") as testfile:
        testfile.write(_msg)
    tcp_client.connect(host=_host, port=_port)
    tcp_client.send_file(file_path)
    with does_not_raise() as dnr:
        tcp_client.receive_file(os.path.join(tmp_path, "received.txt"))
    tcp_client.disconnect()
    osl_server_process.terminate()
    assert dnr is None


## TcpOslServer
def test_get_server_info(osl_server_process, tcp_osl_server):
    """Test ``_get_server_info``."""
    server_info = tcp_osl_server._get_server_info()
    tcp_osl_server.shutdown()
    assert isinstance(server_info, dict)
    assert bool(server_info)


def test_get_basic_project_info(osl_server_process, tcp_osl_server):
    """Test ``_get_basic_project_info``."""
    basic_project_info = tcp_osl_server._get_basic_project_info()
    tcp_osl_server.shutdown()
    assert isinstance(basic_project_info, dict)
    assert bool(basic_project_info)


def test_get_osl_version(osl_server_process, tcp_osl_server):
    """Test ``get_osl_version``."""
    version = tcp_osl_server.get_osl_version()
    tcp_osl_server.shutdown()
    assert isinstance(version, str)
    assert bool(version)


def test_get_project_description(osl_server_process, tcp_osl_server):
    """Test ``get_project_description``."""
    project_description = tcp_osl_server.get_project_description()
    tcp_osl_server.shutdown()
    assert isinstance(project_description, str)
    assert not bool(project_description)


def test_get_project_location(osl_server_process, tcp_osl_server):
    """Test ``get_project_location``."""
    project_location = tcp_osl_server.get_project_location()
    tcp_osl_server.shutdown()
    assert isinstance(project_location, str)
    assert bool(project_location)


def test_get_project_name(osl_server_process, tcp_osl_server):
    """Test ``get_project_name``."""
    project_name = tcp_osl_server.get_project_name()
    tcp_osl_server.shutdown()
    assert isinstance(project_name, str)
    assert bool(project_name)


def test_get_project_status(osl_server_process, tcp_osl_server):
    """Test ``get_get_project_status``."""
    project_status = tcp_osl_server.get_project_status()
    tcp_osl_server.shutdown()
    assert isinstance(project_status, str)
    assert bool(project_status)


def test_get_working_dir(osl_server_process, tcp_osl_server):
    """Test ``get_working_dir``."""
    working_dir = tcp_osl_server.get_working_dir()
    tcp_osl_server.shutdown()
    assert isinstance(working_dir, str)
    assert bool(working_dir)


# not implemented
def test_new(osl_server_process, tcp_osl_server):
    """Test ``new``."""
    with pytest.raises(NotImplementedError):
        tcp_osl_server.new()
    tcp_osl_server.shutdown()


# not implemented
def test_open(osl_server_process, tcp_osl_server):
    """Test ``open``."""
    with pytest.raises(NotImplementedError):
        tcp_osl_server.open("string", False, False, False)
    tcp_osl_server.shutdown()


def test_reset(osl_server_process, tcp_osl_server):
    """Test ``reset``."""
    with does_not_raise() as dnr:
        tcp_osl_server.reset()
    tcp_osl_server.shutdown()
    assert dnr is None


def test_run_python_file(osl_server_process, tcp_osl_server, tmp_path):
    """Test ``run_python_file``."""
    cmd = """
a = 5
b = 10
result = a + b
print(result)
"""
    cmd_path = os.path.join(tmp_path, "commands.txt")
    with open(cmd_path, "w") as f:
        f.write(cmd)
    run_file = tcp_osl_server.run_python_file(file_path=cmd_path)
    tcp_osl_server.shutdown()
    assert isinstance(run_file, tuple)


def test_run_python_script(osl_server_process, tcp_osl_server):
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
def test_save(osl_server_process, tcp_osl_server):
    """Test ``save``."""
    with pytest.raises(NotImplementedError):
        tcp_osl_server.save()
    tcp_osl_server.shutdown()


# not implemented
def test_save_as(osl_server_process, tcp_osl_server):
    """Test ``save_as``."""
    with pytest.raises(NotImplementedError):
        tcp_osl_server.save_as("string", False, False, False)
    tcp_osl_server.shutdown()


def test_save_copy(osl_server_process, tmp_path, tcp_osl_server):
    """Test ``save_copy``."""
    copy_path = os.path.join(tmp_path, "test_save_copy.opf")
    tcp_osl_server.save_copy(copy_path)
    tcp_osl_server.shutdown()
    assert os.path.isfile(copy_path)


def test_start(osl_server_process, tcp_osl_server):
    """Test ``start``."""
    with does_not_raise() as dnr:
        tcp_osl_server.start()
    tcp_osl_server.shutdown()
    assert dnr is None


def test_stop(osl_server_process, tcp_osl_server):
    """Test ``stop``."""
    with does_not_raise() as dnr:
        tcp_osl_server.stop()
    tcp_osl_server.shutdown()
    assert dnr is None


def test_stop_gently(osl_server_process, tcp_osl_server):
    """Test ``stop_gently``."""
    with does_not_raise() as dnr:
        tcp_osl_server.stop_gently()
    tcp_osl_server.shutdown()
    assert dnr is None


def test_shutdown(osl_server_process, tcp_osl_server):
    """Test ``shutdown``."""
    with does_not_raise() as dnr:
        tcp_osl_server.shutdown()
    assert dnr is None
