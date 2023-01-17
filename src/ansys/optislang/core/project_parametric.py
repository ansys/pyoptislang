"""Contains classes Parameter, ParameterManager and Design."""
from __future__ import annotations

import copy
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Tuple, Union
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
        try:
            parameter_type = eval("ParameterType." + label)
            return parameter_type
        except:
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
        try:
            parameter_resolution = eval("ParameterResolution." + label)
            return parameter_resolution
        except:
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
        try:
            parameter_value_type = eval("ParameterValueType." + label)
            return parameter_value_type
        except:
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
        try:
            distribution_type = eval("DistributionType." + label)
            return distribution_type
        except:
            raise ValueError(f"Status `{label}` not available in DistributionType types.")


class Parameter:
    """This class stores parameters data."""

    def __init__(
        self,
        name: str,
        reference_value: Union[bool, float, str, None, Tuple[Any, ParameterValueType]],
        id: str,
        const: bool,
        type: ParameterType,
        reference_value_type: ParameterValueType = None,
    ) -> None:
        """Create a new instance of Parameter.

        Parameters
        ----------
        name: str
            Name of the parameter.
        reference_value: Union[bool, float, str, None, Tuple[Any, ParameterValueType]]
            Parameters reference value.
        id: str
            Parameters unique id.
        const: bool
            Determines whether is parameter constant.
        type: ParameterType
            Parameters type.
        reference_value_type: ParameterValueType, optional
            Type of the reference value.
        """
        self.name = name
        if isinstance(reference_value_type, ParameterValueType):
            self.reference_value = tuple([reference_value, reference_value_type])
        else:
            self.__reference_value_type = None
            self.reference_value = reference_value
        self.id = id
        self.const = const
        self.type = type

    def __eq__(self, other: Parameter):
        r"""Compare properties of two instances of the "Parameter" class.

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
            checks["reference_value_type"] = self.reference_value_type == other.reference_value_type
            checks["id"] = self.id == other.id
            checks["const"] = self.const == other.const
            checks["type"] = self.type == other.type
            return False not in checks.values()
        else:
            return False

    def __deepcopy__(self, memo) -> Parameter:
        """Return deep copy of the parameter."""
        return Parameter(
            self.name,
            self.reference_value,
            self.reference_value_type,
            self.id,
            self.const,
            self.type,
        )

    @property
    def reference_value(
        self,
    ) -> Union[bool, float, str, None]:
        """Return parameters reference value."""
        return self.__reference_value

    @reference_value.setter
    def reference_value(
        self, reference_value: Union[bool, float, str, None, Tuple[Any, ParameterValueType]]
    ) -> None:
        """Set reference value."""
        if isinstance(reference_value, bool):
            self.__reference_value_type = ParameterValueType.BOOL
        elif isinstance(reference_value, float):
            self.__reference_value_type = ParameterValueType.REAL
        elif isinstance(reference_value, int):
            if not self.__reference_value_type == ParameterValueType.INTEGER:
                self.__reference_value_type = ParameterValueType.REAL
        elif isinstance(reference_value, str):
            self.__reference_value_type = ParameterValueType.STRING
        elif reference_value == None:
            self.__reference_value_type = ParameterValueType.UNINITIALIZED
        elif isinstance(reference_value, tuple):
            if not isinstance(reference_value[1], ParameterValueType):
                raise ValueError(f"Tuple must be in format Tuple[Any, ParameterValueType].")
            self.__reference_value = reference_value[0]
            self.__reference_value_type = reference_value[1]
            return
        else:
            raise TypeError(f"Unsupported type of reference_value: ``{type(reference_value)}``.")
        self.__reference_value = reference_value

    @property
    def reference_value_type(self) -> ParameterValueType:
        """Return type of the reference value."""
        return self.__reference_value_type

    @property
    def type(self) -> ParameterType:
        """Return type of the parameter."""
        return self.__type

    @type.setter
    def type(self, type_: Union[ParameterType, str]) -> None:
        """Set type of the parameter."""
        if isinstance(type_, str):
            type_ = ParameterType.from_str(type)
        if isinstance(type_, ParameterType):
            self.__type = type_
        else:
            raise TypeError(
                "Type Union[ParameterType, str] was expected, but type: "
                f"``{type(type_)}`` was given."
            )

    @staticmethod
    def from_dict(par_dict: dict) -> Parameter:
        """Create an instance of Parameter class from optiSLang output.

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
        reference_value: Union[bool, float, str, None, Tuple[Any, ParameterValueType]] = 0,
        reference_value_type: ParameterValueType = None,
        id: str = str(uuid.uuid4()),
        const: bool = False,
        type: Union[ParameterType, str] = ParameterType.DETERMINISTIC,
        deterministic_resolution: Union[ParameterResolution, str] = ParameterResolution.CONTINUOUS,
        range: tuple = (-1, 1),
    ) -> None:
        """Create a new instance of OptimizationParameter.

        Parameters
        ----------
        name: str
            Name of the parameter.
        reference_value: Union[bool, float, str, None, Tuple[Any, ParameterValueType]], optional
            Parameters reference value.
        reference_value_type: ParameterValueType, optional
            Type of the reference value.
        id: str, optional
            Parameters unique id.
        const: bool, optional
            Determines whether is parameter constant.
        type: Union[ParameterType, str], optional
            Parameters type.
        deterministic_resolution: Union[ParameterResolution, str], optional
            Parameters deterministic resolution.
        range: tuple, optional
            Either 2 values specifying range or list of discrete values.
        """
        super().__init__(
            name=name,
            reference_value=reference_value,
            id=id,
            const=const,
            type=type,
            reference_value_type=reference_value_type,
        )
        self.deterministic_resolution = deterministic_resolution
        self.range = range

    def __eq__(self, other: OptimizationParameter):
        r"""Compare properties of two instances of the "OptimizationParameter" class.

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
            checks["reference_value_type"] = self.reference_value_type == other.reference_value_type
            checks["id"] = self.id == other.id
            checks["const"] = self.const == other.const
            checks["type"] = self.type == other.type
            checks["deterministic_resolution"] = (
                self.deterministic_resolution == other.deterministic_resolution
            )
            checks["range"] = self.range == other.range
            return False not in checks.values()
        else:
            return False

    def __deepcopy__(self, memo) -> OptimizationParameter:
        """Return deep copy of the optimization parameter."""
        return OptimizationParameter(
            self.name,
            self.reference_value,
            self.id,
            self.const,
            self.type,
            self.reference_value_type,
            self.deterministic_resolution,
            self.range,
        )

    @property
    def deterministic_resolution(self) -> ParameterResolution:
        """Return deterministic resolution type."""
        return self.__deterministic_resolution

    @deterministic_resolution.setter
    def deterministic_resolution(
        self, deterministic_resolution: Union[ParameterResolution, str]
    ) -> None:
        """Set deterministic resolution type."""
        if isinstance(deterministic_resolution, str):
            deterministic_resolution = ParameterResolution.from_str(deterministic_resolution)
        if isinstance(deterministic_resolution, ParameterResolution):
            self.__deterministic_resolution = deterministic_resolution
        else:
            raise TypeError(
                "Type Union[ParameterResolution, str] was expected, but type: "
                f"``{type(deterministic_resolution)}`` was given."
            )

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
        id = par_dict["id"]
        const = par_dict["const"]
        type = ParameterType.from_str(par_dict["type"]["value"])
        reference_value_type = ParameterValueType.from_str(
            par_dict.get("deterministic_property", {}).get("domain_type", {}).get("value", None)
        )
        reference_value = par_dict["reference_value"]
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
            reference_value_type=reference_value_type,
            id=id,
            const=const,
            type=type,
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
                "domain_type": {"value": self.reference_value_type.name.lower()},
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
        reference_value: Union[bool, float, str, None, Tuple[Any, ParameterValueType]] = 0,
        reference_value_type: ParameterValueType = None,
        id: str = str(uuid.uuid4()),
        const: bool = False,
        type: Union[ParameterType, str] = ParameterType.STOCHASTIC,
        stochastic_resolution: Union[
            ParameterResolution, str
        ] = ParameterResolution.MARGINALDISTRIBUTION,
        distribution_type: Union[DistributionType, str] = DistributionType.NORMAL,
        distribution_parameters: Tuple[float, ...] = (0, 1),
        mean: float = None,
        standard_deviation: float = None,
        covariance: float = None,
    ) -> None:
        """Create a new instance of StochasticParameter.

        Parameters
        ----------
        name: str
            Name of the parameter.
        reference_value: Union[bool, float, str, None, Tuple[Any, ParameterValueType]], optional
            Parameters reference value.
        reference_value_type: ParameterValueType, optional
            Type of the reference value.
        id: str, optional
            Parameters unique id.
        const: bool, optional
            Determines whether is parameter constant.
        type: Union[ParameterType, str], optional
            Parameters type.
        stochastic_resolution: Union[ParameterResolution, str], optional
            Parameters stochastic resolution.
        distribution_type: Union[DistributionType, str], optional
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
        super().__init__(
            name=name,
            reference_value=reference_value,
            id=id,
            const=const,
            type=type,
            reference_value_type=reference_value_type,
        )
        self.stochastic_resolution = stochastic_resolution
        self.distribution_type = distribution_type
        self.distribution_parameters = distribution_parameters
        self.mean = mean
        self.standard_deviation = standard_deviation
        self.covariance = covariance

    def __eq__(self, other: StochasticParameter):
        r"""Compare properties of two instances of the "StochasticParameter" class.

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
            checks["reference_value_type"] = self.reference_value_type == other.reference_value_type
            checks["id"] = self.id == other.id
            checks["const"] = self.const == other.const
            checks["type"] = self.type == other.type
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

    def __deepcopy__(self, memo) -> StochasticParameter:
        """Return deep copy of the stochastic parameter."""
        return StochasticParameter(
            self.name,
            self.reference_value,
            self.id,
            self.const,
            self.type,
            self.reference_value_type,
            self.stochastic_resolution,
            self.distribution_type,
            self.distribution_parameters,
        )

    @property
    def stochastic_resolution(self) -> ParameterResolution:
        """Return stochastic resolution type."""
        return self.__stochastic_resolution

    @stochastic_resolution.setter
    def stochastic_resolution(self, stochastic_resolution: Union[ParameterResolution, str]) -> None:
        """Set stochastic resolution type."""
        if isinstance(stochastic_resolution, str):
            stochastic_resolution = ParameterResolution.from_str(stochastic_resolution)
        if isinstance(stochastic_resolution, ParameterResolution):
            self.__stochastic_resolution = stochastic_resolution
        else:
            raise TypeError(
                "Type Union[ParameterResolution, str] was expected, but type: "
                f"``{type(stochastic_resolution)}`` was given."
            )

    @property
    def distribution_type(self) -> DistributionType:
        """Return distribution type."""
        return self.__distribution_type

    @distribution_type.setter
    def distribution_type(self, distribution_type: Union[DistributionType, str]):
        """Set distribution type."""
        if isinstance(distribution_type, str):
            distribution_type = DistributionType.from_str(distribution_type)
        if isinstance(distribution_type, DistributionType):
            self.__distribution_type = distribution_type
        else:
            raise TypeError(
                "Type Union[DistributionType, str] was expected, but type: "
                f"``{type(distribution_type)}`` was given."
            )

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
            reference_value_type=ParameterValueType.REAL,
            id=id,
            const=const,
            type=type,
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
        reference_value: Union[bool, float, str, None, Tuple[Any, ParameterValueType]] = 0,
        reference_value_type: ParameterValueType = None,
        id: str = str(uuid.uuid4()),
        const: bool = False,
        type: Union[ParameterType, str] = ParameterType.MIXED,
        deterministic_resolution: Union[ParameterResolution, str] = ParameterResolution.CONTINUOUS,
        range: tuple = (-1, 1),
        stochastic_resolution: Union[
            ParameterResolution, str
        ] = ParameterResolution.MARGINALDISTRIBUTION,
        distribution_type: Union[DistributionType, str] = DistributionType.NORMAL,
        distribution_parameters: Tuple[float, ...] = (0, 1),
        mean: float = None,
        standard_deviation: float = None,
        covariance: float = None,
    ) -> None:
        """Create a new instance of MixedParameter.

        Parameters
        ----------
        name: str
            Name of the parameter.
        reference_value: Union[bool, float, str, None, Tuple[Any, ParameterValueType]], optional
            Parameters reference value.
        reference_value_type: ParameterValueType, optional
            Type of the reference value.
        id: str, optional
            Parameters unique id.
        const: bool, optional
            Determines whether is parameter constant.
        type: Union[ParameterType, str], optional
            Parameters type.
        deterministic_resolution: Union[ParameterResolution, str], optional
            Parameters deterministic resolution.
        range: tuple, optional
            Either 2 values specifying range or list of discrete values.
        stochastic_resolution: Union[ParameterResolution, str], optional
            Parameters stochastic resolution.
        distribution_type: Union[DistributionType, str], optional
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
        super().__init__(
            name=name,
            reference_value=reference_value,
            id=id,
            const=const,
            type=type,
            reference_value_type=reference_value_type,
        )
        self.deterministic_resolution = deterministic_resolution
        self.range = range
        self.stochastic_resolution = stochastic_resolution
        self.distribution_type = distribution_type
        self.distribution_parameters = distribution_parameters
        self.mean = mean
        self.standard_deviation = standard_deviation
        self.covariance = covariance

    def __eq__(self, other: MixedParameter):
        r"""Compare properties of two instances of the "MixedParameter" class.

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
            checks["reference_value_type"] = self.reference_value_type == other.reference_value_type
            checks["id"] = self.id == other.id
            checks["const"] = self.const == other.const
            checks["type"] = self.type == other.type
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

    def __deepcopy__(self, memo) -> MixedParameter:
        """Return deep copy of the mixed parameter."""
        return MixedParameter(
            self.name,
            self.reference_value,
            self.id,
            self.const,
            self.type,
            self.reference_value_type,
            self.deterministic_resolution,
            self.range,
            self.stochastic_resolution,
            self.distribution_type,
            self.distribution_parameters,
        )

    @property
    def deterministic_resolution(self) -> ParameterResolution:
        """Return deterministic resolution type."""
        return self.__deterministic_resolution

    @deterministic_resolution.setter
    def deterministic_resolution(
        self, deterministic_resolution: Union[ParameterResolution, str]
    ) -> None:
        """Set deterministic resolution type."""
        if isinstance(deterministic_resolution, str):
            deterministic_resolution = ParameterResolution.from_str(deterministic_resolution)
        if isinstance(deterministic_resolution, ParameterResolution):
            self.__deterministic_resolution = deterministic_resolution
        else:
            raise TypeError(
                "Type Union[ParameterResolution, str] was expected, but type: "
                f"``{type(deterministic_resolution)}`` was given."
            )

    @property
    def stochastic_resolution(self) -> ParameterResolution:
        """Return stochastic resolution type."""
        return self.__stochastic_resolution

    @stochastic_resolution.setter
    def stochastic_resolution(self, stochastic_resolution: Union[ParameterResolution, str]) -> None:
        """Set stochastic resolution type."""
        if isinstance(stochastic_resolution, str):
            stochastic_resolution = ParameterResolution.from_str(stochastic_resolution)
        if isinstance(stochastic_resolution, ParameterResolution):
            self.__stochastic_resolution = stochastic_resolution
        else:
            raise TypeError(
                "Type Union[ParameterResolution, str] was expected, but type: "
                f"``{type(stochastic_resolution)}`` was given."
            )

    @property
    def distribution_type(self) -> DistributionType:
        """Return distribution type."""
        return self.__distribution_type

    @distribution_type.setter
    def distribution_type(self, distribution_type: Union[DistributionType, str]):
        """Set distribution type."""
        if isinstance(distribution_type, str):
            distribution_type = DistributionType.from_str(distribution_type)
        if isinstance(distribution_type, DistributionType):
            self.__distribution_type = distribution_type
        else:
            raise TypeError(
                "Type Union[DistributionType, str] was expected, but type: "
                f"``{type(distribution_type)}`` was given."
            )

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
        reference_value_type = ParameterValueType.from_str(
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
            reference_value_type=reference_value_type,
            id=id,
            const=const,
            type=type,
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
                "domain_type": {"value": self.reference_value_type.name.lower()},
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
        reference_value: Union[bool, float, str, None, Tuple[Any, ParameterValueType]] = 0,
        reference_value_type: ParameterValueType = None,
        id: str = str(uuid.uuid4()),
        const: bool = False,
        type: Union[ParameterType, str] = ParameterType.DEPENDENT,
        operation: str = "0",
    ) -> None:
        """Create a new instance of DependentParameter.

        Parameters
        ----------
        name: str
            Name of the parameter.
        reference_value: Union[bool, float, str, None, Tuple[Any, ParameterValueType]], optional
            Parameters reference value.
        reference_value_type: ParameterValueType, optional
            Type of the reference value.
        id: str, optional
            Parameters unique id.
        const: bool, optional
            Determines whether is parameter constant.
        type: Union[ParameterType, str], optional
            Parameters type.
        operation: str, optional
            Mathematic expression to be evaluated.
        """
        super().__init__(
            name=name,
            reference_value=reference_value,
            id=id,
            const=const,
            type=type,
            reference_value_type=reference_value_type,
        )
        self.operation = operation

    def __eq__(self, other: DependentParameter):
        r"""Compare properties of two instances of the "DependentParameter" class.

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
            checks["reference_value_type"] = self.reference_value_type == other.reference_value_type
            checks["id"] = self.id == other.id
            checks["const"] = self.const == other.const
            checks["type"] = self.type == other.type
            checks["operation"] = self.operation == other.operation
            return False not in checks.values()
        else:
            return False

    def __deepcopy__(self, memo) -> DependentParameter:
        """Return deep copy of the dependent parameter."""
        return DependentParameter(
            self.name,
            self.reference_value,
            self.reference_value_type,
            self.id,
            self.const,
            self.type,
            self.operation,
        )

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
        """Get tuple of systems parameters.

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
        """Get names of systems parameters.

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


