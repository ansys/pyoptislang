from contextlib import nullcontext as does_not_raise
import os

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


def test_get_osl_version_string(optislang):
    "Test ``get_osl_version_string``."
    version = optislang.get_osl_version_string()
    assert isinstance(version, str)
    with does_not_raise() as dnr:
        optislang.dispose()
    assert dnr is None


def test_get_osl_version(optislang):
    """Test ``get_osl_version``."""
    major_version, minor_version, maintenance_version, revision = optislang.get_osl_version()
    assert isinstance(major_version, int)
    assert isinstance(minor_version, int)
    assert isinstance(maintenance_version, int) or maintenance_version == None
    assert isinstance(revision, int) or revision == None
    with does_not_raise() as dnr:
        optislang.shutdown()
    assert dnr is None


def test_get_project_description(optislang):
    "Test ``get_project_description``."
    description = optislang.get_project_description()
    assert isinstance(description, str)
    with does_not_raise() as dnr:
        optislang.dispose()
    assert dnr is None


def test_get_project_location(optislang):
    "Test ``get_project_location``."
    location = optislang.get_project_location()
    assert isinstance(location, str)
    with does_not_raise() as dnr:
        optislang.dispose()
    assert dnr is None


def test_get_project_name(optislang):
    "Test ``get_project_name``."
    name = optislang.get_project_name()
    assert isinstance(name, str)
    with does_not_raise() as dnr:
        optislang.dispose()
    assert dnr is None


def test_get_project_status(optislang):
    "Test ``get_project_status``."
    status = optislang.get_project_status()
    assert isinstance(status, str)
    with does_not_raise() as dnr:
        optislang.dispose()
    assert dnr is None


def test_get_working_dir(optislang):
    "Test ``get_working_dir``."
    working_dir = optislang.get_working_dir()
    assert isinstance(working_dir, str)
    with does_not_raise() as dnr:
        optislang.dispose()
    assert dnr is None


def test_reset(optislang):
    "Test ``reset``."
    with does_not_raise() as dnr:
        optislang.reset()
    assert dnr is None
    with does_not_raise() as dnr:
        optislang.dispose()
    assert dnr is None


def test_run_python_script(optislang):
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
    assert dnr is None


def test_run_python_file(optislang, tmp_path):
    "Test ``run_python_file``."
    cmd = """
a = 5
b = 10
result = a + b
print(result)
"""
    cmd_path = os.path.join(tmp_path, "commands.txt")
    with open(cmd_path, "w") as f:
        f.write(cmd)
    run_file = optislang.run_python_file(file_path=cmd_path)
    assert isinstance(run_file, tuple)
    with does_not_raise() as dnr:
        optislang.dispose()
    assert dnr is None


def test_save_copy(optislang, tmp_path):
    "Test ``save_copy``."
    with does_not_raise() as dnr:
        copy_path = os.path.join(tmp_path, "test_save_copy.opf")
        optislang.save_copy(file_path=copy_path)
    assert dnr is None
    assert os.path.isfile(copy_path)
    with does_not_raise() as dnr:
        optislang.dispose()
    assert dnr is None


def test_start(optislang):
    "Test ``start``."
    with does_not_raise() as dnr:
        optislang.start()
    assert dnr is None
    with does_not_raise() as dnr:
        optislang.dispose()
    assert dnr is None


def test_stop(optislang):
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
        optislang.start()
        optislang.stop()
    assert dnr is None
    with does_not_raise() as dnr:
        optislang.dispose()
    assert dnr is None


def test_stop_gently(optislang):
    "Test ``stop_gently``."
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
        optislang.stop_gently()
        optislang.start()
        optislang.stop()
    assert dnr is None
    with does_not_raise() as dnr:
        optislang.dispose()
    assert dnr is None


def test_dispose(optislang):
    "Test ``dispose``."
    with does_not_raise() as dnr:
        optislang.dispose()
    assert dnr is None
