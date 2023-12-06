import time

import pytest

from ansys.optislang.core import Optislang
from ansys.optislang.core.application import Application
from ansys.optislang.core.logging import OslCustomAdapter
from ansys.optislang.core.osl_server import OslServer
from ansys.optislang.core.project import Project

pytestmark = pytest.mark.local_osl


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


# # def test_close(optislang: Optislang):
#     "Test ``close`` (close opened and create new project)."
#      optislang.close()
#      optislang.new()
#      optislang.dispose()


def test_dispose():
    "Test ``dispose``."
    osl = Optislang()
    osl.dispose()


def test_optislang_properties(optislang: Optislang):
    """Test ``Optislang`` properties."""
    print(optislang)

    application = optislang.application
    assert isinstance(application, Application)

    logger = optislang.log
    assert isinstance(logger, OslCustomAdapter)

    name = optislang.name
    assert isinstance(name, str)

    osl_server = optislang.osl_server
    assert isinstance(osl_server, OslServer)

    version = optislang.osl_version_string
    assert isinstance(version, str)

    major_version, minor_version, maintenance_version, revision = optislang.get_osl_version()
    assert isinstance(major_version, int)
    assert isinstance(minor_version, int)
    assert isinstance(maintenance_version, int)
    assert isinstance(revision, int)

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


def test_shutdown():
    "Test ``shutdown``."
    osl = Optislang(shutdown_on_finished=False)
    osl.shutdown()
    osl.dispose()
    time.sleep(3)
