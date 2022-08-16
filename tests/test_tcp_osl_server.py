from contextlib import nullcontext as does_not_raise
import os
import time

import pytest

from ansys.optislang.core import OslServerProcess
import ansys.optislang.core.tcp_osl_server as tos

NEW_PROJECT_STR = "New project"
OPENED_PROJECT_STR = "Opened project"

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
    # tmp = _host_and_port(osl)
    return tos.TcpOslServer(host="127.0.0.1", port=5310)


def test_get_server_info(tcp_osl_server):
    """Test ``_get_server_info``."""
    tmp = tcp_osl_server._get_server_info()
    print(tmp)
    assert isinstance(tmp, dict)
    assert bool(tmp)


def test_get_basic_project_info(tcp_osl_server):
    """Test ``_get_basic_project_info``."""
    server = tcp_osl_server
    tmp = server._get_basic_project_info()
    print(tmp)
    assert isinstance(tmp, dict)
    assert bool(tmp)


def test_get_osl_version(tcp_osl_server):
    """Test ``get_osl_version``."""
    server = tcp_osl_server
    tmp = server.get_osl_version()
    print(tmp)
    assert isinstance(tmp, str)
    assert bool(tmp)


def test_get_project_description(tcp_osl_server):
    """Test ``get_project_description``."""
    server = tcp_osl_server
    tmp = server.get_project_description()
    print(f"Type of output: {type(tmp)}, len: {len(tmp)},output: {tmp}")
    assert isinstance(tmp, str)
    assert not bool(tmp)


def test_get_project_location(tcp_osl_server):
    """Test ``get_project_location``."""
    server = tcp_osl_server
    tmp = server.get_project_location()
    print(f"Type of output: {type(tmp)}, len: {len(tmp)},output: {tmp}")
    assert isinstance(tmp, str)
    assert bool(tmp)


def test_get_project_name(tcp_osl_server):
    """Test ``get_project_name``."""
    server = tcp_osl_server
    tmp = server.get_project_name()
    print(f"Type of output: {type(tmp)}, len: {len(tmp)},output: {tmp}")
    assert isinstance(tmp, str)
    assert bool(tmp)


def test_get_project_status(tcp_osl_server):
    """Test ``get_get_project_status``."""
    server = tcp_osl_server
    tmp = server.get_project_status()
    print(f"Type of output: {type(tmp)}, len: {len(tmp)},output: {tmp}")
    assert isinstance(tmp, str)
    assert bool(tmp)


def test_get_working_dir(tcp_osl_server):
    """Test ``get_working_dir``."""
    server = tcp_osl_server
    tmp = server.get_working_dir()
    print(f"Type of output: {type(tmp)}, len: {len(tmp)},output: {tmp}")
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
