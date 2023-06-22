"""Contains tcp ``Application`` class."""
from __future__ import annotations

import logging
from pathlib import Path
import re
from typing import TYPE_CHECKING, Tuple, Union

from ansys.optislang.core.application import Application
from ansys.optislang.core.tcp.project import TcpProjectProxy

if TYPE_CHECKING:
    from ansys.optislang.core.tcp.osl_server import TcpOslServer


class TcpApplicationProxy(Application):
    """Class which operates with projects."""

    def __init__(self, osl_server: TcpOslServer, logger=None):  # pragma: no cover
        """Initialize a new instance of ``TcpApplicationProxy``."""
        self.__osl_server = osl_server
        self._logger = logging.getLogger(__name__) if logger is None else logger

        project_uid = self.__get_project_uid()
        self.__project = (
            TcpProjectProxy(osl_server=self.__osl_server, uid=project_uid, logger=self._logger)
            if project_uid
            else None
        )

    @property
    def project(self) -> Union[TcpProjectProxy, None]:
        """Instance of the ``TcpProjectProxy`` class.

        Returns
        -------
        Union[TcpProjectProxy, None]
            Loaded project. If no project is loaded, ``None`` is returned.
        """
        return self.__project

    def get_version_string(self) -> str:
        """Get version of used optiSLang.

        Returns
        -------
        str
            optiSLang version.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        server_info = self.__osl_server.get_server_info()
        return server_info["application"]["version"]

    def get_version(self) -> Tuple[Union[int, None], ...]:
        """Get version of used optiSLang.

        Returns
        -------
        tuple
            optiSLang version as tuple containing
            major version, minor version, maintenance version and revision.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        osl_version_str = self.get_version_string()

        osl_version_entries = re.findall(r"[\w']+", osl_version_str)

        major_version = None
        minor_version = None
        maint_version = None
        revision = None

        if len(osl_version_entries) > 0:
            try:
                major_version = int(osl_version_entries[0])
            except:
                pass
        if len(osl_version_entries) > 1:
            try:
                minor_version = int(osl_version_entries[1])
            except:
                pass
        if len(osl_version_entries) > 2:
            try:
                maint_version = int(osl_version_entries[2])
            except:
                pass
        if len(osl_version_entries) > 3:
            try:
                revision = int(osl_version_entries[3])
            except:
                pass

        return major_version, minor_version, maint_version, revision

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
        self.__project = TcpProjectProxy(
            osl_server=self.__osl_server,
            uid=self.__get_project_uid(),
            logger=self._logger,
        )

    def open(
        self,
        file_path: Union[str, Path],
        force: bool = True,
        restore: bool = False,
        reset: bool = False,
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

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self.__osl_server.open(file_path=file_path, force=force, restore=restore, reset=reset)
        self.__project = TcpProjectProxy(
            osl_server=self.__osl_server, uid=self.__osl_server.get_project_uid()
        )

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

    def __get_project_uid(self) -> Union[str, None]:
        """Get project uid.

        Returns
        -------
        Union[str, None]
            Project uid. If no project is loaded in the optiSLang, returns `None`.

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
        return project_tree.get("projects", [{}])[0].get("system", {}).get("uid", None)

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
