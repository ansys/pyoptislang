import copy

import pytest

from ansys.optislang.core.project_parametric import (
    DependentParameter,
    Design,
    DesignStatus,
    DesignVariable,
    DistributionType,
    MixedParameter,
    OptimizationParameter,
    Parameter,
    ParameterResolution,
    ParameterType,
    ParameterValueType,
    StochasticParameter,
)

DEPENDENT_PARAMETER = DependentParameter(
    name="dependent", id="aaba5b78-4b8c-4cc3-a308-4e122e2af665"
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

# TEST ENUMERATION METHODS:
def test_design_status_from_str():
    """Test `DesignStatus.from_str()`."""
    assert DesignStatus.from_str("IdLe") == DesignStatus.IDLE
    assert DesignStatus.from_str("pending") == DesignStatus.PENDING
    assert DesignStatus.from_str("succeeded") == DesignStatus.SUCCEEDED
    assert DesignStatus.from_str("failed") == DesignStatus.FAILED
    with pytest.raises(ValueError):
        DesignStatus.from_str("nonexistingstatus")


def test_parameter_type():
    """Test `ParameterType`."""
    deterministic = ParameterType.DETERMINISTIC
    deterministic_name = deterministic.name
    deterministic_from_str = ParameterType.from_str("DeTeRmInIsTiC")
    assert isinstance(deterministic, ParameterType)
    assert isinstance(deterministic_from_str, ParameterType)
    assert isinstance(deterministic_name, str)
    assert deterministic_name == "DETERMINISTIC"
    assert deterministic_name == deterministic_from_str.name

    stochastic = ParameterType.STOCHASTIC
    stochastic_name = stochastic.name
    stochastic_from_str = ParameterType.from_str("stochastic")
    assert isinstance(stochastic, ParameterType)
    assert isinstance(stochastic_from_str, ParameterType)
    assert isinstance(stochastic_name, str)
    assert stochastic_name == "STOCHASTIC"
    assert stochastic_name == stochastic_from_str.name

    mixed = ParameterType.MIXED
    mixed_name = mixed.name
    mixed_from_str = ParameterType.from_str("mixed")
    assert isinstance(mixed, ParameterType)
    assert isinstance(mixed_from_str, ParameterType)
    assert isinstance(mixed_name, str)
    assert mixed_name == "MIXED"
    assert mixed_name == mixed_from_str.name

    dependent = ParameterType.DEPENDENT
    dependent_name = dependent.name
    dependent_from_str = ParameterType.from_str("dependent")
    assert isinstance(dependent, ParameterType)
    assert isinstance(dependent_from_str, ParameterType)
    assert isinstance(dependent_name, str)
    assert dependent_name == "DEPENDENT"
    assert dependent_name == dependent_from_str.name

    with pytest.raises(TypeError):
        ParameterType.from_str(1)

    with pytest.raises(ValueError):
        ParameterType.from_str("nonexisting")


def test_parameter_resolution():
    """Test `ParameterResolution`."""
    continuous_from_str = ParameterResolution.from_str("CoNtInUoUs")
    assert isinstance(continuous_from_str, ParameterResolution)
    assert continuous_from_str.name == "CONTINUOUS"

    ordinaldiscrete_value_from_str = ParameterResolution.from_str("ordinaldiscrete_value")
    assert isinstance(ordinaldiscrete_value_from_str, ParameterResolution)
    assert ordinaldiscrete_value_from_str.name == "ORDINALDISCRETE_VALUE"

    ordinaldiscrete_index_from_str = ParameterResolution.from_str("ordinaldiscrete_index")
    assert isinstance(ordinaldiscrete_index_from_str, ParameterResolution)
    assert ordinaldiscrete_index_from_str.name == "ORDINALDISCRETE_INDEX"

    nominaldiscrete_from_str = ParameterResolution.from_str("nominaldiscrete")
    assert isinstance(nominaldiscrete_from_str, ParameterResolution)
    assert nominaldiscrete_from_str.name == "NOMINALDISCRETE"

    deterministic_from_str = ParameterResolution.from_str("deterministic")
    assert isinstance(deterministic_from_str, ParameterResolution)
    assert deterministic_from_str.name == "DETERMINISTIC"

    marginaldistribution_from_str = ParameterResolution.from_str("marginaldistribution")
    assert isinstance(marginaldistribution_from_str, ParameterResolution)
    assert marginaldistribution_from_str.name == "MARGINALDISTRIBUTION"

    empirical_discrete_from_str = ParameterResolution.from_str("empirical_discrete")
    assert isinstance(empirical_discrete_from_str, ParameterResolution)
    assert empirical_discrete_from_str.name == "EMPIRICAL_DISCRETE"

    empirical_continuous_from_str = ParameterResolution.from_str("empirical_continuous")
    assert isinstance(empirical_continuous_from_str, ParameterResolution)
    assert empirical_continuous_from_str.name == "EMPIRICAL_CONTINUOUS"

    with pytest.raises(TypeError):
        ParameterResolution.from_str(1)

    with pytest.raises(ValueError):
        ParameterResolution.from_str("nonexisting")


def test_parameter_value_type():
    """Test `ParameterValueType`."""
    uninitialized_from_str = ParameterValueType.from_str("UnInItIaLiZeD")
    assert isinstance(uninitialized_from_str, ParameterValueType)
    assert uninitialized_from_str.name == "UNINITIALIZED"

    bool_from_str = ParameterValueType.from_str("bool")
    assert isinstance(bool_from_str, ParameterValueType)
    assert bool_from_str.name == "BOOL"

    real_from_str = ParameterValueType.from_str("real")
    assert isinstance(real_from_str, ParameterValueType)
    assert real_from_str.name == "REAL"

    integer_from_str = ParameterValueType.from_str("integer")
    assert isinstance(integer_from_str, ParameterValueType)
    assert integer_from_str.name == "INTEGER"

    string_from_str = ParameterValueType.from_str("string")
    assert isinstance(string_from_str, ParameterValueType)
    assert string_from_str.name == "STRING"

    variant_from_str = ParameterValueType.from_str("variant")
    assert isinstance(variant_from_str, ParameterValueType)
    assert variant_from_str.name == "VARIANT"

    with pytest.raises(TypeError):
        ParameterValueType.from_str(1)

    with pytest.raises(ValueError):
        ParameterValueType.from_str("nonexisting")


def test_distribution_type():
    """Test `DistributionType`."""
    externalcoherence_from_str = DistributionType.from_str("ExTeRnAlCoHeReNcE")
    assert isinstance(externalcoherence_from_str, DistributionType)
    assert externalcoherence_from_str.name == "EXTERNALCOHERENCE"

    untyped_from_str = DistributionType.from_str("untyped")
    assert isinstance(untyped_from_str, DistributionType)
    assert untyped_from_str.name == "UNTYPED"

    external_from_str = DistributionType.from_str("external")
    assert isinstance(external_from_str, DistributionType)
    assert external_from_str.name == "EXTERNAL"

    uniform_from_str = DistributionType.from_str("uniform")
    assert isinstance(uniform_from_str, DistributionType)
    assert uniform_from_str.name == "UNIFORM"

    normal_from_str = DistributionType.from_str("normal")
    assert isinstance(normal_from_str, DistributionType)
    assert normal_from_str.name == "NORMAL"

    truncatednormal_from_str = DistributionType.from_str("truncatednormal")
    assert isinstance(truncatednormal_from_str, DistributionType)
    assert truncatednormal_from_str.name == "TRUNCATEDNORMAL"

    lognormal_from_str = DistributionType.from_str("lognormal")
    assert isinstance(lognormal_from_str, DistributionType)
    assert lognormal_from_str.name == "LOGNORMAL"

    exponential_from_str = DistributionType.from_str("exponential")
    assert isinstance(exponential_from_str, DistributionType)
    assert exponential_from_str.name == "EXPONENTIAL"

    rayleigh_from_str = DistributionType.from_str("rayleigh")
    assert isinstance(rayleigh_from_str, DistributionType)
    assert rayleigh_from_str.name == "RAYLEIGH"

    small_i_from_str = DistributionType.from_str("small_i")
    assert isinstance(small_i_from_str, DistributionType)
    assert small_i_from_str.name == "SMALL_I"

    large_i_from_str = DistributionType.from_str("large_i")
    assert isinstance(large_i_from_str, DistributionType)
    assert large_i_from_str.name == "LARGE_I"

    small_ii_from_str = DistributionType.from_str("small_ii")
    assert isinstance(small_ii_from_str, DistributionType)
    assert small_ii_from_str.name == "SMALL_II"

    large_ii_from_str = DistributionType.from_str("large_ii")
    assert isinstance(large_ii_from_str, DistributionType)
    assert large_ii_from_str.name == "LARGE_II"

    small_iii_from_str = DistributionType.from_str("small_iii")
    assert isinstance(small_iii_from_str, DistributionType)
    assert small_iii_from_str.name == "SMALL_III"

    large_iii_from_str = DistributionType.from_str("large_iii")
    assert isinstance(large_iii_from_str, DistributionType)
    assert large_iii_from_str.name == "LARGE_III"

    triangular_from_str = DistributionType.from_str("triangular")
    assert isinstance(triangular_from_str, DistributionType)
    assert triangular_from_str.name == "TRIANGULAR"

    beta_from_str = DistributionType.from_str("beta")
    assert isinstance(beta_from_str, DistributionType)
    assert beta_from_str.name == "BETA"

    chi_square_from_str = DistributionType.from_str("chi_square")
    assert isinstance(chi_square_from_str, DistributionType)
    assert chi_square_from_str.name == "CHI_SQUARE"

    erlang_from_str = DistributionType.from_str("erlang")
    assert isinstance(erlang_from_str, DistributionType)
    assert erlang_from_str.name == "ERLANG"

    fisher_f_from_str = DistributionType.from_str("fisher_f")
    assert isinstance(fisher_f_from_str, DistributionType)
    assert fisher_f_from_str.name == "FISHER_F"

    gamma_from_str = DistributionType.from_str("gamma")
    assert isinstance(gamma_from_str, DistributionType)
    assert gamma_from_str.name == "GAMMA"

    pareto_from_str = DistributionType.from_str("pareto")
    assert isinstance(pareto_from_str, DistributionType)
    assert pareto_from_str.name == "PARETO"

    weibull_from_str = DistributionType.from_str("weibull")
    assert isinstance(weibull_from_str, DistributionType)
    assert weibull_from_str.name == "WEIBULL"

    extreme_value_from_str = DistributionType.from_str("extreme_value")
    assert isinstance(extreme_value_from_str, DistributionType)
    assert extreme_value_from_str.name == "EXTREME_VALUE"

    students_f_from_str = DistributionType.from_str("students_f")
    assert isinstance(students_f_from_str, DistributionType)
    assert students_f_from_str.name == "STUDENTS_F"

    inverse_normal_from_str = DistributionType.from_str("inverse_normal")
    assert isinstance(inverse_normal_from_str, DistributionType)
    assert inverse_normal_from_str.name == "INVERSE_NORMAL"

    log_gamma_from_str = DistributionType.from_str("log_gamma")
    assert isinstance(log_gamma_from_str, DistributionType)
    assert log_gamma_from_str.name == "LOG_GAMMA"

    log_normal_from_str = DistributionType.from_str("log_normal")
    assert isinstance(log_normal_from_str, DistributionType)
    assert log_normal_from_str.name == "LOG_NORMAL"

    lorentz_from_str = DistributionType.from_str("lorentz")
    assert isinstance(lorentz_from_str, DistributionType)
    assert lorentz_from_str.name == "LORENTZ"

    fisher_tippett_from_str = DistributionType.from_str("fisher_tippett")
    assert isinstance(fisher_tippett_from_str, DistributionType)
    assert fisher_tippett_from_str.name == "FISHER_TIPPETT"

    gumbel_from_str = DistributionType.from_str("gumbel")
    assert isinstance(gumbel_from_str, DistributionType)
    assert gumbel_from_str.name == "GUMBEL"

    fisher_z_from_str = DistributionType.from_str("fisher_z")
    assert isinstance(fisher_z_from_str, DistributionType)
    assert fisher_z_from_str.name == "FISHER_Z"

    laplace_from_str = DistributionType.from_str("laplace")
    assert isinstance(laplace_from_str, DistributionType)
    assert laplace_from_str.name == "LAPLACE"

    levy_from_str = DistributionType.from_str("levy")
    assert isinstance(levy_from_str, DistributionType)
    assert levy_from_str.name == "LEVY"

    logistic_from_str = DistributionType.from_str("logistic")
    assert isinstance(logistic_from_str, DistributionType)
    assert logistic_from_str.name == "LOGISTIC"

    rossi_from_str = DistributionType.from_str("rossi")
    assert isinstance(rossi_from_str, DistributionType)
    assert rossi_from_str.name == "ROSSI"

    frechet_from_str = DistributionType.from_str("frechet")
    assert isinstance(frechet_from_str, DistributionType)
    assert frechet_from_str.name == "FRECHET"

    max_type_from_str = DistributionType.from_str("max_type")
    assert isinstance(max_type_from_str, DistributionType)
    assert max_type_from_str.name == "MAX_TYPE"

    polymap_from_str = DistributionType.from_str("polymap")
    assert isinstance(polymap_from_str, DistributionType)
    assert polymap_from_str.name == "POLYMAP"

    kernel_from_str = DistributionType.from_str("kernel")
    assert isinstance(kernel_from_str, DistributionType)
    assert kernel_from_str.name == "KERNEL"

    bernoulli_from_str = DistributionType.from_str("bernoulli")
    assert isinstance(bernoulli_from_str, DistributionType)
    assert bernoulli_from_str.name == "BERNOULLI"

    log_uniform_from_str = DistributionType.from_str("log_uniform")
    assert isinstance(log_uniform_from_str, DistributionType)
    assert log_uniform_from_str.name == "LOG_UNIFORM"

    discrete_from_str = DistributionType.from_str("discrete")
    assert isinstance(discrete_from_str, DistributionType)
    assert discrete_from_str.name == "DISCRETE"

    multiuniform_from_str = DistributionType.from_str("multiuniform")
    assert isinstance(multiuniform_from_str, DistributionType)
    assert multiuniform_from_str.name == "MULTIUNIFORM"

    lambda_from_str = DistributionType.from_str("lambda")
    assert isinstance(lambda_from_str, DistributionType)
    assert lambda_from_str.name == "LAMBDA"

    poisson_from_str = DistributionType.from_str("poisson")
    assert isinstance(poisson_from_str, DistributionType)
    assert poisson_from_str.name == "POISSON"

    with pytest.raises(TypeError):
        DistributionType.from_str(1)

    with pytest.raises(ValueError):
        DistributionType.from_str("nonexisting")


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
    parameter1 = Parameter(
        name="par1", reference_value=12.0, id="xxx-12-55", const=False, type=ParameterType.MIXED
    )
    assert isinstance(parameter1, Parameter)
    assert isinstance(parameter1.name, str)
    assert isinstance(parameter1.reference_value, (int, float))
    assert isinstance(parameter1.reference_value_type, ParameterValueType)
    assert isinstance(parameter1.id, str)
    assert isinstance(parameter1.const, bool)
    assert isinstance(parameter1.type, ParameterType)

    parameter1_eq = Parameter(
        name="par1", reference_value=12.0, id="xxx-12-55", const=False, type=ParameterType.MIXED
    )
    parameter1_neq = Parameter(
        name="par1", reference_value=12.0, id="xxx-12-56", const=False, type=ParameterType.MIXED
    )
    assert parameter1 == parameter1_eq
    assert not parameter1 == parameter1_neq

    dependent_parameter_from_dict = Parameter.from_dict(DEPENDENT_PARAMETER_DICT)
    assert isinstance(dependent_parameter_from_dict, DependentParameter)
    optimization_parameter_from_dict = Parameter.from_dict(OPTIMIZATION_PARAMETER_DICT)
    assert isinstance(optimization_parameter_from_dict, OptimizationParameter)
    stochastic_parameter_from_dict = Parameter.from_dict(STOCHASTIC_PARAMETER_DICT)
    assert isinstance(stochastic_parameter_from_dict, StochasticParameter)
    mixed_parameter_from_dict = Parameter.from_dict(MIXED_PARAMETER_DICT)
    assert isinstance(mixed_parameter_from_dict, MixedParameter)
    with pytest.raises(ValueError):
        Parameter.from_dict({"type": {"value": "nonexisting"}})


def test_optimization_parameter():
    """Test `OptimizationParameter`."""
    optimization_parameter_dict = OPTIMIZATION_PARAMETER.to_dict()
    assert isinstance(optimization_parameter_dict, dict)
    for key in optimization_parameter_dict.keys():
        assert key in OPTIMIZATION_PARAMETER_DICT

    optimization_parameter_from_dict = OptimizationParameter.from_dict(OPTIMIZATION_PARAMETER_DICT)
    assert OPTIMIZATION_PARAMETER == optimization_parameter_from_dict


def test_stochastic_parameter():
    """Test `StochasticParameter`."""
    stochastic_parameter_dict = STOCHASTIC_PARAMETER.to_dict()
    assert isinstance(stochastic_parameter_dict, dict)
    for key in stochastic_parameter_dict.keys():
        assert key in STOCHASTIC_PARAMETER_DICT

    stochastic_parameter_from_dict = StochasticParameter.from_dict(STOCHASTIC_PARAMETER_DICT)
    assert STOCHASTIC_PARAMETER == stochastic_parameter_from_dict


def test_mixed_parameter():
    """Test `OptimizationParameter`."""
    mixed_parameter_dict = MIXED_PARAMETER.to_dict()
    assert isinstance(mixed_parameter_dict, dict)
    for key in mixed_parameter_dict.keys():
        assert key in MIXED_PARAMETER_DICT

    mixed_parameter_from_dict = MixedParameter.from_dict(MIXED_PARAMETER_DICT)
    assert MIXED_PARAMETER == mixed_parameter_from_dict


def test_dependent_parameter():
    """Test `OptimizationParameter`."""
    dependent_parameter_dict = DEPENDENT_PARAMETER.to_dict()
    assert isinstance(dependent_parameter_dict, dict)
    for key in dependent_parameter_dict.keys():
        assert key in DEPENDENT_PARAMETER_DICT

    dependent_parameter_from_dict = DependentParameter.from_dict(DEPENDENT_PARAMETER_DICT)
    assert DEPENDENT_PARAMETER == dependent_parameter_from_dict


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
    assert isinstance(design.constraint_names, tuple)
    assert isinstance(design.limit_states, tuple)
    assert isinstance(design.limit_state_names, tuple)
    assert isinstance(design.objectives, tuple)
    assert isinstance(design.objective_names, tuple)
    assert isinstance(design.parameters, tuple)
    assert isinstance(design.parameters[0], DesignVariable)
    assert isinstance(design.parameter_names, tuple)
    assert isinstance(design.parameter_names[0], str)
    assert isinstance(design.responses, tuple)
    assert isinstance(design.response_names, tuple)
    assert isinstance(design.variables, tuple)
    assert isinstance(design.variable_names, tuple)
    for parameter in design.parameters:
        assert isinstance(parameter, DesignVariable)


def test_remove_parameters(design: Design):
    """Test `remove_parameters`."""
    design.remove_parameters(to_be_removed=["mixed", "dependent"])
    assert len(design.parameters) > 0
    for parameter in design.parameters:
        assert parameter.name in ["optimization", "stochastic"]
        assert parameter.name not in ["mixed", "dependent"]
    design.remove_parameters()
    assert len(design.parameters) == 0


def test_set_parameter_value(design: Design):
    """Test `set_parameter`."""
    design.remove_parameters()
    design.set_parameter_value(parameter="par1", value=5)
    design.set_parameter_value(parameter=DesignVariable("par2", 10))
    for parameter in design.parameters:
        assert isinstance(parameter, DesignVariable)
        assert parameter.name in ["par1", "par2"]
        assert parameter.value in [5, 10]


@pytest.mark.parametrize(
    "parameters",
    [
        {"par1": 5, "par2": 10},
        [DesignVariable("par1", 5), DesignVariable("par2", 10)],
    ],
)
def test_set_parameter_values(design: Design, parameters):
    """Test `set_parameters`."""
    design.remove_parameters()
    design.set_parameter_values(parameters=parameters)
    for parameter in design.parameters:
        assert isinstance(parameter, DesignVariable)
        assert parameter.name in ["par1", "par2"]
        assert parameter.value in [5, 10]


def test_deep_copy(design: Design):
    """Test deep copy of Design (and parameters inside)."""
    design_copy = copy.deepcopy(design)
    assert design_copy.parameters == design.parameters
    design_copy.remove_parameters("dependent")
    assert not design_copy.parameters == design.parameters