class DesignVariable:
    """Class which stores information about design variable or response."""

    def __init__(
        self,
        name: str,
        value: Union[bool, float, complex, list, dict, None],
    ) -> None:
        """Initialize a new instance of ``DesignVariable`` class.

        Parameters
        ----------
        name: str
            Criterium name.
        value: Union[bool, float, complex, list, dict, None]
            Criterion  value.
        """
        self.name = name
        self.value = value

    def __deepcopy__(self, memo) -> DesignVariable:
        """Return deep copy of the design variable."""
        return DesignVariable(
            self.name,
            self.value,
        )

    def __eq__(self, other: DesignVariable):
        r"""Compare properties of two instances of the "DesignVariable" class.

        Parameters
        ----------
        other: DesignVariable
            Variable for comparison.

        Returns
        -------
        bool
            ``True`` if all properties match; ``False`` otherwise.
        """
        if type(self) == type(other):
            checks = {}
            checks["name"] = self.name == other.name
            checks["value"] = self.value == other.value
            return False not in checks.values()
        else:
            return False

    @property
    def name(self) -> str:
        """Return variable name."""
        return self.__name

    @name.setter
    def name(self, name: str):
        """Set variable name."""
        if not isinstance(name, str):
            raise TypeError(f"String was expected but type: ``{type(name)}`` was given.")
        else:
            self.__name = name

    @property
    def value(self) -> Union[bool, float, complex, list, dict, None]:
        """Return variable value."""
        return self.__value

    @value.setter
    def value(self, value: Union[bool, float, complex, list, dict, None]) -> None:
        """Set variable value."""
        self.__value = value


