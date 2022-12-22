from contextlib import nullcontext as does_not_raise
import logging
import os
from pathlib import Path
import socket
import time
import uuid

import pytest

from ansys.optislang.core import OslServerProcess, examples
import ansys.optislang.core.tcp_osl_server as tos

_host = socket.gethostbyname(socket.gethostname())
_port = 5310


_msg = '{ "What": "SYSTEMS_STATUS_INFO" }'

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
def test_client_properties(osl_server_process: OslServerProcess, tcp_client: tos.TcpClient):
    "Test ``local_address`` and ``remote_address``."
    with does_not_raise() as dnr:
        tcp_client.connect(host=_host, port=_port)
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
    assert dnr is None


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
    with does_not_raise() as dnr:
        tcp_listener.add_callback(print, "print-this")
        tcp_listener.clear_callbacks()
    assert dnr is None
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
# def test_close(tcp_osl_server: tos.TcpOslServer):
#     with does_not_raise() as dnr:
#         tcp_osl_server.close()
#         tcp_osl_server.new()
#         tcp_osl_server.dispose()
#     assert dnr is None


def test_dispose(tcp_osl_server: tos.TcpOslServer):
    """Test `dispose`."""
    with does_not_raise() as dnr:
        tcp_osl_server.shutdown()
        tcp_osl_server.dispose()
    assert dnr is None


def test_get_server_info(tcp_osl_server: tos.TcpOslServer):
    """Test ``_get_server_info``."""
    server_info = tcp_osl_server._get_server_info()
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert isinstance(server_info, dict)
    assert bool(server_info)


def test_get_basic_project_info(tcp_osl_server: tos.TcpOslServer):
    """Test ``_get_basic_project_info``."""
    basic_project_info = tcp_osl_server._get_basic_project_info()
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert isinstance(basic_project_info, dict)
    assert bool(basic_project_info)


def test_get_osl_version_string(osl_server_process, tcp_osl_server):
    """Test ``get_osl_version_string``."""
    version = tcp_osl_server.get_osl_version_string()
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert isinstance(version, str)
    assert bool(version)


def test_get_osl_version(tcp_osl_server):
    """Test ``get_osl_version``."""
    major_version, minor_version, maintenance_version, revision = tcp_osl_server.get_osl_version()
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert isinstance(major_version, int)
    assert isinstance(minor_version, int)
    assert isinstance(maintenance_version, int) or maintenance_version == None
    assert isinstance(revision, int) or revision == None


def test_get_project_description(osl_server_process, tcp_osl_server):
    """Test ``get_project_description``."""
    project_description = tcp_osl_server.get_project_description()
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert isinstance(project_description, str)
    assert not bool(project_description)


def test_get_project_location(tcp_osl_server: tos.TcpOslServer):
    """Test ``get_project_location``."""
    project_location = tcp_osl_server.get_project_location()
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert isinstance(project_location, Path)
    assert bool(project_location)


def test_get_project_name(tcp_osl_server: tos.TcpOslServer):
    """Test ``get_project_name``."""
    project_name = tcp_osl_server.get_project_name()
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert isinstance(project_name, str)
    assert bool(project_name)


def test_get_project_status(tcp_osl_server: tos.TcpOslServer):
    """Test ``get_get_project_status``."""
    project_status = tcp_osl_server.get_project_status()
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert isinstance(project_status, str)
    assert bool(project_status)


def test_get_set_timeout(tcp_osl_server: tos.TcpOslServer):
    """Test ``get_get_timeout``."""
    timeout = tcp_osl_server.get_timeout()
    assert isinstance(timeout, (int, float))
    assert timeout == 10
    tcp_osl_server.set_timeout(15)
    new_timeout = tcp_osl_server.get_timeout()
    assert isinstance(new_timeout, (int, float))
    assert new_timeout == 15
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_get_working_dir(tcp_osl_server: tos.TcpOslServer):
    """Test ``get_working_dir``."""
    working_dir = tcp_osl_server.get_working_dir()
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert isinstance(working_dir, Path)
    assert bool(working_dir)


def test_new(tcp_osl_server: tos.TcpOslServer):
    """Test ``new``."""
    tcp_osl_server.new()
    assert tcp_osl_server.get_project_name() == "Unnamed project"
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


@pytest.mark.parametrize("path_type", [str, Path])
def test_open(tcp_osl_server: tos.TcpOslServer, path_type):
    """Test ``open``."""
    project = examples.get_files("simple_calculator")[1][0]
    assert project.is_file()
    if path_type == str:
        project = str(project)
    tcp_osl_server.open(project)
    assert tcp_osl_server.get_project_name() == "calculator"
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


def test_reset(tcp_osl_server: tos.TcpOslServer):
    """Test ``reset``."""
    with does_not_raise() as dnr:
        tcp_osl_server.reset()
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
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
    tcp_osl_server.dispose()
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
    tcp_osl_server.dispose()
    assert isinstance(run_script, tuple)


def test_save(tcp_osl_server: tos.TcpOslServer):
    """Test ``save``."""
    file_path = tcp_osl_server.get_project_location()
    assert file_path.is_file()
    mod_time = os.path.getmtime(str(file_path))
    tcp_osl_server.save()
    save_time = os.path.getmtime(str(file_path))
    assert mod_time != save_time
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


@pytest.mark.parametrize("path_type", [str, Path])
def test_save_as(tcp_osl_server: tos.TcpOslServer, tmp_path: Path, path_type):
    """Test ``save_as``."""
    file_path = tmp_path / "test_save.opf"
    if path_type == str:
        arg_path = str(file_path)
    elif path_type == Path:
        arg_path = file_path

    tcp_osl_server.save_as(file_path=arg_path)
    assert file_path.is_file()
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()


@pytest.mark.parametrize("path_type", [str, Path])
def test_save_copy(tmp_path: Path, tcp_osl_server: tos.TcpOslServer, path_type):
    """Test ``save_copy``."""
    copy_path = tmp_path / "test_save_copy.opf"
    if path_type == str:
        arg_path = str(copy_path)
    elif path_type == Path:
        arg_path = copy_path

    tcp_osl_server.save_copy(arg_path)
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert copy_path.is_file()


def test_start(tcp_osl_server: tos.TcpOslServer):
    """Test ``start``."""
    with does_not_raise() as dnr:
        tcp_osl_server.start()
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
    assert dnr is None


def test_stop(tcp_osl_server: tos.TcpOslServer):
    """Test ``stop``."""
    with does_not_raise() as dnr:
        tcp_osl_server.stop()
    tcp_osl_server.shutdown()
    tcp_osl_server.dispose()
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
        tcp_osl_server.dispose()
    assert dnr is None
