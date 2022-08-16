from contextlib import nullcontext as does_not_raise
import os
import time

import pytest

from ansys.optislang.core import OslServerProcess
import ansys.optislang.core.tcp_osl_server as tos

_host = "127.0.0.1"
_port = 5310
_msg = '{ "What": "SYSTEMS_STATUS_INFO" }'


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
    tmp = client.receive_msg()
    assert isinstance(tmp, str)


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
    tmp = tcp_osl_server._get_server_info()
    assert isinstance(tmp, dict)
    assert bool(tmp)


def test_get_basic_project_info(tcp_osl_server):
    """Test ``_get_basic_project_info``."""
    server = tcp_osl_server
    tmp = server._get_basic_project_info()
    assert isinstance(tmp, dict)
    assert bool(tmp)


def test_get_osl_version(tcp_osl_server):
    """Test ``get_osl_version``."""
    server = tcp_osl_server
    tmp = server.get_osl_version()
    assert isinstance(tmp, str)
    assert bool(tmp)


def test_get_project_description(tcp_osl_server):
    """Test ``get_project_description``."""
    server = tcp_osl_server
    tmp = server.get_project_description()
    assert isinstance(tmp, str)
    assert not bool(tmp)


def test_get_project_location(tcp_osl_server):
    """Test ``get_project_location``."""
    server = tcp_osl_server
    tmp = server.get_project_location()
    assert isinstance(tmp, str)
    assert bool(tmp)


def test_get_project_name(tcp_osl_server):
    """Test ``get_project_name``."""
    server = tcp_osl_server
    tmp = server.get_project_name()
    assert isinstance(tmp, str)
    assert bool(tmp)


def test_get_project_status(tcp_osl_server):
    """Test ``get_get_project_status``."""
    server = tcp_osl_server
    tmp = server.get_project_status()
    assert isinstance(tmp, str)
    assert bool(tmp)


def test_get_working_dir(tcp_osl_server):
    """Test ``get_working_dir``."""
    server = tcp_osl_server
    tmp = server.get_working_dir()
    assert isinstance(tmp, str)
    assert bool(tmp)


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


# def test_run_python_script():
#     """Test ``run_python_script``."""
#     server = _tcp_osl_server()
#     tmp = server.run_python_script(script: str, args: Sequence[object])
#     assert type(tmp) == type(None)

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
