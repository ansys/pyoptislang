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

import time
from typing import Callable

import pytest

from ansys.optislang.core import Optislang
import ansys.optislang.core.node_types as nt
from ansys.optislang.core.nodes import Node, ParametricSystem
from ansys.optislang.core.project_parametric import (
    ComparisonType,
    ConstraintCriterion,
    ObjectiveCriterion,
    OptimizationParameter,
    Response,
)
from ansys.optislang.core.tcp.nodes import (
    ExecutionOption,
)
from ansys.optislang.parametric.design_study import (
    ExecutableBlock,
    ManagedInstance,
    ManagedParametricSystem,
    OMDBFilesProvider,
    OMDBFilesSpecificationEnum,
    ParametricDesignStudy,
    ParametricDesignStudyManager,
    ProxySolverManagedParametricSystem,
)
from ansys.optislang.parametric.design_study_templates import (
    GeneralAlgorithmTemplate,
    ProxySolverNodeSettings,
)

pytestmark = pytest.mark.local_osl


# region OMDB files


def test_omdb_files_provider(tmp_example_project):
    """Test `OMDBFilesProvider` class."""
    project_path = tmp_example_project("omdb_files")
    manager = ParametricDesignStudyManager(project_path=project_path)

    provider_from_manager = OMDBFilesProvider(manager)
    assert (
        provider_from_manager.omdb_files_specification
        == OMDBFilesSpecificationEnum.DESIGN_STUDY_MANAGER
    )
    assert len(provider_from_manager.get_omdb_files()) == 0

    project = manager.optislang.application.project
    project.reset()
    project.start()
    manager.save()

    wdir = project.get_working_dir()
    provider_from_wdir = OMDBFilesProvider(wdir)
    files = provider_from_wdir.get_omdb_files()
    assert provider_from_wdir.omdb_files_specification == OMDBFilesSpecificationEnum.OMDB_FOLDER
    assert len(files) > 0
    print(files)

    paths = [
        wdir / "Database1.omdb",
        wdir / "dir2" / "Database2.omdb",
        wdir / "dir2" / "subdir" / "Database3.omdb",
    ]
    provider_from_paths = OMDBFilesProvider(paths)
    files = provider_from_paths.get_omdb_files()
    assert provider_from_paths.omdb_files_specification == OMDBFilesSpecificationEnum.OMDB_FILES
    assert len(files) == 3


# endregion


# region managed instances
def test_managed_instances(tmp_example_project):
    """Test `ManagedInstance` classes."""
    project_path = tmp_example_project("omdb_files")
    with Optislang(project_path=project_path) as osl:
        sensitivity: ParametricSystem = osl.application.project.root_system.find_nodes_by_name(
            "Sensitivity"
        )[0]
        solver = sensitivity.get_nodes()[0]

        managed_instance = ManagedInstance(solver)
        assert isinstance(managed_instance.instance, Node)

        managed_parametric_system = ManagedParametricSystem(sensitivity, solver)
        assert isinstance(managed_parametric_system.instance, ParametricSystem)
        assert isinstance(managed_parametric_system.solver_node, Node)

        dummy_callback = lambda x: x**2
        managed_proxy_parametric_system = ProxySolverManagedParametricSystem(
            sensitivity, solver, dummy_callback
        )
        assert isinstance(managed_proxy_parametric_system.instance, ParametricSystem)
        assert isinstance(managed_proxy_parametric_system.solver_node, Node)
        assert isinstance(managed_proxy_parametric_system.callback, Callable)


# endregion


# region executable block
def test_executable_block(tmp_example_project):
    """Test `ExecutableBlock` class."""
    project_path = tmp_example_project("omdb_files")
    with Optislang(project_path=project_path) as osl:
        sensitivity: ParametricSystem = osl.application.project.root_system.find_nodes_by_name(
            "Sensitivity"
        )[0]
        solver = sensitivity.get_nodes()[0]
        managed_instance = ManagedParametricSystem(sensitivity, solver)
        block = ExecutableBlock(
            [
                (
                    managed_instance,
                    ExecutionOption.STARTING_POINT
                    | ExecutionOption.END_POINT
                    | ExecutionOption.ACTIVE,
                )
            ]
        )
        assert len(block.instances) == 1
        assert isinstance(block.instances[0], ManagedParametricSystem)
        assert isinstance(block.instances_with_execution_options[0][0], ManagedParametricSystem)
        assert isinstance(block.instances_with_execution_options[0][1], ExecutionOption)

        from_empty = ExecutableBlock()
        from_empty.add_instance(
            managed_instance,
            ExecutionOption.STARTING_POINT | ExecutionOption.END_POINT | ExecutionOption.ACTIVE,
        )
        assert len(from_empty.instances) == 1
        assert isinstance(from_empty.instances[0], ManagedParametricSystem)
        assert isinstance(
            from_empty.instances_with_execution_options[0][0], ManagedParametricSystem
        )
        assert isinstance(from_empty.instances_with_execution_options[0][1], ExecutionOption)

        from_empty.remove_instance_by_uid(sensitivity.uid)
        assert len(from_empty.instances) == 0