class DesignStatus(Enum):
    """Available design states."""

    IDLE = 0
    PENDING = 1
    SUCCEEDED = 2
    NOT_SUCCEEDED = 3
    FAILED = 4

    @staticmethod
    def from_str(label: str):
        """Convert string to DesignStatus."""
        if not isinstance(label, str):
            raise TypeError(f"String was expected, but `{type(label)}` was given.")
        label = label.upper()
        label = label.replace(" ", "_")
        try:
            design_status = eval("DesignStatus." + label)
            return design_status
        except:
            raise ValueError(f"Status `{label}` not available in DesignStatus states.")


class Design:
    """Class which stores information about design point, exclusive for RootSystem.

    Parameters
    ----------
    parameters: Union[Dict[str, float], Iterable[Union[Parameter, DesignVariable]]], optional
        Dictionary of parameters and it's values {'parname': value, ...}
        or iterable of DesignVariables or Parameters.

    Examples
    --------
    Get reference design:

    >>> from ansys.optislang.core import Optislang
    >>> osl = Optislang()
    >>> root_system = osl.project.root_system
    >>> design = root_system.get_reference_design()
    >>> design.set_parameters_value(parameter = 'a', value = 2)
    >>> design.set_parameters_values(parameters = {'b': 3, 'c': 4})
    >>> print(design)
    >>> osl.dispose()
    """

    def __init__(
        self, parameters: Union[Dict[str, float], Iterable[Union[Parameter, DesignVariable]]]
    ):
        """Initialize a new instance of ``Design`` class."""
        self.__constraints: List[DesignVariable] = []
        self.__feasibility: Union[bool, None] = None
        self.__id: int = None
        self.__limit_states: List[DesignVariable] = []
        self.__objectives: List[DesignVariable] = []
        self.__parameters: List[DesignVariable] = []
        self.__responses: List[DesignVariable] = []
        self.__status: DesignStatus = DesignStatus.IDLE
        self.__variables: List[DesignVariable] = []

        if isinstance(parameters, dict):
            for name, value in parameters.items():
                self.__parameters.append(DesignVariable(name=name, value=value))
        else:
            for parameter in parameters:
                if isinstance(parameter, Parameter):
                    value = parameter.reference_value
                elif isinstance(parameter, DesignVariable):
                    value = parameter.value
                else:
                    raise TypeError(f"Parameters type: ``{type(parameter)}`` is not supported.")
                self.__parameters.append(
                    DesignVariable(
                        name=parameter.name,
                        value=value,
                    )
                )

    def __str__(self) -> str:
        """Return info about design."""
        return (
            "----------------------------------------------------------------------\n"
            f"ID: {self.id}\n"
            f"Status: {self.__status.name}\n"
            f"Feasibility: {self.__feasibility}\n"
            f"Criteria:\n"
            f"   constraints: {self.__constraints.names}\n"
            f"   objectives: {self.__objectives.names}\n"
            f"   limit_states: {self.__limit_states.names}\n"
            f"Parameters: {self.parameter_names}\n"
            f"Responses: {self.response_names}\n"
            f"Variables: {self.variable_names}"
            "----------------------------------------------------------------------"
        )

    def __deepcopy__(self, memo) -> Design:
        """Create copy of unevaluated design."""
        return Design(copy.deepcopy(self.parameters, memo))

    @property
    def feasibility(self) -> Union[bool, None]:
        """Return designs feasibility, ``None`` if not evaluated."""
        return self.__feasibility

    @property
    def id(self) -> Union[int, None]:
        """Return designs id, ``None`` if not assigned."""
        return self.__id

    @property
    def constraints(self) -> Tuple[DesignVariable, ...]:
        """Return all defined constraints."""
        return tuple(self.__constraints)

    @property
    def constraint_names(self) -> Tuple[str, ...]:
        """Return all constraint names."""
        names = []
        for constraint in self.__constraints:
            names.append(constraint.name)
        return tuple(names)

    @property
    def limit_states(self) -> Tuple[DesignVariable, ...]:
        """Return all defined limit_states."""
        return tuple(self.__limit_states)

    @property
    def limit_state_names(self) -> Tuple[str, ...]:
        """Return all constraint names."""
        names = []
        for limit_state in self.__limit_states:
            names.append(limit_state.name)
        return tuple(names)

    @property
    def objectives(self) -> Tuple[DesignVariable, ...]:
        """Return all defined objectives."""
        return tuple(self.__objectives)

    @property
    def objective_names(self) -> Tuple[str, ...]:
        """Return all objective names."""
        names = []
        for objective in self.__objectives:
            names.append(objective.name)
        return tuple(names)

    @property
    def parameters(self) -> Tuple[DesignVariable, ...]:
        """Return all parameters."""
        return tuple(self.__parameters)

    @property
    def parameter_names(self) -> Tuple[str, ...]:
        """Return all parameters names."""
        names = []
        for parameter in self.__parameters:
            names.append(parameter.name)
        return tuple(names)

    @property
    def responses(self) -> Tuple[DesignVariable, ...]:
        """Return all responses."""
        return tuple(self.__responses)

    @property
    def response_names(self) -> Tuple[str, ...]:
        """Return all response names."""
        names = []
        for response in self.__responses:
            names.append(response.name)
        return tuple(names)

    @property
    def status(self) -> DesignStatus:
        """Return status of design."""
        return self.__status

    @property
    def variables(self) -> Tuple[DesignVariable, ...]:
        """Return all variables."""
        return tuple(self.__variables)

    @property
    def variable_names(self) -> Tuple[str, ...]:
        """Return all variable names."""
        names = []
        for variable in self.__variables:
            names.append(variable.name)
        return tuple(names)

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
            index = self.__find_name_index(to_be_removed, type_="parameter")
            if index is not None:
                self.__parameters.pop(index)
        else:
            for parameter in to_be_removed:
                index = self.__find_name_index(parameter, type_="parameter")
                if index is not None:
                    self.__parameters.pop(index)

    def __reset(self) -> None:
        """Reset status and delete output values."""
        self.__status = DesignStatus.IDLE
        self.__feasibility = None
        self.__constraints.clear()
        self.__limit_states.clear()
        self.__objectives.clear()
        self.__responses.clear()
        self.__variables.clear()

    def set_parameter_value(
        self,
        parameter: Union[str, Parameter, DesignVariable],
        value: Union[str, float, bool] = None,
        reset_output: bool = True,
    ) -> None:
        """Set value of parameter.

        Parameters
        ----------
        parameter: Union[str, Parameter]
            Name of parameter or Parameter
        value: float
            Value of parameter, used only with ``type(parameter) == str``.
        reset_output: bool, optional
            Remove criteria, variables and responses, defaults to ``True``.

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
            self.__reset()

        if isinstance(parameter, str):
            index = self.__find_name_index(name=parameter, type_="parameter")
        elif isinstance(parameter, Parameter):
            index = self.__find_name_index(name=parameter.name, type_="parameter")
            value = parameter.reference_value
        elif isinstance(parameter, DesignVariable):
            index = self.__find_name_index(name=parameter.name, type_="parameter")
            name = parameter.name
            value = parameter.value
        else:
            raise TypeError(f"Invalid type of parameter: `{type(parameter)}`.")

        if index is not None:
            self.__parameters[index].value = value
        else:
            name = (
                parameter.name if isinstance(parameter, (Parameter, DesignVariable)) else parameter
            )
            self.__parameters.append(DesignVariable(name=name, value=value))

    def set_parameter_values(
        self,
        parameters: Union[Dict[str, float], Iterable[Union[DesignVariable, Parameter]]],
        reset_output: bool = True,
    ) -> None:
        """Set multiple parameters values.

        Parameters
        ----------
        parameters: Union[Dict[str, float], Iterable[Union[DesignVariable, Parameter]]]
            Dictionary of parameters and it's values {'parname': value, ...}
            or iterable of DesignVariables or Parameters.
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
            self.__reset()
        if isinstance(parameters, dict):
            for parname, value in parameters.items():
                self.set_parameter_value(parameter=parname, value=value, reset_output=False)
        else:
            for parameter in parameters:
                self.set_parameter_value(parameter=parameter, reset_output=False)

    def _receive_results(self, results: Dict) -> None:
        """Receive results and store them in responses.

        Parameters
        ----------
        results: Dict
            Output from ``evaluate_design`` server command.
        """
        self.__reset()
        self.__id = results["result_design"]["hid"]
        self.__feasibility = results["result_design"]["feasible"]
        self.__status = DesignStatus.from_str(results["result_design"]["status"])

        # constraint
        for position, constraint in enumerate(results["result_design"]["constraint_names"]):
            self.__constraints.append(
                DesignVariable(
                    name=constraint,
                    value=results["result_design"]["constraint_values"][position],
                )
            )
        # limit state
        for position, limit_state in enumerate(results["result_design"]["limit_state_names"]):
            self.__limit_states.append(
                DesignVariable(
                    name=limit_state,
                    value=results["result_design"]["limit_state_values"][position],
                )
            )
        # objective
        for position, objective in enumerate(results["result_design"]["objective_names"]):
            self.__objectives.append(
                DesignVariable(
                    name=objective,
                    value=results["result_design"]["objective_values"][position],
                )
            )
        # responses
        for position, response in enumerate(results["result_design"]["response_names"]):
            self.__responses.append(
                DesignVariable(
                    name=response,
                    value=results["result_design"]["response_values"][position],
                )
            )
        # variables
        for position, variable in enumerate(results["result_design"]["variable_names"]):
            self.__variables.append(
                DesignVariable(
                    name=variable,
                    value=results["result_design"]["variable_values"][position],
                )
            )

    def __find_name_index(self, name: str, type_: str) -> Union[int, None]:
        """Find index of the criterion, parameter, response or variable with given name.

        Parameters
        ----------
        name: str
            Name of the criterion, parameter, response or variable.
        type_: str
            Union['constraint', 'limit_state', 'objective', 'parameter', 'response', 'variable']

        Returns
        -------
        Union[int, None]
            Position in list, ``None`` if parameter wasn't found.
        """
        indices = []
        if type_ == "constraint":
            search_in = self.__constraints
        elif type_ == "limit_state":
            search_in = self.__limit_states
        elif type_ == "objective":
            search_in = self.__objectives
        elif type_ == "parameter":
            search_in = self.__parameters
        elif type_ == "response":
            search_in = self.__responses
        elif type_ == "variable":
            search_in = self.__variables
        else:
            raise TypeError(f"Unknown type_: ``{type(type_)}``.")

        for index, parameter in enumerate(search_in):
            if parameter.name == name:
                indices.append(index)
        if len(indices) > 1:
            raise NameError(f"Name `{name}` of `{type_}` is not unique.")
        elif len(indices) == 0:
            return None
        return indices[0]
