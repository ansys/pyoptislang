# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from pathlib import Path

import pytest

from ansys.optislang.core import Optislang
from ansys.optislang.core.io import RegisteredFile
from ansys.optislang.core.project_parametric import Design
from ansys.optislang.core.tcp.managers import (
    TcpCriteriaManagerProxy,
    TcpParameterManagerProxy,
    TcpResponseManagerProxy,
)
from ansys.optislang.core.tcp.nodes import TcpRootSystemProxy
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
    osl = Optislang(ini_timeout=90)
    osl.timeout = 60
    yield osl
    osl.dispose()


def test_project_queries(optislang: Optislang, tmp_example_project):
    """Test project queries."""
    project: TcpProjectProxy = optislang.project
    assert project is not None

    with pytest.deprecated_call():
        available_nodes = project.get_available_nodes()
    assert isinstance(available_nodes, dict)

    available_node_types = project.get_available_node_types()
    assert isinstance(available_node_types, list)

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

    project_tree = project._get_project_tree()
    assert isinstance(project_tree, list)

    optislang.application.open(file_path=tmp_example_project("calculator_with_params"))

    reg_files = project.get_registered_files()
    assert len(reg_files) == 3
    assert isinstance(reg_files[0], RegisteredFile)

    res_files = project.get_result_files()
    assert len(res_files) == 1
    assert isinstance(res_files[0], RegisteredFile)

    project_tree = project._get_project_tree()
    assert isinstance(project_tree, list)


def test_project_properties(optislang: Optislang):
    """Test `root_system`, `uid` and `__str__` method."""
    project: TcpProjectProxy = optislang.project
    assert project is not None
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

    print(project)


def test_evaluate_design(optislang: Optislang):
    """Test `get_reference_design` and `evaluate_design`."""
    project: TcpProjectProxy = optislang.project
    assert project is not None
    ref_design = project.get_reference_design()
    assert isinstance(ref_design, Design)
    eval_design = project.evaluate_design(design=ref_design)
    assert isinstance(eval_design, Design)


def test_reset(optislang: Optislang):
    """Test `reset()` command."""
    project = optislang.project
    assert project is not None
    project.reset()


def test_run_python_file(optislang: Optislang, tmp_path: Path):
    "Test ``run_python_file``."
    project = optislang.project
    assert project is not None
    cmd = "a = 5\nb = 10\nresult = a + b\nprint(result)"
    cmd_path = tmp_path / "commands.txt"
    with open(cmd_path, "w") as f:
        f.write(cmd)
    run_file = project.run_python_file(file_path=cmd_path)
    assert isinstance(run_file, tuple)


def test_run_python_script(optislang: Optislang):
    "Test ``run_python_script``."
    project = optislang.project
    assert project is not None
    run_script = project.run_python_script("a = 5\nb = 10\nresult = a + b\nprint(result)")
    assert isinstance(run_script, tuple)
    assert run_script[0][0:2] == "15"


def test_start(optislang: Optislang):
    """Test `start()` command."""
    project = optislang.project
    assert project is not None
    project.start()


def test_stop(optislang: Optislang):
    """Test `stop()` command."""
    project = optislang.project
    assert project is not None
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


def test_placeholder_methods(optislang: Optislang):
    """Test placeholder management methods."""
    project = optislang.project

    # Test create_placeholder
    placeholder_id = project.create_placeholder(
        value="test_value", placeholder_id="test_placeholder", description="Test placeholder"
    )
    assert placeholder_id == "test_placeholder"

    # Test get_placeholder_ids
    placeholder_ids = project.get_placeholder_ids()
    assert "test_placeholder" in placeholder_ids

    # Test get_placeholder
    placeholder_info = project.get_placeholder("test_placeholder")
    assert placeholder_info is not None
    assert isinstance(placeholder_info, dict)

    # Test set_placeholder_value
    project.set_placeholder_value("test_placeholder", "updated_value")

    # Test rename_placeholder
    project.rename_placeholder("test_placeholder", "renamed_placeholder")
    updated_ids = project.get_placeholder_ids()
    assert "renamed_placeholder" in updated_ids
    assert "test_placeholder" not in updated_ids

    # Test remove_placeholder
    project.remove_placeholder("renamed_placeholder")
    final_ids = project.get_placeholder_ids()
    assert "renamed_placeholder" not in final_ids
