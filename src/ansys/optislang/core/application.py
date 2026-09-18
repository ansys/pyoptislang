# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Contains abstract ``Application`` class."""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Optional, Union

if TYPE_CHECKING:
    from ansys.optislang.core.osl_server import OslVersion
    from ansys.optislang.core.project import Project


class Application(ABC):
    """Base class for classes which operate with projects."""

    @abstractmethod
    def __init__(self):  # pragma: no cover
        """``Application`` class is an abstract base class and cannot be instantiated."""
        pass

    @property
    @abstractmethod
    def project(self) -> Optional[Project]:
        """Instance of the ``Project`` class.

        Returns
        -------
        Optional[Project]
            Loaded project. If no project is loaded, ``None`` is returned.
        """
        pass

    @property
    @abstractmethod
    def version(self) -> OslVersion:  # pragma: no cover
        """Version of used optiSLang.

        Returns
        -------
        OslVersion
            optiSLang version as typing.NamedTuple containing
            major, minor, maintenance and revision versions.
        """
        pass

    @property
    @abstractmethod
    def version_string(self) -> str:  # pragma: no cover
        """Version of used optiSLang.

        Returns
        -------
        str
            optiSLang version.
        """
        pass

    @abstractmethod
    def new(self) -> None:  # pragma: no cover
        """Create and open a new project.

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
    def open(
        self,
        file_path: Union[str, Path],
        force: bool = True,
        restore: bool = False,
        reset: bool = False,
        project_properties_file: Optional[str] = None,
    ) -> None:  # pragma: no cover
        """Open a project.

        Parameters
        ----------
        file_path : Union[str, pathlib.Path]
            Path to the optiSLang project file to open.
        force : bool, optional
            Whether to force opening of the project even if non-critical errors occur.
            Non-critical errors include:

            - Timestamp of the (auto) save point is newer than the project timestamp.
            - Project (file) is incomplete.

        restore : bool, optional
            Whether to restore the project from the last (auto) save point (if present).
        reset : bool, optional
            Whether to reset the project after loading it.
        project_properties_file : Optional[str], optional
            Project properties file to import, by default ``None``.

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
    def save(self) -> None:  # pragma: no cover
        """Save changes to the project data and settings.

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
    def save_as(
        self,
        file_path: Union[str, Path],
        force: bool = True,
        restore: bool = False,
        reset: bool = False,
    ) -> None:  # pragma: no cover
        """Save and open the project at a new location.

        Parameters
        ----------
        file_path : Union[str, pathlib.Path]
            Path for saving the new project file to.
        force : bool, optional
            Whether to force opening of the project even if non-critical errors occur.
            Non-critical errors include:

            - Timestamp of the (auto) save point is newer than the project timestamp.
            - Project (file) is incomplete.

        restore : bool, optional
            Whether to restore the project from the last (auto) save point (if present).
        reset : bool, optional
            Whether to reset the project after loading it.

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
    def save_copy(self, file_path: Union[str, Path]) -> None:  # pragma: no cover
        """Save a copy of the project to a specified location..

        Parameters
        ----------
        file_path : Union[str, pathlib.Path]
            Path for saving the copy of the project file to.

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
    def get_long_running_operation_status(
        self, operation_id: str
    ) -> Dict[str, Any]:  # pragma: no cover
        """Get the status (and, once finished, the result) of a long running operation.

        .. note:: This is a non-destructive, repeatable status poll: the operation is *not*
            removed from the server-side registry, even once finished. Use
            :py:meth:`wait_for_long_running_operation` to also consume/discard it.

        .. note:: Method is supported for Ansys optiSLang version >= 27.1 only.

        Parameters
        ----------
        operation_id: str
            ID of the long running operation, as returned e.g. by a node's ``load`` method
            when called with ``run_async=True``.

        Returns
        -------
        Dict[str, Any]
            Dictionary with keys ``operation_id``, ``is_finished`` and, once finished,
            ``result``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails, e.g. because no such operation is
            registered.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def wait_for_long_running_operation(
        self, operation_id: str
    ) -> Dict[str, Any]:  # pragma: no cover
        """Wait for a long running operation to finish, then return its status.

        .. note:: This method blocks until the operation completes. Unlike
            :py:meth:`get_long_running_operation_status`, it consumes the operation: once this
            call returns, the operation is removed from the server-side registry and a
            subsequent call with the same ``operation_id`` fails.

        .. note:: Method is supported for Ansys optiSLang version >= 27.1 only.

        Parameters
        ----------
        operation_id: str
            ID of the long running operation, as returned e.g. by a node's ``load`` method
            when called with ``run_async=True``.

        Returns
        -------
        Dict[str, Any]
            Dictionary with keys ``operation_id``, ``is_finished`` and, once finished,
            ``result``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails, e.g. because no such operation is
            registered.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def discard_long_running_operation(self, operation_id: str) -> None:  # pragma: no cover
        """Discard a previously registered long running operation.

        .. note:: Method is supported for Ansys optiSLang version >= 27.1 only.

        Unlike :py:meth:`wait_for_long_running_operation`, this does not wait for the
        operation to finish; it removes it from the server-side registry regardless of
        whether it has completed yet.

        Parameters
        ----------
        operation_id: str
            ID of the long running operation, as returned e.g. by a node's ``load`` method
            when called with ``run_async=True``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails, e.g. because no such operation is
            registered.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    # FUTURES:

    # close method doesn't work properly in optiSLang 2023R1, therefore it was commented out
    # TODO: Add this after it's fixed on optiSLang server side.
    # @abstractmethod
    # def close(self) -> None:  # pragma: no cover
    #     """Close the current project.

    #     Raises
    #     ------
    #     OslCommunicationError
    #         Raised when an error occurs while communicating with server.
    #     OslCommandError
    #         Raised when the command or query fails.
    #     TimeoutError
    #         Raised when the timeout float value expires.
    #     """
    #     pass
