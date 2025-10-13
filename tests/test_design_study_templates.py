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
import os
from pathlib import Path
from typing import Callable

import pytest

from ansys.optislang.core import Optislang
from ansys.optislang.core.io import (
    OptislangPath,
    OptislangPathType,
    WorkingDirRelativePath,
)
import ansys.optislang.core.node_types as nt
from ansys.optislang.core.nodes import IntegrationNode, ParametricSystem
from ansys.optislang.core.project_parametric import (
    ObjectiveCriterion,
    OptimizationParameter,
    Response,
)
from ansys.optislang.parametric.design_study import (
    ExecutableBlock,
    ManagedParametricSystem,
)
from ansys.optislang.parametric.design_study_templates import (
    GeneralAlgorithmSettings,
    GeneralAlgorithmTemplate,
    GeneralNodeSettings,
    GeneralParametricSystemSettings,
    MopSolverNodeSettings,
    OptimizationOnMOPTemplate,
    ParametricSystemIntegrationTemplate,
    ProxySolverNodeSettings,
    PythonSolverNodeSettings,
    create_optislang_project_with_solver_node,
    create_workflow_from_template,
)

_PARAMETERS = [
    OptimizationParameter("X1"),
    OptimizationParameter("X2"),
    OptimizationParameter("X3"),
]
_CRITERIA = [ObjectiveCriterion("Y1", "Y")]
_RESPONSES = [Response("Y", 0.0)]
_PYTHON_SOURCE_CODE = r"""
try:
    Y = X1 + X2 + X3
except:
    Y= 0.0
"""


@pytest.fixture()
def optislang(scope="function", autouse=False) -> Optislang:
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


# region Settings


def test_general_node_settings():
    """Test `GeneralNodeSettings` class init and properties."""
    additional_settings = {
        "Property1": "string",
        "Property2": ["x", "y"],
        "Property3": 1,
        "Property4": {"key": "value"},
    }
    general_node_settings = GeneralNodeSettings(additional_settings)
    assert isinstance(general_node_settings.additional_settings, dict)
    assert general_node_settings.additional_settings.get("Property1") == "string"
    assert general_node_settings.additional_settings.get("Property4", {}).get("key") == "value"

    properties_dict = general_node_settings.convert_properties_to_dict()
    assert properties_dict == additional_settings


def test_mopsolver_settings():
    """Test `MopSolverNodeSettings` class init and properties."""
    mopsolver = MopSolverNodeSettings()
    assert mopsolver.multi_design_launch_num == 1
    assert mopsolver.input_file is None
    assert mopsolver.additional_settings == {}

    input1 = "path/to/input/file"
    input2 = Path(input1)
    input3 = WorkingDirRelativePath(head="", tail=input1)
    additional_settings = {
        "Property1": "string",
        "Property2": ["x", "y"],
        "Property3": 1,
        "Property4": {"key": "value"},
    }

    mopsolver1 = MopSolverNodeSettings(input1, -1, additional_settings)
    assert mopsolver1.additional_settings.get("Property1") == "string"
    assert mopsolver1.additional_settings.get("Property4", {}).get("key") == "value"
    assert mopsolver1.multi_design_launch_num == -1
    assert isinstance(mopsolver1.input_file, OptislangPath)
    assert mopsolver1.input_file.type == OptislangPathType.ABSOLUTE_PATH

    mopsolver2 = MopSolverNodeSettings(input2, 1, additional_settings)
    assert isinstance(mopsolver2.input_file, OptislangPath)
    assert mopsolver2.input_file.type == OptislangPathType.ABSOLUTE_PATH

    mopsolver3 = MopSolverNodeSettings(input3, 1, additional_settings)
    assert isinstance(mopsolver3.input_file, OptislangPath)
    assert mopsolver3.input_file.type == OptislangPathType.WORKING_DIR_RELATIVE

    properties_dict = mopsolver1.convert_properties_to_dict()
    assert properties_dict.get("MultiDesignNum") == -1
    assert properties_dict.get("MDBPath", {}).get("path") is not None
    assert properties_dict.get("Property1") == "string"
    assert properties_dict.get("Property4", {}).get("key") == "value"


