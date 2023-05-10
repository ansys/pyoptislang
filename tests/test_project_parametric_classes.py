from __future__ import annotations

import copy
from typing import TYPE_CHECKING, Any

import pytest

from ansys.optislang.core.project_parametric import (
    ComparisonType,
    ConstraintCriterion,
    Criterion,
    CriterionType,
    CriterionValueType,
    DependentParameter,
    Design,
    DesignStatus,
    DesignVariable,
    DistributionType,
    LimitStateCriterion,
    MixedParameter,
    ObjectiveCriterion,
    OptimizationParameter,
    Parameter,
    ParameterResolution,
    ParameterType,
    ParameterValueType,
    Response,
    ResponseValueType,
    StochasticParameter,
    VariableCriterion,
)

if TYPE_CHECKING:
    from enum import Enum

DEPENDENT_PARAMETER = DependentParameter(
    name="dependent",
    id="aaba5b78-4b8c-4cc3-a308-4e122e2af665",
    operation="0",
    reference_value=0,
)
DEPENDENT_PARAMETER_DICT = {
    "active": True,
    "const": False,
    "dependency_expression": "0",
    "id": "aaba5b78-4b8c-4cc3-a308-4e122e2af665",
    "modifiable": False,
    "name": "dependent",
    "reference_value": 0.0,
    "removable": True,
    "type": {"value": "dependent"},
    "unit": "",
}
OPTIMIZATION_PARAMETER = OptimizationParameter(
    name="optimization", id="c06ea75b-7c19-4905-b727-a0f89c540c4a"
)
OPTIMIZATION_PARAMETER_DICT = {
    "active": True,
    "const": False,
    "deterministic_property": {
        "domain_type": {"value": "real"},
        "kind": {"value": "continuous"},
        "lower_bound": -1.0,
        "upper_bound": 1.0,
    },
    "id": "c06ea75b-7c19-4905-b727-a0f89c540c4a",
    "modifiable": False,
    "name": "optimization",
    "reference_value": 0.0,
    "removable": True,
    "type": {"value": "deterministic"},
    "unit": "",
}
STOCHASTIC_PARAMETER = StochasticParameter(
    name="stochastic", id="9dbcac71-5538-485c-9e65-39255903ea78"
)
STOCHASTIC_PARAMETER_DICT = {
    "active": True,
    "const": False,
    "id": "9dbcac71-5538-485c-9e65-39255903ea78",
    "modifiable": False,
    "name": "stochastic",
    "reference_value": 0.0,
    "removable": True,
    "stochastic_property": {
        "kind": {"value": "marginaldistribution"},
        "statistical_moments": [0.0, 1.0],
        "type": {"value": "normal"},
    },
    "type": {"value": "stochastic"},
    "unit": "",
}
MIXED_PARAMETER = MixedParameter(name="mixed", id="ddc173ae-9784-4387-ae66-21fff6e199e5")
MIXED_PARAMETER_DICT = {
    "active": True,
    "const": False,
    "deterministic_property": {
        "domain_type": {"value": "real"},
        "kind": {"value": "continuous"},
        "lower_bound": -1.0,
        "upper_bound": 1.0,
    },
    "id": "ddc173ae-9784-4387-ae66-21fff6e199e5",
    "modifiable": False,
    "name": "mixed",
    "reference_value": 0.0,
    "removable": True,
    "stochastic_property": {
        "kind": {"value": "marginaldistribution"},
        "statistical_moments": [0.0, 1.0],
        "type": {"value": "normal"},
    },
    "type": {"value": "mixed"},
    "unit": "",
}
CONSTRAINT_CRITERION = ConstraintCriterion(
    name="constr",
    expression="0",
    criterion=ComparisonType.LESSEQUAL,
    limit_expression_value=0,
    value=0,
)
CONSTRAINT_CRITERION_DICT = {
    "First": "constr",
    "Second": {
        "lhs": "0",
        "lhs_value": {
            "kind": {
                "enum": ["uninitialized", "bool", "scalar", "vector", "matrix", "signal", "xydata"],
                "value": "scalar",
            },
            "scalar": {"imag": 0.0, "real": 0.0},
        },
        "need_eval": False,
        "rhs": "0",
        "rhs_value": {
            "kind": {
                "enum": ["uninitialized", "bool", "scalar", "vector", "matrix", "signal", "xydata"],
                "value": "scalar",
            },
            "scalar": {"imag": 0.0, "real": 0.0},
        },
        "type": {
            "enum": [
                "ignore",
                "min",
                "max",
                "lessequal",
                "equal",
                "greaterequal",
                "lesslimitstate",
                "greaterlimitstate",
            ],
            "value": "lessequal",
        },
        "value": {"kind": {"enum": [...], "value": "scalar"}, "scalar": {"imag": 0.0, "real": 0.0}},
    },
}
OBJECTIVE_CRITERION = ObjectiveCriterion(
    name="obj", expression="0", criterion=ComparisonType.MIN, value=0
)
OBJECTIVE_CRITERION_DICT = {
    "First": "obj",
    "Second": {
        "lhs": "",
        "lhs_value": None,
        "need_eval": False,
        "rhs": "0",
        "rhs_value": {
            "kind": {
                "enum": ["uninitialized", "bool", "scalar", "vector", "matrix", "signal", "xydata"],
                "value": "scalar",
            },
            "scalar": {"imag": 0.0, "real": 0.0},
        },
        "type": {
            "enum": [
                "ignore",
                "min",
                "max",
                "lessequal",
                "equal",
                "greaterequal",
                "lesslimitstate",
                "greaterlimitstate",
            ],
            "value": "min",
        },
        "value": {
            "kind": {
                "enum": ["uninitialized", "bool", "scalar", "vector", "matrix", "signal", "xydata"],
                "value": "scalar",
            },
            "scalar": {"imag": 0.0, "real": 0.0},
        },
    },
}
LIMIT_STATE_CRITERION = LimitStateCriterion(
    name="lim_st",
    expression="0",
    criterion=ComparisonType.LESSLIMITSTATE,
    limit_expression_value=0,
    value=0,
)
LIMIT_STATE_CRITERION_DICT = {
    "First": "lim_st",
    "Second": {
        "lhs": "0",
        "lhs_value": {
            "kind": {
                "enum": ["uninitialized", "bool", "scalar", "vector", "matrix", "signal", "xydata"],
                "value": "scalar",
            },
            "scalar": {"imag": 0.0, "real": 0.0},
        },
        "need_eval": False,
        "rhs": "0",
        "rhs_value": {
            "kind": {
                "enum": ["uninitialized", "bool", "scalar", "vector", "matrix", "signal", "xydata"],
                "value": "scalar",
            },
            "scalar": {"imag": 0.0, "real": 0.0},
        },
        "type": {
            "enum": [
                "ignore",
                "min",
                "max",
                "lessequal",
                "equal",
                "greaterequal",
                "lesslimitstate",
                "greaterlimitstate",
            ],
            "value": "lesslimitstate",
        },
        "value": {
            "kind": {
                "enum": ["uninitialized", "bool", "scalar", "vector", "matrix", "signal", "xydata"],
                "value": "scalar",
            },
            "scalar": {"imag": 0.0, "real": 0.0},
        },
    },
}
VARIABLE_CRITERION = VariableCriterion(name="var", expression="0", value=0)
VARIABLE_CRITERION_DICT = {
    "First": "var",
    "Second": {
        "lhs": "",
        "lhs_value": None,
        "need_eval": False,
        "rhs": "0",
        "rhs_value": {
            "kind": {
                "enum": ["uninitialized", "bool", "scalar", "vector", "matrix", "signal", "xydata"],
                "value": "scalar",
            },
            "scalar": {"imag": 0.0, "real": 0.0},
        },
        "type": {
            "enum": [
                "ignore",
                "min",
                "max",
                "lessequal",
                "equal",
                "greaterequal",
                "lesslimitstate",
                "greaterlimitstate",
            ],
            "value": "ignore",
        },
        "value": {
            "kind": {
                "enum": {
                    "enum": [
                        "uninitialized",
                        "bool",
                        "scalar",
                        "vector",
                        "matrix",
                        "signal",
                        "xydata",
                    ],
                    "value": "scalar",
                },
                "value": "scalar",
            },
            "scalar": {"imag": 0.0, "real": 0.0},
        },
    },
}
RESPONSE = Response(name="variable_1", value=0)
RESPONSE_DICT = {"variable_1": 0}


