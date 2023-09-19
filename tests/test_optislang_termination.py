from contextlib import closing
from contextlib import nullcontext as does_not_raise
import os
from pathlib import Path
import socket
import tempfile
import time

import pytest

from ansys.optislang.core import Optislang, OslServerProcess
from ansys.optislang.core.errors import ConnectionNotEstablishedError, OslCommunicationError

_host = socket.gethostbyname(socket.gethostname())


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def create_osl_server_process(shutdown_on_finished=False) -> OslServerProcess:
    port = find_free_port()
    with tempfile.TemporaryDirectory() as temp_dir:
        server_info_file = Path(temp_dir) / "osl_server_info.ini"
        osl_server_process = OslServerProcess(
            shutdown_on_finished=shutdown_on_finished,
            port_range=(port, port),
            server_info=server_info_file,
        )
        osl_server_process.start()

        start_timeout = 30
        time_counter = 0
        while not os.path.exists(server_info_file):
            time.sleep(1)
            time_counter += 1
            if time_counter > start_timeout:
                break

        if os.path.exists(server_info_file):
            return osl_server_process
        osl_server_process.terminate()
        raise TimeoutError("optiSLang Process start timed out")


pytestmark = pytest.mark.local_osl


# region CONTEXT MANAGER
@pytest.mark.parametrize(
    "send_dispose, send_shutdown, osl_none",
    [
        (True, False, False),  # send dispose
        (False, True, False),  # send shutdown
        (False, False, True),  # set osl=None
        (False, False, False),  # do nothing
    ],
)
def test_local_default_cm(send_dispose, send_shutdown, osl_none):
    osl_port = None
    with Optislang(shutdown_on_finished=True) as osl:
        version = osl.application.get_version()
        osl.application.project.start()
        osl_port = osl._Optislang__osl_server._TcpOslServer__port
        if send_dispose:
            osl.dispose()
        if send_shutdown:
            osl.shutdown()
        if osl_none:
            osl = None

    # server not running
    with pytest.raises(
        (
            ConnectionNotEstablishedError,
            ConnectionRefusedError,
            OslCommunicationError,
            RuntimeError,
        )
    ):
        osl = Optislang(host="127.0.0.1", port=osl_port, ini_timeout=10)
        osl.shutdown()


@pytest.mark.parametrize(
    "send_dispose, send_shutdown, osl_none",
    [
        (True, False, False),  # send dispose
        (False, True, False),  # send shutdown
        (False, False, True),  # set osl=None
        (False, False, False),  # do nothing
    ],
)
def test_local_shutdown_on_finished_false_cm(send_dispose, send_shutdown, osl_none):
    osl_port = None
    with Optislang(shutdown_on_finished=False) as osl:
        version = osl.application.get_version()
        osl.application.project.start()
        osl_port = osl._Optislang__osl_server._TcpOslServer__port
        if send_dispose:
            osl.dispose()
        if send_shutdown:
            osl.shutdown()
        if osl_none:
            osl = None

    if not send_shutdown:
        with does_not_raise() as dnr:
            osl = Optislang(host="127.0.0.1", port=osl_port, ini_timeout=10)
            osl.shutdown()
        assert dnr is None
    else:
        with pytest.raises(
            (
                ConnectionNotEstablishedError,
                ConnectionRefusedError,
                OslCommunicationError,
                RuntimeError,
            )
        ):
            osl = Optislang(host="127.0.0.1", port=osl_port, ini_timeout=10)
            osl.shutdown()


