import socket
import time

import pytest

from ansys.optislang.core import Optislang, OslServerProcess

_host = socket.gethostbyname(socket.gethostname())
_port = 5310
pytestmark = pytest.mark.local_osl


@pytest.mark.parametrize(
    "send_dispose, osl_none",
    [
        ((True, False), False),  # send dispose, shutdown_optislang=False
        ((False,), False),  # do NOT send dispose
        ((False,), True),  # osl = None
    ],
)
def test_local_default(send_dispose, osl_none):
    with Optislang(shutdown_on_finished=True) as osl:
        msg = print(osl)
        osl.start()
        if send_dispose[0]:
            osl.dispose(send_dispose[1])
        if osl_none:
            osl = None


@pytest.mark.parametrize(
    "send_dispose, osl_none",
    [
        ((True, True), False),  # send dispose, shutdown_optislang=True
        ((False,), False),  # do NOT send dispose
        ((False,), True),  # osl = None
    ],
)
def test_local_shutdown_on_finished_false(send_dispose, osl_none):
    with Optislang(shutdown_on_finished=False) as osl:
        msg = print(osl)
        osl.start()
        if send_dispose[0]:
            osl.dispose(send_dispose[1])
        if osl_none:
            osl = None


@pytest.mark.parametrize(
    "send_dispose, osl_none",
    [
        ((True, True), False),  # send dispose, shutdown_optislang=True
        ((False, True), False),  # do NOT send dispose
        ((False, True), True),  # osl = None
    ],
)
def test_remote(send_dispose, osl_none):
    # start optiSLang server
    time.sleep(2)
    osl_server_process = OslServerProcess(shutdown_on_finished=False)
    osl_server_process.start()
    time.sleep(5)
    # connect to running optiSLang server
    with Optislang(host=_host, port=_port) as osl:
        msg = print(osl)
        osl.start()
        if send_dispose[0]:
            osl.dispose(send_dispose[1])
        if osl_none:
            osl = None

        if osl_none or not send_dispose[1]:
            osl_server_process.terminate()