# endregion

# region parametric design study


def test_parametric_design_study(tmp_example_project):
    """Test `ParametricDesignStudy` class init and properties."""
    project_path = tmp_example_project("omdb_files")
    with Optislang(project_path=project_path) as osl:
        sensitivity: ParametricSystem = osl.application.project.root_system.find_nodes_by_name(
            "Sensitivity"
        )[0]
        solver = sensitivity.get_nodes()[0]
        managed_instance1 = ManagedParametricSystem(sensitivity, solver)

        outer_sensitivity = osl.application.project.root_system.find_nodes_by_name(
            "OuterSensitivity"
        )[0]
        outer_solver = sensitivity.get_nodes()[0]
        managed_instance2 = ManagedParametricSystem(outer_sensitivity, outer_solver)

        executable_blocks = [
            ExecutableBlock(
                [
                    (
                        managed_instance1,
                        ExecutionOption.STARTING_POINT
                        | ExecutionOption.END_POINT
                        | ExecutionOption.ACTIVE,
                    ),
                ]
            ),
            ExecutableBlock(
                [
                    (
                        managed_instance2,
                        ExecutionOption.STARTING_POINT
                        | ExecutionOption.END_POINT
                        | ExecutionOption.ACTIVE,
                    ),
                ]
            ),
        ]

        study = ParametricDesignStudy(
            osl, [managed_instance1, managed_instance2], executable_blocks
        )

        assert len(study.managed_instances) == 2
        assert isinstance(study.managed_instances[0], ManagedInstance)
        assert len(study.execution_order) == 2
        assert isinstance(study.execution_order[0], ExecutableBlock)
        assert not study.is_complete
        assert study.get_last_parametric_system().uid == outer_sensitivity.uid
        assert not study.contains_proxy_solver()

        study.reset()
        assert study.get_status() != "FINISHED"
        study.execute()

        assert study.is_complete
        assert study.get_status() == "FINISHED"
        assert len(study.get_result_designs()) > 0

        study.delete()
        assert len(osl.application.project.root_system.get_nodes()) == 0

        # TODO: start_in_thread


def test_parametric_desings_study_thread_exec(tmp_path):
    """Test `ParametricDesignStudy` class execution in non-blocking mode."""
    project = tmp_path / "Thread_exec.opf"

    def calculator(designs):
        results_designs = []
        for design in designs:
            for param in design["parameters"]:
                if param["name"] == "param1":
                    x1 = param["value"]
                elif param["name"] == "param2":
                    x2 = param["value"]
                elif param["name"] == "param3":
                    x3 = param["value"]
            res1, res2 = calculator_function(x1, x2, x3)
            results_designs.append(
                {
                    "hid": design["hid"],
                    "responses": [
                        {"name": "response1", "value": res1},
                        {"name": "response2", "value": res2},
                    ],
                }
            )
        return results_designs

    def calculator_function(x1, x2, x3):
        response1 = x1**2 + x2**2 + x3**2
        response2 = x1 + x2 + x3
        return response1, response2

    parameters = [
        OptimizationParameter("param1", 0.0),
        OptimizationParameter("param2", 0.0),
        OptimizationParameter("param3", 0.0),
    ]

    responses = [
        Response("response1", 0.0),
        Response("response2", 0.0),
    ]

    criteria = [
        ObjectiveCriterion(name="obj", expression="response1"),
        ConstraintCriterion(
            name="constr",
            expression="response2",
            criterion=ComparisonType.GREATEREQUAL,
            limit_expression="response1",
        ),
    ]

    proxy_solver_settings = ProxySolverNodeSettings(calculator, 10)

    template = GeneralAlgorithmTemplate(
        parameters,
        criteria,
        responses,
        nt.Sensitivity,
        nt.ProxySolver,
        solver_settings=proxy_solver_settings,
    )
    with Optislang(project_path=project) as osl:
        instances, blocks = template.create_workflow(osl.application.project.root_system)
        study = ParametricDesignStudy(osl, instances, blocks)
        study.start_in_thread()
        while True:
            if study.get_status() not in {"FINISHED", "STOPPED"}:
                break
        while True:
            if study.get_status() in {"FINISHED", "STOPPED"}:
                break
            designs = study.get_designs()
            if len(designs):
                results = calculator(designs)
                study.set_designs(results)
            else:
                time.sleep(0.5)
        osl.application.save()
        assert len(study.get_result_designs()) > 0