# TEST ENUMERATION METHODS:
def enumeration_test_method(enumeration_class: Enum, enumeration_name: str):
    """Test instance creation, method `from_str` and spelling."""
    mixed_name = ""
    for index, char in enumerate(enumeration_name):
        if index % 2 == 1:
            mixed_name += char.lower()
        else:
            mixed_name += char
    try:
        enumeration_from_str = enumeration_class.from_str(string=mixed_name)
    except:
        assert False
    assert isinstance(enumeration_from_str, enumeration_class)
    assert isinstance(enumeration_from_str.name, str)
    assert enumeration_from_str.name == enumeration_name


def from_str_invalid_inputs_method(
    enumeration_class: Enum, invalid_value: str, invalid_value_type: float
):
    """Test passing incorrect inputs to enuration classes `from_str` method."""
    with pytest.raises(TypeError):
        enumeration_class.from_str(invalid_value_type)

    with pytest.raises(ValueError):
        enumeration_class.from_str(invalid_value)


@pytest.mark.parametrize(
    "criterion_type, name",
    [
        (CriterionType, "CONSTRAINT"),
        (CriterionType, "LIMIT_STATE"),
        (CriterionType, "OBJECTIVE"),
        (CriterionType, "VARIABLE"),
    ],
)
def test_criterion_type(criterion_type: CriterionType, name: str):
    """Test `CriterionType`."""
    enumeration_test_method(enumeration_class=criterion_type, enumeration_name=name)


@pytest.mark.parametrize(
    "comparison_type, name",
    [
        (ComparisonType, "EQUAL"),
        (ComparisonType, "GREATEREQUAL"),
        (ComparisonType, "GREATERLIMITSTATE"),
        (ComparisonType, "IGNORE"),
        (ComparisonType, "LESSEQUAL"),
        (ComparisonType, "LESSLIMITSTATE"),
        (ComparisonType, "MAX"),
        (ComparisonType, "MIN"),
    ],
)
def test_comparison_type(comparison_type: ComparisonType, name: str):
    """Test `CriterionType`."""
    enumeration_test_method(enumeration_class=comparison_type, enumeration_name=name)


