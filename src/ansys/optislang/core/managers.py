# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Contains abstract classes for obtaining and operating with project parametric."""
from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Iterable, Optional, Tuple, Union

if TYPE_CHECKING:
    from pathlib import Path

    from ansys.optislang.core.io import File
    from ansys.optislang.core.osl_server import OslServer
    from ansys.optislang.core.project_parametric import (
        Criterion,
        Design,
        DesignStatus,
        Parameter,
        Response,
    )


class CriteriaManager:
    """Base classes for classes that obtains and operate with criteria."""

    @abstractmethod
    def __init__(self, uid: str, osl_server: OslServer) -> None:  # pragma: no cover
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


class DesignManager:
    """Base classes for classes that obtains and operate with designs."""

    @abstractmethod
    def __init__(self, uid: str, osl_server: OslServer) -> None:  # pragma: no cover
        """``DesignManager`` class is an abstract base class and cannot be instantiated."""
        pass

    @abstractmethod
    def get_design(self, id: str) -> Design:  # pragma: no cover
        """Get design by id.

        Parameters
        ----------
        id : str
            Design id.

        Returns
        -------
        Design
            Design object.

        Notes
        -----
        Information about `pareto_design` property is not provided by this query.
        """
        pass

    @abstractmethod
    def get_designs(
        self,
        hid: Optional[str] = None,
        include_design_values=True,
        include_non_scalar_design_values=False,
    ) -> Tuple[Design]:  # pragma: no cover
        """Get designs for a given state.

        Parameters
        ----------
        hid : Optional[str], optional
            State/Design hierarchical id. By default ``None``.
        include_design_values : bool, optional
            Include values. By default ``True``.
        include_non_scalar_design_values : Optional[bool], optional
            Include non scalar values. By default ``False``.

        Returns
        -------
        Tuple[Design]
            Tuple of designs for a given state.
        """
        pass

    @abstractmethod
    def save_designs_as_json(
        self, hid: str, file_path: Union[Path, str]
    ) -> File:  # pragma: no cover
        """Save designs for a given state to JSON file.

        Parameters
        ----------
        hid : str
            Actor's state.
        file_path : Union[Path, str]
            Path to the file.

        Returns
        -------
        File
            Object representing saved file.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        TypeError
            Raised when the `hid` is `None`
            -or-
            `file_path` is `None` or unsupported type.
        ValueError
            Raised when ``hid`` does not exist.
        """
        pass

    @abstractmethod
    def save_designs_as_csv(
        self, hid: str, file_path: Union[Path, str]
    ) -> File:  # pragma: no cover
        """Save designs for a given state to CSV file.

        Parameters
        ----------
        hid : str
            Actor's state.
        file_path : Union[Path, str]
            Path to the file.

        Returns
        -------
        File
            Object representing saved file.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        TypeError
            Raised when the `hid` is `None`
            -or-
            `file_path` is `None` or unsupported type.
        ValueError
            Raised when ``hid`` does not exist.
        """
        pass

    @staticmethod
    @abstractmethod
    def filter_designs_by(
        designs: Iterable[Design],
        hid: Optional[str] = None,
        status: Optional[DesignStatus] = None,
        pareto_design: Optional[bool] = None,
        feasible: Optional[bool] = None,
    ) -> Tuple[Design]:  # pragma: no cover
        """Filter designs by given parameters.

        Parameters
        ----------
        designs : Iterable[Design]
            Designs to be filtered.
        hid : Optional[str], optional
            State/Design hierarchical id. By default ``None``.
        status : Optional[DesignStatus], optional
            Design status. By default ``None``.
        pareto_design : Optional[bool], optional
            Pareto flag. By default ``None``.
        feasible : Optional[bool], optional
            Feasibility of design. By default ``None``.

        Returns
        -------
        Tuple[Design]
            Tuple of filtered designs
        """
        pass

    @staticmethod
    @abstractmethod
    def sort_designs_by_hid(designs: Iterable[Design]) -> Tuple[Design]:  # pragma: no cover
        """Sort designs by hierarchical id.

        Parameters
        ----------
        designs : Iterable[Design]
            Designs to be sorted.

        Returns
        -------
        Tuple[Design]
            Tuple of sorted designs.
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
        self, parameter_name: str, property_name: str, property_value: Any
    ) -> None:  # pragma: no cover
        """Modify property of parameter in the system.

        Parameters
        ----------
        parameter_name: str
            Name of the parameter to be modified.
        property_name: str
            Name of the property to be modified.
        property_value: Any
            New value of the modified property.

        Raises
        ------
        NameError
            Raised when the parameter with the given name doesn't exists.
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