@pytest.mark.parametrize(
    "send_dispose, send_shutdown, osl_none",
    [
        (True, False, False),  # send dispose
        (False, True, False),  # send shutdown
        (False, False, True),  # set osl=None
        (False, False, False),  # do nothing
    ],
)
def test_remote_cm(send_dispose, send_shutdown, osl_none):
    # start optiSLang server
    osl_server_process = create_osl_server_process(shutdown_on_finished=False)
    # connect to running optiSLang server
    with Optislang(host=_host, port=osl_server_process.port_range[0]) as osl:
        version = osl.application.get_version()
        osl.application.project.start()
        if send_dispose:
            osl.dispose()
        if send_shutdown:
            osl.shutdown()
        if osl_none:
            osl = None

    if not send_shutdown:
        with does_not_raise() as dnr:
            osl = Optislang(host="127.0.0.1", port=osl_server_process.port_range[0], ini_timeout=10)
            osl.shutdown()
        assert dnr is None
    else:
        with pytest.raises(
            (
                ConnectionNotEstablishedError,
                ConnectionRefusedError,
                OslCommunicationError,
                RuntimeError,
            )
        ):
            osl = Optislang(host="127.0.0.1", port=osl_server_process.port_range[0], ini_timeout=10)
            osl.shutdown()


# endregion


# region WITHOUT CM
@pytest.mark.parametrize(
    "send_dispose, send_shutdown",
    [
        (True, False),  # send dispose
        (False, True),  # send shutdown
    ],
)
def test_local_default_wocm(send_dispose, send_shutdown):
    osl = Optislang(shutdown_on_finished=True)
    version = osl.application.get_version()
    osl.application.project.start()
    osl_port = osl._Optislang__osl_server._TcpOslServer__port
    if send_dispose:
        osl.dispose()
    if send_shutdown:
        osl.shutdown()

    # server not running
    with pytest.raises(
        (
            ConnectionNotEstablishedError,
            ConnectionRefusedError,
            OslCommunicationError,
            RuntimeError,
        )
    ):
        osl = Optislang(host="127.0.0.1", port=osl_port, ini_timeout=10)
        osl.shutdown()


@pytest.mark.parametrize(
    "send_dispose, send_shutdown",
    [
        (True, False),  # send dispose
        (False, True),  # send shutdown
    ],
)
def test_local_shutdown_on_finished_false_wocm(send_dispose, send_shutdown):
    osl = Optislang(shutdown_on_finished=False)
    version = osl.application.get_version()
    osl.application.project.start()
    osl_port = osl._Optislang__osl_server._TcpOslServer__port
    if send_dispose:
        osl.dispose()
    if send_shutdown:
        osl.shutdown()

    if not send_shutdown:
        with does_not_raise() as dnr:
            osl = Optislang(host="127.0.0.1", port=osl_port, ini_timeout=10)
            osl.shutdown()
        assert dnr is None
    else:
        with pytest.raises(
            (
                ConnectionNotEstablishedError,
                ConnectionRefusedError,
                OslCommunicationError,
                RuntimeError,
            )
        ):
            osl = Optislang(host="127.0.0.1", port=osl_port, ini_timeout=10)
            osl.shutdown()


@pytest.mark.parametrize(
    "send_dispose, send_shutdown",
    [
        (True, False),  # send dispose
        (False, True),  # send shutdown
    ],
)
def test_remote_wocm(send_dispose, send_shutdown):
    port = find_free_port()
    # start optiSLang server
    osl_server_process = create_osl_server_process(shutdown_on_finished=False)
    # connect to running optiSLang server
    osl = Optislang(host=_host, port=osl_server_process.port_range[0])
    version = osl.application.get_version()
    osl.application.project.start()
    if send_dispose:
        osl.dispose()
    if send_shutdown:
        osl.shutdown()

    if not send_shutdown:
        with does_not_raise() as dnr:
            osl = Optislang(host="127.0.0.1", port=osl_server_process.port_range[0], ini_timeout=10)
            osl.shutdown()
        assert dnr is None
    else:
        with pytest.raises(
            (
                ConnectionNotEstablishedError,
                ConnectionRefusedError,
                OslCommunicationError,
                RuntimeError,
            )
        ):
            osl = Optislang(host="127.0.0.1", port=osl_server_process.port_range[0], ini_timeout=10)
            osl.shutdown()


def test_local_and_remote_simultaneously():
    """Test connection to locally started server, dispose locally started instance."""
    osl_local = Optislang()
    osl_remote = Optislang(port=osl_local.osl_server.port, host=osl_local.osl_server.host)
    osl_local.dispose()
    time.sleep(30)
    version = osl_remote.application.get_version_string()
    osl_remote.dispose()


# endregion
