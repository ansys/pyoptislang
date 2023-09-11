"""Contains classes for a node, system, parametric system, and root system."""
from __future__ import annotations

from collections import OrderedDict
import copy
import csv
from enum import Enum
from io import StringIO
import json
from pathlib import Path
import time
from typing import TYPE_CHECKING, Dict, Iterable, List, Tuple, Union

from ansys.optislang.core.io import File, FileOutputFormat, RegisteredFile, RegisteredFileUsage
from ansys.optislang.core.project_parametric import (
    ConstraintCriterion,
    CriteriaManager,
    Design,
    LimitStateCriterion,
    ObjectiveCriterion,
    ParameterManager,
    ResponseManager,
    VariableCriterion,
)
from ansys.optislang.core.utils import enum_from_str

if TYPE_CHECKING:
    from ansys.optislang.core.osl_server import OslServer
    from ansys.optislang.core.project_parametric import Criterion

from ansys.optislang.core import server_commands as commands

PROJECT_COMMANDS_RETURN_STATES = {
    "start": "PROCESSING",
    "restart": "PROCESSING",
    "stop": "STOPPED",
    "stop_gently": "GENTLY_STOPPED",
    "reset": "FINISHED",
}


ACTOR_COMMANDS_RETURN_STATES = {
    "start": "Running",
    "restart": "Running",
    "stop": "Aborted",
    "stop_gently": "Gently stopped",
    "reset": "Finished",
}


class DesignFlow(Enum):
    """Provides design flow options."""

    NONE = 0
    RECEIVE = 1
    SEND = 2
    RECEIVE_SEND = 3

    @staticmethod
    def from_str(string: str) -> DesignFlow:
        """Convert string to an instance of the ``DesignFlow`` class.

        Parameters
        ----------
        string: str
            String to be converted.

        Returns
        -------
        DesignFlow
            Instance of the ``DesignFlow`` class.

        Raises
        ------
        TypeError
            Raised when an invalid type of ``string`` is given.
        ValueError
            Raised when an invalid value of ``string`` is given.
        """
        return enum_from_str(string=string, enum_class=__class__, replace=(" ", "_"))