@pytest.mark.parametrize(
    "criterion_value_type, name",
    [
        (CriterionValueType, "BOOL"),
        (CriterionValueType, "MATRIX"),
        (CriterionValueType, "SCALAR"),
        (CriterionValueType, "SIGNAL"),
        (CriterionValueType, "UNINITIALIZED"),
        (CriterionValueType, "VECTOR"),
        (CriterionValueType, "XYDATA"),
    ],
)
def test_criterion_value_type(criterion_value_type: CriterionValueType, name: str):
    """Test `CriterionValueType`."""
    enumeration_test_method(enumeration_class=criterion_value_type, enumeration_name=name)


@pytest.mark.parametrize(
    "design_status, name",
    [
        (DesignStatus, "IDLE"),
        (DesignStatus, "PENDING"),
        (DesignStatus, "SUCCEEDED"),
        (DesignStatus, "FAILED"),
    ],
)
def test_design_status(design_status: DesignStatus, name: str):
    """Test `DesignStatus`."""
    enumeration_test_method(enumeration_class=design_status, enumeration_name=name)


@pytest.mark.parametrize(
    "parameter_type, name",
    [
        (ParameterType, "DEPENDENT"),
        (ParameterType, "DETERMINISTIC"),
        (ParameterType, "MIXED"),
        (ParameterType, "STOCHASTIC"),
    ],
)
def test_parameter_type(parameter_type: ParameterType, name: str):
    """Test `ParameterType`."""
    enumeration_test_method(enumeration_class=parameter_type, enumeration_name=name)


@pytest.mark.parametrize(
    "parameter_resolution, name",
    [
        (ParameterResolution, "CONTINUOUS"),
        (ParameterResolution, "ORDINALDISCRETE_VALUE"),
        (ParameterResolution, "ORDINALDISCRETE_INDEX"),
        (ParameterResolution, "NOMINALDISCRETE"),
        (ParameterResolution, "DETERMINISTIC"),
        (ParameterResolution, "MARGINALDISTRIBUTION"),
        (ParameterResolution, "EMPIRICAL_CONTINUOUS"),
        (ParameterResolution, "EMPIRICAL_DISCRETE"),
        (ParameterResolution, "EMPIRICAL_CONTINUOUS"),
    ],
)
def test_parameter_resolution(parameter_resolution: ParameterResolution, name: str):
    """Test `ParameterResolution`."""
    enumeration_test_method(enumeration_class=parameter_resolution, enumeration_name=name)


@pytest.mark.parametrize(
    "parameter_value_type, name",
    [
        (ParameterValueType, "UNINITIALIZED"),
        (ParameterValueType, "BOOL"),
        (ParameterValueType, "REAL"),
        (ParameterValueType, "INTEGER"),
        (ParameterValueType, "STRING"),
        (ParameterValueType, "VARIANT"),
    ],
)
def test_parameter_value_type(parameter_value_type: ParameterValueType, name: str):
    """Test `ParameterValueType`."""
    enumeration_test_method(enumeration_class=parameter_value_type, enumeration_name=name)


@pytest.mark.parametrize(
    "response_value_type, name",
    [
        (ResponseValueType, "BOOL"),
        (ResponseValueType, "SCALAR"),
        (ResponseValueType, "SIGNAL"),
        (ResponseValueType, "UNINITIALIZED"),
        (ResponseValueType, "VECTOR"),
        (ResponseValueType, "XYDATA"),
    ],
)
def test_response_value_type(response_value_type: ResponseValueType, name: str):
    """Test `ResponseValueType`."""
    enumeration_test_method(enumeration_class=response_value_type, enumeration_name=name)


@pytest.mark.parametrize(
    "distribution_type, name",
    [
        (DistributionType, "EXTERNALCOHERENCE"),
        (DistributionType, "UNTYPED"),
        (DistributionType, "EXTERNAL"),
        (DistributionType, "UNIFORM"),
        (DistributionType, "NORMAL"),
        (DistributionType, "TRUNCATEDNORMAL"),
        (DistributionType, "LOGNORMAL"),
        (DistributionType, "EXPONENTIAL"),
        (DistributionType, "RAYLEIGH"),
        (DistributionType, "SMALL_I"),
        (DistributionType, "LARGE_I"),
        (DistributionType, "SMALL_II"),
        (DistributionType, "LARGE_II"),
        (DistributionType, "SMALL_III"),
        (DistributionType, "LARGE_III"),
        (DistributionType, "TRIANGULAR"),
        (DistributionType, "BETA"),
        (DistributionType, "CHI_SQUARE"),
        (DistributionType, "ERLANG"),
        (DistributionType, "FISHER_F"),
        (DistributionType, "GAMMA"),
        (DistributionType, "PARETO"),
        (DistributionType, "WEIBULL"),
        (DistributionType, "EXTREME_VALUE"),
        (DistributionType, "STUDENTS_F"),
        (DistributionType, "INVERSE_NORMAL"),
        (DistributionType, "LOG_GAMMA"),
        (DistributionType, "LOG_NORMAL"),
        (DistributionType, "LORENTZ"),
        (DistributionType, "FISHER_TIPPETT"),
        (DistributionType, "GUMBEL"),
        (DistributionType, "FISHER_Z"),
        (DistributionType, "LAPLACE"),
        (DistributionType, "LEVY"),
        (DistributionType, "LOGISTIC"),
        (DistributionType, "ROSSI"),
        (DistributionType, "FRECHET"),
        (DistributionType, "MAX_TYPE"),
        (DistributionType, "POLYMAP"),
        (DistributionType, "KERNEL"),
        (DistributionType, "BERNOULLI"),
        (DistributionType, "LOG_UNIFORM"),
        (DistributionType, "DISCRETE"),
        (DistributionType, "MULTIUNIFORM"),
        (DistributionType, "LAMBDA"),
        (DistributionType, "POISSON"),
    ],
)
def test_distribution_type(distribution_type: DistributionType, name: str):
    """Test `DistributionType`."""
    enumeration_test_method(enumeration_class=distribution_type, enumeration_name=name)