def test_paramatric_design_study_auto_detect_executable_blocks(tmp_example_project):
    """Test `ParametricDesignStudy` class auto-detection of executable-blocks."""
    project_path = tmp_example_project("omdb_files")
    with Optislang(project_path=project_path) as osl:
        sensitivity: ParametricSystem = osl.application.project.root_system.find_nodes_by_name(
            "Sensitivity"
        )[0]
        solver = sensitivity.get_nodes()[0]
        managed_instance1 = ManagedParametricSystem(sensitivity, solver)

        outer_sensitivity = osl.application.project.root_system.find_nodes_by_name(
            "OuterSensitivity"
        )[0]
        outer_solver = sensitivity.get_nodes()[0]
        managed_instance2 = ManagedParametricSystem(outer_sensitivity, outer_solver)

        study = ParametricDesignStudy(osl, [managed_instance1, managed_instance2])

        assert len(study.managed_instances) == 2
        assert isinstance(study.managed_instances[0], ManagedInstance)
        assert len(study.execution_order) == 2
        assert isinstance(study.execution_order[0], ExecutableBlock)
        assert not study.is_complete
        assert study.get_last_parametric_system().uid == outer_sensitivity.uid
        assert not study.contains_proxy_solver()

        study.reset()
        assert study.get_status() != "FINISHED"
        study.execute()

        assert study.is_complete
        assert study.get_status() == "FINISHED"
        assert len(study.get_result_designs()) > 0


# endregion


# region parametric study manager


def test_parametric_design_study_manager_initialized_osl(tmp_example_project):
    """Test `ParametricDesignStudyManaged` class initialization with provided optiSLang instance."""
    project_path = tmp_example_project("omdb_files")
    with Optislang(project_path=project_path) as osl:
        sensitivity: ParametricSystem = osl.application.project.root_system.find_nodes_by_name(
            "Sensitivity"
        )[0]
        solver = sensitivity.get_nodes()[0]
        managed_instance1 = ManagedParametricSystem(sensitivity, solver)

        outer_sensitivity = osl.application.project.root_system.find_nodes_by_name(
            "OuterSensitivity"
        )[0]
        outer_solver = sensitivity.get_nodes()[0]
        managed_instance2 = ManagedParametricSystem(outer_sensitivity, outer_solver)

        manager = ParametricDesignStudyManager(osl)

        study = ParametricDesignStudy(
            osl,
            [managed_instance1, managed_instance2],
        )

        manager.append_design_study(study)

        assert isinstance(manager.optislang, Optislang)
        assert len(manager.design_studies) == 1
        assert isinstance(manager.design_studies[0], ParametricDesignStudy)

        manager.reset()

        unfinished_studies = manager.get_unfinished_design_studies()
        assert len(unfinished_studies) == 1
        finished_studies = manager.get_finished_design_studies()
        assert len(finished_studies) == 0

        unfinished_studies[0].execute()

        unfinished_studies = manager.get_unfinished_design_studies()
        assert len(unfinished_studies) == 0
        finished_studies = manager.get_finished_design_studies()
        assert len(finished_studies) == 1

        manager.clear_design_studies(True)
        assert len(osl.application.project.root_system.get_nodes()) == 0


def test_parametric_design_study_manager_initialize_osl(tmp_path):
    """Test `ParametricDesignStudyManaged` class init without provided optiSLang instance."""

    def calculator(designs):
        results_designs = []
        for design in designs:
            for param in design["parameters"]:
                if param["name"] == "param1":
                    x1 = param["value"]
                elif param["name"] == "param2":
                    x2 = param["value"]
                elif param["name"] == "param3":
                    x3 = param["value"]
            res1, res2 = calculator_function(x1, x2, x3)
            results_designs.append(
                {
                    "hid": design["hid"],
                    "responses": [
                        {"name": "response1", "value": res1},
                        {"name": "response2", "value": res2},
                    ],
                }
            )
        return results_designs

    def calculator_function(x1, x2, x3):
        response1 = x1**2 + x2**2 + x3**2
        response2 = x1 + x2 + x3
        return response1, response2

    parameters = [
        OptimizationParameter("param1", 0.0),
        OptimizationParameter("param2", 0.0),
        OptimizationParameter("param3", 0.0),
    ]

    responses = [
        Response("response1", 0.0),
        Response("response2", 0.0),
    ]

    criteria = [
        ObjectiveCriterion(name="obj", expression="response1"),
        ConstraintCriterion(
            name="constr",
            expression="response2",
            criterion=ComparisonType.GREATEREQUAL,
            limit_expression="response1",
        ),
    ]

    proxy_solver_settings = ProxySolverNodeSettings(
        calculator, 10, {"ForwardHPCLicenseContextEnvironment": True}
    )

    template = GeneralAlgorithmTemplate(
        parameters,
        criteria,
        responses,
        nt.Sensitivity,
        nt.ProxySolver,
        solver_settings=proxy_solver_settings,
    )
    project_path = tmp_path / "test_manager.opf"

    manager = ParametricDesignStudyManager()
    manager.save_as(project_path)
    manager.create_design_study(template)
    assert len(manager.design_studies) == 1
    manager.save()

    manager.design_studies[0].execute()
    manager.save()
    assert len(manager.get_finished_design_studies()) == 1


# endregion