class Node:
    """Provides for creating and operating on nodes."""

    def __init__(
        self,
        uid: str,
        osl_server: OslServer,
    ) -> None:
        """Create a ``Node`` instance.

        Parameters
        ----------
        uid: str
            Unique ID of the node.
        osl_server: OslServer
            Object providing access to the optiSLang server.
        """
        self._osl_server = osl_server
        self.__uid = uid

    def __str__(self):
        """Return formatted string."""
        return f"Node type: {self.get_type()} Name: {self.get_name()} Uid: {self.uid}"

    @property
    def uid(self) -> str:
        """Unique ID of the node.

        Returns
        -------
        str
            Unique ID of the node.
        """
        return self.__uid

    def get_name(self) -> str:
        """Get the name of the node.

        Returns
        -------
        str
            Name of the node.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        actor_info = self._osl_server.get_actor_info(uid=self.__uid)
        return actor_info["name"]

    def get_parent(self) -> Node:
        """Get the instance of the parent node.

        Returns
        -------
        Node
            Instance of the parent node.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        project_tree = self._osl_server.get_full_project_tree_with_properties()
        root_system_uid = project_tree["projects"][0]["system"]["uid"]
        parent_tree = project_tree["projects"][0]["system"]
        parent_uid = Node._find_parent_node_uid(
            tree=parent_tree,
            parent_uid=root_system_uid,
            node_uid=self.uid,
        )
        properties_dicts_list = [
            {
                "uid": parent_uid,
                "kind": "root_system" if parent_uid == root_system_uid else "system",
            }
        ]
        return self._create_nodes_from_properties_dicts(
            properties_dicts_list=properties_dicts_list
        )[0]

    def get_parent_name(self) -> str:
        """Get the name of the parent node.

        Returns
        -------
        str
            Name of the parent node.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        parent_uid = self._get_parent_uid()
        actor_info = self._osl_server.get_actor_info(uid=parent_uid)
        return actor_info["name"]

    def get_properties(self) -> dict:
        """Get the raw server output with the node properties.

        Returns
        -------
        dict
            Dictionary with the node properties.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self._osl_server.get_actor_properties(self.uid)

    def get_registered_files(self) -> Tuple[RegisteredFile]:
        """Get node's registered files.

        Returns
        -------
        Tuple[RegisteredFile]
            Tuple of registered files.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        registered_files_uids = self._get_info()["registered_files"]
        if not registered_files_uids:
            return ()
        project_registered_files = self._osl_server.get_basic_project_info()["projects"][0][
            "registered_files"
        ]
        return tuple(
            [
                RegisteredFile(
                    path=Path(file["local_location"]["split_path"]["head"])
                    / file["local_location"]["split_path"]["tail"],
                    id=file["ident"],
                    comment=file["comment"],
                    tag=file["tag"],
                    usage=file["usage"],
                )
                for file in project_registered_files
                if file["tag"] in registered_files_uids
            ]
        )

    def get_result_files(self) -> Tuple[RegisteredFile]:
        """Get node's result files.

        Returns
        -------
        Tuple[RegisteredFile]
            Tuple of result files.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return tuple(
            filter(
                lambda file: file.usage == RegisteredFileUsage.OUTPUT_FILE,
                self.get_registered_files(),
            )
        )

    def get_states_ids(self) -> Tuple[str]:
        """Get available actor states ids.

        Returns
        -------
        Tuple[str]
            Actor states ids.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        states = self._osl_server.get_actor_states(self.uid)
        if not states.get("states", None):
            return tuple([])
        return tuple([state["hid"] for state in states["states"]])

    def get_status(self) -> str:
        """Get the status of the node.

        Returns
        -------
        str
            Status of the node.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        actor_info = self._osl_server.get_actor_info(uid=self.__uid)
        return actor_info["status"]

    def get_type(self) -> str:
        """Get the type of the node.

        Returns
        -------
        str
            Type of the node.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        actor_info = self._osl_server.get_actor_info(uid=self.__uid)
        return actor_info["type"]

    def control(
        self,
        command: str,
        hid: str = None,
        wait_for_completion: bool = True,
        timeout: Union[float, int] = 100,
    ) -> Union[str, None]:
        """Control the node state.

        Parameters
        ----------
        command: str
            Command to execute. Options are ``"start"``, ``"restart"``, ``"stop_gently"``,
            ``"stop"``, and ``"reset"``.
        hid: str, optional
            Hid entry. The default is ``None``. The actor unique ID is required.
        wait_for_completion: bool, optional
            Whether to wait for completion. The default is ``True``.
        timeout: Union[float, int], optional
            Time limit for monitoring the status of the command. The default is ``100 s``.

        Returns
        -------
        boolean
            ``True`` when successful, ``False`` when failed.
        """
        if not hid:  # Run command against all designs
            hids = self.get_states_ids()
            if len(hids) == 0:
                raise RuntimeError(
                    "There are no hids available because the node has not been started yet."
                    f" The {command} command cannot be executed."
                )
        else:  # Run command against the given design
            hids = [hid]

        for hid in hids:
            response = self._osl_server.send_command(
                getattr(commands, command)(actor_uid=self.uid, hid=hid)
            )
            if response[0]["status"] != "success":
                raise Exception(f"{command} command execution failed.")

        if wait_for_completion:
            time_stamp = time.time()
            while True:
                print(
                    f"Project: {self.get_name()} | "
                    f"State: {self.get_status()} | "
                    f"Time: {round(time.time() - time_stamp)}s"
                )
                if self.get_status() == ACTOR_COMMANDS_RETURN_STATES[command]:
                    print(f"{command} command successfully executed.")
                    status = True
                    break
                if (time.time() - time_stamp) > timeout:
                    print("Timeout limit reached. Skip monitoring of command {command}.")
                    status = False
                    break
                time.sleep(3)

            return status

    def _create_nodes_from_properties_dicts(
        self, properties_dicts_list: List[dict]
    ) -> Tuple[Node, ...]:
        """Create nodes from a dictionary of properties.

        Parameters
        ----------
        properties_dicts_list : List[dict]
            Dictionary of node properties.

        Returns
        -------
        Tuple[Node, ...]
            Tuple of nodes.

        Raises
        ------
        TypeError
            Raised when an unknown type of component is found.
        """
        nodes_list = []
        for node in properties_dicts_list:
            kind = node["kind"]
            uid = node["uid"]
            if kind == "actor":
                nodes_list.append(Node(uid=uid, osl_server=self._osl_server))
            elif kind == "system":
                if self._is_parametric_system(uid=uid):
                    nodes_list.append(ParametricSystem(uid=uid, osl_server=self._osl_server))
                else:
                    nodes_list.append(System(uid=uid, osl_server=self._osl_server))
            elif kind == "root_system":
                nodes_list.append(RootSystem(uid=node["uid"], osl_server=self._osl_server))
            else:
                TypeError(
                    f'Unknown kind of component: "{kind}", '
                    '"node", "system" or "root_system" were expected.'
                )

        return tuple(nodes_list)

    def _get_info(self) -> dict:
        """Get the raw server output with the node info.

        Returns
        -------
        dict
            Dictionary with the node info.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self._osl_server.get_actor_info(self.uid)

    def _get_parent_uid(self) -> str:
        """Get the unique ID of the parent node.

        Return
        ------
        str
            Unique ID of the parent node.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        project_tree = self._osl_server.get_full_project_tree_with_properties()
        root_system_uid = project_tree["projects"][0]["system"]["uid"]
        parent_tree = project_tree["projects"][0]["system"]
        return Node._find_parent_node_uid(
            tree=parent_tree,
            parent_uid=root_system_uid,
            node_uid=self.uid,
        )

    def _get_status_info(self) -> Tuple[dict]:
        """Get node's status info for each state.

        Returns
        -------
        Tuple[dict]
            Tuple with status info dictionary for each state.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        hids = self.get_states_ids()
        return tuple([self._osl_server.get_actor_status_info(self.uid, hid) for hid in hids])

    def _is_parametric_system(self, uid: str) -> bool:
        """Check if the system is parametric.

        Parameters
        ----------
        uid : str
            Unique ID of the system.

        Returns
        -------
        bool
            ``True`` when the system is parametric, ``False`` otherwise.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        props = self._osl_server.get_actor_properties(uid=uid)
        return "ParameterManager" in props["properties"]

    @staticmethod
    def _find_parent_node_uid(tree: dict, parent_uid: str, node_uid: str) -> str:
        """Get the unique ID of the the parent node.

        Parameters
        ----------
        tree: dict
            Dictionary with children nodes.
        parent_uid: str
            Uniquie ID of the system to loop through.
        node_uid: str
            Unique ID of the node for which to search for the parent.

        Return
        ------
        str
            Unique ID of the parent node.
        """
        for node in tree["nodes"]:
            if node["uid"] == node_uid:
                return parent_uid
            if node["kind"] == "system":
                Node._find_parent_node_uid(tree=node, parent_uid=tree["uid"], node_uid=node_uid)
        raise RuntimeError(f'Node "{node_uid}" was not located in structure tree.')


class System(Node):
    """Provides for creating and operatating on a system."""

    def __init__(
        self,
        uid: str,
        osl_server: OslServer,
    ) -> None:
        """Create a ``System`` instance.

        Parameters
        ----------
        uid: str
            Unique ID.
        osl_server: OslServer
            Object providing access to the optiSLang server.
        """
        super().__init__(
            uid=uid,
            osl_server=osl_server,
        )

    def find_node_by_uid(self, uid: str, search_depth: int = 1) -> Union[Node, None]:
        """Find a node in the system with a specified unique ID.

        This method searches only in the descendant nodes for the current system.

        Parameters
        ----------
        uid : str
            Unique ID of the node.
        search_depth: int, optional
            Depth of the node subtree to search. The default is ``1``, which corresponds
            to direct children nodes of the current system. Set to ``-1`` to search throughout
            the full depth.

        Returns
        -------
        Union[Node, None]
            ``Node`` with the specified unique ID. If this ID isn't located in any
            descendant node, ``None`` is returned.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        TypeError
            Raised when an unknown type of component is found.
        """
        project_tree = self._osl_server.get_full_project_tree_with_properties()
        if self.uid == project_tree["projects"][0]["system"]["uid"]:
            system_tree = project_tree["projects"][0]["system"]
        else:
            system_tree = System._find_subtree(
                tree=project_tree["projects"][0]["system"],
                uid=self.uid,
            )
        properties_dicts_list = System._find_node_with_uid(
            uid=uid,
            tree=system_tree,
            properties_dicts_list=[],
            current_depth=1,
            max_search_depth=search_depth,
        )

        if len(properties_dicts_list) == 0:
            self._osl_server._logger.error(f"Node `{uid}` not found in the current system.")
            return None

        return self._create_nodes_from_properties_dicts(
            properties_dicts_list=properties_dicts_list
        )[0]

    def find_nodes_by_name(self, name: str, search_depth: int = 1) -> Tuple[Node, ...]:
        """Find nodes in the system with a specified name.

        This method searches only in the descendant nodes for the current system.

        Parameters
        ----------
        name : str
            Name of the node.
        search_depth: int, optional
            Depth of the node subtree to search. The default is ``1``, which corresponds
            to direct children nodes of the current system. Set to ``-1`` to search throughout
            the full depth.

        Returns
        -------
        Tuple[Node, ...]
            Tuple of nodes with the specified name.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        TypeError
            Raised when an unknown type of component is found.
        """
        project_tree = self._osl_server.get_full_project_tree_with_properties()
        if self.uid == project_tree["projects"][0]["system"]["uid"]:
            system_tree = project_tree["projects"][0]["system"]
        else:
            system_tree = System._find_subtree(
                tree=project_tree["projects"][0]["system"],
                uid=self.uid,
            )
        properties_dicts_list = System._find_nodes_with_name(
            name=name,
            tree=system_tree,
            properties_dicts_list=[],
            current_depth=1,
            max_search_depth=search_depth,
        )

        if len(properties_dicts_list) == 0:
            self._osl_server._logger.error(f"Node `{name}` not found in the current system.")
            return tuple()

        return self._create_nodes_from_properties_dicts(properties_dicts_list=properties_dicts_list)

    def get_nodes(self) -> Tuple[Node, ...]:
        """Get the direct children nodes.

        Returns
        -------
        Tuple[Node, ...]
            Current system nodes.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self._create_nodes_from_properties_dicts(
            properties_dicts_list=self._get_nodes_dicts()
        )

    def _get_nodes_dicts(self) -> List[dict]:
        """Get data for children nodes.

        Returns
        -------
        List[dict]
            List of dictionaries with data for children nodes.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        RuntimeError
            Raised when the system wasn't located in the project tree.
        """
        project_tree = self._osl_server.get_full_project_tree_with_properties()
        if self.uid == project_tree["projects"][0]["system"]["uid"]:
            system_tree = project_tree["projects"][0]["system"]
        else:
            system_tree = System._find_subtree(
                tree=project_tree["projects"][0]["system"],
                uid=self.uid,
            )
        if len(system_tree) == 0:
            raise RuntimeError(f"System `{self.uid}` wasn't found.")

        children_dicts_list = []
        for node in system_tree["nodes"]:
            children_dicts_list.append(
                {
                    "type": node["type"],
                    "name": node["name"],
                    "uid": node["uid"],
                    "kind": node["kind"],
                }
            )
        return children_dicts_list

    @staticmethod
    def _find_nodes_with_name(
        name: str,
        tree: dict,
        properties_dicts_list: List[dict],
        current_depth: int,
        max_search_depth: int = 1,
    ) -> List[dict]:
        """Find nodes with the specified name.

        Parameters
        ----------
        name : str
            Node name.
        tree : dict
            Tree to search for nodes with the specified name.
        properties_dicts_list : dict
            Dictionary with properties.
        current_depth: int
            Current depth of the search.
        max_search_depth: int, optional
            Maximum depth of the search. The default is ``1``. Set to ``-1``
            to search throughout the full depth.

        Returns
        -------
        dict
            Dictionary with necessary information for creation of a node.
        """
        for node in tree["nodes"]:
            if node["name"] == name:
                properties_dicts_list.append(
                    {
                        "type": node["type"],
                        "name": node["name"],
                        "uid": node["uid"],
                        "parent_uid": tree["uid"],
                        "parent_name": tree["name"],
                        "kind": node["kind"],
                    }
                )
            if node["kind"] == "system" and (
                current_depth < max_search_depth or max_search_depth == -1
            ):
                System._find_nodes_with_name(
                    name=name,
                    tree=node,
                    properties_dicts_list=properties_dicts_list,
                    current_depth=current_depth + 1,
                    max_search_depth=max_search_depth,
                )
        return properties_dicts_list

    @staticmethod
    def _find_node_with_uid(
        uid: str,
        tree: dict,
        properties_dicts_list: List[dict],
        current_depth: int,
        max_search_depth: int = 1,
    ) -> List[dict]:
        """Find a node with a specified unique ID.

        Parameters
        ----------
        uid : str
            Unique ID of the node.
        tree : dict
            Tree to search for nodes with the specified unique ID.
        properties_dicts_list : List[dict]
            Dictionary with properties.
        current_depth: int
            Current depth of the search.
        max_search_depth: int, optional
            Maximum depth of the search. The default is ``1``. Set to ``-1``
            to search throughout the full depth.


        Returns
        -------
        dict
            Dictionary with the necessary information for creation of a node.
        """
        for node in tree["nodes"]:
            if node["uid"] == uid:
                properties_dicts_list.append(
                    {
                        "type": node["type"],
                        "name": node["name"],
                        "uid": node["uid"],
                        "parent_uid": tree["uid"],
                        "parent_name": tree["name"],
                        "kind": node["kind"],
                    }
                )
            if node["kind"] == "system" and (
                current_depth < max_search_depth or max_search_depth == -1
            ):
                System._find_node_with_uid(
                    uid=uid,
                    tree=node,
                    properties_dicts_list=properties_dicts_list,
                    current_depth=current_depth + 1,
                    max_search_depth=max_search_depth,
                )
        return properties_dicts_list

    @staticmethod
    def _find_subtree(tree: dict, uid: str) -> dict:
        """Find the subtree with a root node matching a specified unique ID.

        Parameters
        ----------
        tree: dict
            Dictionary with the parent structure.
        uid: str
            Unique ID of the subtree root node.

        Returns
        -------
        dict
            Dictionary representing the subtree found.
        """
        for node in tree["nodes"]:
            if node["uid"] == uid:
                return node
            if node["kind"] == "system":
                System._find_subtree(tree=node, uid=uid)


