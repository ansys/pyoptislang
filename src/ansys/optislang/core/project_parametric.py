"""Contains classes Parameter, ParameterManager and Design."""
from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Dict, Iterable, Tuple, Union
import uuid

if TYPE_CHECKING:
    from ansys.optislang.core.osl_server import OslServer


class ParameterType(Enum):
    """Available parameter types."""

    DETERMINISTIC = 0
    STOCHASTIC = 1
    MIXED = 2
    DEPENDENT = 3

    @staticmethod
    def from_str(label: str):
        """Convert string to ParameterType."""
        if not isinstance(label, str):
            raise TypeError(f"String was expected, but `{type(label)}` was given.")
        label = label.upper()
        if label == "DETERMINISTIC":
            return ParameterType.DETERMINISTIC
        elif label == "STOCHASTIC":
            return ParameterType.STOCHASTIC
        elif label == "MIXED":
            return ParameterType.MIXED
        elif label == "DEPENDENT":
            return ParameterType.DEPENDENT
        else:
            raise ValueError(f"Status `{label}` not available in ParameterType types.")


class ParameterResolution(Enum):
    """Available parameter resolution kinds."""

    # optimization (deterministic)
    CONTINUOUS = 0
    ORDINALDISCRETE_VALUE = 1
    ORDINALDISCRETE_INDEX = 2
    NOMINALDISCRETE = 3
    # stochastic
    DETERMINISTIC = 4
    MARGINALDISTRIBUTION = 5
    EMPIRICAL_DISCRETE = 6
    EMPIRICAL_CONTINUOUS = 7

    @staticmethod
    def from_str(label: str):
        """Convert string to ParameterResolution."""
        if not isinstance(label, str):
            raise TypeError(f"String was expected, but `{type(label)}` was given.")
        label = label.upper()
        if label == "CONTINUOUS":
            return ParameterResolution.CONTINUOUS
        elif label == "ORDINALDISCRETE_VALUE":
            return ParameterResolution.ORDINALDISCRETE_VALUE
        elif label == "ORDINALDISCRETE_INDEX":
            return ParameterResolution.ORDINALDISCRETE_INDEX
        elif label == "NOMINALDISCRETE":
            return ParameterResolution.NOMINALDISCRETE
        elif label == "DETERMINISTIC":
            return ParameterResolution.DETERMINISTIC
        elif label == "MARGINALDISTRIBUTION":
            return ParameterResolution.MARGINALDISTRIBUTION
        elif label == "EMPIRICAL_DISCRETE":
            return ParameterResolution.EMPIRICAL_DISCRETE
        elif label == "EMPIRICAL_CONTINUOUS":
            return ParameterResolution.EMPIRICAL_CONTINUOUS
        else:
            raise ValueError(f"Status `{label}` not available in ParameterResolution kinds.")


class ParameterValueType(Enum):
    """Available parameter value types."""

    UNINITIALIZED = 0
    BOOL = 1
    REAL = 2
    INTEGER = 3
    STRING = 4
    VARIANT = 5

    @staticmethod
    def from_str(label: str):
        """Convert string to ParameterValueType."""
        if not isinstance(label, str):
            raise TypeError(f"String was expected, but `{type(label)}` was given.")
        label = label.upper()
        if label == "UNINITIALIZED":
            return ParameterValueType.UNINITIALIZED
        elif label == "BOOL":
            return ParameterValueType.BOOL
        elif label == "REAL":
            return ParameterValueType.REAL
        elif label == "INTEGER":
            return ParameterValueType.INTEGER
        elif label == "STRING":
            return ParameterValueType.STRING
        elif label == "VARIANT":
            return ParameterValueType.VARIANT
        else:
            raise ValueError(f"Status `{label}` not available in ParameterValueType types.")


