import os
from pathlib import Path

import pytest

from ansys.optislang.core import Optislang
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
    osl.set_timeout(20)
    yield osl
    osl.dispose()


# # def test_close(optislang: Optislang):
#     "Test ``close`` (close opened and create new project)."
#     with does_not_raise() as dnr:
#         optislang.close()
#         optislang.new()
#         optislang.dispose()
#     assert dnr is None


# def test_dispose(optislang: Optislang):
# "Test ``dispose``."
# with does_not_raise() as dnr:
# optislang.dispose()
# time.sleep(3)
# assert dnr is None


def test_has_active_project(optislang: Optislang):
    """Test `has_active_project`"""
    # print(optislang)
    assert optislang.has_active_project


def test_get_osl_version_string(optislang: Optislang):
    """Test ``get_osl_version_string``."""
    version = optislang.get_osl_version_string()
    assert isinstance(version, str)


def test_get_osl_version(optislang: Optislang):
    """Test ``get_osl_version``."""
    major_version, minor_version, maintenance_version, revision = optislang.get_osl_version()
    assert isinstance(major_version, int)
    assert isinstance(minor_version, int)
    assert isinstance(maintenance_version, int) or maintenance_version == None
    assert isinstance(revision, int) or revision == None


def test_get_project(optislang: Optislang):
    """Test `get_project`."""
    project = optislang.project
    assert isinstance(project, Project)


def test_get_set_timeout(optislang: Optislang):
    """Test `get_timeout` and `set_timeout`.
    Note: default value is `None` but timeout set to 20 in @pytest.fixture optislang.
    """
    timeout = optislang.get_timeout()
    assert isinstance(timeout, (float, int))
    assert timeout == 20


def test_get_working_dir(optislang: Optislang):
    "Test ``get_working_dir``."
    working_dir = optislang.get_working_dir()
    assert isinstance(working_dir, Path)


def test_new(optislang: Optislang, tmp_path: Path):
    "Test ``new``."
    optislang.new()
    assert optislang.project is not None
    assert optislang.project.get_name() == "Unnamed project"
    optislang.save_as(file_path=tmp_path / "newProject.opf")


@pytest.mark.parametrize("path_type", [str, Path])
def test_open(optislang: Optislang, tmp_example_project, path_type):
    "Test ``open``."
    project = tmp_example_project("simple_calculator")
    if path_type == str:
        project = str(project)

    optislang.open(file_path=project)
    assert optislang.project is not None
    project_name = optislang.project.get_name()
    assert project_name == "calculator"


def test_reset(optislang: Optislang):
    "Test ``reset``."
    optislang.reset()


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


def test_save(optislang: Optislang):
    "Test save."
    project = optislang.project
    # XXX Property might not need to be an optional
    assert project is not None
    file_path = project.get_location()
    assert file_path.is_file()
    mod_time = os.path.getmtime(str(file_path))
    optislang.save()
    save_time = os.path.getmtime(str(file_path))
    assert mod_time != save_time


@pytest.mark.parametrize("path_type", [str, Path])
def test_save_as(optislang: Optislang, tmp_path: Path, path_type):
    "Test save_as."
    file_path = tmp_path / "test_save.opf"
    if path_type == str:
        optislang.save_as(file_path=str(file_path))
    else:
        optislang.save_as(file_path=file_path)
    assert file_path.is_file()


@pytest.mark.parametrize("path_type", [str, Path])
def test_save_copy(optislang: Optislang, tmp_path: Path, path_type):
    "Test ``save_copy``."
    copy_path = tmp_path / "test_save_copy.opf"
    if path_type == str:
        optislang.save_copy(file_path=str(copy_path))
    else:
        optislang.save_copy(file_path=copy_path)
    assert copy_path.is_file()


def test_start(optislang: Optislang):
    "Test ``start``."
    optislang.start()


def test_stop(optislang: Optislang):
    "Test ``stop``."
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