@pytest.mark.parametrize(
    "enumeration_class, invalid_value, invalid_value_type",
    [
        (CriterionType, "invalid", 1),
        (ComparisonType, "invalid", 1),
        (CriterionValueType, "invalid", 1),
        (DesignStatus, "invalid", 1),
        (ParameterType, "invalid", 1),
        (ParameterResolution, "invalid", 1),
        (ParameterValueType, "invalid", 1),
        (ResponseValueType, "invalid", 1),
        (DistributionType, "invalid", 1),
    ],
)
def test_invalid_inputs(enumeration_class: Enum, invalid_value: str, invalid_value_type: Any):
    from_str_invalid_inputs_method(
        enumeration_class=enumeration_class,
        invalid_value=invalid_value,
        invalid_value_type=invalid_value_type,
    )


# TEST PARAMETERS:
def test_design_variable():
    """Test `DesignVariable`."""
    design_variable = DesignVariable(name="par1", value=12)
    assert isinstance(design_variable, DesignVariable)
    assert isinstance(design_variable.name, str)
    assert isinstance(design_variable.value, (int, float))

    design_variable_eq = DesignVariable(name="par1", value=12.0)
    assert isinstance(design_variable, DesignVariable)
    assert isinstance(design_variable.name, str)
    assert isinstance(design_variable.value, (int, float))

    design_variable_neq = DesignVariable(name="par2", value=12)
    assert design_variable == design_variable_eq
    assert not design_variable == design_variable_neq


def test_parameter():
    """Test `Parameter`."""
    parameter = Parameter(
        name="par", reference_value=13.0, id="xxx-12-58", const=True, type_=ParameterType.MIXED
    )
    assert isinstance(parameter, Parameter)
    assert isinstance(parameter.name, str)
    assert isinstance(parameter.reference_value, (int, float))
    assert isinstance(parameter.id, str)
    assert isinstance(parameter.const, bool)
    assert isinstance(parameter.type, ParameterType)

    parameter.name = "par1"
    assert parameter.name == "par1"
    parameter.reference_value = 12
    assert parameter.reference_value == 12
    parameter.id = "xxx-12-55"
    assert parameter.id == "xxx-12-55"
    parameter.const = False
    assert parameter.const == False

    with pytest.raises(AttributeError):
        parameter.type = ParameterType.DEPENDENT
    with pytest.raises(TypeError):
        parameter.name = 10
    with pytest.raises(TypeError):
        parameter.reference_value = ["10"]
    with pytest.raises(TypeError):
        parameter.id = 12
    with pytest.raises(TypeError):
        parameter.const = "YES"

    parameter_eq = Parameter(
        name="par1", reference_value=12.0, id="xxx-12-55", const=False, type_=ParameterType.MIXED
    )
    parameter_neq = Parameter(
        name="par1", reference_value=12.0, id="xxx-12-56", const=False, type_=ParameterType.MIXED
    )
    parameter_copy = copy.deepcopy(parameter)
    assert parameter == parameter_eq
    assert parameter == parameter_copy
    assert not parameter == parameter_neq

    dependent_parameter_from_dict = Parameter.from_dict(DEPENDENT_PARAMETER_DICT)
    assert isinstance(dependent_parameter_from_dict, DependentParameter)
    optimization_parameter_from_dict = Parameter.from_dict(OPTIMIZATION_PARAMETER_DICT)
    assert isinstance(optimization_parameter_from_dict, OptimizationParameter)
    stochastic_parameter_from_dict = Parameter.from_dict(STOCHASTIC_PARAMETER_DICT)
    assert isinstance(stochastic_parameter_from_dict, StochasticParameter)
    mixed_parameter_from_dict = Parameter.from_dict(MIXED_PARAMETER_DICT)
    assert isinstance(mixed_parameter_from_dict, MixedParameter)
    with pytest.raises(ValueError):
        Parameter.from_dict({"type": {"value": "invalid"}})


