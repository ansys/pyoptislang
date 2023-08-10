"""Contains classes for a node, system, parametric system, and root system."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Tuple, Union

from deprecated import deprecated

from ansys.optislang.core.base_nodes import (
    DesignFlow,
    Edge,
    InputSlot,
    Node,
    ParametricSystem,
    RootSystem,
    Slot,
    SlotType,
    System,
    TcpInnerInputSlotProxy,
    TcpInnerOutputSlotProxy,
    TcpOutputSlotProxy,
)
from ansys.optislang.core.node_types import AddinType, NodeType
from ansys.optislang.core.project_parametric import (
    ConstraintCriterion,
    Design,
    DesignStatus,
    DesignVariable,
    LimitStateCriterion,
    ObjectiveCriterion,
    VariableCriterion,
)
from ansys.optislang.core.tcp.managers import (
    TcpCriteriaManagerProxy,
    TcpParameterManagerProxy,
    TcpResponseManagerProxy,
)

if TYPE_CHECKING:
    from ansys.optislang.core.project_parametric import Criterion
    from ansys.optislang.core.tcp.osl_server import TcpOslServer


class TcpNodeProxy(Node):
    """Provides for creating and operating on nodes."""

    def __init__(
        self,
        uid: str,
        osl_server: TcpOslServer,
        type_: Union[NodeType, str],
        logger=None,
    ) -> None:
        """Create a ``TcpNodeProxy`` instance.

        Parameters
        ----------
        uid: str
            Unique ID of the node.
        osl_server: TcpOslServer
            Object providing access to the optiSLang server.
        type_: Union[NodeType, str]
            Instance of the ``NodeType`` class for supported nodes, ``string`` otherwise.
        logger: Any, optional
            Object for logging. If ``None``, standard logging object is used. Defaults to ``None``.
        """
        self._osl_server = osl_server
        self.__uid = uid
        if not isinstance(type_, NodeType):
            raise TypeError(f"Unsupported type of type_: ``{type(type_)}``.")
        self.__type = type_
        self._logger = logging.getLogger(__name__) if logger is None else logger

    def __str__(self):
        """Return formatted string."""
        type_ = self.type.id
        return f"Node type: {type_} Name: {self.get_name()} Uid: {self.uid}"

    @property
    def uid(self) -> str:
        """Unique ID of the node.

        Returns
        -------
        str
            Unique ID of the node.
        """
        return self.__uid

    @property
    def type(self) -> NodeType:
        """Type of the node.

        Returns
        -------
        NodeType
            Instance of the ``NodeType`` class.
        """
        return self.__type

    def delete(self) -> None:
        """Delete current node and it's children from active project.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self._osl_server.remove_node(self.uid)

    def exists(self) -> bool:
        """Get info whether node exists in active project.

        Returns
        -------
        bool
            Whether current node exists in active project.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        project_tree = self._osl_server.get_full_project_tree()
        return (
            len(
                self.__class__._find_node_with_uid(
                    uid=self.uid,
                    tree=project_tree["projects"][0]["system"],
                    properties_dicts_list=[],
                    current_depth=1,
                    max_search_depth=float("inf"),
                )
            )
            > 0
        )

    def get_ancestors(self) -> Tuple[TcpNodeProxy, ...]:
        """Get tuple of ordered ancestors starting from root system at position 0.

        Return
        ------
        Tuple[TcpNodeProxy, ...]
            Tuple of ordered ancestors, starting from root system at position.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        if isinstance(self, TcpRootSystemProxy):
            self._logger.warning(
                "``TcpRootSystemProxy`` doesn't have any ancestors, empty tuple will be returned."
            )
            return ()
        project_tree = self._osl_server.get_full_project_tree_with_properties()
        parent_tree = project_tree["projects"][0]["system"]
        ancestors_line_dicts = [
            {
                "type": parent_tree["type"],
                "name": parent_tree["name"],
                "uid": parent_tree["uid"],
                "kind": "root_system",
                "is_parametric_system": "ParameterManager" in parent_tree.get("properties", {}),
            },
        ]
        ancestors_line_dicts = self.__class__._find_ancestor_line(
            tree=parent_tree,
            ancestor_line=ancestors_line_dicts,
            node_uid=self.uid,
            current_depth=1,
            was_found=[],
        )
        return self._create_nodes_from_properties_dicts(properties_dicts_list=ancestors_line_dicts)

    def get_connections(
        self, slot_type: Union[SlotType, None] = None, slot_name: Union[str, None] = None
    ) -> Tuple[Edge]:
        """Get connections of a given direction and slot.

        Parameters
        ----------
        slot_type: Union[SlotType, None], optional
            Slot type, by default ``None``
        slot_name : Union[str, None], optional
            Slot name, by default ``None``.

        Returns
        -------
        Tuple[Edge]
            Tuple of connections of given direction and slot.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expire
        """
        project_tree = self._osl_server.get_full_project_tree_with_properties()
        connections = project_tree.get("projects", [{}])[0].get("connections")
        direction = SlotType.to_dir_str(type_=slot_type)
        filtered_connections = self._filter_connections(
            connections=connections,
            uid=self.uid,
            direction=direction,
            slot_name=slot_name,
        )
        edges = []
        for connection in filtered_connections:
            edges.append(
                self._create_edge_from_dict(
                    project_tree=project_tree["projects"][0]["system"], connection=connection
                )
            )
        return tuple(edges)

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

    def get_parent(self) -> TcpNodeProxy:
        """Get the instance of the parent node.

        Returns
        -------
        TcpNodeProxy
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
        return self.get_ancestors()[-1]

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
        return self.get_parent().get_name()

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
        return self._osl_server.get_actor_properties(uid=self.uid)

    def get_property(self, name: str) -> Any:
        """Get property from properties dictionary.

        Parameters
        ----------
        name
            Name of property to be returned.

        Returns
        -------
        Any
            Value of given property, ``None`` if property doesn't exits.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self._osl_server.get_actor_properties(uid=self.uid).get(name, None)

    def get_slots(
        self, type_: Union[SlotType, None] = None, name: Union[str, None] = None
    ) -> Tuple[TcpSlotProxy, ...]:
        """Get current node's slots of given type and name.

        Parameters
        ----------
        type_: Union[SlotType, None], optional
            Type of slots to be returned, by default ``None``.
        name : Union[str, None], optional
            Slot name, by default ``None``.

        Returns
        -------
        Tuple[TcpSlotProxy, ...]
            Tuple of current node's slots of given type.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        info = self._get_info()
        if isinstance(type_, SlotType):
            keys = [type_.name.lower() + "_slots"]
        else:
            keys = [slot_type.name.lower() + "_slots" for slot_type in SlotType]
        slots_dicts_mapping = {}
        for key in keys:
            slots_dicts_mapping[key] = info.get(key, [])
        slots_list = []
        for slot_type, slots_dicts in slots_dicts_mapping.items():
            for slot_dict in slots_dicts:
                if name is not None and name != slot_dict["name"]:
                    continue
                slots_list.append(
                    TcpSlotProxy.create_slot(
                        osl_server=self._osl_server,
                        node=self,
                        name=slot_dict["name"],
                        type_=SlotType.from_str(string=slot_type[0:-6]),
                        type_hint=slot_dict["type"],
                    )
                )
        return tuple(slots_list)

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

    @deprecated(version="0.2.1", reason="Use ``TcpNodeProxy.type`` instead.")
    def get_type(self) -> NodeType:
        """Get the type of the node.

        Returns
        -------
        NodeType
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
        return self.__class__._create_nodetype_from_str(string=actor_info["type"])

    def set_property(self, name: str, value: Any) -> None:
        """Set node's property.

        Parameters
        ----------
        name : str
            Property name.
        value : Any
            Property value.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self._osl_server.set_actor_property(actor_uid=self.uid, name=name, value=value)

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

    def _get_parent_dict(self) -> dict:
        """Get the unique ID of the parent node.

        Return
        ------
        dict
            Dictionary with necessary information for creating instance of parent node.

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
        return self.__class__._find_parent_node_info(
            tree=parent_tree,
            parent_uid=root_system_uid,
            node_uid=self.uid,
        )

    def _create_edge_from_dict(self, project_tree: dict, connection: dict) -> Edge:
        """Create edge from project tree and connection dictionary.

        Parameters
        ----------
        project_tree : dict
            Dictionary with project structure.
        connection : dict
            Dictionary describing connection.

        Returns
        -------
        Edge
            Instance of the Edge class.
        """
        rec_slot_name = connection["receiving_slot"]
        rec_slot_type = connection.get("receiving_slot_type", None)
        # TODO: replace query after dictionary extension
        info = self._osl_server.get_actor_info(connection["receiving_uuid"])
        if not rec_slot_type:
            info = self._osl_server.get_actor_info(connection["receiving_uuid"])
            if True in [item["name"] == rec_slot_name for item in info["input_slots"]]:
                rec_slot_type = SlotType.INPUT
            elif True in [
                item["name"] == rec_slot_name for item in info.get("inner_input_slots", [])
            ]:
                rec_slot_type = SlotType.INNER_INPUT
            else:
                raise ValueError(f"Slot ``{rec_slot_name}`` doesn't exist for given node.")
        rec_slot = self._create_slot_from_project_tree(
            project_tree=project_tree,
            uid=connection["receiving_uuid"],
            slot_name=rec_slot_name,
            slot_type=rec_slot_type,
        )

        sen_slot_name = connection["sending_slot"]
        sen_slot_type = connection.get("sending_slot_type", None)
        # TODO: replace query after dictionary extension
        if not sen_slot_type:
            info = self._osl_server.get_actor_info(connection["sending_uuid"])
            if True in [item["name"] == sen_slot_name for item in info["output_slots"]]:
                sen_slot_type = SlotType.OUTPUT
            elif True in [
                item["name"] == sen_slot_name for item in info.get("inner_output_slots", [])
            ]:
                sen_slot_type = SlotType.INNER_OUTPUT
            else:
                raise ValueError(f"Slot ``{rec_slot_name}`` doesn't exist for given node.")
        sen_slot = self._create_slot_from_project_tree(
            project_tree=project_tree,
            uid=connection["sending_uuid"],
            slot_name=sen_slot_name,
            slot_type=sen_slot_type,
        )

        return Edge(from_slot=sen_slot, to_slot=rec_slot)

    def _create_nodes_from_properties_dicts(
        self, properties_dicts_list: List[dict]
    ) -> Tuple[TcpNodeProxy, ...]:
        """Create nodes from a dictionary of properties.

        Parameters
        ----------
        properties_dicts_list : List[dict]
            Dictionary of node properties.

        Returns
        -------
        Tuple[TcpNodeProxy, ...]
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
            type_ = self.__class__._create_nodetype_from_str(node["type"])
            if kind == "actor":
                nodes_list.append(
                    TcpNodeProxy(
                        uid=uid, osl_server=self._osl_server, type_=type_, logger=self._logger
                    )
                )
            elif kind == "system":
                if node["is_parametric_system"]:
                    nodes_list.append(
                        TcpParametricSystemProxy(
                            uid=uid, osl_server=self._osl_server, type_=type_, logger=self._logger
                        )
                    )
                else:
                    nodes_list.append(
                        TcpSystemProxy(
                            uid=uid, osl_server=self._osl_server, type_=type_, logger=self._logger
                        )
                    )
            elif kind == "root_system":
                nodes_list.append(
                    TcpRootSystemProxy(
                        uid=node["uid"], osl_server=self._osl_server, logger=self._logger
                    )
                )
            else:
                TypeError(
                    f'Unknown kind of component: "{kind}", '
                    '"node", "system" or "root_system" were expected.'
                )

        return tuple(nodes_list)

    def _create_slot_from_project_tree(
        self,
        project_tree: dict,
        uid: str,
        slot_name: str,
        slot_type: SlotType,
        node: Union[TcpNodeProxy, None] = None,
    ) -> TcpSlotProxy:
        """Create slot from project tree.

        Parameters
        ----------
        project_tree : dict
            Project tree
        uid: str
            Node uid.
        slot_name: str
            Slot name.
        slot_type: SlotType
            Slot type.

        Returns
        -------
        TcpSlotProxy
            Instance of the ``TcpSlotProxy`` class.
        """
        if uid == self.uid:
            node = self
        elif uid == project_tree["uid"]:
            node = TcpRootSystemProxy(uid=uid, osl_server=self._osl_server, logger=self._logger)
        else:
            node_dict = self.__class__._find_node_with_uid(
                uid=uid,
                tree=project_tree,
                properties_dicts_list=[],
                current_depth=1,
                max_search_depth=float("inf"),
            )
            node = self._create_nodes_from_properties_dicts(properties_dicts_list=node_dict)[0]
        return TcpSlotProxy.create_slot(
            osl_server=self._osl_server, node=node, name=slot_name, type_=slot_type
        )

    @deprecated(version="0.2.1", reason="Not used anymore.")
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

    def _filter_connections(
        self,
        connections: List[dict],
        uid: str,
        slot_type: Union[SlotType, None],
        slot_name: Union[str, None] = None,
    ) -> Tuple[dict]:
        """Filter list of connections to by given node, slot type and optionally slot name.

        Parameters
        ----------
        connections : List[dict]
            List of connections.
        uid: str
            Node uid.
        slot_type: Union[SlotType, None], optional
            Type of the slot, by default ``None``.
        slot_name: Union[str, None], optional
            Name of the slot, by default ``None``.

        Returns
        -------
        Tuple[dict]
            Tuple of filtered connections dictionaries.
        """
        filtered_connections = []

        # skip for combination of inner slot with TcpNodeProxy or it's subclasses
        if not (
            isinstance(self.__class__, TcpSystemProxy) or issubclass(self.__class__, TcpSystemProxy)
        ) and isinstance(slot_type, SlotType):
            if slot_type in [SlotType.INNER_INPUT, SlotType.INNER_OUTPUT]:
                return tuple(filtered_connections)

        # prepare keys for tcp server output dictionary
        if isinstance(slot_type, SlotType):
            direction = SlotType.to_dir_str(slot_type)
            uid_keys = [direction + "_uuid"]
            slot_name_keys = [direction + "_slot"]
        else:
            uid_keys = ["receiving_uuid", "sending_uuid"]
            slot_name_keys = ["receiving_slot", "sending_slot"]
        for connection in connections:
            # filter connections, that do not contain current node
            if uid not in [connection[key] for key in uid_keys]:
                continue
            # filter slots, that do not contain given name
            if slot_name is not None and slot_name not in [
                connection[key] for key in slot_name_keys
            ]:
                continue
            # filter connections by slot type (only for system and subclasses), since nodes
            # do not have inner input slots and this combination was excluded at the beginning
            if (
                isinstance(self.__class__, TcpSystemProxy)
                or issubclass(self.__class__, TcpSystemProxy)
            ) and isinstance(slot_type, SlotType):
                info = self._osl_server.get_actor_info(connection[uid_keys[0]])
                if True in [
                    item["name"] == connection[slot_name_keys[0]]
                    for item in info[slot_type.name.lower() + "_slots"]
                ]:
                    connection[slot_name_keys[0] + "_type"] = slot_type
                else:
                    continue
            filtered_connections.append(connection)
        return tuple(filtered_connections)

    @staticmethod
    def _create_nodetype_from_str(string: str) -> NodeType:
        """Create instance of ``NodeType`` from optiSLang server output.

        Parameters
        ----------
        string : str
            Actor type in optiSLang server output format.

        Returns
        -------
        NodeType
            Instance of ``NodeType`` class.
        """
        customs = {
            "AlgorithmSystem_": AddinType.PYTHON_BASED_ALGORITHM_PLUGIN,
            "AlgorithmSystemPlugin_": AddinType.ALGORITHM_PLUGIN,
            "Custom_": AddinType.PYTHON_BASED_NODE_PLUGIN,
            "CustomETKIntegration_": "",  # TODO: append addin type
            "CustomIntegration_": AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
            "CustomMop_": AddinType.PYTHON_BASED_MOP_NODE_PLUGIN,
            "IntegrationPlugin_": AddinType.INTEGRATION_PLUGIN,
        }
        if string in customs.keys():
            id = string[:-1]
            subtype = AddinType.BUILT_IN
        else:
            was_found = False
            for custom in customs.keys():
                if string.startswith(custom):
                    id = string.replace(custom, "")
                    subtype = customs[custom]
                    was_found = True
                    break
            if not was_found:
                id = string
                subtype = AddinType.BUILT_IN
        return NodeType(id=id, subtype=subtype)

    @staticmethod
    def _find_ancestor_line(
        tree: dict,
        ancestor_line: List[dict],
        node_uid: str,
        current_depth: int,
        was_found: list,
    ) -> Tuple[dict, ...]:
        """Get ancestor line starting from root system.

        Parameters
        ----------
        tree: dict
            Dictionary with children nodes.
        ancestor_line: List[dict]
            List of dictionaries with necessary information for node creation.
        node_uid: str
            Unique ID of the node for which to search for the parent.
        current_depth: int
            Current depth of the search.
        was_found: list
            Empty list, until node_uid is located.

        Return
        ------
        str
            Unique ID of the parent node.

        Raises
        ------
        RuntimeError
            Raised when node was not located in structure tree.
        """
        for node in tree["nodes"]:
            if node["uid"] == node_uid:
                was_found.append("True")
                return ancestor_line
            if node["kind"] == "system":
                ancestor_line.append(
                    {
                        "type": node["type"],
                        "name": node["name"],
                        "uid": node["uid"],
                        "kind": node["kind"],
                        "is_parametric_system": "ParameterManager" in node.get("properties", {}),
                    }
                )
                __class__._find_ancestor_line(
                    tree=node,
                    ancestor_line=ancestor_line,
                    node_uid=node_uid,
                    current_depth=current_depth + 1,
                    was_found=was_found,
                )
                if len(was_found) == 1:
                    return ancestor_line
                else:
                    ancestor_line = ancestor_line[0:current_depth]
        return ancestor_line

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
        List[dict]
            List of dictionaries with necessary information for creation of a node.
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
                        "is_parametric_system": node.get("properties", {}).get(
                            "ParameterManager", False
                        ),
                    }
                )
            if node["kind"] == "system" and current_depth < max_search_depth:
                __class__._find_nodes_with_name(
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
        List[dict]
            List of dictionaries with the necessary information for creation of a node.
        """
        for node in tree["nodes"]:
            if len(properties_dicts_list) != 0:
                break
            if node["uid"] == uid:
                properties_dicts_list.append(
                    {
                        "type": node["type"],
                        "name": node["name"],
                        "uid": node["uid"],
                        "parent_uid": tree["uid"],
                        "parent_name": tree["name"],
                        "kind": node["kind"],
                        "is_parametric_system": "ParameterManager" in node.get("properties", {}),
                    }
                )
            if node["kind"] == "system" and current_depth < max_search_depth:
                __class__._find_node_with_uid(
                    uid=uid,
                    tree=node,
                    properties_dicts_list=properties_dicts_list,
                    current_depth=current_depth + 1,
                    max_search_depth=max_search_depth,
                )
        return properties_dicts_list

    @staticmethod
    def _find_parent_node_info(tree: dict, parent_info: dict, node_uid: str) -> dict:
        """Get dictionary with necessary information for parent node creation.

        Parameters
        ----------
        tree: dict
            Dictionary with children nodes.
        parent_info: str
            Dictionary with necessary information for parent node creation.
        node_uid: str
            Unique ID of the node for which to search for the parent.

        Return
        ------
        dict
            Dictionary with necessary information for parent node creation.

        Raises
        ------
        RuntimeError
            Raised when node was not located in structure tree.
        """
        for node in tree["nodes"]:
            if parent_info.get("child_node_was_found"):
                return parent_info
            if node["uid"] == node_uid:
                parent_info["child_node_was_found"] = True
            if node["kind"] == "system":
                new_parent_info = {
                    "type": node["type"],
                    "name": node["name"],
                    "uid": node["uid"],
                    "kind": node["kind"],
                    "is_parametric_system": "ParameterManager" in node.get("properties", {}),
                }
                __class__._find_parent_node_info(
                    tree=node,
                    parent_info=new_parent_info,
                    node_uid=node_uid,
                )


