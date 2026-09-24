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

"""Contains tcp ``Application`` class."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Union

from ansys.optislang.core.application import Application
from ansys.optislang.core.errors import OslCommandError
from ansys.optislang.core.tcp.project import TcpProjectProxy

if TYPE_CHECKING:
    from ansys.optislang.core.osl_server import OslVersion
    from ansys.optislang.core.tcp.osl_server import TcpOslServer


class TcpApplicationProxy(Application):
    """Class which operates with projects."""

    def __init__(self, osl_server: TcpOslServer, logger=None):  # pragma: no cover
        """Initialize a new instance of ``TcpApplicationProxy``."""
        self.__osl_server = osl_server
        self._logger = logging.getLogger(__name__) if logger is None else logger
        self.__project = self.__create_current_project_proxy()

    @property
    def project(self) -> Optional[TcpProjectProxy]:
        """Instance of the ``TcpProjectProxy`` class.

        If the project currently loaded on the server no longer matches the cached
        instance (for example because the project was closed/opened directly in the
        optiSLang UI, bypassing :py:meth:`new`/:py:meth:`open`), the cached instance is
        transparently rebuilt so a stale project/root system is never returned.

        Returns
        -------
        Optional[TcpProjectProxy]
            Loaded project. If no project is loaded, ``None`` is returned.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self.__refresh_project_if_stale()
        return self.__project

    @property
    def version(self) -> OslVersion:
        """Version of used optiSLang.

        Returns
        -------
        OslVersion
            optiSLang version as typing.NamedTuple containing
            major, minor, maintenance and revision versions.
        """
        return self.__osl_server.osl_version

    @property
    def version_string(self) -> str:
        """Version of used optiSLang.

        Returns
        -------
        str
            optiSLang version.
        """
        return self.__osl_server.osl_version_string

    def new(self) -> None:
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
        self.__osl_server.new()
        self.__project = self.__create_current_project_proxy()

    def open(
        self,
        file_path: Union[str, Path],
        force: bool = True,
        restore: bool = False,
        reset: bool = False,
        project_properties_file: Optional[str] = None,
    ) -> None:
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
        self.__osl_server.open(
            file_path=file_path,
            force=force,
            restore=restore,
            reset=reset,
            project_properties_file=project_properties_file,
        )
        self.__project = self.__create_current_project_proxy()

    def save(self) -> None:
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
        self.__osl_server.save()

    def save_as(
        self,
        file_path: Union[str, Path],
        force: bool = True,
        restore: bool = False,
        reset: bool = False,
    ) -> None:
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
        self.__osl_server.save_as(file_path=file_path, force=force, restore=restore, reset=reset)

    def save_copy(self, file_path: Union[str, Path]) -> None:
        """Save a copy of the project to a specified location.

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
        self.__osl_server.save_copy(file_path=file_path)

    def __get_project_uid(self) -> str:
        """Get project uid.

        Returns
        -------
        str
            Project uid.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        project_tree = self.__osl_server.get_full_project_tree_with_properties()
        return project_tree["projects"][0]["system"]["uid"]

    def __get_project_uid_or_none(self) -> Optional[str]:
        """Get the uid of the project currently loaded on the server, if any."""
        try:
            return self.__get_project_uid()
        except OslCommandError:
            return None

    def __create_current_project_proxy(self) -> Optional[TcpProjectProxy]:
        """Build a ``TcpProjectProxy`` bound to whatever project is currently active."""
        project_uid = self.__get_project_uid_or_none()
        if project_uid is None:
            return None
        return TcpProjectProxy(osl_server=self.__osl_server, uid=project_uid, logger=self._logger)

    def __refresh_project_if_stale(self) -> None:
        """Rebuild the cached project if the server's active project uid has changed.

        This covers project switches made outside this instance's own
        :py:meth:`new`/:py:meth:`open` calls, e.g. directly in the optiSLang UI, on the
        same, still-alive server connection.
        """
        current_uid = self.__get_project_uid_or_none()
        cached_uid = self.__project.uid if self.__project is not None else None
        if current_uid == cached_uid:
            return
        self.__project = (
            TcpProjectProxy(osl_server=self.__osl_server, uid=current_uid, logger=self._logger)
            if current_uid is not None
            else None
        )

    # FUTURES:

    # close method doesn't work properly in optiSLang 2023R1, therefore it was commented out
    # TODO: Add this after it's fixed on optiSLang server side.
    # def close(self) -> None:
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