def test_optimization_parameter():
    """Test `OptimizationParameter`."""
    optimization_parameter_dict = OPTIMIZATION_PARAMETER.to_dict()
    assert isinstance(optimization_parameter_dict, dict)
    for key in optimization_parameter_dict.keys():
        assert key in OPTIMIZATION_PARAMETER_DICT

    optimization_parameter_from_dict = OptimizationParameter.from_dict(OPTIMIZATION_PARAMETER_DICT)
    assert OPTIMIZATION_PARAMETER == optimization_parameter_from_dict

    optimization_parameter_copy = copy.deepcopy(OPTIMIZATION_PARAMETER)
    assert OPTIMIZATION_PARAMETER == optimization_parameter_copy

    assert isinstance(optimization_parameter_copy.reference_value_type, ParameterValueType)
    assert isinstance(optimization_parameter_copy.deterministic_resolution, ParameterResolution)
    assert isinstance(optimization_parameter_copy.range, tuple)

    with pytest.raises(TypeError):
        optimization_parameter_copy.reference_value_type = ["REAL"]
    optimization_parameter_copy.reference_value_type = "integer"
    assert optimization_parameter_copy.reference_value_type == ParameterValueType.INTEGER
    optimization_parameter_copy.reference_value_type = ParameterValueType.REAL
    assert optimization_parameter_copy.reference_value_type == ParameterValueType.REAL

    with pytest.raises(TypeError):
        optimization_parameter_copy.deterministic_resolution = ["deterministic"]
    optimization_parameter_copy.deterministic_resolution = "ordinaldiscrete_index"
    assert (
        optimization_parameter_copy.deterministic_resolution
        == ParameterResolution.ORDINALDISCRETE_INDEX
    )
    optimization_parameter_copy.deterministic_resolution = ParameterResolution.CONTINUOUS
    assert optimization_parameter_copy.deterministic_resolution == ParameterResolution.CONTINUOUS

    optimization_parameter_copy.range = [[1, 2, 3]]
    assert optimization_parameter_copy.range == ((1, 2, 3),)
    optimization_parameter_copy.range = [1, 2]
    assert optimization_parameter_copy.range == (1, 2)


def test_stochastic_parameter():
    """Test `StochasticParameter`."""
    stochastic_parameter_dict = STOCHASTIC_PARAMETER.to_dict()
    assert isinstance(stochastic_parameter_dict, dict)
    for key in stochastic_parameter_dict.keys():
        assert key in STOCHASTIC_PARAMETER_DICT

    stochastic_parameter_from_dict = StochasticParameter.from_dict(STOCHASTIC_PARAMETER_DICT)
    assert STOCHASTIC_PARAMETER == stochastic_parameter_from_dict

    stochastic_parameter_copy = copy.deepcopy(STOCHASTIC_PARAMETER)
    assert STOCHASTIC_PARAMETER == stochastic_parameter_copy

    assert isinstance(stochastic_parameter_copy.reference_value_type, ParameterValueType)
    assert isinstance(stochastic_parameter_copy.stochastic_resolution, ParameterResolution)
    assert isinstance(stochastic_parameter_copy.distribution_type, DistributionType)
    assert isinstance(stochastic_parameter_copy.distribution_parameters, tuple)

    with pytest.raises(AttributeError):
        stochastic_parameter_copy.reference_value_type = "REAL"
    assert stochastic_parameter_copy.reference_value_type == ParameterValueType.REAL

    with pytest.raises(TypeError):
        stochastic_parameter_copy.stochastic_resolution = ["deterministic"]
    stochastic_parameter_copy.stochastic_resolution == "marginaldistribution"
    assert (
        stochastic_parameter_copy.stochastic_resolution == ParameterResolution.MARGINALDISTRIBUTION
    )
    stochastic_parameter_copy.stochastic_resolution = ParameterResolution.EMPIRICAL_CONTINUOUS
    assert (
        stochastic_parameter_copy.stochastic_resolution == ParameterResolution.EMPIRICAL_CONTINUOUS
    )

    with pytest.raises(TypeError):
        stochastic_parameter_copy.distribution_type = ["BERNOULLI"]
    stochastic_parameter_copy.distribution_type = "beta"
    assert stochastic_parameter_copy.distribution_type == DistributionType.BETA
    stochastic_parameter_copy.distribution_type = DistributionType.BERNOULLI
    assert stochastic_parameter_copy.distribution_type == DistributionType.BERNOULLI

    stochastic_parameter_copy.distribution_parameters = [1, 2]
    assert stochastic_parameter_copy.distribution_parameters == (1, 2)
    stochastic_parameter_copy.distribution_parameters = [1]
    assert stochastic_parameter_copy.distribution_parameters == (1,)


