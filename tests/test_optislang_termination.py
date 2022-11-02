from contextlib import nullcontext as does_not_raise
import socket
import time

import pytest

from ansys.optislang.core import Optislang, OslServerProcess
from ansys.optislang.core.errors import ConnectionNotEstablishedError, OslCommunicationError

_host = socket.gethostbyname(socket.gethostname())
_port = 5310
pytestmark = pytest.mark.local_osl

#%% CONTEXT MANAGER
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
    with Optislang(shutdown_on_finished=True) as osl:
        version = osl.get_osl_version()
        osl.start()
        if send_dispose:
            osl.dispose()
        if send_shutdown:
            osl.shutdown()
        if osl_none:
            osl = None

    # server not running
    time.sleep(5)
    with pytest.raises(
        (
            ConnectionNotEstablishedError,
            ConnectionRefusedError,
            OslCommunicationError,
        )
    ):
        osl = Optislang(host="127.0.0.1", port=5310, ini_timeout=5)
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
    with Optislang(shutdown_on_finished=False) as osl:
        version = osl.get_osl_version()
        osl.start()
        if send_dispose:
            osl.dispose()
        if send_shutdown:
            osl.shutdown()
        if osl_none:
            osl = None

    if not send_shutdown:
        with does_not_raise() as dnr:
            time.sleep(5)
            osl = Optislang(host="127.0.0.1", port=5310, ini_timeout=5)
            osl.shutdown()
        assert dnr is None
    else:
        time.sleep(5)
        with pytest.raises(
            (
                ConnectionNotEstablishedError,
                ConnectionRefusedError,
                OslCommunicationError,
            )
        ):
            osl = Optislang(host="127.0.0.1", port=5310, ini_timeout=5)
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
    time.sleep(2)
    osl_server_process = OslServerProcess(shutdown_on_finished=False)
    osl_server_process.start()
    time.sleep(5)
    # connect to running optiSLang server
    with Optislang(host=_host, port=_port) as osl:
        version = osl.get_osl_version()
        osl.start()
        if send_dispose:
            osl.dispose()
        if send_shutdown:
            osl.shutdown()
        if osl_none:
            osl = None

    if not send_shutdown:
        with does_not_raise() as dnr:
            time.sleep(5)
            osl = Optislang(host="127.0.0.1", port=5310, ini_timeout=10)
            osl.shutdown()
        assert dnr is None
    else:
        time.sleep(5)
        with pytest.raises(
            (
                ConnectionNotEstablishedError,
                ConnectionRefusedError,
                OslCommunicationError,
            )
        ):
            osl = Optislang(host="127.0.0.1", port=5310, ini_timeout=10)
            osl.shutdown()


#%% WITHOUT CM
@pytest.mark.parametrize(
    "send_dispose, send_shutdown",
    [
        (True, False),  # send dispose
        (False, True),  # send shutdown
    ],
)
def test_local_default_wocm(send_dispose, send_shutdown):
    osl = Optislang(shutdown_on_finished=True)
    version = osl.get_osl_version()
    osl.start()
    if send_dispose:
        osl.dispose()
    if send_shutdown:
        osl.shutdown()

    # server not running
    time.sleep(5)
    with pytest.raises(
        (
            ConnectionNotEstablishedError,
            ConnectionRefusedError,
            OslCommunicationError,
        )
    ):
        osl = Optislang(host="127.0.0.1", port=5310, ini_timeout=5)
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
    version = osl.get_osl_version()
    osl.start()
    if send_dispose:
        osl.dispose()
    if send_shutdown:
        osl.shutdown()

    if not send_shutdown:
        with does_not_raise() as dnr:
            time.sleep(5)
            osl = Optislang(host="127.0.0.1", port=5310, ini_timeout=5)
            osl.shutdown()
        assert dnr is None
    else:
        time.sleep(5)
        with pytest.raises(
            (
                ConnectionNotEstablishedError,
                ConnectionRefusedError,
                OslCommunicationError,
            )
        ):
            osl = Optislang(host="127.0.0.1", port=5310, ini_timeout=5)
            osl.shutdown()


@pytest.mark.parametrize(
    "send_dispose, send_shutdown",
    [
        (True, False),  # send dispose
        (False, True),  # send shutdown
    ],
)
def test_remote_wocm(send_dispose, send_shutdown):
    # start optiSLang server
    time.sleep(2)
    osl_server_process = OslServerProcess(shutdown_on_finished=False)
    osl_server_process.start()
    time.sleep(5)
    # connect to running optiSLang server
    osl = Optislang(host=_host, port=_port)
    version = osl.get_osl_version()
    osl.start()
    if send_dispose:
        osl.dispose()
    if send_shutdown:
        osl.shutdown()

    if not send_shutdown:
        with does_not_raise() as dnr:
            time.sleep(5)
            osl = Optislang(host="127.0.0.1", port=5310, ini_timeout=10)
            osl.shutdown()
        assert dnr is None
    else:
        time.sleep(5)
        with pytest.raises(
            (
                ConnectionNotEstablishedError,
                ConnectionRefusedError,
                OslCommunicationError,
            )
        ):
            osl = Optislang(host="127.0.0.1", port=5310, ini_timeout=10)
            osl.shutdown()
