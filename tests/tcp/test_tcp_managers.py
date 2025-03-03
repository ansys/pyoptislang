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
from ansys.optislang.core.io import File
from ansys.optislang.core.managers import DesignManager
from ansys.optislang.core.nodes import ParametricSystem
from ansys.optislang.core.project_parametric import (
    ComparisonType,
    ConstraintCriterion,
    Criterion,
    DependentParameter,
    Design,
    DistributionType,
    LimitStateCriterion,
    MixedParameter,
    ObjectiveCriterion,
    OptimizationParameter,
    Parameter,
    ParameterResolution,
    ParameterType,
    Response,
    StochasticParameter,
    VariableCriterion,
)

# pytestmark = pytest.mark.local_osl


@pytest.fixture()
def optislang(tmp_example_project, scope="function", autouse=False) -> Optislang:
    """Create Optislang class.

    Returns
    -------
    Optislang:
        Connects to the optiSLang application and provides an API to control it.
    """
    osl = Optislang(project_path=tmp_example_project("calculator_with_params"), ini_timeout=90)
    osl.timeout = 60
    yield osl
    osl.dispose()


# region Criteria
def test_add_criterion(optislang: Optislang):
    """Test ``add_criterion``."""
    criteria_manager = optislang.project.root_system.criteria_manager
    criteria_manager.remove_all_criteria()
    criteria_dict = {
        "default_constraint": ConstraintCriterion(name="default_constraint"),
        "default_objective": ObjectiveCriterion(name="default_objective"),
        "default_limit_state": LimitStateCriterion(name="default_limit_state"),
        "default_variable": VariableCriterion(name="default_variable"),
        "custom_constraint": ConstraintCriterion(
            name="custom_constraint",
            expression="2*10+1",
            criterion=ComparisonType.LESSEQUAL,
            limit_expression="2*20-5",
        ),
        "custom_objective": ObjectiveCriterion(
            name="custom_objective", expression="11+12", criterion=ComparisonType.MAX
        ),
        "custom_limit_state": LimitStateCriterion(
            name="custom_limit_state",
            expression="1e-3+2e-3",
            criterion=ComparisonType.LESSLIMITSTATE,
            limit_expression="2**3+3^2",
        ),
        "custom_variable": VariableCriterion(name="custom_variable", expression=".5+.7"),
        "custom_variable_2": VariableCriterion(
            name="custom_variable_2", expression="default_constraint+default_objective"
        ),
        "custom_limit_state_2": LimitStateCriterion(
            name="custom_limit_state_2",
            expression="default_variable",
            criterion=ComparisonType.GREATERLIMITSTATE,
            limit_expression="custom_variable",
        ),
    }
    for criterion in criteria_dict.values():
        criteria_manager.add_criterion(criterion=criterion)
    criteria = criteria_manager.get_criteria()
    assert len(criteria) == 10

    for criterion in criteria:
        if criteria_dict.get(criterion.name):
            criterion_from_dict: Criterion = criteria_dict[criterion.name]
        else:
            assert False
            break
        assert criterion.name == criterion_from_dict.name
        assert criterion.expression == criterion_from_dict.expression
        assert criterion.criterion == criterion_from_dict.criterion
        if isinstance(criterion, (ConstraintCriterion, LimitStateCriterion)):
            assert criterion.limit_expression == criterion_from_dict.limit_expression
        # TODO: test values after issue with value updated is solved


def test_get_criteria(optislang: Optislang):
    """Test ``get_criteria``."""
    criteria_manager = optislang.project.root_system.criteria_manager
    criteria = criteria_manager.get_criteria()
    assert isinstance(criteria, tuple)
    assert len(criteria) > 0
    assert isinstance(criteria[0], ObjectiveCriterion)


def test_get_criteria_names(optislang: Optislang):
    """Test ``get_criteria_names``."""
    criteria_manager = optislang.project.root_system.criteria_manager
    criteria_names = criteria_manager.get_criteria_names()
    assert isinstance(criteria_names, tuple)
    assert len(criteria_names) > 0
    assert criteria_names[0] == "obj_c"


