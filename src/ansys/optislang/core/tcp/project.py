"""Contains class TcpProjectProxy."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List

from ansys.optislang.core.tcp.base_nodes import TcpRootSystemProxy

if TYPE_CHECKING:
    from ansys.optislang.core.tcp.managers import (
        Design,
        TcpCriteriaManagerProxy,
        TcpParameterManagerProxy,
        TcpResponseManagerProxy,
    )
    from ansys.optislang.core.tcp.osl_server import TcpOslServer


class TcpProjectProxy:
    """Provides the class containing the root system and queries related to the loaded project."""

    def __init__(self, osl_server: TcpOslServer, uid: str, logger=None) -> None:
        """Initialize an instance of the ``TcpProjectProxy`` class.

        Parameters
        ----------
        osl_server: TcpOslServer
            Instance of ``TcpOslServer``.
        uid: str
            Unique ID of the loaded project.
        logger: Any, optional
            Object for logging. If ``None``, standard logging object is used. Defaults to ``None``.
        """
        self.__osl_server = osl_server
        self.__uid = uid
        self.__logger = logging.getLogger(__name__) if logger is None else logger
        self.__root_system = TcpRootSystemProxy(
            uid=uid,
            osl_server=self.__osl_server,
            logger=self.__logger,
        )

    def __str__(self):
        """Return formatted string."""
        return (
            f"Name: {self.get_name()}\n"
            f"Description: {self.get_description()}\n"
            f"Status: {self.get_status()}\n"
            f"Location: {str(self.get_location())}"
        )

    @property
    def criteria_manager(self) -> TcpCriteriaManagerProxy:
        """Instance of the ``TcpCriteriaManagerProxy`` class at the root system.

        Returns
        -------
        TcpCriteriaManagerProxy
            Criteria manager at the root system.
        """
        return self.__root_system.criteria_manager

    @property
    def logger(self):
        """Return object for logging."""
        return self.__logger

    @property
    def parameter_manager(self) -> TcpParameterManagerProxy:
        """Instance of the ``TcpParameterManagerProxy`` class at the root system.

        Returns
        -------
        TcpParameterManagerProxy
            Parameter manager at the root system.
        """
        return self.__root_system.parameter_manager

    @property
    def response_manager(self) -> TcpResponseManagerProxy:
        """Instance of the ``TcpResponseManagerProxy`` class at the root system.

        Returns
        -------
        TcpResponseManagerProxy
            Response manager at the root system.
        """
        return self.__root_system.response_manager

    @property
    def root_system(self) -> TcpRootSystemProxy:
        """Instance of the ``TcpRootSystemProxy`` class.

        Returns
        -------
        TcpRootSystemProxy
            Loaded project's root system.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.__root_system

    @property
    def uid(self) -> str:
        """Unique ID of the optiSLang project.

        Returns
        -------
        str
            Unique ID of the loaded project.
        """
        return self.__uid

    def evaluate_design(self, design: Design, update_design: bool = True) -> Design:
        """Evaluate a design.

        Parameters
        ----------
        design: Design
            Instance of a ``Design`` class with defined parameters.
        update_design: bool, optional
            Determines whether given design should be updated and returned or new instance
            should be created. When ``True`` given design is updated and returned, otherwise
            new ``Design`` is created. Defaults to ``True``.

        Returns
        -------
        Design
            Evaluated design.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.root_system.evaluate_design(design=design, update_design=update_design)

    def get_available_nodes(self) -> Dict[str, List[str]]:
        """Get raw dictionary of available nodes sorted by subtypes.

        Returns
        -------
        Dict[str, List[str]]
            Dictionary of available node types, sorted by subtype.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.__osl_server.get_available_nodes()

    def get_description(self) -> str:
        """Get the description of the optiSLang project.

        Returns
        -------
        str
            Description of the optiSLang project. If no project is loaded in optiSLang,
            ``None`` is returned.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        project_info = self.__osl_server.get_basic_project_info()
        return (
            project_info.get("projects", [{}])[0].get("settings", {}).get("short_description", None)
        )

    def get_location(self) -> Path:
        """Get the path to the optiSLang project file.

        Returns
        -------
        pathlib.Path
            Path to the optiSLang project file. If no project is loaded in the optiSLang,
            ``None`` is returned.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        project_info = self.__osl_server.get_basic_project_info()
        project_path = project_info.get("projects", [{}])[0].get("location", None)
        return None if not project_path else Path(project_path)

    def get_name(self) -> str:
        """Get the name of the optiSLang project.

        Returns
        -------
        str
            Name of the optiSLang project. If no project is loaded in the optiSLang,
            ``None`` is returned.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        project_info = self.__osl_server.get_basic_project_info()
        return project_info.get("projects", [{}])[0].get("name", None)

    def get_reference_design(self) -> Design:
        """Get a design with reference values of the parameters.

        Returns
        -------
        Design
            Instance of the ``Design`` class with defined parameters and reference values.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.root_system.get_reference_design()

    def get_status(self) -> str:
        """Get the status of the optiSLang project.

        Returns
        -------
        str
            Status of the optiSLang project. If no project is loaded in optiSLang,
            ``None`` is returned.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        project_info = self.__osl_server.get_basic_project_info()
        return project_info.get("projects", [{}])[0].get("state", None)

    def get_working_dir(self) -> Path:
        """Get the path to the optiSLang project's working directory.

        Returns
        -------
        pathlib.Path
            Path to the optiSLang project's working directory. If no project is loaded
            in optiSLang, ``None`` is returned.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        project_info = self.__osl_server.get_basic_project_info()
        if len(project_info.get("projects", [])) == 0:
            return None
        return Path(project_info.get("projects", [{}])[0].get("working_dir", None))

    def reset(self) -> None:
        """Reset complete project.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self.__osl_server.reset()

    def start(self, wait_for_started: bool = True, wait_for_finished: bool = True) -> None:
        """Start project execution.

        Parameters
        ----------
        wait_for_started : bool, optional
            Determines whether this function call should wait on the optiSlang to start
            the command execution. I.e. don't continue on next line of python script
            after command was successfully sent to optiSLang but wait for execution of
            flow inside optiSLang to start.
            Defaults to ``True``.
        wait_for_finished : bool, optional
            Determines whether this function call should wait on the optiSlang to finish
            the command execution. I.e. don't continue on next line of python script
            after command was successfully sent to optiSLang but wait for execution of
            flow inside optiSLang to finish.
            This implicitly interprets wait_for_started as True.
            Defaults to ``True``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self.__osl_server.start(
            wait_for_started=wait_for_started, wait_for_finished=wait_for_finished
        )

    def stop(self, wait_for_finished: bool = True) -> None:
        """Stop project execution.

        Parameters
        ----------
        wait_for_finished : bool, optional
            Determines whether this function call should wait on the optiSlang to finish
            the command execution. I.e. don't continue on next line of python script after command
            was successfully sent to optiSLang but wait for execution of command inside optiSLang.
            Defaults to ``True``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self.__osl_server.stop(wait_for_finished=wait_for_finished)

    # FUTURES:
    # TODO: Add this after it's fixed on optiSLang server side.
    # stop_gently method doesn't work properly in optiSLang 2023R1, therefore it was commented out
    # def stop_gently(self, wait_for_finished: bool = True) -> None:
    #     """Stop project execution after the current design is finished.

    #     Parameters
    #     ----------
    #     wait_for_finished : bool, optional
    #         Determines whether this function call should wait on the optiSlang to finish
    #         the command execution. I.e. don't continue on next line of python script after command
    #         was successfully sent to optiSLang but wait for execution of command inside optiSLang.
    #         Defaults to ``True``.

    #     Raises
    #     ------
    #     OslCommunicationError
    #         Raised when an error occurs while communicating with server.
    #     OslCommandError
    #         Raised when the command or query fails.
    #     TimeoutError
    #         Raised when the timeout float value expires.
    #     """
