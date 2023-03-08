"""Contains class ProjectSystem."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from ansys.optislang.core.nodes import RootSystem

if TYPE_CHECKING:
    from ansys.optislang.core.osl_server import OslServer
    from ansys.optislang.core.project_parametric import Design, ParameterManager


class Project:
    """Class containing root_system and queries related to the loaded project."""

    def __init__(self, osl_server: OslServer, uid: str) -> None:
        """Initialize an instance of the Project class.

        Parameters
        ----------
        osl_server: OslServer
            Instance of `OslServer`.
        uid: str
            Unique id of the loaded project.
        """
        self.__osl_server = osl_server
        self.__uid = uid
        self.__root_system = RootSystem(
            uid=uid,
            osl_server=self.__osl_server,
        )

    def __str__(self):
        """Return formatted string."""
        return (
            f"Name: {self.get_name()}\n"
            f"Description: {self.get_description()}\n"
            f"Status: {self.get_status()}\n"
            f"Location: {str(self.get_location())}"
        )

    def evaluate_design(self, design: Design) -> Design:
        """Evaluate given design.

        Parameters
        ----------
        design: Design
            Instance of ``Design`` class with defined parameters.

        Returns
        -------
        Design
            Evaluated design.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.root_system.evaluate_design(design=design)

    def get_description(self) -> str:
        """Get description of the optiSLang project.

        Returns
        -------
        str
            optiSLang project description. If no project is loaded in the optiSLang,
            returns ``None``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.__osl_server.get_project_description()

    def get_location(self) -> Path:
        """Get path to the optiSLang project file.

        Returns
        -------
        Path
            Path to the optiSLang project file. If no project is loaded in the optiSLang,
            returns ``None``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.__osl_server.get_project_location()

    def get_name(self) -> str:
        """Get name of the optiSLang project.

        Returns
        -------
        str
            Name of the optiSLang project. If no project is loaded in the optiSLang,
            returns ``None``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.__osl_server.get_project_name()

    def get_reference_design(self) -> Design:
        """Get design with reference values of parameters.

        Returns
        -------
        Design
            Instance of ``Design`` class with defined parameters and reference values.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.root_system.get_reference_design()

    def get_status(self) -> str:
        """Get status of the optiSLang project.

        Returns
        -------
        str
            optiSLang project status. If no project is loaded in the optiSLang,
            returns ``None``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.__osl_server.get_project_status()

    @property
    def parameter_manager(self) -> ParameterManager:
        """Get instance of the ``ParameterManager`` class at the root system.

        Returns
        -------
        ParameterManager
            Parameter manager at the root system.
        """
        return self.__root_system.parameter_manager

    @property
    def root_system(self) -> RootSystem:
        """Get instance of the ``RootSystem`` class.

        Returns
        -------
        RootSystem
            Loaded project's root system.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.__root_system

    @property
    def uid(self) -> str:
        """Get uid of the optiSLang project.

        Returns
        -------
        str
            Uid of the loaded project.
        """
        return self.__uid