def test_modify_criterion(optislang: Optislang):
    """Test ``modify_criterion``."""
    criteria_manager = optislang.project.root_system.criteria_manager
    criteria_manager.modify_criterion(
        ObjectiveCriterion(name="obj_c", expression="2*c", criterion=ComparisonType.MAX)
    )
    modified_criterion = criteria_manager.get_criteria()[0]
    assert modified_criterion.expression == "2*c"
    assert modified_criterion.criterion == ComparisonType.MAX

    criteria_manager.modify_criterion(
        ConstraintCriterion(
            name="obj_c",
            expression="c+c",
            criterion=ComparisonType.LESSEQUAL,
            limit_expression="c**2",
        )
    )
    modified_criterion = criteria_manager.get_criteria()[0]
    assert modified_criterion.expression == "c+c"
    assert modified_criterion.criterion == ComparisonType.LESSEQUAL
    assert modified_criterion.limit_expression == "c**2"


def test_modify_criterion_property(optislang: Optislang):
    """Test ``modify_criterion_property``."""
    criteria_manager = optislang.project.root_system.criteria_manager
    criteria_manager.modify_criterion_property(
        criterion_name="obj_c", property_name="type", property_value="lessequal"
    )
    criteria_manager.modify_criterion_property(
        criterion_name="obj_c", property_name="expression", property_value="c+c"
    )
    criteria_manager.modify_criterion_property(
        criterion_name="obj_c", property_name="limit_expression", property_value="c**2"
    )
    modified_criterion = criteria_manager.get_criteria()[0]
    assert modified_criterion.expression == "c+c"
    assert modified_criterion.criterion == ComparisonType.LESSEQUAL
    assert modified_criterion.limit_expression == "c**2"


def test_remove_criterion(optislang: Optislang):
    """Test ``remove_criterion``."""
    criteria_manager = optislang.project.root_system.criteria_manager
    criteria_manager.remove_criterion(criterion_name="obj_c")
    criteria = criteria_manager.get_criteria()
    assert len(criteria) == 0


def test_remove_all_criteria(optislang: Optislang):
    """Test ``remove_all_criteria``."""
    criteria_manager = optislang.project.root_system.criteria_manager
    criteria_manager.remove_all_criteria()
    criteria = criteria_manager.get_criteria()
    assert len(criteria) == 0


# endregion


# region Parameters
def test_add_parameter(optislang: Optislang):
    """Test ``add_parameter``."""
    parameter_manager = optislang.project.root_system.parameter_manager
    parameter_manager.remove_all_parameters()
    parameter_dict = {
        "default_optimization": OptimizationParameter(name="default_optimization"),
        "default_mixed": MixedParameter(name="default_mixed"),
        "default_dependent": DependentParameter(name="default_dependent"),
        "default_stochastic": StochasticParameter(name="default_stochastic"),
        "custom_optimization": OptimizationParameter(
            name="custom_optimization",
            reference_value=3.0,
            const=True,
            deterministic_resolution=ParameterResolution.NOMINALDISCRETE,
            range=[1.0, 2.0, 3.0],
        ),
        "custom_mixed": MixedParameter(
            name="custom_mixed", reference_value=10.0, distribution_type=DistributionType.CHI_SQUARE
        ),
        "custom_dependent": DependentParameter(
            name="custom_dependent", operation="default_optimization+custom_optimization"
        ),
        "custom_stochastic": StochasticParameter(
            name="custom_stochastic",
            reference_value=12.0,
            statistical_moments=[12.0],
            cov=0.5,
        ),
        "custom_stochastic_2": StochasticParameter(
            name="custom_stochastic_2",
            reference_value=12.0,
            statistical_moments=[12.0, 6.0],
        ),
        "custom_stochastic_3": StochasticParameter(
            name="custom_stochastic_3",
            reference_value=12.0,
            distribution_parameters=[12.0, 6.0],
        ),
        "custom_mixed_2": MixedParameter(
            name="custom_mixed_2",
            reference_value=10.0,
            distribution_type=DistributionType.TRIANGULAR,
            distribution_parameters=[6.0, 12.0, 18.0],
            range=(0.0, 20.0),
        ),
    }
    for parameter in parameter_dict.values():
        parameter_manager.add_parameter(parameter=parameter)
    with pytest.raises(NameError):
        parameter_manager.add_parameter(parameter=MixedParameter("custom_mixed"))

    parameters = parameter_manager.get_parameters()
    assert len(parameters) == 11

    for parameter in parameters:
        if parameter_dict.get(parameter.name):
            parameter_from_dict: Parameter = parameter_dict[parameter.name]
        else:
            assert False
            break
        assert parameter.name == parameter_from_dict.name
        assert parameter.reference_value == parameter_from_dict.reference_value
        assert parameter.const == parameter_from_dict.const
        assert parameter.id == parameter_from_dict.id
        if isinstance(parameter, (OptimizationParameter, MixedParameter)):
            assert parameter.reference_value_type == parameter_from_dict.reference_value_type
            assert (
                parameter.deterministic_resolution == parameter_from_dict.deterministic_resolution
            )
            assert parameter.range == parameter_from_dict.range
        if isinstance(parameter, (StochasticParameter, MixedParameter)):
            assert parameter.stochastic_resolution == parameter_from_dict.stochastic_resolution
            assert parameter.distribution_type == parameter_from_dict.distribution_type


