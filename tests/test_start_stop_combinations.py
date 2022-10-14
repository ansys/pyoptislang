"""Test different start/stop/stop_gently combinations with Optislang class."""
from contextlib import nullcontext as does_not_raise

import pytest

from ansys.optislang.core import Optislang

pytestmark = pytest.mark.local_osl


@pytest.fixture
def optislang(scope="function", autouse=True) -> Optislang:
    """Create Optislang class.

    Returns
    -------
    Optislang:
        Connects to the optiSLang application and provides an API to control it.
    """
    return Optislang()


@pytest.mark.parametrize(
    "input, expected",
    [
        ((("start", True, True), ("stop", True)), None),  # default
        ((("start", False, True), ("stop", True)), None),  # don't wait for started -> also default
        ((("start", True, True), ("stop", False)), None),  # stop: don't wait for finished
        ((("start", True, False), ("stop", True)), None),  # start: don't wait for finished
        ((("start", False, False), ("stop", False)), None),  # all false
        ((("start", True, True), ("stop", True), ("stop", True)), None),
        ((("start", True, True), ("stop", True), ("start", True, True)), None),
        ((("stop", True), ("stop", True), ("start", True, True)), None),
        ((("start", True, True), ("start", True, True), ("start", True, True)), None),
    ],
)
def test_combinations(optislang, input, expected):
    "Test combinations."
    with does_not_raise() as dnr:
        for method in input:
            if method[0] == "start":
                optislang.start(method[1], method[2])
            if method[0] == "stop":
                optislang.stop(method[1])
        optislang.shutdown()
    assert dnr is expected
