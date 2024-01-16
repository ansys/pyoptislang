"""Test different start/stop/stop_gently combinations with Optislang class."""
import pytest

from ansys.optislang.core import Optislang

pytestmark = pytest.mark.local_osl


@pytest.fixture
def optislang() -> Optislang:
    """Create Optislang class.

    Returns
    -------
    Optislang:
        Connects to the optiSLang application and provides an API to control it.
    """
    osl = Optislang(ini_timeout=60)
    yield osl
    osl.dispose()


@pytest.mark.parametrize(
    "input",
    [
        (("start", True, True), ("stop", True)),  # default
        (("start", False, True), ("stop", True)),  # don't wait for started -> also default
        (("start", True, True), ("stop", False)),  # stop: don't wait for finished
        (("start", True, False), ("stop", True)),  # start: don't wait for finished
        (("start", False, False), ("stop", False)),  # all false
        (("start", True, True), ("stop", True), ("stop", True)),
        (("start", True, True), ("stop", True), ("start", True, True)),
        (("stop", True), ("stop", True), ("start", True, True)),
        (("start", True, True), ("start", True, True), ("start", True, True)),
    ],
)
def test_combinations(optislang: Optislang, input):
    "Test combinations."
    for method in input:
        if method[0] == "start":
            optislang.start(method[1], method[2])
        if method[0] == "stop":
            optislang.stop(method[1])
