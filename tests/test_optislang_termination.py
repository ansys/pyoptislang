# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
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
        osl.project.start()
        osl_port = osl._Optislang__osl_server._TcpOslServer__port
        if send_dispose:
            osl.dispose()
        if send_shutdown:
            osl.shutdown(True)
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
        osl.project.start()
        osl_port = osl._Optislang__osl_server._TcpOslServer__port
        if send_dispose:
            osl.dispose()
        if send_shutdown:
            osl.shutdown()
        if osl_none:
            osl = None

    if not send_shutdown:
        osl = Optislang(host="127.0.0.1", port=osl_port, ini_timeout=10)
        osl.shutdown()
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
        osl.project.start()
        if send_dispose:
            osl.dispose()
        if send_shutdown:
            osl.shutdown()
        if osl_none:
            osl = None

    if not send_shutdown:
        osl = Optislang(host="127.0.0.1", port=osl_server_process.port_range[0], ini_timeout=10)
        osl.shutdown()
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
    osl = Optislang(shutdown_on_finished=True, ini_timeout=60)
    osl.project.start()
    osl_port = osl._Optislang__osl_server._TcpOslServer__port
    if send_dispose:
        osl.dispose()
    if send_shutdown:
        osl.shutdown(True)

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
    osl = Optislang(shutdown_on_finished=False, ini_timeout=60)
    osl.project.start()
    osl_port = osl._Optislang__osl_server._TcpOslServer__port
    if send_dispose:
        osl.dispose()
    if send_shutdown:
        osl.shutdown()

    if not send_shutdown:
        osl = Optislang(host="127.0.0.1", port=osl_port, ini_timeout=10)
        osl.shutdown()
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
    osl.project.start()
    if send_dispose:
        osl.dispose()
    if send_shutdown:
        osl.shutdown()

    if not send_shutdown:
        osl = Optislang(host="127.0.0.1", port=osl_server_process.port_range[0], ini_timeout=10)
        osl.shutdown()
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
    osl_local = Optislang(ini_timeout=60)
    osl_remote = Optislang(port=osl_local.osl_server.port, host=osl_local.osl_server.host)
    osl_local.dispose()
    time.sleep(30)
    name = osl_remote.application.project.get_name()
    osl_remote.dispose()


# endregion
