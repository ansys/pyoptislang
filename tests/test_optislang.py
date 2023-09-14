from contextlib import nullcontext as does_not_raise
import time

import pytest

from ansys.optislang.core import Optislang, examples
from ansys.optislang.core.application import Application
from ansys.optislang.core.logging import OslCustomAdapter
from ansys.optislang.core.osl_server import OslServer
from ansys.optislang.core.project import Project

pytestmark = pytest.mark.local_osl
parametric_project = examples.get_files("calculator_with_params")[1][0]


@pytest.fixture()
def optislang(scope="function", autouse=False) -> Optislang:
    """Create Optislang class.

    Returns
    -------
    Optislang:
        Connects to the optiSLang application and provides an API to control it.
    """
    osl = Optislang()
    osl.timeout = 20
    return osl


def test_dispose(optislang: Optislang):
    "Test ``dispose``."
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


def test_optislang_properties(optislang: Optislang):
    """Test ``Optislang`` properties."""
    with does_not_raise() as dnr:
        print(optislang)

    application = optislang.application
    assert isinstance(application, Application)

    logger = optislang.log
    assert isinstance(logger, OslCustomAdapter)

    name = optislang.name
    assert isinstance(name, str)

    osl_server = optislang.osl_server
    assert isinstance(osl_server, OslServer)

    project = optislang.project
    assert isinstance(project, Project)

    timeout = optislang.timeout
    assert isinstance(timeout, (float, int))
    assert timeout == 20
    optislang.timeout = 30
    assert isinstance(timeout, (int, float))
    assert optislang.timeout == 30
    with pytest.raises(TypeError):
        optislang.timeout = "20"
    with pytest.raises(ValueError):
        optislang.timeout = -20

    optislang.dispose()
    time.sleep(3)