class DistributionType(Enum):
    """Available distribution types."""

    EXTERNALCOHERENCE = 0
    UNTYPED = 1
    EXTERNAL = 2
    UNIFORM = 3
    NORMAL = 4
    TRUNCATEDNORMAL = 5
    LOGNORMAL = 6
    EXPONENTIAL = 7
    RAYLEIGH = 8
    SMALL_I = 9
    LARGE_I = 10
    SMALL_II = 11
    LARGE_II = 12
    SMALL_III = 13
    LARGE_III = 14
    TRIANGULAR = 15
    BETA = 16
    CHI_SQUARE = 17
    ERLANG = 18
    FISHER_F = 19
    GAMMA = 20
    PARETO = 21
    WEIBULL = 22
    EXTREME_VALUE = 23
    STUDENTS_F = 24
    INVERSE_NORMAL = 25
    LOG_GAMMA = 26
    LOG_NORMAL = 27
    LORENTZ = 28
    FISHER_TIPPETT = 29
    GUMBEL = 30
    FISHER_Z = 31
    LAPLACE = 32
    LEVY = 33
    LOGISTIC = 34
    ROSSI = 35
    FRECHET = 36
    MAX_TYPE = 37
    POLYMAP = 38
    KERNEL = 39
    BERNOULLI = 40
    LOG_UNIFORM = 41
    DISCRETE = 42
    MULTIUNIFORM = 43
    LAMBDA = 44
    POISSON = 45

    @staticmethod
    def from_str(label: str):
        """Convert string to DistributionType."""
        if not isinstance(label, str):
            raise TypeError(f"String was expected, but `{type(label)}` was given.")
        label = label.upper()
        if label == "EXTERNALCOHERENCE":
            return DistributionType.EXTERNALCOHERENCE
        elif label == "UNTYPED":
            return DistributionType.UNTYPED
        elif label == "EXTERNAL":
            return DistributionType.EXTERNAL
        elif label == "UNIFORM":
            return DistributionType.UNIFORM
        elif label == "NORMAL":
            return DistributionType.NORMAL
        elif label == "TRUNCATEDNORMAL":
            return DistributionType.TRUNCATEDNORMAL
        elif label == "LOGNORMAL":
            return DistributionType.LOGNORMAL
        elif label == "EXPONENTIAL":
            return DistributionType.EXPONENTIAL
        elif label == "RAYLEIGH":
            return DistributionType.RAYLEIGH
        elif label == "SMALL_I":
            return DistributionType.SMALL_I
        elif label == "LARGE_I":
            return DistributionType.LARGE_I
        elif label == "SMALL_II":
            return DistributionType.SMALL_II
        elif label == "LARGE_II":
            return DistributionType.LARGE_II
        elif label == "SMALL_III":
            return DistributionType.SMALL_III
        elif label == "LARGE_III":
            return DistributionType.LARGE_III
        elif label == "TRIANGULAR":
            return DistributionType.TRIANGULAR
        elif label == "BETA":
            return DistributionType.BETA
        elif label == "CHI_SQUARE":
            return DistributionType.CHI_SQUARE
        elif label == "ERLANG":
            return DistributionType.ERLANG
        elif label == "FISHER_F":
            return DistributionType.FISHER_F
        elif label == "GAMMA":
            return DistributionType.GAMMA
        elif label == "PARETO":
            return DistributionType.PARETO
        elif label == "WEIBULL":
            return DistributionType.WEIBULL
        elif label == "EXTREME_VALUE":
            return DistributionType.EXTREME_VALUE
        elif label == "STUDENTS_F":
            return DistributionType.STUDENTS_F
        elif label == "INVERSE_NORMAL":
            return DistributionType.INVERSE_NORMAL
        elif label == "LOG_GAMMA":
            return DistributionType.LOG_GAMMA
        elif label == "LOG_NORMAL":
            return DistributionType.LOG_NORMAL
        elif label == "LORENTZ":
            return DistributionType.LORENTZ
        elif label == "FISHER_TIPPETT":
            return DistributionType.FISHER_TIPPETT
        elif label == "GUMBEL":
            return DistributionType.GUMBEL
        elif label == "FISHER_Z":
            return DistributionType.FISHER_Z
        elif label == "LAPLACE":
            return DistributionType.LAPLACE
        elif label == "LEVY":
            return DistributionType.LEVY
        elif label == "LOGISTIC":
            return DistributionType.LOGISTIC
        elif label == "ROSSI":
            return DistributionType.ROSSI
        elif label == "FRECHET":
            return DistributionType.FRECHET
        elif label == "MAX_TYPE":
            return DistributionType.MAX_TYPE
        elif label == "POLYMAP":
            return DistributionType.POLYMAP
        elif label == "KERNEL":
            return DistributionType.KERNEL
        elif label == "BERNOULLI":
            return DistributionType.BERNOULLI
        elif label == "LOG_UNIFORM":
            return DistributionType.LOG_UNIFORM
        elif label == "DISCRETE":
            return DistributionType.DISCRETE
        elif label == "MULTIUNIFORM":
            return DistributionType.MULTIUNIFORM
        elif label == "LAMBDA":
            return DistributionType.LAMBDA
        elif label == "POISSON":
            return DistributionType.POISSON
        else:
            raise ValueError(f"Status `{label}` not available in DistributionType types.")


class DesignParameter:
    """This class stores design parameters data."""

    def __init__(self, name: str, reference_value: float):
        """Create a new instance of DesignParameter.

        Parameters
        ----------
        name: str
            Name of the parameter.
        reference_value: float
            Parameters reference value.
        """
        self.name = name
        self.reference_value = reference_value

    def __eq__(self, other: DesignParameter):
        r"""Compare properties of two instances of "DesignParameter" class.

        Parameters
        ----------
        other: DesignParameter
            Parameter for comparison.

        Returns
        -------
        bool
            ``True`` if all properties match; ``False`` otherwise.
        """
        if type(self) == type(other):
            checks = []
            checks.append(self.name == other.name)
            checks.append(self.reference_value == other.reference_value)
            return False not in checks
        else:
            return False