class ParametricSystem(System):
    """Provides methods to obtain data from a parametric system."""

    def __init__(
        self,
        uid: str,
        osl_server: OslServer,
    ) -> None:
        """Create a parametric system.

        Parameters
        ----------
        uid: str
            Unique ID.
        osl_server: OslServer
            Object providing access to the optiSLang server.
        """
        super().__init__(
            uid=uid,
            osl_server=osl_server,
        )
        self.__criteria_manager = CriteriaManager(uid, osl_server)
        self.__parameter_manager = ParameterManager(uid, osl_server)
        self.__response_manager = ResponseManager(uid, osl_server)

    @property
    def criteria_manager(self) -> CriteriaManager:
        """Criteria manager of the current system.

        Returns
        -------
        CriteriaManager
            Instance of the ``CriteriaManager`` class.
        """
        return self.__criteria_manager

    @property
    def parameter_manager(self) -> ParameterManager:
        """Parameter manager of the current system.

        Returns
        -------
        ParameterManager
            Instance of the ``ParameterManager`` class.
        """
        return self.__parameter_manager

    @property
    def response_manager(self) -> ResponseManager:
        """Response manager of the current system.

        Returns
        -------
        ResponseManager
            Instance of the ``ResponseManager`` class.
        """
        return self.__response_manager

    def get_omdb_files(self) -> Tuple[File]:
        """Get paths to omdb files.

        Returns
        -------
        Tuple[File]
            Tuple with File objects containing path.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        statuses_info = self._get_status_info()
        wdirs = [Path(status_info["working dir"]) for status_info in statuses_info]
        omdb_files = []
        for wdir in wdirs:
            omdb_files.extend([File(path) for path in wdir.glob("*.omdb")])
        return tuple(omdb_files)

    def save_designs_as(
        self,
        hid: str,
        file_name: str,
        format: FileOutputFormat = FileOutputFormat.JSON,
        dir: Union[Path, str] = None,
    ) -> File:
        """Save designs for a given state.

        Parameters
        ----------
        hid : str
            Actor's state.
        file_name : str
            Name of the file.
        format : FileOutputFormat, optional
            Format of the file, by default ``FileOutputFormat.JSON``.
        dir : Union[Path, str], optional
            Directory, where file should be saved, by default ``None``.
            Project's working directory is used by default.

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
            Raised when incorrect type of ``dir`` is passed.
        ValueError
            Raised when unsupported value of ``format`` or non-existing ``hid``
            is passed.
        """
        if dir is not None and isinstance(dir, str):
            dir = Path(dir)
        elif dir is None:
            dir = self._osl_server.get_working_dir()

        if not isinstance(dir, Path):
            raise TypeError(f"Unsupported type of dir: `{type(dir)}`.")

        designs = self._get_designs_dicts()
        if not designs.get(hid):
            raise ValueError(f"Design for given hid: `{hid}` not available.")

        if format == FileOutputFormat.JSON:
            output_file = json.dumps(designs[hid])
            newline = None
        elif format == FileOutputFormat.CSV:
            output_file = self.__class__.__convert_design_dict_to_csv(designs[hid])
            newline = ""
        else:
            raise ValueError(f"Output type `{format}` is not supported.")

        output_file_path = dir / (file_name + format.to_str())
        with open(output_file_path, "w", newline=newline) as f:
            f.write(output_file)
        return File(output_file_path)

    def _get_designs_dicts(self) -> OrderedDict:
        """Get parametric system's designs.

        Returns
        -------
        OrderedDict
            Ordered dictionary of designs, key is hid and value
            is list of corresponding designs.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        statuses_info = self._get_status_info()
        if not statuses_info:
            return {}
        designs = {}
        # TODO: sort by hid? -> delete / use OrderedDict
        for status_info in statuses_info:
            designs[status_info["hid"]] = status_info["designs"]
            for idx, design in enumerate(designs[status_info["hid"]]["values"]):
                self.__class__.__append_status_info_to_design(
                    design, status_info["design_status"][idx]
                )
        for i in range(2, len(statuses_info[0]["designs"]["values"][0]["hid"].split("."))):
            designs = self.__class__.__sort_dict_by_key_hid(
                designs, max(1, len(statuses_info[0]["designs"]["values"][0]["hid"].split(".")) - i)
            )
        for hid, design in designs.items():
            # sort by design number, stripped from hid prefix
            # (0.10, 0.9 ..., 0.1) -> (0.1, ..., 0.9, 0.10)
            design["values"] = self.__class__.__sort_list_of_dicts_by_hid(
                design["values"], len(hid.split("."))
            )
        return designs

    @staticmethod
    def __append_status_info_to_design(design: dict, status_info: dict) -> None:
        if design["hid"] != status_info["id"]:
            raise ValueError(f'{design["hid"]} != {status_info["id"]}')
        to_append = {
            key: status_info[key] for key in ("feasible", "status", "pareto_design", "directory")
        }
        design.update(to_append)

    @staticmethod
    def __convert_design_dict_to_csv(designs: dict) -> str:
        csv_buffer = StringIO()
        try:
            csv_writer = csv.writer(csv_buffer)
            header = ["Design"]
            header.append("Feasible")
            header.append("Status")
            header.append("Pareto")
            header.extend(designs["constraint_names"])
            header.extend(designs["limit_state_names"])
            header.extend(designs["objective_names"])
            header.extend(designs["parameter_names"])
            header.extend(designs["response_names"])
            csv_writer.writerow(header)
            for design in designs["values"]:
                line = [design["hid"]]
                line.append(design["feasible"])
                line.append(design["status"])
                line.append(design["pareto_design"])
                line.extend(design["constraint_values"])
                line.extend(design["limit_state_values"])
                line.extend(design["objective_values"])
                line.extend(design["parameter_values"])
                line.extend(design["response_values"])
                csv_writer.writerow(line)
            return csv_buffer.getvalue()
        finally:
            if csv_buffer is not None:
                csv_buffer.close()

    @staticmethod
    def __sort_list_of_dicts_by_hid(unsorted_list: List[dict], sort_by_position: int) -> List[dict]:
        sort_key = lambda x: int(x["hid"].split(".")[sort_by_position])
        return sorted(unsorted_list, key=sort_key)

    @staticmethod
    def __sort_dict_by_key_hid(unsorted_dict: dict, sort_by_position: int) -> dict:
        sort_key = lambda item: int(item[0].split(".")[sort_by_position])
        return OrderedDict(sorted(unsorted_dict.items(), key=sort_key))


