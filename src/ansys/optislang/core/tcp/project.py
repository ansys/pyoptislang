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

"""Contains class TcpProjectProxy."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Tuple, Union

from deprecated.sphinx import deprecated

from ansys.optislang.core.io import RegisteredFile, RegisteredFileUsage
from ansys.optislang.core.node_types import NodeType
from ansys.optislang.core.placeholder_types import PlaceholderInfo, PlaceholderType, UserLevel
from ansys.optislang.core.project import Project
from ansys.optislang.core.tcp.nodes import TcpRootSystemProxy

if TYPE_CHECKING:
    from ansys.optislang.core.project_parametric import Design
    from ansys.optislang.core.tcp.managers import (
        TcpCriteriaManagerProxy,
        TcpParameterManagerProxy,
        TcpResponseManagerProxy,
    )
    from ansys.optislang.core.tcp.osl_server import TcpOslServer


class TcpProjectProxy(Project):
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

    def evaluate_design(self, design: Design) -> Design:
        """Evaluate a design.

        Parameters
        ----------
        design: Design
            Instance of a ``Design`` class with defined parameters.

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
        return self.root_system.evaluate_design(design=design)

    @deprecated(
        version="1.1.0", reason="Use :py:attr:`TcpProjectProxy.get_available_node_types` instead."
    )
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

    def get_available_node_types(self) -> List[NodeType]:
        """Get list of available node types.

        Returns
        -------
        List[NodeType]
            Available nodes types.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.__osl_server.get_available_node_types()

    def get_description(self) -> Optional[str]:
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

    def get_location(self) -> Optional[Path]:
        """Get the path to the optiSLang project file.

        Returns
        -------
        Optional[pathlib.Path]
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

    def get_name(self) -> Optional[str]:
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

    def get_reference_files_dir(self) -> Optional[Path]:
        """Get the path to the optiSLang project's reference files directory.

        Returns
        -------
        Optional[pathlib.Path]
            Path to the optiSLang project's reference files directory. If no project is loaded
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
        return Path(project_info.get("projects", [{}])[0].get("reference_files_dir", None))

    def get_registered_files(self) -> Tuple[RegisteredFile, ...]:
        """Get all registered files in the current project.

        Returns
        -------
        Tuple[RegisteredFile, ...]
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

    def get_result_files(self) -> Tuple[RegisteredFile, ...]:
        """Get result files.

        Returns
        -------
        Tuple[RegisteredFile, ...]
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

    def get_status(self) -> Optional[str]:
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

    def get_working_dir(self) -> Optional[Path]:
        """Get the path to the optiSLang project's working directory.

        Returns
        -------
        Optional[pathlib.Path]
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

    def run_python_file(
        self,
        file_path: Union[str, Path],
        args: Union[Sequence[object], None] = None,
    ) -> Tuple[str, str]:
        """Read a Python script from a file, load it in a project context, and run it.

        Parameters
        ----------
        file_path : Union[str, pathlib.Path]
            Path to the Python script file with the content to execute on the server.
        args : Sequence[object], None, optional
            Sequence of arguments to use in the Python script. The default is ``None``.

        Returns
        -------
        Tuple[str, str]
            STDOUT and STDERR from the executed Python script.

        Raises
        ------
        FileNotFoundError
            Raised when the specified Python script file does not exist.
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.__osl_server.run_python_file(file_path, args)

    def run_python_script(
        self,
        script: str,
        args: Union[Sequence[object], None] = None,
    ) -> Tuple[str, str]:
        """Load a Python script in a project context and run it.

        Parameters
        ----------
        script : str
            Python commands to execute on the server.
        args : Sequence[object], None, optional
            Sequence of arguments used in the Python script. The default
            is ``None``.

        Returns
        -------
        Tuple[str, str]
            STDOUT and STDERR from the executed Python script.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.__osl_server.run_python_script(script, args)

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

    def get_placeholder_ids(self) -> List[str]:
        """Get IDs of all placeholders in the project.

        .. note:: Method is supported for Ansys optiSLang version >= 26.1 only.

        Returns
        -------
        List[str]
            List of placeholder IDs.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.__osl_server.get_placeholder_ids()

    def get_placeholder(self, placeholder_id: str) -> PlaceholderInfo:
        """Get placeholder information.

        .. note:: Method is supported for Ansys optiSLang version >= 26.1 only.

        Parameters
        ----------
        placeholder_id : str
            ID of the placeholder.

        Returns
        -------
        PlaceholderInfo
            Named tuple containing placeholder information with separate fields
            for placeholder_id, user_level, type, description, range, value, and expression.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.__osl_server.get_placeholder(placeholder_id=placeholder_id)

    def create_placeholder(
        self,
        value: Optional[Any] = None,
        placeholder_id: Optional[str] = None,
        overwrite: bool = False,
        user_level: Optional[UserLevel] = None,
        description: Optional[str] = None,
        range_: Optional[str] = None,
        type_: Optional[PlaceholderType] = None,
        expression: Optional[str] = None,
    ) -> str:
        """Create a placeholder.

        .. note:: Method is supported for Ansys optiSLang version >= 26.1 only.

        Parameters
        ----------
        value : Optional[Any], optional
            Value for the placeholder, by default ``None``.
            If neither value nor expression are specified, the placeholder will be created
            with a suitable default value.
            If specified, the value must be of a type compatible with the placeholder type.
        placeholder_id : Optional[str], optional
            Desired placeholder ID, by default ``None``.
            If not specified, a unique ID will be generated.
        overwrite : bool, optional
            Whether to overwrite existing placeholder, by default ``False``.
        user_level : Optional[UserLevel], optional
            User level for the placeholder, by default ``None``.
            If not specified, the default user level will be used.
        description : Optional[str], optional
            Description of the placeholder, by default ``None``.
        range_ : Optional[str], optional
            Range of the placeholder, by default ``None``.
        type_ : Optional[PlaceholderType], optional
            Type of the placeholder, by default ``None``.
            If not specified, the UNKNOWN type will be used.
        expression : Optional[str], optional
            Macro expression for the placeholder, by default ``None``.

        Returns
        -------
        str
            ID of the created placeholder.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.__osl_server.create_placeholder(
            value=value,
            placeholder_id=placeholder_id,
            overwrite=overwrite,
            user_level=user_level,
            description=description,
            range_=range_,
            type_=type_,
            expression=expression,
        )

    def remove_placeholder(self, placeholder_id: str) -> None:
        """Remove a placeholder.

        .. note:: Method is supported for Ansys optiSLang version >= 26.1 only.

        Parameters
        ----------
        placeholder_id : str
            ID of the placeholder to remove.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self.__osl_server.remove_placeholder(placeholder_id=placeholder_id)

    def rename_placeholder(self, placeholder_id: str, new_placeholder_id: str) -> None:
        """Rename a placeholder.

        .. note:: Method is supported for Ansys optiSLang version >= 26.1 only.

        Parameters
        ----------
        placeholder_id : str
            Current ID of the placeholder.
        new_placeholder_id : str
            New ID for the placeholder.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self.__osl_server.rename_placeholder(
            placeholder_id=placeholder_id, new_placeholder_id=new_placeholder_id
        )

    def set_placeholder_value(self, placeholder_id: str, value: Any) -> None:
        """Set the value of a placeholder.

        Parameters
        ----------
        placeholder_id : str
            ID of the placeholder.
        value : Any
            New value for the placeholder.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self.__osl_server.set_placeholder_value(placeholder_id=placeholder_id, value=value)

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
