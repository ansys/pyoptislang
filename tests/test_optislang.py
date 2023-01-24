from contextlib import nullcontext as does_not_raise
import os
from pathlib import Path
import time

import pytest

from ansys.optislang.core import Optislang, examples
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
    osl.set_timeout(20)
    return osl


# # def test_close(optislang: Optislang):
#     "Test ``close`` (close opened and create new project)."
#     with does_not_raise() as dnr:
#         optislang.close()
#         optislang.new()
#         optislang.dispose()
#     assert dnr is None


def test_dispose(optislang: Optislang):
    "Test ``dispose``."
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


def test_has_active_project(optislang: Optislang):
    """Test `has_active_project`"""
    print(optislang)
    assert optislang.has_active_project
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


def test_get_osl_version_string(optislang: Optislang):
    """Test ``get_osl_version_string``."""
    version = optislang.get_osl_version_string()
    assert isinstance(version, str)
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


def test_get_osl_version(optislang: Optislang):
    """Test ``get_osl_version``."""
    major_version, minor_version, maintenance_version, revision = optislang.get_osl_version()
    assert isinstance(major_version, int)
    assert isinstance(minor_version, int)
    assert isinstance(maintenance_version, int) or maintenance_version == None
    assert isinstance(revision, int) or revision == None
    with does_not_raise() as dnr:
        optislang.dispose()
    assert dnr is None


def test_get_project(optislang: Optislang):
    """Test `get_project`."""
    with does_not_raise() as dnr:
        project = optislang.project
    optislang.dispose()
    assert dnr is None
    assert isinstance(project, Project)


def test_get_set_timeout(optislang: Optislang):
    """Test `get_timeout` and `set_timeout`.
    Note: default value is `None` but timeout set to 20 in @pytest.fixture optislang.
    """
    timeout = optislang.get_timeout()
    assert isinstance(timeout, (float, int))
    assert timeout == 20
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


def test_get_working_dir(optislang: Optislang):
    "Test ``get_working_dir``."
    working_dir = optislang.get_working_dir()
    assert isinstance(working_dir, Path)
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


def test_new(optislang: Optislang, tmp_path: Path):
    "Test ``new``."
    optislang.new()
    assert optislang.project.get_name() == "Unnamed project"
    with does_not_raise() as dnr:
        optislang.save_as(file_path=tmp_path / "newProject.opf")
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


@pytest.mark.parametrize("path_type", [str, Path])
def test_open(optislang: Optislang, path_type):
    "Test ``open``."
    project = examples.get_files("simple_calculator")[1][0]
    if path_type == str:
        project = str(project)

    optislang.open(file_path=project)
    project_name = optislang.project.get_name()
    assert project_name == "calculator"
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


def test_reset(optislang: Optislang):
    "Test ``reset``."
    with does_not_raise() as dnr:
        optislang.reset()
    assert dnr is None
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


def test_run_python_script(optislang: Optislang):
    "Test ``run_python_script``."
    run_script = optislang.run_python_script(
        """
a = 5
b = 10
result = a + b
print(result)
"""
    )
    assert isinstance(run_script, tuple)
    assert run_script[0][0:2] == "15"
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


def test_run_python_file(optislang: Optislang, tmp_path: Path):
    "Test ``run_python_file``."
    cmd = """
a = 5
b = 10
result = a + b
print(result)
"""
    cmd_path = tmp_path / "commands.txt"
    with open(cmd_path, "w") as f:
        f.write(cmd)
    run_file = optislang.run_python_file(file_path=cmd_path)
    assert isinstance(run_file, tuple)
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


def test_save(optislang: Optislang):
    "Test save."
    project = optislang.project
    file_path = project.get_location()
    assert file_path.is_file()
    mod_time = os.path.getmtime(str(file_path))
    optislang.save()
    save_time = os.path.getmtime(str(file_path))
    assert mod_time != save_time
    optislang.dispose()


@pytest.mark.parametrize("path_type", [str, Path])
def test_save_as(optislang: Optislang, tmp_path: Path, path_type):
    "Test save_as."
    file_path = tmp_path / "test_save.opf"
    if path_type == str:
        arg_path = str(file_path)
    else:
        arg_path = file_path
    optislang.save_as(file_path=arg_path)
    optislang.dispose()
    assert file_path.is_file()


@pytest.mark.parametrize("path_type", [str, Path])
def test_save_copy(optislang: Optislang, tmp_path: Path, path_type):
    "Test ``save_copy``."
    copy_path = tmp_path / "test_save_copy.opf"
    if path_type == str:
        arg_path = str(copy_path)
    else:
        arg_path = copy_path
    optislang.save_copy(file_path=arg_path)
    assert copy_path.is_file()
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


def test_start(optislang: Optislang):
    "Test ``start``."
    with does_not_raise() as dnr:
        optislang.start()
    assert dnr is None
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


def test_stop(optislang: Optislang):
    "Test ``stop``."
    with does_not_raise() as dnr:
        optislang.run_python_script(
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
        optislang.start(wait_for_finished=False)
        optislang.stop()
    assert dnr is None
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


# def test_stop_gently(optislang):
#     "Test ``stop_gently``."
#     with does_not_raise() as dnr:
#         optislang.run_python_script(
#             r"""
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
#         )
#         optislang.start(wait_for_finished=False)
#         optislang.stop_gently()
#     assert dnr is None
#     with does_not_raise() as dnr:
#         optislang.dispose()
#         time.sleep(3)
#     assert dnr is None


def test_dispose(optislang):
    "Test ``dispose``."
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None