def test_mixed_parameter():
    """Test `OptimizationParameter`."""
    mixed_parameter_dict = MIXED_PARAMETER.to_dict()
    assert isinstance(mixed_parameter_dict, dict)
    for key in mixed_parameter_dict.keys():
        assert key in MIXED_PARAMETER_DICT

    mixed_parameter_from_dict = MixedParameter.from_dict(MIXED_PARAMETER_DICT)
    assert MIXED_PARAMETER == mixed_parameter_from_dict

    mixed_parameter_copy = copy.deepcopy(MIXED_PARAMETER)
    assert MIXED_PARAMETER == mixed_parameter_copy

    assert isinstance(mixed_parameter_copy.reference_value_type, ParameterValueType)
    assert isinstance(mixed_parameter_copy.deterministic_resolution, ParameterResolution)
    assert isinstance(mixed_parameter_copy.range, tuple)
    assert isinstance(mixed_parameter_copy.stochastic_resolution, ParameterResolution)
    assert isinstance(mixed_parameter_copy.distribution_type, DistributionType)
    assert isinstance(mixed_parameter_copy.distribution_parameters, tuple)

    with pytest.raises(AttributeError):
        mixed_parameter_copy.reference_value_type = "REAL"
    assert mixed_parameter_copy.reference_value_type == ParameterValueType.REAL

    with pytest.raises(TypeError):
        mixed_parameter_copy.deterministic_resolution = ["deterministic"]
    mixed_parameter_copy.deterministic_resolution = "deterministic"
    assert mixed_parameter_copy.deterministic_resolution == ParameterResolution.DETERMINISTIC
    mixed_parameter_copy.deterministic_resolution = ParameterResolution.CONTINUOUS
    assert mixed_parameter_copy.deterministic_resolution == ParameterResolution.CONTINUOUS

    mixed_parameter_copy.range = [[1, 2, 3]]
    assert mixed_parameter_copy.range == ((1, 2, 3),)
    mixed_parameter_copy.range = [1, 2]
    assert mixed_parameter_copy.range == (1, 2)

    with pytest.raises(TypeError):
        mixed_parameter_copy.stochastic_resolution = ["deterministic"]
    mixed_parameter_copy.stochastic_resolution == "marginaldistribution"
    assert mixed_parameter_copy.stochastic_resolution == ParameterResolution.MARGINALDISTRIBUTION
    mixed_parameter_copy.stochastic_resolution = ParameterResolution.EMPIRICAL_CONTINUOUS
    assert mixed_parameter_copy.stochastic_resolution == ParameterResolution.EMPIRICAL_CONTINUOUS

    with pytest.raises(TypeError):
        mixed_parameter_copy.distribution_type = ["BERNOULLI"]
    mixed_parameter_copy.distribution_type = "beta"
    assert mixed_parameter_copy.distribution_type == DistributionType.BETA
    mixed_parameter_copy.distribution_type = DistributionType.BERNOULLI
    assert mixed_parameter_copy.distribution_type == DistributionType.BERNOULLI

    mixed_parameter_copy.distribution_parameters = [1, 2]
    assert mixed_parameter_copy.distribution_parameters == (1, 2)
    mixed_parameter_copy.distribution_parameters = [1]
    assert mixed_parameter_copy.distribution_parameters == (1,)


def test_dependent_parameter():
    """Test `OptimizationParameter`."""
    dependent_parameter_dict = DEPENDENT_PARAMETER.to_dict()
    assert isinstance(dependent_parameter_dict, dict)
    for key in dependent_parameter_dict.keys():
        assert key in DEPENDENT_PARAMETER_DICT

    dependent_parameter_from_dict = DependentParameter.from_dict(DEPENDENT_PARAMETER_DICT)
    assert DEPENDENT_PARAMETER == dependent_parameter_from_dict

    dependent_parameter_copy = copy.deepcopy(DEPENDENT_PARAMETER)
    assert DEPENDENT_PARAMETER == dependent_parameter_copy

    assert isinstance(dependent_parameter_copy.operation, str)
    with pytest.raises(TypeError):
        dependent_parameter_copy.operation = 10
    dependent_parameter_copy.operation = "10+Parameter_1"
    assert dependent_parameter_copy.operation == "10+Parameter_1"


# TEST CRITERIA:
def test_criterion():
    """Test `Criterion`."""
    criterion = Criterion(
        name="criterion",
        type_=CriterionType.VARIABLE,
        expression="0",
        criterion=ComparisonType.IGNORE,
    )
    assert isinstance(criterion, Criterion)
    assert isinstance(criterion.name, str)
    assert isinstance(criterion.type, CriterionType)
    assert isinstance(criterion.expression, str)
    assert criterion.expression_value == None
    assert isinstance(criterion.expression_value_type, CriterionValueType)
    assert isinstance(criterion.criterion, ComparisonType)
    assert criterion.value == None
    assert isinstance(criterion.value_type, CriterionValueType)

    criterion_eq = Criterion(
        name="criterion",
        type_=CriterionType.VARIABLE,
        expression="0",
        criterion=ComparisonType.IGNORE,
    )
    criterion_neq = Criterion(
        name="criterion",
        type_=CriterionType.VARIABLE,
        expression="1",
        criterion=ComparisonType.IGNORE,
    )
    criterion_copy = copy.deepcopy(criterion)
    assert criterion == criterion_eq
    assert not criterion == criterion_neq
    assert criterion == criterion_copy

    constraint_criterion_from_dict = Criterion.from_dict(criterion_dict=CONSTRAINT_CRITERION_DICT)
    assert isinstance(constraint_criterion_from_dict, ConstraintCriterion)
    limit_state_criterion_from_dict = Criterion.from_dict(criterion_dict=LIMIT_STATE_CRITERION_DICT)
    assert isinstance(limit_state_criterion_from_dict, LimitStateCriterion)
    objective_criterion_from_dict = Criterion.from_dict(criterion_dict=OBJECTIVE_CRITERION_DICT)
    assert isinstance(objective_criterion_from_dict, ObjectiveCriterion)
    variable_criterion_from_dict = Criterion.from_dict(criterion_dict=VARIABLE_CRITERION_DICT)
    assert isinstance(variable_criterion_from_dict, VariableCriterion)

    with pytest.raises(ValueError):
        Criterion.from_dict({"Second": {"type": {"value": "invalid"}}})

    with pytest.raises(AttributeError):
        criterion.type = CriterionType.LIMIT_STATE
    with pytest.raises(TypeError):
        criterion.name = 10
    criterion.name = "criterion1"
    assert criterion.name == "criterion1"
    with pytest.raises(TypeError):
        criterion.expression = ["10"]
    criterion.expression = "10+Parameter_1"
    assert criterion.expression == "10+Parameter_1"
    criterion.expression_value = 10
    assert criterion.expression_value == 10
    assert criterion.expression_value_type == CriterionValueType.SCALAR

    with pytest.raises(TypeError):
        criterion.criterion = ["equal"]
    criterion.criterion = "EQUAL"
    assert criterion.criterion == ComparisonType.EQUAL
    criterion.criterion = ComparisonType.GREATEREQUAL
    assert criterion.criterion == ComparisonType.GREATEREQUAL

    criterion.value = 10.0
    assert criterion.value == 10
    assert criterion.value_type == CriterionValueType.SCALAR

    criterion.value = complex(10, 10)
    assert criterion.value == complex(10, 10)
    assert criterion.value_type == CriterionValueType.SCALAR

    criterion.value = True
    assert criterion.value == True
    assert criterion.value_type == CriterionValueType.BOOL

    criterion.value = None
    assert criterion.value == None
    assert criterion.value_type == CriterionValueType.UNINITIALIZED

    criterion.value = [1, 2, 3]
    assert criterion.value == [1, 2, 3]
    assert criterion.value_type == CriterionValueType.VECTOR

    criterion.value = [[1, 2, 3], [1, 2, 3]]
    assert criterion.value == [[1, 2, 3], [1, 2, 3]]
    assert criterion.value_type == CriterionValueType.MATRIX

    criterion.value = {"channels": [1, 2, 3]}
    assert criterion.value == {"channels": [1, 2, 3]}
    assert criterion.value_type == CriterionValueType.SIGNAL

    criterion.value = {"matrix": [1, 2, 3]}
    assert criterion.value == {"matrix": [1, 2, 3]}
    assert criterion.value_type == CriterionValueType.XYDATA

    with pytest.raises(TypeError):
        criterion.value = (1, 2, 3)