class Parameter(DesignParameter):
    """This class stores parameters data."""

    def __init__(
        self, name: str, reference_value: float, id: str, const: bool, type: ParameterType
    ):
        """Create a new instance of Parameter.

        Parameters
        ----------
        name: str
            Name of the parameter.
        reference_value: float
            Parameters reference value.
        id: str
            Parameters unique id.
        const: bool
            Determines whether is parameter constant.
        type: ParameterType
            Parameters type.
        """
        super().__init__(name=name, reference_value=reference_value)
        self.id = id
        self.const = const
        self.type = type

    def __eq__(self, other: Parameter):
        r"""Compare properties of two instances of "Parameter" class.

        Parameters
        ----------
        other: Parameter
            Parameter for comparison.

        Returns
        -------
        bool
            ``True`` if all properties match; ``False`` otherwise.
        """
        if type(self) == type(other):
            checks = {}
            checks["name"] = self.name == other.name
            checks["reference_value"] = self.reference_value == other.reference_value
            checks["id"] = self.id == other.id
            checks["const"] = self.const == other.const
            checks["type"] = self.type == other.type
            return False not in checks.values()
        else:
            return False

    @staticmethod
    def from_dict(par_dict: dict) -> Parameter:
        """Create instance of Parameter class from optiSLang output.

        Parameters
        ----------
        par_dict : dict
            Output from optiSLang server.

        Returns
        -------
        Parameter
            Instance of Parameter class.

        Raises
        ------
        TypeError
            Raised when undefined type of parameter is given.
        """
        type = ParameterType.from_str(par_dict["type"]["value"])

        if type == ParameterType.DEPENDENT:
            return DependentParameter.from_dict(par_dict=par_dict)
        elif type == ParameterType.DETERMINISTIC:
            return OptimizationParameter.from_dict(par_dict=par_dict)
        elif type == ParameterType.STOCHASTIC:
            return StochasticParameter.from_dict(par_dict=par_dict)
        elif type == ParameterType.MIXED:
            return MixedParameter.from_dict(par_dict=par_dict)
        else:
            raise TypeError("Undefined type of parameter.")


class OptimizationParameter(Parameter):
    """This class stores OptimizationParameters data."""

    def __init__(
        self,
        name: str,
        reference_value: float = 0,
        id: str = str(uuid.uuid4()),
        const: bool = False,
        type: ParameterType = ParameterType.DETERMINISTIC,
        value_type: ParameterValueType = ParameterValueType.REAL,
        deterministic_resolution: ParameterResolution = ParameterResolution.CONTINUOUS,
        range: tuple = (-1, 1),
    ):
        """Create a new instance of OptimizationParameter.

        Parameters
        ----------
        name: str
            Name of the parameter.
        reference_value: float, optional
            Parameters reference value.
        id: str, optional
            Parameters unique id.
        const: bool, optional
            Determines whether is parameter constant.
        type: ParameterType, optional
            Parameters type.
        value_type: ParameterValueType, optional
            Parameters value type.
        deterministic_resolution: ParameterResolution, optional
            Parameters deterministic resolution.
        range: tuple, optional
            Either 2 values specifying range or list of discrete values.
        """
        super().__init__(name=name, reference_value=reference_value, id=id, const=const, type=type)
        self.value_type = value_type
        self.deterministic_resolution = deterministic_resolution
        self.range = range

    def __eq__(self, other: OptimizationParameter):
        r"""Compare properties of two instances of "OptimizationParameter" class.

        Parameters
        ----------
        other: OptimizationParameter
            Parameter for comparison.

        Returns
        -------
        bool
            ``True`` if all properties match; ``False`` otherwise.
        """
        if type(self) == type(other):
            checks = {}
            checks["name"] = self.name == other.name
            checks["reference_value"] = self.reference_value == other.reference_value
            checks["id"] = self.id == other.id
            checks["const"] = self.const == other.const
            checks["type"] = self.type == other.type
            checks["value_type"] = self.value_type == other.value_type
            checks["deterministic_resolution"] = (
                self.deterministic_resolution == other.deterministic_resolution
            )
            checks["range"] = self.range == other.range
            return False not in checks.values()
        else:
            return False

    @staticmethod
    def from_dict(par_dict: dict) -> OptimizationParameter:
        """Create instance of OptimizationParameter class from optiSLang output.

        Parameters
        ----------
        par_dict : dict
            Output from optiSLang server.

        Returns
        -------
        OptimizationParameter
            Instance of Parameter class.
        """
        name = par_dict["name"]
        reference_value = par_dict["reference_value"]
        id = par_dict["id"]
        const = par_dict["const"]
        type = ParameterType.from_str(par_dict["type"]["value"])
        value_type = ParameterValueType.from_str(
            par_dict.get("deterministic_property", {}).get("domain_type", {}).get("value", None)
        )
        deterministic_resolution = ParameterResolution.from_str(
            par_dict.get("deterministic_property", {}).get("kind", {}).get("value", None)
        )
        # range for continuous parameters, stored as (val1, val2)
        if deterministic_resolution == ParameterResolution.CONTINUOUS:
            range = (
                par_dict.get("deterministic_property", {}).get("lower_bound", None),
                par_dict.get("deterministic_property", {}).get("upper_bound", None),
            )
        # discrete values otherwise, stored as ([val1, val2, val3 ..])
        else:
            range = (par_dict.get("deterministic_property", {}).get("discrete_states", None),)
        return OptimizationParameter(
            name=name,
            reference_value=reference_value,
            id=id,
            const=const,
            type=type,
            value_type=value_type,
            deterministic_resolution=deterministic_resolution,
            range=range,
        )

    def to_dict(self) -> dict:
        """Convert parameter to input dictionary for optiSLang server.

        Returns
        -------
        dict
            Input dictionary for optiSLang server.

        Raises
        ------
        TypeError
            Raised when parameter is modified to unknown type.
        """
        if len(self.range) == 1:
            range_dict = {"discrete_states": self.range[0]}
        else:
            range_dict = {
                "lower_bound": self.range[0],
                "upper_bound": self.range[1],
            }
        output_dict = {
            "active": True,
            "const": self.const if self.const is not None else False,
            "deterministic_property": {
                "domain_type": {"value": self.value_type.name.lower()},
                "kind": {"value": self.deterministic_resolution.name.lower()},
            },
            "id": self.id,
            "modifiable": False,
            "name": self.name,
            "reference_value": self.reference_value,
            "removable": True,
            "type": {"value": "deterministic"},
            "unit": "",
        }
        output_dict["deterministic_property"].update(range_dict)
        return output_dict