def test_get_parameters(optislang: Optislang):
    """Test ``get_parameters``."""
    project = optislang.project
    root_system = project.root_system
    parameter_manager = root_system.parameter_manager
    parameters = parameter_manager.get_parameters()
    assert isinstance(parameters, tuple)
    assert len(parameters) > 0
    for parameter in parameters:
        assert isinstance(parameter, MixedParameter)


def test_get_parameters_names(optislang: Optislang):
    """Test ``get_parameters_names``."""
    project = optislang.project
    root_system = project.root_system
    parameter_manager = root_system.parameter_manager
    parameters_names = parameter_manager.get_parameters_names()
    assert isinstance(parameters_names, tuple)
    assert len(parameters_names) > 0
    assert set(["a", "b"]) == set(parameters_names)


def test_modify_parameter(optislang: Optislang):
    """Test ``modify_parameter``."""
    parameter_manager = optislang.project.root_system.parameter_manager
    parameter_manager.modify_parameter(
        OptimizationParameter(name="a", reference_value=10, const=False)
    )
    with pytest.raises(NameError):
        parameter_manager.modify_parameter(
            MixedParameter(name="xxx", reference_value=15.0, const=False)
        )
    modified_parameter = [
        parameter for parameter in parameter_manager.get_parameters() if parameter.name == "a"
    ][0]

    assert isinstance(modified_parameter, OptimizationParameter)
    assert modified_parameter.reference_value == 10
    assert modified_parameter.const == False
    assert modified_parameter.type == ParameterType.DETERMINISTIC


def test_modify_parameter_property(optislang: Optislang):
    """Test ``modify_parameter_property``."""
    parameter_manager = optislang.project.root_system.parameter_manager
    parameter_manager.modify_parameter_property(
        parameter_name="b", property_name="const", property_value=False
    )
    parameter_manager.modify_parameter_property(
        parameter_name="b", property_name="reference_value", property_value=10
    )
    parameter_manager.modify_parameter_property(
        parameter_name="b", property_name="type", property_value=ParameterType.STOCHASTIC.name
    )
    modified_parameter = [
        parameter for parameter in parameter_manager.get_parameters() if parameter.name == "b"
    ][0]
    assert isinstance(modified_parameter, StochasticParameter)
    assert modified_parameter.type == ParameterType.STOCHASTIC
    assert modified_parameter.reference_value == 10.0
    assert modified_parameter.const == False


def test_remove_parameter(optislang: Optislang):
    """Test ``remove_parameter``."""
    parameter_manager = optislang.project.root_system.parameter_manager
    parameter_manager.remove_parameter(parameter_name="b")
    parameters = parameter_manager.get_parameters()
    assert len(parameters) == 1


def test_remove_all_parameters(optislang: Optislang):
    """Test ``remove_all_parameters``."""
    parameter_manager = optislang.project.root_system.parameter_manager
    parameter_manager.remove_all_parameters()
    parameters = parameter_manager.get_parameters()
    assert len(parameters) == 0


# endregion


# region Responses
def test_get_responses(optislang: Optislang):
    """Test ``get_responses``."""
    project = optislang.project
    root_system = project.root_system
    response_manager = root_system.response_manager
    responses = response_manager.get_responses()
    assert isinstance(responses, tuple)
    assert len(responses) > 0
    for response in responses:
        assert isinstance(response, Response)


def test_get_responses_names(optislang: Optislang):
    """Test ``get_responses_names``."""
    project = optislang.project
    root_system = project.root_system
    response_manager = root_system.response_manager
    responses_names = response_manager.get_responses_names()
    assert isinstance(responses_names, tuple)
    assert len(responses_names) > 0
    assert set(["c", "d"]) == set(responses_names)


# endregion