def test_contraint_criterion():
    """Test ``ConstraintCriterion``."""
    constraint_criterion_dict = CONSTRAINT_CRITERION.to_dict()
    assert isinstance(constraint_criterion_dict, dict)
    for key in constraint_criterion_dict.keys():
        assert key in CONSTRAINT_CRITERION_DICT

    constraint_criterion_from_dict = ConstraintCriterion.from_dict(CONSTRAINT_CRITERION_DICT)
    assert CONSTRAINT_CRITERION == constraint_criterion_from_dict

    constraint_criterion_copy = copy.deepcopy(CONSTRAINT_CRITERION)
    assert CONSTRAINT_CRITERION == constraint_criterion_copy

    assert isinstance(constraint_criterion_copy.limit_expression, str)
    assert isinstance(constraint_criterion_copy.limit_expression_value_type, CriterionValueType)

    with pytest.raises(TypeError):
        constraint_criterion_copy.limit_expression = ["a+b"]
    constraint_criterion_copy.limit_expression = "a+b"
    assert constraint_criterion_copy.limit_expression == "a+b"

    constraint_criterion_copy.limit_expression_value = 10
    assert constraint_criterion_copy.limit_expression_value == 10
    assert constraint_criterion_copy.limit_expression_value_type == CriterionValueType.SCALAR


def test_limit_state_criterion():
    """Test ``LimitStateCriterion``."""
    limit_state_criterion_dict = LIMIT_STATE_CRITERION.to_dict()
    assert isinstance(limit_state_criterion_dict, dict)
    for key in limit_state_criterion_dict.keys():
        assert key in LIMIT_STATE_CRITERION_DICT

    limit_state_criterion_from_dict = LimitStateCriterion.from_dict(LIMIT_STATE_CRITERION_DICT)
    assert LIMIT_STATE_CRITERION == limit_state_criterion_from_dict

    limit_state_criterion_copy = copy.deepcopy(LIMIT_STATE_CRITERION)
    assert LIMIT_STATE_CRITERION == limit_state_criterion_copy

    assert isinstance(limit_state_criterion_copy.limit_expression, str)
    assert isinstance(limit_state_criterion_copy.limit_expression_value_type, CriterionValueType)

    with pytest.raises(TypeError):
        limit_state_criterion_copy.limit_expression = ["a+b"]
    limit_state_criterion_copy.limit_expression = "a+b"
    assert limit_state_criterion_copy.limit_expression == "a+b"

    limit_state_criterion_copy.limit_expression_value = 10
    assert limit_state_criterion_copy.limit_expression_value == 10
    assert limit_state_criterion_copy.limit_expression_value_type == CriterionValueType.SCALAR


def test_objective_criterion():
    """Test ``ObjectiveCriterion``."""
    objective_criterion_dict = OBJECTIVE_CRITERION.to_dict()
    assert isinstance(objective_criterion_dict, dict)
    for key in objective_criterion_dict.keys():
        assert key in OBJECTIVE_CRITERION_DICT

    objective_criterion_from_dict = ObjectiveCriterion.from_dict(OBJECTIVE_CRITERION_DICT)
    assert OBJECTIVE_CRITERION == objective_criterion_from_dict

    objective_criterion_copy = copy.deepcopy(OBJECTIVE_CRITERION)
    assert OBJECTIVE_CRITERION == objective_criterion_copy