class StochasticParameter(Parameter):
    """This class stores StochasticParameters data."""

    def __init__(
        self,
        name: str,
        reference_value: float = 0,
        id: str = str(uuid.uuid4()),
        const: bool = False,
        type: ParameterType = ParameterType.STOCHASTIC,
        value_type: ParameterValueType = ParameterValueType.REAL,
        stochastic_resolution: ParameterResolution = ParameterResolution.MARGINALDISTRIBUTION,
        distribution_type: DistributionType = DistributionType.NORMAL,
        distribution_parameters: Tuple[float, ...] = (0, 1),
        mean: float = None,
        standard_deviation: float = None,
        covariance: float = None,
    ):
        """Create a new instance of StochasticParameter.

        Parameters
        ----------
        name: str
            Name of the parameter.
        reference_value: float, optional
            Parameters reference value.
        id: str, optional
            Parameters unique id.
        const: bool, optional
            Determines whether is parameter constant.
        type: ParameterType, optional
            Parameters type.
        value_type: ParameterValueType, optional
            Parameters value type.
        stochastic_resolution: ParameterResolution, optional
            Parameters stochastic resolution.
        distribution_type: DistributionType, optional
            Parameters distribution type.
        distribution_parameters: Tuple[float, ...], optional
            Distributions parameters.
        mean: float, optional
            Mean value.
        standard_deviation: float, optional
            Standard deviation value.
        covariance: float, optional
            Covariance value.
        """
        super().__init__(name=name, reference_value=reference_value, id=id, const=const, type=type)
        self.value_type = value_type
        self.stochastic_resolution = stochastic_resolution
        self.distribution_type = distribution_type
        self.distribution_parameters = distribution_parameters
        self.mean = mean
        self.standard_deviation = standard_deviation
        self.covariance = covariance

    def __eq__(self, other: StochasticParameter):
        r"""Compare properties of two instances of "StochasticParameter" class.

        Parameters
        ----------
        other: StochasticParameter
            Parameter for comparison.

        Returns
        -------
        bool
            ``True`` if all properties match; ``False`` otherwise.
        """
        if type(self) == type(other):
            checks = {}
            checks["name"] = self.name == other.name
            checks["reference_value"] = self.reference_value == other.reference_value
            checks["id"] = self.id == other.id
            checks["const"] = self.const == other.const
            checks["type"] = self.type == other.type
            checks["value_type"] = self.value_type == other.value_type
            checks["stochastic_resolution"] = (
                self.stochastic_resolution == other.stochastic_resolution
            )
            checks["distribution_type"] = self.distribution_type == other.distribution_type
            checks["distribution_parameters"] = (
                self.distribution_parameters == other.distribution_parameters
            )
            return False not in checks.values()
        else:
            return False

    @staticmethod
    def from_dict(par_dict: dict) -> StochasticParameter:
        """Create instance of StochasticParameter class from optiSLang output.

        Parameters
        ----------
        par_dict : dict
            Output from optiSLang server.

        Returns
        -------
        StochasticParameter
            Instance of Parameter class.
        """
        name = par_dict["name"]
        reference_value = par_dict["reference_value"]
        id = par_dict["id"]
        const = par_dict["const"]
        type = ParameterType.from_str(par_dict["type"]["value"])
        value_type = ParameterValueType.REAL
        stochastic_resolution = ParameterResolution.from_str(
            par_dict.get("stochastic_property", {}).get("kind", {}).get("value", None)
        )
        distribution_type = DistributionType.from_str(
            par_dict.get("stochastic_property", {}).get("type", {}).get("value", None)
        )
        # TODO: parameter.mean=
        # TODO: parameter.standard_deviation=
        # TODO: parameter.covariance=
        distribution_parameters = tuple(
            par_dict.get("stochastic_property", {}).get("statistical_moments", None)
        )
        return StochasticParameter(
            name=name,
            reference_value=reference_value,
            id=id,
            const=const,
            type=type,
            value_type=value_type,
            stochastic_resolution=stochastic_resolution,
            distribution_type=distribution_type,
            distribution_parameters=distribution_parameters,
        )

    def to_dict(self) -> dict:
        """Convert StochasticParameter to input dictionary for optiSLang server.

        Returns
        -------
        dict
            Input dictionary for optiSLang server.

        Raises
        ------
        TypeError
            Raised when parameter is modified to unknown type.
        """
        return {
            "active": True,
            "const": self.const if self.const is not None else False,
            "id": self.id,
            "modifiable": False,
            "name": self.name,
            "reference_value": self.reference_value,
            "removable": True,
            "stochastic_property": {
                "kind": {"value": self.stochastic_resolution.name.lower()},
                "statistical_moments": self.distribution_parameters,
                "type": {"value": self.distribution_type.name.lower()},
            },
            "type": {"value": "stochastic"},
            "unit": "",
        }


