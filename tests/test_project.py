from contextlib import nullcontext as does_not_raise
from pathlib import Path
import time

import pytest

from ansys.optislang.core import Optislang, examples
from ansys.optislang.core.io import RegisteredFile
from ansys.optislang.core.nodes import RootSystem
from ansys.optislang.core.project_parametric import Design, ParameterManager

pytestmark = pytest.mark.local_osl
calculator_w_parameters = examples.get_files("calculator_with_params")[1][0]


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


def test_project_queries(optislang: Optislang):
    """Test project queries."""
    project = optislang.project

    description = project.get_description()
    assert isinstance(description, str)

    location = project.get_location()
    assert isinstance(location, Path)

    name = project.get_name()
    assert isinstance(name, str)

    status = project.get_status()
    assert isinstance(status, str)

    optislang.open(file_path=calculator_w_parameters)

    reg_files = project.get_registered_files()
    assert len(reg_files) == 3
    assert isinstance(reg_files[0], RegisteredFile)

    res_files = project.get_result_files()
    assert len(res_files) == 1
    assert isinstance(res_files[0], RegisteredFile)

    optislang.dispose()


def test_project_properties(optislang: Optislang):
    """Test `root_system`, `uid` and `__str__` method."""
    project = optislang.project
    uid = project.uid
    assert isinstance(uid, str)
    root_system = project.root_system
    assert isinstance(root_system, RootSystem)
    parameter_manager = project.parameter_manager
    assert isinstance(parameter_manager, ParameterManager)
    with does_not_raise() as dnr:
        print(project)
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


def test_get_evaluate_design(optislang: Optislang):
    """Test `get_reference_design` and `evaluate_design`."""
    project = optislang.project
    ref_design = project.get_reference_design()
    assert isinstance(ref_design, Design)
    eval_design = project.evaluate_design(design=ref_design)
    assert isinstance(eval_design, Design)
    optislang.dispose()
    time.sleep(3)
