"""Contains abstract classes for obtaining and operating with project parametric."""
from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Tuple

from ansys.optislang.core.project_parametric import Criterion, Parameter, Response

if TYPE_CHECKING:
    from ansys.optislang.core.osl_server import OslServer


class CriteriaManager:
    """Base classes for classes that obtains and operate with criteria."""

    @abstractmethod
    def __init__(self) -> None:  # pragma: no cover
        """``CriteriaManager`` class is an abstract base class and cannot be instantiated."""
        pass

    @abstractmethod
    def get_criteria(self) -> Tuple[Criterion, ...]:  # pragma: no cover
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
        pass

    @abstractmethod
    def get_criteria_names(self) -> Tuple[str, ...]:  # pragma: no cover
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
        pass


class ParameterManager:
    """Base classes for classes that obtains and operate with parameters."""

    @abstractmethod
    def __init__(self, uid: str, osl_server: OslServer) -> None:  # pragma: no cover
        """``ParameterManager`` class is an abstract base class and cannot be instantiated."""
        pass

    @abstractmethod
    def get_parameters(self) -> Tuple[Parameter, ...]:  # pragma: no cover
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
        pass

    @abstractmethod
    def get_parameters_names(self) -> Tuple[str, ...]:  # pragma: no cover
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
        pass


class ResponseManager:
    """Base classes for classes that obtains and operate with responses."""

    @abstractmethod
    def __init__(self, uid: str, osl_server: OslServer) -> None:  # pragma: no cover
        """``ResponseManager`` class is an abstract base class and cannot be instantiated."""
        pass

    @abstractmethod
    def get_responses(self) -> Tuple[Response, ...]:  # pragma: no cover
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
        pass

    @abstractmethod
    def get_responses_names(self) -> Tuple[str, ...]:  # pragma: no cover
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
        pass