class MixedParameter(Parameter):
    """This class stores MixedParameters data."""

    def __init__(
        self,
        name: str,
        reference_value: float = 0,
        id: str = str(uuid.uuid4()),
        const: bool = False,
        type: ParameterType = ParameterType.MIXED,
        value_type: ParameterValueType = ParameterValueType.REAL,
        deterministic_resolution: ParameterResolution = ParameterResolution.CONTINUOUS,
        range: tuple = (-1, 1),
        stochastic_resolution: ParameterResolution = ParameterResolution.MARGINALDISTRIBUTION,
        distribution_type: DistributionType = DistributionType.NORMAL,
        distribution_parameters: Tuple[float, ...] = (0, 1),
        mean: float = None,
        standard_deviation: float = None,
        covariance: float = None,
    ):
        """Create a new instance of MixedParameter.

        Parameters
        ----------
        name: str
            Name of the parameter.
        reference_value: float, optional
            Parameters reference value.
        id: str, optional
            Parameters unique id.
        const: bool, optional
            Determines whether is parameter constant.
        type: ParameterType, optional
            Parameters type.
        value_type: ParameterValueType, optional
            Parameters value type.
        deterministic_resolution: ParameterResolution, optional
            Parameters deterministic resolution.
        range: tuple, optional
            Either 2 values specifying range or list of discrete values.
        stochastic_resolution: ParameterResolution, optional
            Parameters stochastic resolution.
        distribution_type: DistributionType, optional
            Parameters distribution type.
        distribution_parameters: Tuple[float, ...], optional
            Distributions parameters.
        mean: float, optional
            Mean value.
        standard_deviation: float, optional
            Standard deviation value.
        covariance: float, optional
            Covariance value.
        """
        super().__init__(name=name, reference_value=reference_value, id=id, const=const, type=type)
        self.value_type = value_type
        self.deterministic_resolution = deterministic_resolution
        self.range = range
        self.stochastic_resolution = stochastic_resolution
        self.distribution_type = distribution_type
        self.distribution_parameters = distribution_parameters
        self.mean = mean
        self.standard_deviation = standard_deviation
        self.covariance = covariance

    def __eq__(self, other: MixedParameter):
        r"""Compare properties of two instances of "MixedParameter" class.

        Parameters
        ----------
        other: MixedParameter
            Parameter for comparison.

        Returns
        -------
        bool
            ``True`` if all properties match; ``False`` otherwise.
        """
        if type(self) == type(other):
            checks = {}
            checks["name"] = self.name == other.name
            checks["reference_value"] = self.reference_value == other.reference_value
            checks["id"] = self.id == other.id
            checks["const"] = self.const == other.const
            checks["type"] = self.type == other.type
            checks["value_type"] = self.value_type == other.value_type
            checks["deterministic_resolution"] = (
                self.deterministic_resolution == other.deterministic_resolution
            )
            checks["range"] = self.range == other.range
            checks["stochastic_resolution"] = (
                self.stochastic_resolution == other.stochastic_resolution
            )
            checks["distribution_type"] = self.distribution_type == other.distribution_type
            checks["distribution_parameters"] = (
                self.distribution_parameters == other.distribution_parameters
            )
            return False not in checks.values()
        else:
            return False

    @staticmethod
    def from_dict(par_dict: dict) -> MixedParameter:
        """Create instance of MixedParameter class from optiSLang output.

        Parameters
        ----------
        par_dict : dict
            Output from optiSLang server.

        Returns
        -------
        MixedParameter
            Instance of MixedParameter class.
        """
        # create `Parameter` instance with mandatory parameters
        name = par_dict["name"]
        reference_value = par_dict["reference_value"]
        id = par_dict["id"]
        const = par_dict["const"]
        type = ParameterType.from_str(par_dict["type"]["value"])
        value_type = ParameterValueType.from_str(
            par_dict.get("deterministic_property", {}).get("domain_type", {}).get("value", None)
        )
        deterministic_resolution = ParameterResolution.from_str(
            par_dict.get("deterministic_property", {}).get("kind", {}).get("value", None)
        )
        stochastic_resolution = ParameterResolution.from_str(
            par_dict.get("stochastic_property", {}).get("kind", {}).get("value", None)
        )

        # range for continuous parameters, stored as (val1, val2)
        if deterministic_resolution == ParameterResolution.CONTINUOUS:
            range = (
                par_dict.get("deterministic_property", {}).get("lower_bound", None),
                par_dict.get("deterministic_property", {}).get("upper_bound", None),
            )
        # discrete values otherwise, stored as ([val1, val2, val3 ..])
        else:
            range = (par_dict.get("deterministic_property", {}).get("discrete_states", None),)

        distribution_type = DistributionType.from_str(
            par_dict.get("stochastic_property", {}).get("type", {}).get("value", None)
        )
        distribution_parameters = tuple(
            par_dict.get("stochastic_property", {}).get("statistical_moments", None)
        )
        # TODO: parameter.mean=
        # TODO: parameter.standard_deviation=
        # TODO: parameter.covariance=
        return MixedParameter(
            name=name,
            reference_value=reference_value,
            id=id,
            const=const,
            type=type,
            value_type=value_type,
            deterministic_resolution=deterministic_resolution,
            stochastic_resolution=stochastic_resolution,
            range=range,
            distribution_type=distribution_type,
            distribution_parameters=distribution_parameters,
        )

    def to_dict(self) -> dict:
        """Convert parameter to input dictionary for optiSLang server.

        Returns
        -------
        dict
            Input dictionary for optiSLang server.

        Raises
        ------
        TypeError
            Raised when parameter is modified to unknown type.
        """
        if len(self.range) == 1:
            range_dict = {"discrete_states": self.range[0]}
        else:
            range_dict = {
                "lower_bound": self.range[0],
                "upper_bound": self.range[1],
            }
        output_dict = {
            "active": True,
            "const": self.const if self.const is not None else False,
            "deterministic_property": {
                "domain_type": {"value": self.value_type.name.lower()},
                "kind": {"value": self.deterministic_resolution.name.lower()},
            },
            "id": self.id,
            "modifiable": False,
            "name": self.name,
            "reference_value": self.reference_value if self.reference_value else 0,
            "removable": True,
            "stochastic_property": {
                "kind": {"value": self.stochastic_resolution.name.lower()},
                "statistical_moments": self.distribution_parameters,
                "type": {"value": self.distribution_type.name.lower()},
            },
            "type": {"value": "mixed"},
            "unit": "",
        }

        output_dict["deterministic_property"].update(range_dict)
        return output_dict


