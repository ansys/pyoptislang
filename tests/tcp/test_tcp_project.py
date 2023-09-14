from contextlib import nullcontext as does_not_raise
from pathlib import Path
import time

import pytest

from ansys.optislang.core import Optislang
from ansys.optislang.core.project_parametric import Design
from ansys.optislang.core.tcp.base_nodes import TcpRootSystemProxy
from ansys.optislang.core.tcp.managers import (
    TcpCriteriaManagerProxy,
    TcpParameterManagerProxy,
    TcpResponseManagerProxy,
)
from ansys.optislang.core.tcp.project import TcpProjectProxy

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
    osl.timeout = 20
    return osl


def test_project_queries(optislang: Optislang):
    """Test project queries."""
    project: TcpProjectProxy = optislang.project

    available_nodes = project.get_available_nodes()
    assert isinstance(available_nodes, dict)

    description = project.get_description()
    assert isinstance(description, str)

    location = project.get_location()
    assert isinstance(location, Path)

    name = project.get_name()
    assert isinstance(name, str)

    status = project.get_status()
    assert isinstance(status, str)

    wdir = project.get_working_dir()
    assert isinstance(wdir, Path)

    optislang.dispose()
    time.sleep(3)


def test_project_properties(optislang: Optislang):
    """Test `root_system`, `uid` and `__str__` method."""
    project: TcpProjectProxy = optislang.project
    uid = project.uid
    assert isinstance(uid, str)
    root_system = project.root_system
    assert isinstance(root_system, TcpRootSystemProxy)
    criteria_manager = project.criteria_manager
    assert isinstance(criteria_manager, TcpCriteriaManagerProxy)
    parameter_manager = project.parameter_manager
    assert isinstance(parameter_manager, TcpParameterManagerProxy)
    response_manager = project.response_manager
    assert isinstance(response_manager, TcpResponseManagerProxy)

    with does_not_raise() as dnr:
        print(project)

    optislang.dispose()
    time.sleep(3)


def test_evaluate_design(optislang: Optislang):
    """Test `get_reference_design` and `evaluate_design`."""
    project: TcpProjectProxy = optislang.project
    ref_design = project.get_reference_design()
    assert isinstance(ref_design, Design)
    eval_design = project.evaluate_design(design=ref_design)
    assert isinstance(eval_design, Design)
    optislang.dispose()
    time.sleep(3)


def test_reset(optislang: Optislang):
    """Test `reset()` command."""
    project = optislang.project
    with does_not_raise() as dnr:
        project.reset()
    optislang.dispose()
    time.sleep(3)


def test_run_python_file(optislang: Optislang, tmp_path: Path):
    "Test ``run_python_file``."
    project = optislang.project
    cmd = "a = 5\nb = 10\nresult = a + b\nprint(result)"
    cmd_path = tmp_path / "commands.txt"
    with open(cmd_path, "w") as f:
        f.write(cmd)
    run_file = project.run_python_file(file_path=cmd_path)
    assert isinstance(run_file, tuple)
    optislang.dispose()
    time.sleep(3)


def test_run_python_script(optislang: Optislang):
    "Test ``run_python_script``."
    project = optislang.project
    run_script = project.run_python_script("a = 5\nb = 10\nresult = a + b\nprint(result)")
    assert isinstance(run_script, tuple)
    assert run_script[0][0:2] == "15"
    optislang.dispose()
    time.sleep(3)


def test_start(optislang: Optislang):
    """Test `start()` command."""
    project = optislang.project
    with does_not_raise() as dnr:
        project.start()
    optislang.dispose()
    time.sleep(3)


def test_stop(optislang: Optislang):
    """Test `stop()` command."""
    project = optislang.project
    project.run_python_script(
        r"""
from py_os_design import *
sens = actors.SensitivityActor("Sensitivity")
add_actor(sens)
python = actors.PythonActor('python_sleep')
sens.add_actor(python)
python.source = 'import time\ntime.sleep(0.1)\noutput_value = input_value*2'
python.add_parameter("input_value", PyOSDesignEntry(5.0))
python.add_response(("output_value", PyOSDesignEntry(10)))
connect(sens, "IODesign", python, "IDesign")
connect(python, "ODesign", sens, "IIDesign")
"""
    )
    project.start(wait_for_finished=False)
    project.stop()
    optislang.dispose()
    time.sleep(3)


# def test_stop_gently(optislang: Optislang):
#     "Test ``stop_gently``."
#     project = optislang.project
#     project.run_python_script(
#         r"""
# from py_os_design import *
# sens = actors.SensitivityActor("Sensitivity")
# add_actor(sens)
# python = actors.PythonActor('python_sleep')
# sens.add_actor(python)
# python.source = 'import time\ntime.sleep(0.1)\noutput_value = input_value*2'
# python.add_parameter("input_value", PyOSDesignEntry(5.0))
# python.add_response(("output_value", PyOSDesignEntry(10)))
# connect(sens, "IODesign", python, "IDesign")
# connect(python, "ODesign", sens, "IIDesign")
# """
#     )
#     project.start(wait_for_finished=False)
#     project.stop_gently()
#     optislang.dispose()
#     time.sleep(3)
