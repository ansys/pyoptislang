"""Contains class ProjectSystem."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Tuple

from ansys.optislang.core.io import RegisteredFile, RegisteredFileUsage
from ansys.optislang.core.nodes import RootSystem

if TYPE_CHECKING:
    from ansys.optislang.core.osl_server import OslServer
    from ansys.optislang.core.project_parametric import (
        CriteriaManager,
        Design,
        ParameterManager,
        ResponseManager,
    )


class Project:
    """Provides the class containing the root system and queries related to the loaded project."""

    def __init__(self, osl_server: OslServer, uid: str) -> None:
        """Initialize an instance of the ``Project`` class.

        Parameters
        ----------
        osl_server: OslServer
            Instance of ``OslServer``.
        uid: str
            Unique ID of the loaded project.
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
        return self.__osl_server.get_project_description()

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
        return self.__osl_server.get_project_location()

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
        return self.__osl_server.get_project_name()

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

    def get_registered_files(self) -> Tuple[RegisteredFile]:
        """Get all registered files in the current project.

        Returns
        -------
        Tuple[RegisteredFile]
            Tuple with registered files.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        project_registered_files_dicts = self.__osl_server.get_basic_project_info()["projects"][0][
            "registered_files"
        ]
        return tuple(
            [
                RegisteredFile(
                    path=Path(file["local_location"]["split_path"]["head"]),
                    id=file["ident"],
                    comment=file["comment"],
                    tag=file["tag"],
                    usage=file["usage"],
                )
                for file in project_registered_files_dicts
            ]
        )

    def get_result_files(self) -> Tuple[RegisteredFile]:
        """Get result files.

        Returns
        -------
        Tuple[RegisteredFile]
            Tuple with result files

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        registered_files = self.get_registered_files()
        return tuple(
            [file for file in registered_files if file.usage == RegisteredFileUsage.OUTPUT_FILE]
        )

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
        return self.__osl_server.get_project_status()

    def _get_project_tree(self) -> list:
        """Return the project tree in a list format.

        Returns
        -------
        List
            List with all the nodes in the project tree.
        """
        full_project_tree = self.__osl_server.get_full_project_tree()
        project_tree = [
            {
                "uid": full_project_tree["projects"][0]["system"]["uid"],
                "name": full_project_tree["projects"][0]["system"]["name"],
                "is_root": True,
                "kind": full_project_tree["projects"][0]["system"]["kind"],
                "level": 0,
            }
        ]
        return self._get_child_nodes(
            full_project_tree["projects"][0]["system"]["nodes"], project_tree
        )

    def _get_child_nodes(self, node_properties: dict, project_tree: list) -> list:
        """Recursively walk throughout the full project tree and collect the nodes.

        Parameters
        ----------
        node_properties : dict
            Properties of the node from querying the full project tree.
        project_tree: list
           List with nodes collected from the full project tree.

        Returns
        -------
        List
            Updated list with collected nodes from the full project tree.
        """
        level = project_tree[-1]["level"]
        for i, child_node_properties in enumerate(node_properties):
            if i == 0:
                level += 1
            project_tree.append(
                {
                    "uid": child_node_properties["uid"],
                    "name": child_node_properties["name"],
                    "is_root": False,
                    "kind": child_node_properties["kind"],
                    "level": level,
                }
            )
            if "nodes" in child_node_properties.keys():
                project_tree = self._get_child_nodes(child_node_properties["nodes"], project_tree)
        return project_tree

    @property
    def parameter_manager(self) -> ParameterManager:
        """Instance of the ``ParameterManager`` class at the root system.

        Returns
        -------
        ParameterManager
            Parameter manager at the root system.
        """
        return self.__root_system.parameter_manager

    @property
    def response_manager(self) -> ResponseManager:
        """Instance of the ``ResponseManager`` class at the root system.

        Returns
        -------
        ResponseManager
            Response manager at the root system.
        """
        return self.__root_system.response_manager

    @property
    def criteria_manager(self) -> CriteriaManager:
        """Instance of the ``CriteriaManager`` class at the root system.

        Returns
        -------
        CriteriaManager
            Criteria manager at the root system.
        """
        return self.__root_system.criteria_manager

    @property
    def root_system(self) -> RootSystem:
        """Instance of the ``RootSystem`` class.

        Returns
        -------
        RootSystem
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