class DependentParameter(Parameter):
    """This class stores DependentParameters data."""

    def __init__(
        self,
        name: str,
        reference_value: float = 0,
        id: str = str(uuid.uuid4()),
        const: bool = False,
        type: ParameterType = ParameterType.DEPENDENT,
        operation: str = "0",
    ):
        """Create a new instance of DependentParameter.

        Parameters
        ----------
        name: str
            Name of the parameter.
        reference_value: float, optional
            Parameters reference value.
        id: str, optional
            Parameters unique id.
        const: bool, optional
            Determines whether is parameter constant.
        type: ParameterType, optional
            Parameters type.
        operation: str, optional
            Mathematic expression to be evaluated.
        """
        super().__init__(name=name, reference_value=reference_value, id=id, const=const, type=type)
        self.operation = operation

    def __eq__(self, other: DependentParameter):
        r"""Compare properties of two instances of "DependentParameter" class.

        Parameters
        ----------
        other: DependentParameter
            Parameter for comparison.

        Returns
        -------
        bool
            ``True`` if all properties match; ``False`` otherwise.
        """
        if type(self) == type(other):
            checks = {}
            checks["name"] = self.name == other.name
            checks["reference_value"] = self.reference_value == other.reference_value
            checks["id"] = self.id == other.id
            checks["const"] = self.const == other.const
            checks["type"] = self.type == other.type
            checks["operation"] = self.operation == other.operation
            return False not in checks.values()
        else:
            return False

    @staticmethod
    def from_dict(par_dict: dict) -> DependentParameter:
        """Create instance of Parameter class from optiSLang output.

        Parameters
        ----------
        par_dict : dict
            Output from optiSLang server.

        Returns
        -------
        Parameter
            Instance of Parameter class.
        """
        name = par_dict["name"]
        reference_value = par_dict["reference_value"]
        id = par_dict["id"]
        const = par_dict["const"]
        type = ParameterType.from_str(par_dict["type"]["value"])
        operation = par_dict.get("dependency_expression")

        return DependentParameter(
            name=name,
            reference_value=reference_value,
            id=id,
            const=const,
            type=type,
            operation=operation,
        )

    def to_dict(self) -> dict:
        """Convert parameter to input dictionary for optiSLang server.

        Returns
        -------
        dict
            Input dictionary for optiSLang server.

        Raises
        ------
        TypeError
            Raised when parameter is modified to unknown type.
        """
        return {
            "active": True,
            "const": self.const if self.const is not None else False,
            "dependency_expression": self.operation if self.operation is not None else 0,
            "id": self.id,
            "modifiable": False,
            "name": self.name,
            "reference_value": self.reference_value if self.reference_value is not None else None,
            "removable": True,
            "type": {"value": "dependent"},
            "unit": "",
        }