# region Designs
def test_get_design_s(optislang: Optislang, tmp_example_project):
    """Test ``get_design`` and ``get_designs`` method."""
    with Optislang(project_path=tmp_example_project("omdb_files")) as osl:
        project = osl.project
        root_system = project.root_system
        sensitivity_outer: ParametricSystem = root_system.find_nodes_by_name("Sensitivity")[0]
        sensitivity_inner: ParametricSystem = root_system.find_nodes_by_name(
            "MostInnerSensitivity", 3
        )[0]
        design_manager_outer = sensitivity_outer.design_manager
        design_manager_inner = sensitivity_inner.design_manager
        hids_outer = sensitivity_outer.get_states_ids()
        hids_inner = sensitivity_inner.get_states_ids()

        for design_manager, hids in [
            (design_manager_outer, hids_outer),
            (design_manager_inner, hids_inner),
        ]:
            designs = design_manager.get_designs(hids[0])
            assert len(designs) > 0
            assert isinstance(designs, tuple)
            assert all(isinstance(d, Design) for d in designs)
            __test_design_values(designs, True)

            design = design_manager.get_design(hids[0] + ".1")
            assert isinstance(design, Design)
            filtered_design = design_manager.filter_designs_by(designs, hid=hids[0] + ".1")[0]
            assert (
                design.parameters == filtered_design.parameters
                and design.constraints == filtered_design.constraints
                and design.limit_states == filtered_design.limit_states
                and design.objectives == filtered_design.objectives
                and design.variables == filtered_design.variables
                and design.responses == filtered_design.responses
                and design.feasibility == filtered_design.feasibility
                and design.id == filtered_design.id
                and design.status == filtered_design.status
            )
            # TODO: replace above with below after `pareto_design` is provided by `get_design` query
            # assert design == design_manager.filter_designs_by(designs, hid=hids[0] + ".1")[0]

            sorted_designs = design_manager.sort_designs_by_hid(designs)
            for idx, d in enumerate(sorted_designs[1:], start=1):
                for idx, d in enumerate(sorted_designs[1:], start=1):
                    prev_id_parts = sorted_designs[idx - 1].id.split(".")
                    curr_id_parts = d.id.split(".")
                    for prev_part, curr_part in zip(prev_id_parts, curr_id_parts):
                        assert int(curr_part) >= int(prev_part)

            designs_no_values = design_manager.get_designs(hids[0], include_design_values=False)
            assert len(designs_no_values) > 0
            assert isinstance(designs_no_values, tuple)
            assert all(isinstance(d, Design) for d in designs_no_values)
            __test_design_values(designs_no_values, False)


def test_save_designs_as(tmp_path: Path, tmp_example_project):
    """Test `save_designs_as_json` and `save_designs_as_csv` methods."""
    with Optislang(project_path=tmp_example_project("omdb_files")) as osl:
        project = osl.project
        root_system = project.root_system
        sensitivity_outer: ParametricSystem = root_system.find_nodes_by_name("Sensitivity")[0]
        sensitivity_inner: ParametricSystem = root_system.find_nodes_by_name(
            "MostInnerSensitivity", 3
        )[0]
        design_manager_outer = sensitivity_outer.design_manager
        hids_outer = sensitivity_outer.get_states_ids()
        design_manager_inner = sensitivity_inner.design_manager
        hids_inner = sensitivity_inner.get_states_ids()
        __test_save_designs_as_csv(tmp_path, "outerSensi_csv", design_manager_outer, hids_outer)
        __test_save_designs_as_json(tmp_path, "outerSensi_json", design_manager_outer, hids_outer)
        __test_save_designs_as_csv(tmp_path, "innerSensi_csv", design_manager_inner, hids_inner)
        __test_save_designs_as_json(tmp_path, "innerSensi_json", design_manager_inner, hids_inner)


def __test_design_values(designs, values):
    for design in designs:
        for attribute in ["parameters", "responses", "constraints", "limit_states", "objectives"]:
            for item in getattr(design, attribute):
                assert (item.value is not None) if values else (item.value is None)


def __test_save_designs_as_csv(
    tmp_path: Path, filename: str, design_manager: DesignManager, hids: tuple
):
    """Test `save_designs_as_csv` method."""
    csv_file_path = tmp_path / (filename + ".csv")
    csv_file = design_manager.save_designs_as_csv(hid=hids[0], file_path=csv_file_path)
    assert isinstance(csv_file, File)
    assert csv_file.exists


def __test_save_designs_as_json(
    tmp_path: Path, filename: str, design_manager: DesignManager, hids: tuple
):
    """Test `save_designs_as_json` method."""
    json_file_path = tmp_path / (filename + ".json")
    json_file = design_manager.save_designs_as_json(hids[0], json_file_path)
    assert isinstance(json_file, File)
    assert json_file.exists


# endregion