def test_proxysolver_settings():
    """Test `ProxySolverNodeSettings` class init and properties."""

    callback = lambda x: x**2
    proxysolver = ProxySolverNodeSettings(callback)
    assert isinstance(proxysolver.callback, Callable)
    assert proxysolver.multi_design_launch_num == 1
    assert proxysolver.additional_settings == {}

    additional_settings = {
        "Property1": "string",
        "Property2": ["x", "y"],
        "Property3": 1,
        "Property4": {"key": "value"},
    }

    proxysolver1 = ProxySolverNodeSettings(callback, -1, additional_settings)
    assert proxysolver1.additional_settings.get("Property1") == "string"
    assert proxysolver1.additional_settings.get("Property4", {}).get("key") == "value"
    assert proxysolver1.multi_design_launch_num == -1

    properties_dict = proxysolver1.convert_properties_to_dict()
    assert properties_dict.get("MultiDesignLaunchNum") == -1
    assert properties_dict.get("Property1") == "string"
    assert properties_dict.get("Property4", {}).get("key") == "value"


def test_python_solver_settings():
    """Test `PythonSolverNodeSettings` class init and properties."""
    pythonsolver = PythonSolverNodeSettings()
    assert pythonsolver.input_file is None
    assert pythonsolver.input_code is None
    assert pythonsolver.additional_settings == {}

    input_path1 = "path/to/input/file"
    input_path2 = Path(input_path1)
    input_path3 = WorkingDirRelativePath(head="", tail=input_path1)
    input_code = "X=1"
    additional_settings = {
        "Property1": "string",
        "Property2": ["x", "y"],
        "Property3": 1,
        "Property4": {"key": "value"},
    }

    pythonsolver1 = PythonSolverNodeSettings(input_path1, None, additional_settings)
    assert pythonsolver1.additional_settings.get("Property1") == "string"
    assert pythonsolver1.additional_settings.get("Property4", {}).get("key") == "value"
    assert pythonsolver1.input_code is None
    assert isinstance(pythonsolver1.input_file, OptislangPath)
    assert pythonsolver1.input_file.type == OptislangPathType.ABSOLUTE_PATH

    pythonsolver2 = PythonSolverNodeSettings(input_path2, None, additional_settings)
    assert isinstance(pythonsolver2.input_file, OptislangPath)
    assert pythonsolver2.input_file.type == OptislangPathType.ABSOLUTE_PATH
    assert pythonsolver2.input_code is None

    pythonsolver3 = PythonSolverNodeSettings(input_path3, None, additional_settings)
    assert isinstance(pythonsolver3.input_file, OptislangPath)
    assert pythonsolver3.input_file.type == OptislangPathType.WORKING_DIR_RELATIVE

    pythonsolver4 = PythonSolverNodeSettings(None, input_code, additional_settings)
    assert pythonsolver4.input_file is None
    assert isinstance(pythonsolver4.input_code, str)

    properties_dict = pythonsolver1.convert_properties_to_dict()
    assert properties_dict.get("Path", {}).get("path") is not None
    assert properties_dict.get("Property1") == "string"
    assert properties_dict.get("Property4", {}).get("key") == "value"

    properties_dict1 = pythonsolver4.convert_properties_to_dict()
    assert properties_dict1.get("Source") == input_code


def test_general_parametric_system_settings():
    """Test `GeneralParametricSystemSettings` class init and properties."""
    additional_settings = {
        "Property1": "string",
        "Property2": ["x", "y"],
        "Property3": 1,
        "Property4": {"key": "value"},
    }
    general_parametric_settings = GeneralParametricSystemSettings(additional_settings)
    assert isinstance(general_parametric_settings.additional_settings, dict)
    assert general_parametric_settings.additional_settings.get("Property1") == "string"
    assert (
        general_parametric_settings.additional_settings.get("Property4", {}).get("key") == "value"
    )

    properties_dict = general_parametric_settings.convert_properties_to_dict()
    assert properties_dict == additional_settings


def test_general_algorithm_settings():
    """Test `GeneralAlgorithmSettings` class init and properties."""
    additional_settings = {
        "Property1": "string",
        "Property2": ["x", "y"],
        "Property3": 1,
        "Property4": {"key": "value"},
    }
    general_algo_settings = GeneralAlgorithmSettings(additional_settings)
    assert isinstance(general_algo_settings.additional_settings, dict)
    assert general_algo_settings.additional_settings.get("Property1") == "string"
    assert general_algo_settings.additional_settings.get("Property4", {}).get("key") == "value"

    properties_dict = general_algo_settings.convert_properties_to_dict()
    assert properties_dict == additional_settings


# endregion