class ParameterManager:
    """This class contains methods to obtain parameters.

    Parameters
    ----------
    uid: str
        Specific unique ID.

    Raises
    ------
    OslCommunicationError
        Raised when an error occurs while communicating with server.
    OslCommandError
        Raised when the command or query fails.
    TimeoutError
        Raised when the timeout float value expires.
    """

    def __init__(self, uid: str, osl_server: OslServer) -> None:
        """Initialize a new instance of ParameterManager."""
        self.__uid = uid
        self.__osl_server = osl_server

    def __str__(self) -> str:
        """Return list of parameters."""
        return str(self.get_parameters_names())

    def get_parameters(self) -> Tuple[Parameter, ...]:
        """Get parameters of object (project, system) defined by uid.

        Returns
        -------
        Tuple[Parameter, ...]
            Tuple of defined parameters.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        props = self.__osl_server.get_actor_properties(uid=self.__uid)
        container = props["properties"].get("ParameterManager", {}).get("parameter_container", [])
        parameters = []
        for par_dict in container:
            parameters.append(Parameter.from_dict(par_dict))
        return tuple(parameters)

    def get_parameters_names(self) -> Tuple[str, ...]:
        """Get parameters list of object (project, system) defined by uid.

        Returns
        -------
        Tuple[str, ...]
            Tuple of defined parameters names.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        props = self.__osl_server.get_actor_properties(uid=self.__uid)
        container = props["properties"].get("ParameterManager", {}).get("parameter_container", [])
        parameters_list = []
        for par in container:
            parameters_list.append(par["name"])
        return tuple(parameters_list)


class DesignStatus(Enum):
    """Available design statuses."""

    IDLE = 0
    PENDING = 1
    SUCCEEDED = 2
    FAILED = 3

    @staticmethod
    def from_str(label: str):
        """Convert string to DesignStatus."""
        if not isinstance(label, str):
            raise TypeError(f"String was expected, but `{type(label)}` was given.")
        label = label.upper()
        if label == "IDLE":
            return DesignStatus.IDLE
        elif label == "PENDING":
            return DesignStatus.PENDING
        elif label == "SUCCEEDED":
            return DesignStatus.SUCCEEDED
        elif label == "FAILED":
            return DesignStatus.FAILED
        else:
            raise ValueError(f"Status `{label}` not available in DesignStatus states.")


