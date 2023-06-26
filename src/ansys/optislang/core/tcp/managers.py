"""Contains classes to obtain operate with project parametric."""
from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

from ansys.optislang.core.managers import CriteriaManager, ParameterManager, ResponseManager
from ansys.optislang.core.project_parametric import Criterion, Parameter, Response

if TYPE_CHECKING:
    from ansys.optislang.core.tcp.osl_server import TcpOslServer


class TcpCriteriaManagerProxy(CriteriaManager):
    """Contains methods for obtaining criteria."""

    def __init__(self, uid: str, osl_server: TcpOslServer) -> None:
        """Initialize a new instance of the ``TcpCriteriaManagerProxy`` class.

        Parameters
        ----------
        uid: str
            Unique ID of the instance.
        osl_server: TcpOslServer
            Object providing access to the optiSLang server.
        """
        self.__uid = uid
        self.__osl_server = osl_server

    def __str__(self) -> str:
        """Get the unique ID of the criteria manager."""
        return f"CriteriaManager uid: {self.__uid}"

    def get_criteria(self) -> Tuple[Criterion, ...]:
        """Get the criteria of the system.

        Returns
        -------
        Tuple[Criterion, ...]
            Tuple of the criterion for the system.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        props = self.__osl_server.get_actor_properties(uid=self.__uid)
        container = props.get("properties", {}).get("Criteria", {}).get("sequence", [{}])
        criteria = []
        for criterion_dict in container:
            criteria.append(Criterion.from_dict(criterion_dict))
        return tuple(criteria)

    def get_criteria_names(self) -> Tuple[str, ...]:
        """Get all criteria names.

        Returns
        -------
        Tuple[str, ...]
            Tuple of all criteria names.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        props = self.__osl_server.get_actor_properties(uid=self.__uid)
        container = props.get("properties", {}).get("Criteria", {}).get("sequence", [{}])
        criteria_list = []
        for par in container:
            criteria_list.append(par["First"])
        return tuple(criteria_list)


class TcpParameterManagerProxy(ParameterManager):
    """Contains methods for obtaining parameters."""

    def __init__(self, uid: str, osl_server: TcpOslServer) -> None:
        """Initialize a new instance of the ``TcpParameterManagerProxy`` class.

        Parameters
        ----------
        uid: str
            Unique ID of the instance.
        osl_server: TcpOslServer
            Object providing access to the optiSLang server.
        """
        self.__uid = uid
        self.__osl_server = osl_server

    def __str__(self) -> str:
        """Get the unique ID of the parameter manager."""
        return f"ParameterManager uid: {self.__uid}"

    def get_parameters(self) -> Tuple[Parameter, ...]:
        """Get the parameters of the system.

        Returns
        -------
        Tuple[Parameter, ...]
            Tuple of the parameters for the system.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
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
        """Get all parameter names.

        Returns
        -------
        Tuple[str, ...]
            Tuple of all parameter names.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        props = self.__osl_server.get_actor_properties(uid=self.__uid)
        container = props["properties"].get("ParameterManager", {}).get("parameter_container", [])
        parameters_list = []
        for par in container:
            parameters_list.append(par["name"])
        return tuple(parameters_list)


class TcpResponseManagerProxy(ResponseManager):
    """Contains methods for obtaining responses."""

    def __init__(self, uid: str, osl_server: TcpOslServer) -> None:
        """Initialize a new instance of the ``TcpResponseManagerProxy`` class.

        Parameters
        ----------
        uid: str
            Unique ID of the instance.
        osl_server: TcpOslServer
            Object providing access to the optiSLang server.
        """
        self.__uid = uid
        self.__osl_server = osl_server

    def __str__(self) -> str:
        """Get the unique ID of the response manager."""
        return f"ResponseManager uid: {self.__uid}"

    def get_responses(self) -> Tuple[Response, ...]:
        """Get the responses of the system.

        Returns
        -------
        Tuple[Criterion, ...]
            Tuple of the responses for the system.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        info = self.__osl_server.get_actor_info(uid=self.__uid)
        container = info.get("responses", {})
        responses = []
        for key, res_dict in container.items():
            responses.append(Response.from_dict(key, res_dict))
        return tuple(responses)

    def get_responses_names(self) -> Tuple[str, ...]:
        """Get all responses names.

        Returns
        -------
        Tuple[str, ...]
            Tuple of all responses names.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        info = self.__osl_server.get_actor_info(uid=self.__uid)
        container = info.get("responses", {})
        return tuple(container.keys())
