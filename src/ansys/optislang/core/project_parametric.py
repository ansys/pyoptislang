"""Contains classes ParameterManager, DesignStatus and Design."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Dict, Iterable, List, Union

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
        """Convert string to ParameterResolution."""
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
            raise ValueError(f"Status `{label}` not available in ParameterResolution kinds.")


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


@dataclass
class Parameter:
    """This class stores parameters data."""

    name: str
    reference_value: Union[int, float]
    const: bool = None
    type: str = None
    operation: str = None
    value_type: str = None
    resolution: str = None
    range: tuple = None
    distribution_type: str = None
    mean: Union[int, float] = None
    standard_deviation: Union[int, float] = None
    covariance: Union[int, float] = None
    distribution_parameters: tuple = None


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
        return str(self.__get_parameters_list)

    def __get_parameters(self, uid: str) -> Dict:
        """Get parameters of object (project, system) defined by uid.

        Parameters
        ----------
        uid: str
            Specific unique ID.

        Returns
        -------
        Dict
            Dictionary of defined parameters.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        props = self.__osl_server.get_actor_properties(uid=uid)
        container = props["properties"].get("ParameterManager", {}).get("parameter_container", [])
        parameters = {}
        for par in container:
            # create `Parameter` instance with mandatory parameters
            par: dict
            parameter = Parameter(
                name=par["name"],
                reference_value=par["reference_value"],
                const=par["const"],
                type=ParameterType.from_str(par["type"]["value"]),
            )

            # parameters dependent on parameter type:

            # only dependent parameter has 'dependency_expression'
            if parameter.type == ParameterType.DEPENDENT:
                parameter.operation = par.get("dependency_expression")

            # different keys for 'value_type' and 'resolution'
            # in (Deterministic, Mixed) and Stochastic parameters
            if parameter.type in [ParameterType.DETERMINISTIC, ParameterType.MIXED]:
                parameter.value_type = ParameterValueType.from_str(
                    par.get("deterministic_property", {}).get("domain_type", {}).get("value", None)
                )
                parameter.resolution = ParameterResolution.from_str(
                    par.get("deterministic_property", {}).get("kind", {}).get("value", None)
                )
            elif parameter.type == ParameterType.STOCHASTIC:
                parameter.value_type = ParameterValueType.REAL
                parameter.resolution = ParameterResolution.from_str(
                    par.get("stochastic_property", {}).get("kind", {}).get("value", None)
                )

            # range used only with Deterministic and Mixed parameters
            if parameter.type in [ParameterType.DETERMINISTIC, ParameterType.MIXED]:
                # range for continuous parameters, stored as (val1, val2)
                if parameter.resolution == ParameterResolution.CONTINUOUS:
                    parameter.range = (
                        par.get("deterministic_property", {}).get("lower_bound", None),
                        par.get("deterministic_property", {}).get("upper_bound", None),
                    )
                # discrete values otherwise, stored as ([val1, val2, val3 ..])
                else:
                    parameter.range = par.get("deterministic_property", {}).get(
                        "discrete_states", None
                    )

            # distribution parameteres are used only with Stochastic and Mixed parameters
            if parameter.type in [ParameterType.STOCHASTIC, ParameterType.MIXED]:
                parameter.distribution_type = DistributionType.from_str(
                    par.get("stochastic_property", {}).get("type", {}).get("value", None)
                )
                # TODO: parameter.mean=
                # TODO: parameter.standard_deviation=
                # TODO: parameter.covariance=
                parameter.distribution_parameters = par.get("stochastic_property", {}).get(
                    "statistical_moments", None
                )
            parameters[par["name"]] = parameter
        return parameters

    def __get_parameters_list(self, uid: str) -> List:
        """Get parameters list of object (project, system) defined by uid.

        Parameters
        ----------
        uid: str
            Specific unique ID.

        Returns
        -------
        List
            List of defined parameters.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        props = self.__osl_server.get_actor_properties(uid=uid)
        container = props["properties"].get("ParameterManager", {}).get("parameter_container", [])
        parameters_list = []
        for par in container:
            parameters_list.append(par["name"])
        return parameters_list

    @property
    def parameters_list(self) -> List:
        """Get list of defined parameters."""
        return self.__get_parameters_list(self.__uid)

    @property
    def parameters(self) -> Dict:
        """Get dictionary of defined parameters."""
        return self.__get_parameters(self.__uid)


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
    """Class which stores information about design point.

    Currently it cannot create new parameters and criteria in optiSLang project, these has to be
    created in project beforehand.

    Parameters
    ----------
    parameters: Dict, opt
        Dictionary of parameters and it's values {'parname': value, ...}.

    Examples
    --------
    Create new design from Optislang class:
    >>> from ansys.optislang.core import Optislang
    >>> osl = Optislang()
    >>> design = osl.create_design(parameters = {'a': 1})
    >>> design.set_parameter(parameter = 'b', value = 2)
    >>> design.set_parameters(parameters = {'c': 3, 'd': 4})
    >>> print(design)
    >>> osl.shutdown()

    Create new design independently of Optislang class:
    >>> from ansys.optislang.core.project_parametric import Design
    >>> design = Design(parameters = {'a': 5})

    Create design with Parameter instances
    >>> from ansys.optislang.core.project_parametric import Parameter
    >>> par1 = Parameter(name='a', reference_value = 5)
    >>> design = Design(parameters = {'a': par1})
    """

    def __init__(self, parameters: Dict = None):
        """Initialize a new instance of ``Design`` class."""
        self.__criteria = {}
        self.__feasibility = "NOT_EVALUATED"
        self.__id = "NOT ASSIGNED"
        self.__parameters = {}
        self.__responses = {}
        self.__status = DesignStatus.IDLE.name

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
    def status(self) -> bool:
        """Return status of design."""
        return self.__status

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
        self.__status = DesignStatus.IDLE.name
        self.__feasibility = "NOT_EVALUATED"
        self.__responses = {}

    def set_parameter(
        self, parameter: str, value: Union[float, Parameter], reset_output: bool = True
    ) -> None:
        """Set value of parameter.

        Parameters
        ----------
        parameter: str
            Name of parameter.
        value: Union[float, Parameter]
            Value of parameter or instance of Parameter class.
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
        if not isinstance(value, Parameter):
            value = Parameter(name=parameter, reference_value=value)

        if not parameter in self.__parameters:
            self.__parameters[parameter] = value
        else:
            self.__parameters[parameter].reference_value = value.reference_value

    def set_parameters(self, parameters: Dict, reset_output: bool = True) -> None:
        """Set multiple parameters values.

        Parameters
        ----------
        parameters: Dict
            Dictionary of parameters and it's values {'parname': value, ...}.
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
        for key, value in parameters.items():
            self.set_parameter(parameter=key, value=value)

    def _receive_results(self, results: Dict):
        """Receive results and store them in responses.

        Parameters
        ----------
        results: Dict
            Output from ``evaluate_design`` server command.
        """
        for position, response in enumerate(results["result_design"]["response_names"]):
            self.__responses[response] = Parameter(
                name=response, reference_value=results["result_design"]["response_values"][position]
            )
        if results["status"] == "success":
            self.__status = DesignStatus.SUCCEEDED.name
        else:
            self.__status = DesignStatus.FAILED.name
        self.__feasibility = results["result_design"]["feasible"]