def test_variable_criterion():
    """Test ``VariableCriterion``."""
    variable_criterion_dict = VARIABLE_CRITERION.to_dict()
    assert isinstance(variable_criterion_dict, dict)
    for key in variable_criterion_dict.keys():
        assert key in VARIABLE_CRITERION_DICT

    variable_criterion_from_dict = VariableCriterion.from_dict(VARIABLE_CRITERION_DICT)
    assert VARIABLE_CRITERION == variable_criterion_from_dict

    variable_criterion_copy = copy.deepcopy(VARIABLE_CRITERION)
    assert VARIABLE_CRITERION == variable_criterion_copy


# TEST RESPONSES:
def test_response():
    """Test `Response`."""
    response = Response(name="variable_1", value=0)
    assert isinstance(response, Response)
    assert isinstance(response.name, str)
    assert response.value == 0
    assert isinstance(response.value_type, ResponseValueType)

    response_eq = Response(name="variable_1", value=0)
    response_neq = Response(name="variable_1", value=[0])
    response_copy = copy.deepcopy(response)
    assert response == response_eq
    assert not response == response_neq
    assert response == response_copy

    with pytest.raises(TypeError):
        response.name = 10
    response.name = "response1"
    assert response.name == "response1"

    response.value = 10.0
    assert response.value == 10
    assert response.value_type == ResponseValueType.SCALAR

    response.value = complex(10, 10)
    assert response.value == complex(10, 10)
    assert response.value_type == ResponseValueType.SCALAR

    response.value = True
    assert response.value == True
    assert response.value_type == ResponseValueType.BOOL

    response.value = None
    assert response.value == None
    assert response.value_type == ResponseValueType.UNINITIALIZED

    response.value = [1, 2, 3]
    assert response.value == [1, 2, 3]
    assert response.value_type == ResponseValueType.VECTOR

    response.value = {"channels": [1, 2, 3], "type": "signal"}
    assert response.value == {"channels": [1, 2, 3], "type": "signal"}
    assert response.value_type == ResponseValueType.SIGNAL

    response.value = {"matrix": [1, 2, 3], "type": "xydata"}
    assert response.value == {"matrix": [1, 2, 3], "type": "xydata"}
    assert response.value_type == ResponseValueType.XYDATA

    with pytest.raises(TypeError):
        response.value = (1, 2, 3)


# TEST DESIGN:
@pytest.fixture()
def design(scope="function", autouse=False) -> Design:
    """Create an instance of Design class."""
    return Design(
        [
            DEPENDENT_PARAMETER,
            MIXED_PARAMETER,
            OPTIMIZATION_PARAMETER,
            STOCHASTIC_PARAMETER,
        ]
    )


def test_design_properties(design: Design):
    """Test properties of instance of Design class."""
    assert design.id == None
    assert design.feasibility == None
    assert design.status == DesignStatus.IDLE
    assert isinstance(design.constraints, tuple)
    assert isinstance(design.constraints_names, tuple)
    assert isinstance(design.limit_states, tuple)
    assert isinstance(design.limit_states_names, tuple)
    assert isinstance(design.objectives, tuple)
    assert isinstance(design.objectives_names, tuple)
    assert isinstance(design.parameters, tuple)
    assert isinstance(design.parameters[0], DesignVariable)
    assert isinstance(design.parameters_names, tuple)
    assert isinstance(design.parameters_names[0], str)
    assert isinstance(design.responses, tuple)
    assert isinstance(design.responses_names, tuple)
    assert isinstance(design.variables, tuple)
    assert isinstance(design.variables_names, tuple)
    for parameter in design.parameters:
        assert isinstance(parameter, DesignVariable)


def test_clear_parameters(design: Design):
    """Test `clear_parameters`."""
    design.clear_parameters()
    assert len(design.parameters) == 0


def test_copy_unevaluated_design(design: Design):
    """Test deep copy of Design (and parameters inside)."""
    design_copy = design.copy_unevaluated_design()
    assert design_copy.parameters == design.parameters
    design_copy.remove_parameter("dependent")
    assert not design_copy.parameters == design.parameters


def test_remove_parameter(design: Design):
    """Test `remove_parameters`."""
    for name in ["mixed", "dependent"]:
        design.remove_parameter(name=name)
    assert len(design.parameters) > 0
    for parameter in design.parameters:
        assert parameter.name in ["optimization", "stochastic"]
        assert parameter.name not in ["mixed", "dependent"]


def test_set_parameter_value(design: Design):
    """Test `set_parameter` and `set_parameter_by_name`."""
    design.clear_parameters()
    design.set_parameter_by_name(name="par1", value=5)
    design.set_parameter(parameter=DesignVariable("par2", 10))
    for parameter in design.parameters:
        assert isinstance(parameter, DesignVariable)
        assert parameter.name in ["par1", "par2"]
        assert parameter.value in [5, 10]
    design.set_parameter_by_name(name="par1", value=15)
    design.set_parameter(
        parameter=Parameter(
            name="par2", reference_value=20, id="xxx", const=False, type_=ParameterType.MIXED
        )
    )
    for parameter in design.parameters:
        assert isinstance(parameter, DesignVariable)
        assert parameter.name in ["par1", "par2"]
        assert parameter.value in [15, 20]