class Design:
    """Class which stores information about design point, exclusive for RootSystem.

    Parameters
    ----------
    parameters: Union[Dict[str, float], Iterable[Parameter]], optional
        Dictionary of parameters and it's values {'parname': value, ...}
        or iterable of DesignParameters.

    Examples
    --------
    Create new design from Optislang class:

    >>> from ansys.optislang.core import Optislang
    >>> osl = Optislang()
    >>> project = osl.get_project()
    >>> root_system = project.root_system
    >>> design = root_system.create_design(parameters = {'a': 1})
    >>> design.set_parameter(parameter = 'b', value = 2)
    >>> design.set_parameters(parameters = {'c': 3, 'd': 4})
    >>> print(design)
    >>> osl.dispose()

    Create new design independently of Optislang class:

    >>> from ansys.optislang.core.project_parametric import Design
    >>> design = Design(parameters = {'a': 5})

    Create design with Parameter instances:

    >>> from ansys.optislang.core.project_parametric import DesignParameter
    >>> par1 = DesignParameter(name='a', reference_value = 5)
    >>> par2 = DesignParameter(name='b', reference_value = 10)
    >>> design = Design(parameters = [par1, par2])
    """

    def __init__(self, parameters: Union[Dict[str, float], Iterable[DesignParameter]] = None):
        """Initialize a new instance of ``Design`` class."""
        self.__criteria = {}
        self.__feasibility = "NOT_EVALUATED"
        self.__id = "NOT_ASSIGNED"
        self.__parameters = {}
        self.__responses = {}
        self.__status = DesignStatus.IDLE

        if parameters is not None:
            self.set_parameters(parameters)

    def __str__(self) -> str:
        """Return info about design."""
        return (
            "----------------------------------------------------------------------\n"
            f"ID: {self.id}\n"
            f"Status: {self.__status}\n"
            f"Feasibility: {self.__feasibility}\n"
            f"Criteria: {self.__criteria}\n"
            f"Parameters: {self.__parameters}\n"
            f"Responses: {self.__responses}\n"
            "----------------------------------------------------------------------"
        )

    @property
    def id(self) -> int:
        """Return designs ID."""
        return self.__id

    @property
    def status(self) -> str:
        """Return status of design."""
        return self.__status.name

    @property
    def criteria(self) -> Dict:
        """Return all defined criteria."""
        return self.__criteria

    @property
    def parameters(self) -> Dict:
        """Return all parameters."""
        return self.__parameters

    @property
    def responses(self) -> Dict:
        """Return all responses."""
        return self.__responses

    def remove_parameters(self, to_be_removed: Union[str, Iterable[str]] = None) -> None:
        """Remove parameters defined in ``to_be_removed`` from design.

        Parameters
        ----------
        to_be_removed: Union[str, Iterable[str]], opt
            Name of single parameter or Iterable of parameters to be removed.
            If not specified, all parameters are removed.
        """
        if not to_be_removed:
            self.__parameters.clear()
        elif isinstance(to_be_removed, str):
            self.__parameters.pop(to_be_removed, None)
        else:
            for parameter in to_be_removed:
                self.__parameters.pop(parameter, None)

    def reset(self) -> None:
        """Reset status and delete output values."""
        self.__status = DesignStatus.IDLE
        self.__feasibility = "NOT_EVALUATED"
        self.__responses = {}

    def set_parameter(
        self, parameter: Union[str, Parameter], value: float = None, reset_output: bool = True
    ) -> None:
        """Set value of parameter.

        Parameters
        ----------
        parameter: Union[str, Parameter]
            Name of parameter or Parameter
        value: float
            Value of parameter, not used if instance of Parameter was passed in parameter.
        reset_output: bool, optional
            Remove responses, default value ``True``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        TypeError
            Raised when invalid type of parameter is passed.
        """
        if reset_output:
            self.reset()
        if isinstance(parameter, str):
            parameter = DesignParameter(name=parameter, reference_value=value)
        if not isinstance(parameter, DesignParameter):
            raise TypeError(f"Invalid type of parameter: `{type(parameter)}`.")
        self.__parameters[parameter.name] = parameter

    def set_parameters(
        self,
        parameters: Union[Dict[str, float], Iterable[DesignParameter]],
        reset_output: bool = True,
    ) -> None:
        """Set multiple parameters values.

        Parameters
        ----------
        parameters: Union[Dict[str, float], Iterable[DesignParameter]]
            Dictionary of parameters and it's values {'parname': value, ...}
            or iterable of DesignParameters.
        reset_output: bool, optional
            Remove responses, default value ``True``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        if reset_output:
            self.reset()
        if isinstance(parameters, dict):
            for parname, value in parameters.items():
                self.set_parameter(parameter=parname, value=value)
        else:
            for parameter in parameters:
                self.set_parameter(parameter=parameter)

    def _receive_results(self, results: Dict) -> None:
        """Receive results and store them in responses.

        Parameters
        ----------
        results: Dict
            Output from ``evaluate_design`` server command.
        """
        for position, response in enumerate(results["result_design"]["response_names"]):
            self.__responses[response] = DesignParameter(
                name=response, reference_value=results["result_design"]["response_values"][position]
            )
        if results["status"] == "success":
            self.__status = DesignStatus.SUCCEEDED
        else:
            self.__status = DesignStatus.FAILED
        self.__feasibility = results["result_design"]["feasible"]
