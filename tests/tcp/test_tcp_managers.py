import pytest

from ansys.optislang.core import Optislang
from ansys.optislang.core.project_parametric import (
    ComparisonType,
    ConstraintCriterion,
    Criterion,
    DependentParameter,
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

pytestmark = pytest.mark.local_osl


@pytest.fixture()
def optislang(tmp_example_project, scope="function", autouse=False) -> Optislang:
    """Create Optislang class.

    Returns
    -------
    Optislang:
        Connects to the optiSLang application and provides an API to control it.
    """
    osl = Optislang(project_path=tmp_example_project("calculator_with_params"), ini_timeout=60)
    osl.timeout = 20
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
            reference_value=3,
            const=True,
            deterministic_resolution=ParameterResolution.NOMINALDISCRETE,
            range=[[1, 2, 3]],
        ),
        "custom_mixed": MixedParameter(
            name="custom_mixed", reference_value=10, distribution_type=DistributionType.CHI_SQUARE
        ),
        "custom_dependent": DependentParameter(
            name="custom_dependent", operation="default_optimization+custom_optimization"
        ),
        "custom_stochastic": StochasticParameter(name="custom_stochastic", reference_value=12),
    }
    for parameter in parameter_dict.values():
        parameter_manager.add_parameter(parameter=parameter)
    with pytest.raises(NameError):
        parameter_manager.add_parameter(parameter=MixedParameter("custom_mixed"))

    parameters = parameter_manager.get_parameters()
    assert len(parameters) == 8

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
            MixedParameter(name="xxx", reference_value=15, const=False)
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
    assert modified_parameter.reference_value == 10
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
