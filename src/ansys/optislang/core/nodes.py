"""Contains classes for a node, system, parametric system, and root system."""
from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Iterable, List, Tuple, Union

from ansys.optislang.core.project_parametric import Design, ParameterManager

if TYPE_CHECKING:
    from ansys.optislang.core.osl_server import OslServer


class DesignFlow(Enum):
    """Provides design flow options."""

    NONE = 0
    RECEIVE = 1
    SEND = 2
    RECEIVE_SEND = 3

    @staticmethod
    def from_str(label: str) -> DesignFlow:
        """Convert string to an instance of the ``DesignFlow`` class.

        Parameters
        ----------
        label: str
            String to convert.

        Returns
        -------
        DesignFlow
            Instance of the ``DesignFlow`` class.

        Raises
        ------
        TypeError

        ValueError
            Raised when an inappropriate type of label is given.
        """
        if not isinstance(label, str):
            raise TypeError(f"String was expected, but `{type(label)}` was given.")
        label = label.upper()
        try:
            return eval("DesignFlow." + label)
        except:
            raise ValueError(f"Option `{label}` not available in ``DesignFlow`` options.")


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
            to direct children nodes of the current system.

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
            to direct children nodes of the current system.

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
        max_search_depth: int,
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
        max_search_depth: int
            Maximum depth of the search.

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
            if node["kind"] == "system" and current_depth < max_search_depth:
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
        max_search_depth: int,
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
        max_search_depth: int
            Maximum depth of the search.

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
            if node["kind"] == "system" and current_depth < max_search_depth:
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
    """Provides for creating and operating on a parametric system."""

    def __init__(
        self,
        uid: str,
        osl_server: OslServer,
    ) -> None:
        """Create a ``ParametricSystem`` instance.

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
        self.__parameter_manager = ParameterManager(uid, osl_server)

    @property
    def parameter_manager(self) -> ParameterManager:
        """Instance of the ``ParameterManager`` class.

        Returns
        -------
        ParameterManager
            Instance of the ``ParameterManager`` class.
        """
        return self.__parameter_manager


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
        evaluate_dict = {}
        for parameter in design.parameters:
            evaluate_dict[parameter.name] = parameter.value
        output_dict = self._osl_server.evaluate_design(evaluate_dict=evaluate_dict)
        design._receive_results(output_dict[0])

        design_parameters = design.parameters_names
        output_parameters = output_dict[0]["result_design"]["parameter_names"]
        missing_parameters = RootSystem._compare_two_sets(output_parameters, design_parameters)
        undefined_parameters = RootSystem._compare_two_sets(design_parameters, output_parameters)

        if undefined_parameters:
            self._osl_server._logger.debug(f"Parameters ``{undefined_parameters}`` weren't used.")
        if missing_parameters:
            self._osl_server._logger.warning(
                f"Parameters ``{missing_parameters}`` were missing, "
                "reference values were used for evaluation and list of parameters will be updated."
            )

        for parameter in missing_parameters:
            position = output_dict[0]["result_design"]["parameter_names"].index(parameter)
            design.set_parameter_by_name(
                parameter,
                output_dict[0]["result_design"]["parameter_values"][position],
                False,
            )

        return design

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
        pm = self.parameter_manager
        parameters = pm.get_parameters()
        return Design(parameters=parameters)

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
        return RootSystem._compare_two_sets(
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
        return RootSystem._compare_two_sets(
            first=design.parameters_names,
            second=self.parameter_manager.get_parameters_names(),
        )

    @staticmethod
    def _compare_two_sets(first: Iterable[str], second: Iterable[str]) -> Tuple[str, ...]:
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