class RootSystem(ParametricSystem):
    """Provides for creating and operating on a project system."""

    def __init__(
        self,
        uid: str,
        osl_server: OslServer,
    ) -> None:
        """Create a ``RootSystem`` system.

        Parameters
        ----------
        uid: str
            Unique ID.
        osl_server: OslServer
            Object providing access to the optiSLang server.
        """
        super().__init__(
            uid=uid,
            osl_server=osl_server,
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
        evaluate_dict = {}
        for parameter in design.parameters:
            evaluate_dict[parameter.name] = parameter.value
        output_dict = self._osl_server.evaluate_design(evaluate_dict=evaluate_dict)
        if update_design:
            return_design = design
            return_design._receive_results(output_dict[0])
        else:
            return_design = copy.deepcopy(design)
            return_design._receive_results(output_dict[0])

        design_parameters = return_design.parameters_names
        output_parameters = output_dict[0]["result_design"]["parameter_names"]
        missing_parameters = __class__.__get_sorted_difference_of_sets(
            output_parameters, design_parameters
        )
        undefined_parameters = __class__.__get_sorted_difference_of_sets(
            design_parameters, output_parameters
        )
        unused = __class__.__compare_input_w_processed_values(evaluate_dict, output_dict)

        if undefined_parameters:
            self._osl_server._logger.debug(f"Parameters ``{undefined_parameters}`` weren't used.")
        if missing_parameters:
            self._osl_server._logger.warning(
                f"Parameters ``{missing_parameters}`` were missing, "
                "reference values were used for evaluation and list of parameters will be updated."
            )
        if unused:
            self._osl_server._logger.warning(
                "Values of parameters were changed:"
                f"{[par[0] + ': ' + str(par[1]) + ' -> ' + str(par[2]) for par in unused]}"
            )

        for parameter in missing_parameters:
            position = output_dict[0]["result_design"]["parameter_names"].index(parameter)
            design.set_parameter_by_name(
                parameter,
                output_dict[0]["result_design"]["parameter_values"][position],
                False,
            )

        return return_design

    def get_reference_design(self) -> Design:
        """Get the design with reference values of the parameters.

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
        parameters = self.parameter_manager.get_parameters()
        responses = self.response_manager.get_responses()
        criteria = self.criteria_manager.get_criteria()
        sorted_criteria = __class__.__categorize_criteria(criteria=criteria)
        return Design(
            parameters=parameters,
            constraints=sorted_criteria.get("constraints", []),
            limit_states=sorted_criteria.get("limit_states", []),
            objectives=sorted_criteria.get("objectives", []),
            variables=sorted_criteria.get("variables", []),
            responses=responses,
        )

    def get_missing_parameters_names(self, design: Design) -> Tuple[str, ...]:
        """Get the names of the parameters that are missing in a design.

        This method compare design parameters with the root system's parameters.

        Parameters
        ----------
        design: Design
            Instance of the ``Design`` class with defined parameters.

        Returns
        -------
        Tuple[str, ...]
            Names of the parameters that are missing in the instance of ``Design`` class.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return __class__.__get_sorted_difference_of_sets(
            first=self.parameter_manager.get_parameters_names(),
            second=design.parameters_names,
        )

    def get_undefined_parameters_names(self, design: Design) -> Tuple[str, ...]:
        """Get the names of the parameters that are not defined in the root system.

        This method compare design parameters with the root system's parameters.

        Parameters
        ----------
        design: Design
            Instance of the ``Design`` class with defined parameters.

        Returns
        -------
        Tuple[str, ...]
            Names of the parameters that are not defined in the root system.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return __class__.__get_sorted_difference_of_sets(
            first=design.parameters_names,
            second=self.parameter_manager.get_parameters_names(),
        )

    def control(
        self, command: str, wait_for_completion: bool = True, timeout: Union[float, int] = 100
    ) -> Union[str, None]:
        """Control the node state.

        Parameters
        ----------
        command: str
            Command to execute. Options are ``"restart"``, ``"stop_gently"``, ``"stop"``
            and ``"reset"``.
        wait_for_completion: bool, opt
            True/False
        timeout: Union[float, int], opt
            Time limit for monitoring the status of the command. Default is 100 s.

        Returns
        -------
        boolean
            ``True`` when successful, ``False`` when failed.
        """
        response = self._osl_server.send_command(getattr(commands, command)())
        if response[0]["status"] != "success":
            raise Exception(f"{command} command execution failed.")

        if wait_for_completion:
            time_stamp = time.time()
            while True:
                print(
                    f"Project: {self.get_name()} | "
                    f"State: {self.get_status()} | "
                    f"Time: {round(time.time() - time_stamp)}s"
                )
                if self.get_status() == PROJECT_COMMANDS_RETURN_STATES[command]:
                    print(f"{command} command successfully executed.")
                    status = True
                    break
                if (time.time() - time_stamp) > timeout:
                    print("Timeout limit reached. Skip monitoring of command {command}.")
                    status = False
                    break
                time.sleep(3)

            return status

    @staticmethod
    def __categorize_criteria(criteria: Tuple[Criterion]) -> Dict[str, List[Criterion]]:
        """Get criteria sorted by its kinds.

        Parameters
        ----------
        criteria : Tuple[Criterion]
           Tuple of unsorted criteria.

        Returns
        -------
        Dict[str, Criterion]
            Dictionary of criteria sorted by its kinds.

        Raises
        ------
        TypeError
            Raised when an invalid type of criterion is passed.
        """
        constraints = []
        limit_states = []
        objectives = []
        variables = []
        for criterion in criteria:
            if isinstance(criterion, ConstraintCriterion):
                constraints.append(criterion)
            elif isinstance(criterion, LimitStateCriterion):
                limit_states.append(criterion)
            elif isinstance(criterion, ObjectiveCriterion):
                objectives.append(criterion)
            elif isinstance(criterion, VariableCriterion):
                variables.append(criterion)
            else:
                raise TypeError(f"Invalid type of criterion: `{type(criterion)}`.")
        return {
            "constraints": constraints,
            "limit_states": limit_states,
            "objectives": objectives,
            "variables": variables,
        }

    @staticmethod
    def __get_sorted_difference_of_sets(
        first: Iterable[str], second: Iterable[str]
    ) -> Tuple[str, ...]:
        """Get the sorted asymmetric difference of two string sets.

        This method executes the difference of two string sets: ``first - second``.

        Parameters
        ----------
        first: Iterable[str]
            Iterable of strings.
        second: Iterable[str]
            Iterable of string.

        Returns
        -------
        Tuple[str, ...]
            Tuple with the sorted difference.
        """
        diff = list(set(first) - set(second))
        diff.sort()
        return tuple(diff)

    @staticmethod
    def __compare_input_w_processed_values(
        input: dict, processed: dict
    ) -> Tuple[Tuple[str, Union[float, str, bool], Union[float, str, bool]]]:
        """Compare input values of parameters before and after it's processed by server.

        Parameters
        ----------
        input: Dict[str: Union[float, str, bool]]
            Dictionary with parameter's names and values.
        processed: dict
            Server output.

        Return
        ------
        Tuple[Tuple[str, Union[float, str, bool], Union[float, str, bool]]]
            Tuple of parameters with different values before and after processing by server.
                Tuple[0]: name
                Tuple[1]: input value
                Tuple[2]: processed value
        """
        differences = []
        for index, parameter_name in enumerate(processed[0]["result_design"]["parameter_names"]):
            input_value = input.get(parameter_name)
            output_value = processed[0]["result_design"]["parameter_values"][index]
            if input_value and input_value != output_value:
                differences.append((parameter_name, input_value, output_value))
        return tuple(differences)
