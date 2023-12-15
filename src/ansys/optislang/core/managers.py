"""Contains abstract classes for obtaining and operating with project parametric."""
from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Tuple

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
    def add_criterion(self, criterion: Criterion) -> None:  # pragma: no cover
        """Add criterion to the system.

        Returns
        -------
        Criterion
            Criterion to be created in the system.

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

    @abstractmethod
    def modify_criterion(self, criterion: Criterion) -> None:  # pragma: no cover
        """Modify criterion in the system.

        Parameters
        ----------
        criterion : Criterion
            Criterion to be modified. Criterion name is used as idefentifier.

        Raises
        ------
        NotImplementedError
            Raised when unsupported optiSLang server is used.
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def modify_criterion_property(
        self, criterion_name: str, property_name: str, property_value: Any
    ) -> None:  # pragma: no cover
        """Modify property of criterion in the system.

        Parameters
        ----------
        criterion_name : str
            Name of criterion to be modified.
        property_name: str
            Name of property to be modified.
        property_value: Any
            New value of the modified property.

        Raises
        ------
        NotImplementedError
            Raised when unsupported optiSLang server is used.
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def remove_all_criteria(self) -> None:  # pragma: no cover
        """Remove all criteria from the system.

        Raises
        ------
        NotImplementedError
            Raised when unsupported optiSLang server is used.
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def remove_criterion(self, criterion_name: str) -> None:  # pragma: no cover
        """Remove criterion from the system.

        Parameters
        ----------
        criterion_name : str
            Name of the criterion to be removed.

        Raises
        ------
        NotImplementedError
            Raised when unsupported optiSLang server is used.
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
    def add_parameter(self, parameter: Parameter) -> None:  # pragma: no cover
        """Add parameter to the system.

        Returns
        -------
        Parameter
            Parameter to be created in the system.

        Raises
        ------
        NameError
            Raised when parameter with given name already exists.
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
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

    @abstractmethod
    def modify_parameter(self, parameter: Parameter):  # pragma: no cover
        """Modify parameter in the system.

        Parameters
        ----------
        parameter: Parameter
            Parameter to be modified. Parameter name is used as identifier.

        Raises
        ------
        NameError
            Raised when the parameter with the given name doesn't exist.
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def modify_parameter_property(
        self, parameter_name: str, property_name: str, value: Any
    ) -> None:  # pragma: no cover
        """Modify property of parameter in the system.

        Returns
        -------
        Parameter
            Parameter to be modified. Parameter name is used as identifier.

        Raises
        ------
        NameError
            Raised when the parameter with the given name already exists.
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def remove_all_parameters(self) -> None:  # pragma: no cover
        """Remove all parameters from the system.

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
    def remove_parameter(self, parameter_name: str) -> None:  # pragma: no cover
        """Remove parameter from the system.

        Parameters
        ----------
        parameter_name : str
            Name of the parameter to be removed.

        Raises
        ------
        NotImplementedError
            Raised when unsupported optiSLang server is used.
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
