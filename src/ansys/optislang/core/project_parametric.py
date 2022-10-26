"""Contains classes ParameterManager, DesignStatus and Design."""
from enum import Enum
from typing import TYPE_CHECKING, Dict, Iterable, List, Union

from ansys.optislang.core import server_queries as queries

if TYPE_CHECKING:
    from ansys.optislang.core.osl_server import OslServer


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

    def __init__(self, uid: str, osl_server: "OslServer") -> None:
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
        props = self.__osl_server._send_command(queries.actor_properties(uid))
        container = props["properties"].get("ParameterManager", {}).get("parameter_container", [])
        parameters = {}
        for par in container:
            parameters[par["name"]] = {
                # independent
                "parameter_type": container[0]["type"]["value"],
                "reference_value": container[0]["reference_value"],
                "is_constant": par["const"],
                # dependent (return `None` if key not available)
                "operation": par.get("dependency_expression", None),
                "value_type": container[0]
                .get("deterministic_property", {})
                .get("domain_type", {})
                .get("value", None),
                "resolution": container[0].get("deterministic_property", {}).get("kind", None),
                "range": [
                    container[0].get("deterministic_property", {}).get("lower_bound", None),
                    container[0].get("deterministic_property", {}).get("upper_bound", None),
                ],
                "distribution_type": par.get("stochastic_property", {})
                .get("type", {})
                .get("value", None),
                "distribution_params": par.get("stochastic_property", {}).get(
                    "statistical_moments", None
                ),
            }
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
        props = self.__osl_server._send_command(queries.actor_properties(uid))
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


class Design:
    """Class which stores information about design point.

    Currently it cannot create new parameters and criteria in optiSLang project, these has to be
    created in project beforehand.

    Parameters
    ----------
    inputs: Dict, opt
        Dictionary of parameters and it's values {'parname': value, ...}.

    Examples
    --------
    Create new design from Optislang class:
    >>> from ansys.optislang.core import Optislang
    >>> osl = Optislang()
    >>> design = osl.create_design(inputs = {'a': 1})
    >>> design.set_parameter(parameter = 'b', value = 2)
    >>> design.set_parameters(parameters = {'c': 3, 'd': 4})
    >>> print(design)
    >>> osl.shutdown()

    Create new design independently of Optislang class:
    >>> from ansys.optislang.core.nodes import Design
    >>> design = Design(inputs = {'a': 5})
    """

    def __init__(self, inputs: Dict = None):
        """Initialize a new instance of ``Design`` class."""
        self.__criteria = {}
        self.__feasibility = "NOT_EVALUATED"
        self.__id = "NOT ASSIGNED"
        self.__parameters = {}
        self.__responses = {}
        self.__status = DesignStatus.IDLE.name

        if inputs is not None:
            self.set_parameters(inputs)

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
        """Return all parameters input values."""
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

    def set_parameter(self, parameter: str, value: float, reset_output: bool = True) -> None:
        """Set input value of parameter.

        Parameters
        ----------
        parameter: str
            Name of parameter.
        value: float
            Value of parameter.
        reset_output: bool, optional
            Remove responses, default value ``True``.
        """
        if reset_output:
            self.reset()
        self.__parameters[parameter] = value

    def set_parameters(self, parameters: Dict, reset_output: bool = True) -> None:
        """Set multiple input values of parameters.

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
            self.__parameters[key] = value

    def _receive_results(self, results: Dict):
        """Receive results and store them in outputs.

        Parameters
        ----------
        results: Dict
            Output from ``evaluate_design`` server command.
        """
        for position, response in enumerate(results["result_design"]["response_names"]):
            print(response)
            self.__responses[response] = results["result_design"]["response_values"][position]
        if results["status"] == "success":
            self.__status = DesignStatus.SUCCEEDED.name
        else:
            self.__status = DesignStatus.FAILED.name
        self.__feasibility = results["result_design"]["feasible"]