# region templates
@pytest.mark.local_osl
def test_parametric_system_integration_template(optislang: Optislang):
    """Test `ParametricSystemIntegrationTemplate` class."""
    python_code = r"""
try:
    Y = X1 + X2 + X3
except:
    Y = 0
"""
    template = ParametricSystemIntegrationTemplate(
        _PARAMETERS,
        nt.Python2,
        "ParSys",
        None,
        "Python",
        PythonSolverNodeSettings(None, python_code),
    )
    instances, executable_blocks = template.create_workflow(
        optislang.application.project.root_system
    )
    assert len(instances) == 1
    assert len(executable_blocks) == 1
    assert isinstance(instances[0], ManagedParametricSystem)
    assert isinstance(instances[0].instance, ParametricSystem)
    assert isinstance(instances[0].solver_node, IntegrationNode)
    assert isinstance(executable_blocks[0], ExecutableBlock)


@pytest.mark.local_osl
def test_general_algorithm_template(optislang: Optislang):
    """Test `GeneralAlgorithmTemplate` class."""
    template = GeneralAlgorithmTemplate(
        _PARAMETERS,
        _CRITERIA,
        _RESPONSES,
        nt.ARSM,
        nt.Python2,
        "ParSys",
        None,
        "Python",
        PythonSolverNodeSettings(None, _PYTHON_SOURCE_CODE),
    )
    instances, executable_blocks = template.create_workflow(
        optislang.application.project.root_system
    )
    assert len(instances) == 1
    assert len(executable_blocks) == 1
    assert isinstance(instances[0], ManagedParametricSystem)
    assert isinstance(instances[0].instance, ParametricSystem)
    assert isinstance(instances[0].solver_node, IntegrationNode)
    assert isinstance(executable_blocks[0], ExecutableBlock)


@pytest.mark.local_osl
def test_optimization_on_mop_template(optislang: Optislang):
    """Test `OptimizationOnMOPTemplate` class."""

    python_code = r"""
try:
    Y = X1 + X2 + X3
except:
    Y = 0
"""
    mop_template = GeneralAlgorithmTemplate(
        parameters=_PARAMETERS,
        criteria=_CRITERIA,
        responses=_RESPONSES,
        algorithm_type=nt.AMOP,
        solver_type=nt.Python2,
        solver_settings=PythonSolverNodeSettings(None, python_code),
    )

    instances, executable_blocks = mop_template.create_workflow(
        optislang.application.project.root_system
    )
    assert len(instances) == 1
    mop_predecessor = instances[0].instance

    template = OptimizationOnMOPTemplate(
        _PARAMETERS,
        _CRITERIA,
        _RESPONSES,
        mop_predecessor,
        validator_solver_settings=ProxySolverNodeSettings(lambda x: x**2),
    )
    instances, executable_blocks = template.create_workflow(
        optislang.application.project.root_system
    )
    assert len(instances) == 5
    assert len(executable_blocks) == 3


# endregion


# region helpers
@pytest.mark.local_osl
def test_create_optislang_project_with_solver_node(tmp_path, tmp_example_project):
    """Test `create_optislang_project_with_solver_node` method."""
    project_path = tmp_path / "test_create_project.opf"
    reference_path = project_path.with_suffix(".opr")
    node_type = nt.Python2
    settings = PythonSolverNodeSettings(input_code=_PYTHON_SOURCE_CODE)
    example_project = tmp_example_project("omdb_files")
    example_wdir = example_project.with_suffix(".opd")

    with Optislang(project_path=example_project) as osl:
        osl.application.project.reset()
        osl.application.project.start()
    create_optislang_project_with_solver_node(
        project_path, node_type, settings, example_wdir, _PARAMETERS
    )
    copied_files = os.listdir(reference_path)
    assert project_path.exists
    assert len(copied_files) > 0


@pytest.mark.local_osl
def test_create_workflow_from_template(tmp_path):
    """Test `create_workflow_from_template` method."""
    template = GeneralAlgorithmTemplate(
        _PARAMETERS,
        _CRITERIA,
        _RESPONSES,
        nt.ARSM,
        nt.Python2,
        "ParSys",
        None,
        "Python",
        PythonSolverNodeSettings(None, _PYTHON_SOURCE_CODE),
    )
    project_path = tmp_path / "test_create_workflow.opf"
    osl = create_workflow_from_template(template, project_path)
    nodes = osl.application.project.root_system.get_nodes()
    assert len(nodes) > 0
    osl.dispose()


# endregion