class TcpSystemProxy(TcpNodeProxy, System):
    """Provides for creating and operating on a system."""

    def __init__(
        self,
        uid: str,
        osl_server: TcpOslServer,
        type_: NodeType,
        logger=None,
    ) -> None:
        """Create an ``TcpSystemProxy`` instance.

        Parameters
        ----------
        uid: str
            Unique ID.
        osl_server: TcpOslServer
            Object providing access to the optiSLang server.
        type_: NodeType
            Instance of the ``NodeType`` class.
        logger: Any, optional
            Object for logging. If ``None``, standard logging object is used. Defaults to ``None``.
        """
        super().__init__(
            uid=uid,
            osl_server=osl_server,
            type_=type_,
            logger=logger,
        )

    def create_node(
        self,
        type_: NodeType,
        name: Union[str, None] = None,
        design_flow: Union[DesignFlow, None] = None,
    ) -> TcpNodeProxy:
        """Create a new node in current system in active project.

        Parameters
        ----------
        type_ : NodeType
            Type of created node.
        name : Union[str, None], optional
            Name of created node, by default None.
        design_flow : Union[DesignFlow, None], optional
            Design flow, by default None.

        Returns
        -------
        TcpNodeProxy
            Instance of the created node.

        Raises
        ------
        TypeError
            Raised when unsupported type of type_ is given.
        ValueError
            Raised when unsupported value of type_ is given.
        """
        if not isinstance(type_, NodeType):
            raise TypeError(
                f"Invalid type of ``type_: {type(type_)}``, "
                "``NodeType`` or ``str`` was expected."
            )
        if type_.id == "RunnableSystem":
            raise ValueError("Creation of RootSystem is not supported.")

        (
            algorithm_type,
            integration_type,
            mop_node_type,
            node_type,
        ) = self.__class__._get_subtypes(addin_type=type_.subtype)

        design_flow_name = design_flow.name.lower() if design_flow is not None else None
        uid = self._osl_server.create_node(
            type_=type_.id,
            name=name,
            algorithm_type=algorithm_type,
            integration_type=integration_type,
            mop_node_type=mop_node_type,
            node_type=node_type,
            parent_uid=self.uid,
            design_flow=design_flow_name,
        )
        info = self._osl_server.get_actor_info(uid=uid)
        info["is_parametric_system"] = "estimated_designs" in info.keys()
        return self._create_nodes_from_properties_dicts([info])[0]

    def delete_children_nodes(self) -> None:
        """Delete all children nodes from the active project.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        nodes = self.get_nodes()
        for node in nodes:
            node.delete()

    def find_node_by_uid(self, uid: str, search_depth: int = 1) -> Union[TcpNodeProxy, None]:
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
        Union[TcpNodeProxy, None]
            ``TcpNodeProxy`` with the specified unique ID. If this ID isn't located in any
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
            system_tree = self.__class__._find_subtree(
                tree=project_tree["projects"][0]["system"],
                uid=self.uid,
            )
        properties_dicts_list = self.__class__._find_node_with_uid(
            uid=uid,
            tree=system_tree,
            properties_dicts_list=[],
            current_depth=1,
            max_search_depth=search_depth,
        )

        if len(properties_dicts_list) == 0:
            self._logger.error(f"Node `{uid}` was not found in the current system.")
            return None

        return self._create_nodes_from_properties_dicts(
            properties_dicts_list=properties_dicts_list
        )[0]

    def find_nodes_by_name(self, name: str, search_depth: int = 1) -> Tuple[TcpNodeProxy, ...]:
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
        Tuple[TcpNodeProxy, ...]
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
            system_tree = self.__class__._find_subtree(
                tree=project_tree["projects"][0]["system"],
                uid=self.uid,
            )
        properties_dicts_list = self.__class__._find_nodes_with_name(
            name=name,
            tree=system_tree,
            properties_dicts_list=[],
            current_depth=1,
            max_search_depth=search_depth,
        )

        if len(properties_dicts_list) == 0:
            self._logger.error(f"Node `{name}` not found in the current system.")
            return tuple()

        return self._create_nodes_from_properties_dicts(properties_dicts_list=properties_dicts_list)

    def get_nodes(self) -> Tuple[TcpNodeProxy, ...]:
        """Get the direct children nodes.

        Returns
        -------
        Tuple[TcpNodeProxy, ...]
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

    def _get_nodes_dicts(self) -> Tuple[dict, ...]:
        """Get data for children nodes.

        Returns
        -------
        Tuple[dict, ...]
            Tuple of dictionaries with data for children nodes.

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
            system_tree = self.__class__._find_subtree(
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
                    "is_parametric_system": "ParameterManager" in node.get("properties", {}),
                }
            )
        return tuple(children_dicts_list)

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
                __class__._find_subtree(tree=node, uid=uid)

    @staticmethod
    def _get_subtypes(
        addin_type: AddinType,
    ) -> Tuple[Union[str, None], Union[str, None], Union[str, None], Union[str, None]]:
        """Get subtypes in tcp server input format.

        Parameters
        ----------
        addin_type: AddinType
            Node's subtype.

        Returns
        -------
        Tuple[Union[str, None], Union[str, None], Union[str, None], Union[str, None]]
            algorithm_type, integration_type, mop_node_type, node_type
        """
        if not isinstance(addin_type, AddinType):
            raise TypeError(f"Unsupported value of addin_type: ``{type(addin_type)}``.")

        algorithm_type, integration_type, mop_node_type, node_type = None, None, None, None
        if addin_type == AddinType.BUILT_IN:
            pass
        elif addin_type == AddinType.INTEGRATION_PLUGIN:
            integration_type = "integration_plugin"
        elif addin_type == AddinType.PYTHON_BASED_INTEGRATION_PLUGIN:
            integration_type = "python_based_integration_plugin"
        elif addin_type == AddinType.PYTHON_BASED_ALGORITHM_PLUGIN:
            algorithm_type = "python_based_algorithm_plugin"
        elif addin_type == AddinType.ALGORITHM_PLUGIN:
            algorithm_type = "algorithm_plugin"
        elif addin_type == AddinType.PYTHON_BASED_MOP_NODE_PLUGIN:
            mop_node_type = "python_based_mop_node_plugin"
        elif addin_type == AddinType.PYTHON_BASED_NODE_PLUGIN:
            node_type = "python_based_node_plugin"
        else:
            raise ValueError(f"Unsupported value of addin_type: ``{addin_type}``.")

        return algorithm_type, integration_type, mop_node_type, node_type


class TcpParametricSystemProxy(TcpSystemProxy, ParametricSystem):
    """Provides for creating and operationg on parametric system."""

    def __init__(
        self,
        uid: str,
        osl_server: TcpOslServer,
        type_: NodeType,
        logger=None,
    ) -> None:
        """Create a parametric system.

        Parameters
        ----------
        uid: str
            Unique ID.
        osl_server: TcpOslServer
            Object providing access to the optiSLang server.
        type_: NodeType
            Instance of the ``NodeType`` class.
        logger: Any, optional
            Object for logging. If ``None``, standard logging object is used. Defaults to ``None``.
        """
        super().__init__(
            uid=uid,
            osl_server=osl_server,
            type_=type_,
            logger=logger,
        )
        self.__criteria_manager = TcpCriteriaManagerProxy(uid, osl_server)
        self.__parameter_manager = TcpParameterManagerProxy(uid, osl_server)
        self.__response_manager = TcpResponseManagerProxy(uid, osl_server)

    @property
    def criteria_manager(self) -> TcpCriteriaManagerProxy:
        """Criteria manager of the current system.

        Returns
        -------
        TcpCriteriaManagerProxy
            Instance of the ``TcpCriteriaManagerProxy`` class.
        """
        return self.__criteria_manager

    @property
    def parameter_manager(self) -> TcpParameterManagerProxy:
        """Parameter manager of the current system.

        Returns
        -------
        TcpParameterManagerProxy
            Instance of the ``TcpParameterManagerProxy`` class.
        """
        return self.__parameter_manager

    @property
    def response_manager(self) -> TcpResponseManagerProxy:
        """Response manager of the current system.

        Returns
        -------
        TcpResponseManagerProxy
            Instance of the ``TcpResponseManagerProxy`` class.
        """
        return self.__response_manager


class TcpRootSystemProxy(TcpParametricSystemProxy, RootSystem):
    """Provides for creating and operating on a project system."""

    def __init__(
        self,
        uid: str,
        osl_server: TcpOslServer,
        logger=None,
    ) -> None:
        """Create an instance of ``TcpRootSystemProxy`` class.

        Parameters
        ----------
        uid: str
            Unique ID.
        osl_server: TcpOslServer
            Object providing access to the optiSLang server.
        logger: Any, optional
            Object for logging. If ``None``, standard logging object is used. Defaults to ``None``.
        """
        super().__init__(
            uid=uid,
            osl_server=osl_server,
            type_=NodeType(id="RunnableSystem", subtype=AddinType.BUILT_IN),
            logger=logger,
        )

    def delete(self) -> None:
        """Delete current node and it's children from active project.

        Raises
        ------
        NotImplementedError
            Raised always.
        """
        raise NotImplementedError("``RootSystem`` cannot be deleted.")

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
        return self.__create_evaluated_design(
            input_design=design, evaluate_dict=evaluate_dict, results=output_dict[0]
        )

    def get_reference_design(self) -> Design:
        """Get the design with reference values of the parameters.

        Returns
        -------
        TcpDesign
            Instance of the ``TcpDesign`` class with defined parameters and reference values.

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
        design: TcpDesign
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
        design: TcpDesign
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

    def __create_evaluated_design(
        self, input_design: Design, evaluate_dict: Dict, results: Dict
    ) -> Design:
        """Create a new instance of ``Design`` with results.

        Parameters
        ----------
        input_design: Design
            Design that was evaluated.
        evaluate_dict: dict
            Dictionary used for evaluation.
        results: Dict
            Output from the evaluation of the input design.

        Return
        ------
        Design
            Instance of the ``Design`` class with results.
        """
        id = results["result_design"]["hid"]
        feasibility = results["result_design"]["feasible"]
        status = DesignStatus.from_str(results["result_design"]["status"])

        # constraint
        constraints = []
        for position, constraint in enumerate(results["result_design"]["constraint_names"]):
            constraints.append(
                DesignVariable(
                    name=constraint,
                    value=results["result_design"]["constraint_values"][position],
                )
            )
        # limit state
        limit_states = []
        for position, limit_state in enumerate(results["result_design"]["limit_state_names"]):
            limit_states.append(
                DesignVariable(
                    name=limit_state,
                    value=results["result_design"]["limit_state_values"][position],
                )
            )
        # objective
        objectives = []
        for position, objective in enumerate(results["result_design"]["objective_names"]):
            objectives.append(
                DesignVariable(
                    name=objective,
                    value=results["result_design"]["objective_values"][position],
                )
            )
        # responses
        responses = []
        for position, response in enumerate(results["result_design"]["response_names"]):
            responses.append(
                DesignVariable(
                    name=response,
                    value=results["result_design"]["response_values"][position],
                )
            )
        # variables
        variables = []
        for position, variable in enumerate(results["result_design"]["variable_names"]):
            variables.append(
                DesignVariable(
                    name=variable,
                    value=results["result_design"]["variable_values"][position],
                )
            )

        # create instance of design with new values
        output_design = Design(
            parameters=input_design.parameters,
            constraints=constraints,
            limit_states=limit_states,
            objectives=objectives,
            variables=variables,
            responses=responses,
            feasibility=feasibility,
            design_id=id,
            status=status,
        )

        # compare input and output values
        input_design_parameters = input_design.parameters_names
        output_parameters = results["result_design"]["parameter_names"]
        missing_parameters = __class__.__get_sorted_difference_of_sets(
            output_parameters, input_design_parameters
        )
        undefined_parameters = __class__.__get_sorted_difference_of_sets(
            input_design_parameters, output_parameters
        )
        unused = __class__.__compare_input_w_processed_parameters_values(evaluate_dict, results)

        if undefined_parameters:
            self._logger.debug(f"Parameters ``{undefined_parameters}`` weren't used.")
        if missing_parameters:
            self._logger.warning(
                f"Parameters ``{missing_parameters}`` were missing, "
                "reference values were used for evaluation and list of parameters will be updated."
            )
        if unused:
            self._logger.warning(
                "Values of parameters were changed:"
                f"{[par[0] + ': ' + str(par[1]) + ' -> ' + str(par[2]) for par in unused]}"
            )

        # update design with missing parameters
        # (parameters not defined in input design, but used for evaluation)
        for parameter in missing_parameters:
            position = results["result_design"]["parameter_names"].index(parameter)
            output_design.set_parameter_by_name(
                parameter,
                results["result_design"]["parameter_values"][position],
                False,
            )

        return output_design

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
    def __compare_input_w_processed_parameters_values(
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
        for index, parameter_name in enumerate(processed["result_design"]["parameter_names"]):
            input_value = input.get(parameter_name)
            output_value = processed["result_design"]["parameter_values"][index]
            if input_value and input_value != output_value:
                differences.append((parameter_name, input_value, output_value))
        return tuple(differences)

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


# TODO: test
class TcpSlotProxy(Slot):
    """Provides for creating and operating on slots."""

    def __init__(
        self,
        osl_server: TcpOslServer,
        node: TcpNodeProxy,
        name: str,
        type_: SlotType,
        type_hint: Union[str, None] = None,
    ) -> None:
        """Create an ``TcpSlotProxy`` instance.

        Parameters
        ----------
        osl_server: TcpOslServer
            Object providing access to the optiSLang server.
        node : TcpNodeProxy
            Node to which the slot belongs.
        name : str
           Slot name.
        type_ : SlotType
            Slot type.
        type_hint : Union[str, None], optional
            Description, by default None.
        """
        self._osl_server = osl_server
        self.__node = node
        self.__name = name
        self.__type = type_
        self.__type_hint = type_hint

    def __str__(self):
        """Return formatted string."""
        return f"Slot type: {self.type.name} Name: {self.name()}"

    @property
    def name(self) -> str:
        """Get slot name.

        Return
        ------
        str
            Slot name.
        """
        return self.__name

    @property
    def node(self) -> TcpNodeProxy:
        """Get node to which the slot belongs.

        Return
        ------
        TcpNodeProxy
            Node to which the slot belongs.
        """
        return self.__node

    @property
    def type(self) -> SlotType:
        """Get slot type.

        Return
        ------
        SlotType
            Type of current slot.
        """
        return self.__type

    @property
    def type_hint(self) -> Union[str, None]:
        """Get type hint.

        Return
        ------
        Union[str, None]
            Data type of the current slot, ``None`` if not specified.
        """
        return self.__type_hint

    def get_connections(self) -> Tuple[Edge]:
        """Get connections for the current slot.

        Returns
        -------
        Tuple[Edge]
            Tuple with connections of the current slot.
        """
        return self.node.get_connections(slot_type=self.type, slot_name=self.name)

    def get_type_hint(self) -> str:
        """Get slot's expected data type.

        Returns
        -------
        str
            Type hint.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        info = self.node._get_info()
        key = self.type.name.lower() + "_slots"
        slots_dict_list = info.get(key)
        for slot in slots_dict_list:
            if self.name == slot["name"]:
                self.__type_hint = slot["type"]
                return self.type_hint
        raise NameError(f"Current slot: ``{self.name}`` wasn't found in node: ``{self.node.uid}``.")

    @staticmethod
    def create_slot(
        osl_server: TcpOslServer,
        node: TcpNodeProxy,
        name: str,
        type_: SlotType,
        type_hint: Union[str, None] = None,
    ) -> TcpSlotProxy:
        """Create instance of new slot.

        Parameters
        ----------
        osl_server: TcpOslServer
            Object providing access to the optiSLang server.
        node : TcpNodeProxy
            Node to which slot belongs to.
        name : str
            Slot name.
        type_ : SlotType
            Slot type.
        type_hint : Union[str, None], optional
            Slot's expected data type, by default None.

        Returns
        -------
        TcpSlotProxy
            Instance of TcpInputSlotProxy, TcpOutputSlotProxy, TcpInnerInputSlotProxy
            or TcpInnerOutputSlotProxy class.
        """
        if type_ == SlotType.INPUT:
            return TcpInputSlotProxy(
                osl_server=osl_server, node=node, name=name, type_=type_, type_hint=type_hint
            )
        elif type_ == SlotType.INNER_INPUT:
            return TcpInnerInputSlotProxy(
                osl_server=osl_server, node=node, name=name, type_=type_, type_hint=type_hint
            )
        elif type_ == SlotType.OUTPUT:
            return TcpOutputSlotProxy(
                osl_server=osl_server, node=node, name=name, type_=type_, type_hint=type_hint
            )
        elif type_ == SlotType.INNER_OUTPUT:
            return TcpInnerOutputSlotProxy(
                osl_server=osl_server, node=node, name=name, type_=type_, type_hint=type_hint
            )
        else:
            raise TypeError(
                f"Type of ``type_`` = ``SlotType`` was expected, but ``{type(type_)}`` was given."
            )

    @staticmethod
    def _create_connection_script(from_slot: TcpSlotProxy, to_slot: TcpSlotProxy) -> str:
        """Create optiSLang python script for slot connection.

        Parameters
        ----------
        from_slot : TcpSlotProxy
            Sending slot.
        to_slot : TcpSlotProxy
            Receiving slot.

        Returns
        -------
        str
            Python script for slot connection.
        """
        # TODO: Remove this, after server command `connect_nodes` is fixed (works for inner slots).
        if isinstance(from_slot.node, TcpRootSystemProxy):
            from_actor_script = "from_actor = project.get_root_system()\n"
        else:
            from_actor_script = __class__._create_find_actor_script(
                node=from_slot.node, name="from_actor"
            )

        if isinstance(to_slot.node, TcpRootSystemProxy):
            to_actor_script = "to_actor = project.get_root_system()"
        else:
            to_actor_script = __class__._create_find_actor_script(
                node=to_slot.node, name="to_actor"
            )

        final_script = (
            f"{from_actor_script}\n"
            f"{to_actor_script}\n"
            f"connect(from_actor=from_actor, from_slot='{from_slot.name}', "
            f"to_actor=to_actor, to_slot='{to_slot.name}')\n"
        )
        return final_script

    @staticmethod
    def _create_find_actor_script(node: TcpNodeProxy, name: str):
        """Create optiSLang python script to find actor.

        Parameters
        ----------
        node : TcpNodeProxy
            Node to be found.
        name : str
            Name used to store actor.

        Returns
        -------
        str
            Python script for finding given node.
        """
        actor_ancestors = node.get_ancestors()
        actor_ancestors_uids = [ancestor.uid for ancestor in actor_ancestors]
        actor_script = f"{name}_children_0 = get_children()\n"
        idx = 0
        if len(actor_ancestors) > 1:
            for idx in range(len(actor_ancestors_uids[0:-1])):
                actor_script += f"for child in {name}_children_{idx}:\n"
                actor_script += (
                    f"   if str(child.uuid)=='{actor_ancestors_uids[idx+1]}':\n"
                    f"      {name}_children_{idx+1} = child.get_children()\n"
                )
            idx += 1
        actor_script += f"for child in {name}_children_{idx}:\n"
        actor_script += f"   if str(child.uuid)=='{node.uid}': {name} = child\n"
        return actor_script


# TODO: test
class TcpInputSlotProxy(TcpSlotProxy, InputSlot):
    """Provides for creating and operating on input slots."""

    def __init__(
        self,
        osl_server: TcpOslServer,
        node: TcpNodeProxy,
        name: str,
        type_: SlotType,
        type_hint: Union[str, None] = None,
    ) -> None:
        """Create an ``TcpInputSlotProxy`` instance.

        Parameters
        ----------
        osl_server: TcpOslServer
            Object providing access to the optiSLang server.
        node : TcpNodeProxy
            Node to which the slot belongs.
        name : str
           Slot name.
        type_ : SlotType
            Slot type.
        type_hint : Union[str, None], optional
            Description, by default None.
        """
        super().__init__(
            osl_server=osl_server,
            node=node,
            name=name,
            type_=type_,
            type_hint=type_hint,
        )

    def connect_from(self, from_slot: TcpSlotProxy) -> Edge:
        """Connect slot from another slot.

        Parameters
        ----------
        from_slot: TcpSlotProxy
            Sending (output) slot.

        Return
        ------
        Edge
            Object determining connection.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        if not isinstance(from_slot, (TcpInnerInputSlotProxy, TcpInnerOutputSlotProxy)):
            self._osl_server.connect_nodes(
                from_actor_uid=from_slot.node.uid,
                from_slot=from_slot.name,
                to_actor_uid=self.node.uid,
                to_slot=self.name,
            )
        else:
            python_script = self.__class__._create_connection_script(
                from_slot=from_slot, to_slot=self
            )
            self._osl_server.run_python_script(script=python_script)
        return Edge(from_slot=from_slot, to_slot=self)

    def disconnect(self) -> None:
        """Remove all connections for the current slot.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        if self.type in [SlotType.INPUT, SlotType.INNER_INPUT]:
            direction = "sdInputs"
        elif self.type in [SlotType.OUTPUT, SlotType.INNER_OUTPUT]:
            direction = "sdOutputs"
        self._osl_server.disconnect_slot(
            uid=self.node.uid, slot_name=self.name, direction=direction
        )


# TODO: test
class TcpOutputSlotProxy(TcpSlotProxy, TcpOutputSlotProxy):
    """Provides for creating and operating on output slots."""

    def __init__(
        self,
        osl_server: TcpOslServer,
        node: TcpNodeProxy,
        name: str,
        type_: SlotType,
        type_hint: Union[str, None] = None,
    ) -> None:
        """Create an ``OutputSlotProxy`` instance.

        Parameters
        ----------
        osl_server: TcpOslServer
            Object providing access to the optiSLang server.
        node : TcpNodeProxy
            Node to which the slot belongs.
        name : str
           Slot name.
        type_ : SlotType
            Slot type.
        type_hint : Union[str, None], optional
            Description, by default None.
        """
        super().__init__(
            osl_server=osl_server,
            node=node,
            name=name,
            type_=type_,
            type_hint=type_hint,
        )

    def connect_to(self, to_slot: TcpSlotProxy) -> Edge:
        """Connect slot to another slot.

        Parameters
        ----------
        to_slot: TcpSlotProxy
            Receiving (input) slot

        Return
        ------
        Edge
            Object determining connection.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        if not isinstance(to_slot, (TcpInnerInputSlotProxy, TcpInnerOutputSlotProxy)):
            self._osl_server.connect_nodes(
                from_actor_uid=self.node.uid,
                from_slot=self.name,
                to_actor_uid=to_slot.node.uid,
                to_slot=to_slot.name,
            )
        else:
            python_script = self.__class__._create_connection_script(
                from_slot=self, to_slot=to_slot
            )
            self._osl_server.run_python_script(script=python_script)
        return Edge(from_slot=self, to_slot=to_slot)

    def disconnect(self) -> None:
        """Remove all connections for the current slot.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        if self.type in [SlotType.INPUT, SlotType.INNER_INPUT]:
            direction = "sdInputs"
        elif self.type in [SlotType.OUTPUT, SlotType.INNER_OUTPUT]:
            direction = "sdOutputs"
        self._osl_server.disconnect_slot(
            uid=self.node.uid, slot_name=self.name, direction=direction
        )


# TODO: test
class TcpInnerInputSlotProxy(TcpSlotProxy, TcpInnerInputSlotProxy):
    """Provides for creating and operating on inner input slots."""

    def __init__(
        self,
        osl_server: TcpOslServer,
        node: TcpNodeProxy,
        name: str,
        type_: SlotType,
        type_hint: Union[str, None] = None,
    ) -> None:
        """Create a ``InnerInputSlotProxy`` instance.

        Parameters
        ----------
        osl_server: TcpOslServer
            Object providing access to the optiSLang server.
        node : TcpNodeProxy
            Node to which the slot belongs.
        name : str
           Slot name.
        type_ : SlotType
            Slot type.
        type_hint : Union[str, None], optional
            Description, by default None.
        """
        super().__init__(
            osl_server=osl_server,
            node=node,
            name=name,
            type_=type_,
            type_hint=type_hint,
        )

    def connect_from(self, from_slot: TcpSlotProxy) -> Edge:
        """Connect slot from another slot.

        Parameters
        ----------
        from_slot: TcpSlotProxy
            Sending (output) slot

        Return
        ------
        Edge
            Object determining connection.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        python_script = self.__class__._create_connection_script(from_slot=from_slot, to_slot=self)
        self._osl_server.run_python_script(script=python_script)
        return Edge(from_slot=from_slot, to_slot=self)


# TODO: test
class TcpInnerOutputSlotProxy(TcpSlotProxy, TcpInnerOutputSlotProxy):
    """Provides for creating and operating on inner output slots."""

    def __init__(
        self,
        osl_server: TcpOslServer,
        node: TcpNodeProxy,
        name: str,
        type_: SlotType,
        type_hint: Union[str, None] = None,
    ) -> None:
        """Create a ``InnerOutputSlotProxy`` instance.

        Parameters
        ----------
        osl_server: TcpOslServer
            Object providing access to the optiSLang server.
        node : TcpNodeProxy
            Node to which the slot belongs.
        name : str
           Slot name.
        type_ : SlotType
            Slot type.
        type_hint : Union[str, None], optional
            Description, by default None.
        """
        super().__init__(
            osl_server=osl_server,
            node=node,
            name=name,
            type_=type_,
            type_hint=type_hint,
        )

    def connect_to(self, to_slot: TcpSlotProxy) -> Edge:
        """Connect slot to another slot.

        Parameters
        ----------
        to_slot: TcpSlotProxy
            Receiving (input) slot

        Return
        ------
        Edge
            Object determining connection.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        python_script = self.__class__._create_connection_script(from_slot=self, to_slot=to_slot)
        self._osl_server.run_python_script(script=python_script)
        return Edge(from_slot=self, to_slot=to_slot)
