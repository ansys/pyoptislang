from contextlib import nullcontext as does_not_raise
from pathlib import Path
import time

import pytest

from ansys.optislang.core import Optislang
from ansys.optislang.core.nodes import RootSystem

pytestmark = pytest.mark.local_osl


@pytest.fixture()
def optislang(scope="function", autouse=True) -> Optislang:
    """Create Optislang class.

    Returns
    -------
    Optislang:
        Connects to the optiSLang application and provides an API to control it.
    """
    osl = Optislang()
    osl.set_timeout(20)
    return osl


def test_get_description(optislang: Optislang):
    """Test `get_description`."""
    project = optislang.project
    description = project.get_description()
    assert isinstance(description, str)
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


def test_get_location(optislang: Optislang):
    """Test ``get_location``."""
    project = optislang.project
    location = project.get_location()
    assert isinstance(location, Path)
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


def test_get_name(optislang: Optislang):
    """Test ``get_name``."""
    project = optislang.project
    name = project.get_name()
    assert isinstance(name, str)
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


def test_get_status(optislang: Optislang):
    """Test ``get_status``."""
    project = optislang.project
    status = project.get_status()
    assert isinstance(status, str)
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


def test_project_properties(optislang: Optislang):
    """Test `root_system`, `uid` and `__str__` method."""
    project = optislang.project
    uid = project.uid
    assert isinstance(uid, str)
    root_system = project.root_system
    assert isinstance(root_system, RootSystem)
    with does_not_raise() as dnr:
        print(project)
        optislang.dispose()
        time.sleep(3)
    assert dnr is None
