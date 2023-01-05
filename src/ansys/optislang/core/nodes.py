"""Contains classes Node, System, ParametricSystem and RootSystem."""
from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Dict, Iterable, List, Tuple, Union

from ansys.optislang.core.project_parametric import Design, DesignParameter, ParameterManager

if TYPE_CHECKING:
    from ansys.optislang.core.osl_server import OslServer


class DesignFlow(Enum):
    """Available design flow options."""

    NONE = 0
    RECEIVE = 1
    SEND = 2
    RECEIVE_SEND = 3

    @staticmethod
    def from_str(label: str):
        """Convert string to DesignFlow."""
        if not isinstance(label, str):
            raise TypeError(f"String was expected, but `{type(label)}` was given.")
        label = label.upper()
        if label == "NONE":
            return DesignFlow.NONE
        elif label == "RECEIVE":
            return DesignFlow.RECEIVE
        elif label == "SEND":
            return DesignFlow.SEND
        elif label == "RECEIVE_SEND":
            return DesignFlow.RECEIVE_SEND
        else:
            raise ValueError(f"Option `{label}` not available in DesignFlow options.")


class Node:
    """Class responsible for creation and operations on Node."""

    def __init__(
        self,
        uid: str,
        osl_server: OslServer,
    ):
        """Create a new instance of Node.

        Parameters
        ----------
        uid: str
            Uid.
        osl_server: TcpOslServer
            Connection to python class.
        """
        self._osl_server = osl_server
        self.__uid = uid

    def __str__(self):
        """Return formatted string."""
        return (
            "----------------------------------------------------------------------\n"
            f"Node type: {self.get_type()}\n"
            f"Name: {self.get_name()}\n"
            f"Uid: {self.uid}\n"
            "----------------------------------------------------------------------"
        )

    @property
    def uid(self) -> str:
        """Return nodes uid.

        Returns
        -------
        str
            Nodes uid.
        """
        return self.__uid

    def get_name(self) -> str:
        """Get name of the current node.

        Returns
        -------
        str
            Nodes name.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        actor_info = self._osl_server.get_actor_info(uid=self.__uid)
        return actor_info["name"]

    def get_parent(self) -> Node:
        """Get instance of the parent node.

        Returns
        -------
        Node
            Instance of the parent node.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        project_tree = self._osl_server.get_full_project_tree_with_properties()
        root_system_uid = project_tree["projects"][0]["system"]["uid"]
        parent_tree = project_tree["projects"][0]["system"]
        parent_uid = self.__find_parents_node_uid(
            parent_tree=parent_tree,
            parent_uid=root_system_uid,
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
        """Get name of the parent node.

        Returns
        -------
        str
            Parents system name.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        parent_uid = self._get_parent_uid()
        actor_info = self._osl_server.get_actor_info(uid=parent_uid)
        return actor_info["name"]

    def get_status(self) -> str:
        """Get status of the current node.

        Returns
        -------
        str
            Status of node.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        actor_info = self._osl_server.get_actor_info(uid=self.__uid)
        return actor_info["status"]

    def get_type(self) -> str:
        """Get type of the current node.

        Returns
        -------
        str
            Type of node.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        actor_info = self._osl_server.get_actor_info(uid=self.__uid)
        return actor_info["type"]

    def _get_parent_uid(self) -> str:
        """Get uid of the parent node.

        Return
        ------
        str
            Parents node uid.
        """
        project_tree = self._osl_server.get_full_project_tree_with_properties()
        root_system_uid = project_tree["projects"][0]["system"]["uid"]
        parent_tree = project_tree["projects"][0]["system"]
        return self.__find_parents_node_uid(
            parent_tree=parent_tree,
            parent_uid=root_system_uid,
        )

    def _create_nodes_from_properties_dicts(
        self, properties_dicts_list: List[dict]
    ) -> Tuple[Node, ...]:
        """Create nodes from properties dict.

        Parameters
        ----------
        properties_dicts_list : List[dict]
            Properties of nodes.

        Returns
        -------
        Tuple[Node, ...]
            Tuple of Nodes.

        Raises
        ------
        TypeError
            Raised when unknown type of component was found.
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

    def __find_parents_node_uid(self, parent_tree: dict, parent_uid: str) -> str:
        """Get uid of the parent node.

        Parameters
        ----------
        parent_tree: dict
            Dictionary with children nodes.
        parent_uid: str
            Uid of the system that is being looped through.

        Return
        ------
        str
            Uid of the parent node.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        NameError
            Raised when parent system wasn't located in project tree.
        """
        for node in parent_tree["nodes"]:
            if node["uid"] == self.uid:
                return parent_uid
            if node["kind"] == "system":
                self.__find_parents_node_uid(parent_tree=node, parent_uid=parent_tree["uid"])
        raise NameError(f'Node "{self.__uid}" was not located in structure tree.')

    def _is_parametric_system(self, uid: str) -> bool:
        """Check whether system is parametric.

        Parameters
        ----------
        uid : str
            Systems uid.

        Returns
        -------
        bool
            True/False.
        """
        props = self._osl_server.get_actor_properties(uid=uid)
        return "ParameterManager" in props["properties"]


class System(Node):
    """Class responsible for creation and operations on System."""

    def __init__(
        self,
        uid: str,
        osl_server: OslServer,
    ):
        """Create a new instance of System.

        Parameters
        ----------
        uid: str
            Uid.
        osl_server: TcpOslServer
            Connection to python class.
        """
        super().__init__(
            uid=uid,
            osl_server=osl_server,
        )

    def __str__(self):
        """Return formatted string."""
        return (
            "----------------------------------------------------------------------\n"
            f"Node type: {self.get_type()}\n"
            f"Name: {self.get_name()}\n"
            f"Uid: {self.uid}\n"
            f"Nodes: {str(self._get_nodes_list())}\n"
            "----------------------------------------------------------------------"
        )

    def find_node_by_uid(self, uid: str, level_depth: int = 0) -> Node:
        """Find node from the current system by uid.

        Parameters
        ----------
        uid : str
            Nodes uid.
        level_depth: int, optional
            Zero-based level of search.

        Returns
        -------
        Tuple[Node, ...]
            Tuple of Nodes with defined uid; None if node with requested

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        TypeError
            Raised when unknown type of component was found.
        """
        project_tree = self._osl_server.get_full_project_tree_with_properties()
        if self.uid == project_tree["projects"][0]["system"]["uid"]:
            system_tree = project_tree["projects"][0]["system"]
        else:
            system_tree = self._find_system_parent_tree(
                parent_tree=project_tree["projects"][0]["system"]
            )
        properties_dicts_list = self._find_nodes_with_uid(
            uid=uid,
            parent_tree=system_tree,
            properties_dicts_list=[],
            current_level=0,
            max_level=level_depth,
        )

        if len(properties_dicts_list) == 0:
            self._osl_server._logger.error(f"Node `{uid}` not found in the current system.")
            return None

        return self._create_nodes_from_properties_dicts(
            properties_dicts_list=properties_dicts_list
        )[0]

    def find_nodes_by_name(self, name: str, level_depth: int = 0) -> Tuple[Node, ...]:
        """Find children nodes by name in current system.

        Parameters
        ----------
        name : str
            Name of node.
        level_depth: int, optional
            Zero-based level of search.

        Returns
        -------
        Tuple[Node, ...]
            Tuple of nodes with given name.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        NameError
            Raised when multiple nodes with the same name were found.
        TypeError
            Raised when unknown type of component was found.
        """
        project_tree = self._osl_server.get_full_project_tree_with_properties()
        if self.uid == project_tree["projects"][0]["system"]["uid"]:
            system_tree = project_tree["projects"][0]["system"]
        else:
            system_tree = self._find_system_parent_tree(
                parent_tree=project_tree["projects"][0]["system"]
            )
        properties_dicts_list = self._find_nodes_with_name(
            name=name,
            parent_tree=system_tree,
            properties_dicts_list=[],
            current_level=0,
            max_level=level_depth,
        )

        if len(properties_dicts_list) == 0:
            self._osl_server._logger.error(f"Node `{name}` not found in the current system.")
            return None

        return self._create_nodes_from_properties_dicts(properties_dicts_list=properties_dicts_list)

    def get_nodes(self) -> Tuple[Node, ...]:
        """Get tuple of the current systems nodes.

        Returns
        -------
        Tuple[Node, ...]
            Instances of `Node` class.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self._create_nodes_from_properties_dicts(
            properties_dicts_list=self._get_nodes_list()
        )

    def _find_nodes_with_name(
        self,
        name: str,
        parent_tree: dict,
        properties_dicts_list: List[dict],
        current_level: int,
        max_level: int,
    ) -> List[dict]:
        """Loop through the project tree and find nodes by name.

        Parameters
        ----------
        name : str
            Nodes name.
        parent_tree : dict
            Dictionary with children nodes.
        properties_dicts_list : dict
            Dictionary with properties.
        current_level: int
            Current level of recursion.
        max_level: int
            Maximum level of recursion.
        Returns
        -------
        dict
            Dictionary with necessary info for creation of Node.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        for node in parent_tree["nodes"]:
            if node["name"] == name:
                properties_dicts_list.append(
                    {
                        "type": node["type"],
                        "name": node["name"],
                        "uid": node["uid"],
                        "parent_uid": parent_tree["uid"],
                        "parent_name": parent_tree["name"],
                        "kind": node["kind"],
                    }
                )
            if node["kind"] == "system" and current_level < max_level:
                self._find_nodes_with_name(
                    name=name,
                    parent_tree=node,
                    properties_dicts_list=properties_dicts_list,
                    current_level=current_level + 1,
                    max_level=max_level,
                )
        return properties_dicts_list

    def _find_nodes_with_uid(
        self,
        uid: str,
        parent_tree: dict,
        properties_dicts_list: List[dict],
        current_level: int,
        max_level: int,
    ) -> List[dict]:
        """Loop through the project tree and find nodes by uid.

        Parameters
        ----------
        uid : str
            Nodes uid.
        parent_tree : dict
            Nodes below.
        properties_dicts_list : List[dict]
            Dictionary with
        current_level: int
            Current level of recursion.
        max_level: int
            Maximum level of recursion.

        Returns
        -------
        dict
            Dictionary with necessary info for creation of Node.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        for node in parent_tree["nodes"]:
            if node["uid"] == uid:
                properties_dicts_list.append(
                    {
                        "type": node["type"],
                        "name": node["name"],
                        "uid": node["uid"],
                        "parent_uid": parent_tree["uid"],
                        "parent_name": parent_tree["name"],
                        "kind": node["kind"],
                    }
                )
            if node["kind"] == "system" and current_level < max_level:
                self._find_nodes_with_uid(
                    uid=uid,
                    parent_tree=node,
                    properties_dicts_list=properties_dicts_list,
                    current_level=current_level + 1,
                    max_level=max_level,
                )
        return properties_dicts_list

    def _find_system_parent_tree(self, parent_tree: dict) -> dict:
        """Loop through the project tree and find system parent tree.

        Parameters
        ----------
        parent_tree: dict
            Dictionary with parent structure.

        Returns
        -------
        dict
            Dictionary with system structure.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        NameError
            Raised when system wasn't found in structure tree.
        """
        for node in parent_tree["nodes"]:
            if node["uid"] == self.uid:
                return node
            if node["kind"] == "system":
                self._find_system_parent_tree(
                    parent_tree=node,
                )

    def _get_nodes_list(self) -> List[dict]:
        """Get list of nodes.

        Returns
        -------
        List
            List of nodes.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        NameError
            Raised when system wasn't located in project tree.
        """
        project_tree = self._osl_server.get_full_project_tree_with_properties()
        if self.uid == project_tree["projects"][0]["system"]["uid"]:
            system_tree = project_tree["projects"][0]["system"]
        else:
            system_tree = self._find_system_parent_tree(
                parent_tree=project_tree["projects"][0]["system"]
            )
        if len(system_tree) == 0:
            raise NameError(f"System `{self.uid}` wasn't found.")

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


class ParametricSystem(System):
    """Class responsible for creation and operations on parametric system."""

    def __init__(
        self,
        uid: str,
        osl_server: OslServer,
    ):
        """Create a new instance of ParametricSystem.

        Parameters
        ----------
        uid: str
            Uid.
        osl_server: TcpOslServer
            Connection to python class.
        """
        super().__init__(
            uid=uid,
            osl_server=osl_server,
        )

        self.__parameter_manager = ParameterManager(uid, osl_server)

    def __str__(self):
        """Return formatted string."""
        return (
            "----------------------------------------------------------------------\n"
            f"Node type: {self.get_type()}\n"
            f"Name: {self.get_name()}\n"
            f"Uid: {self.uid}\n"
            f"Nodes: {str(self._get_nodes_list())}\n"
            f"Parameters: {str(self.parameter_manager.get_parameters_names())}\n"
            "----------------------------------------------------------------------"
        )

    @property
    def parameter_manager(self) -> ParameterManager:
        """Get instance of the ``ParameterManager`` class.

        Returns
        -------
        ParameterManager
            Instance of the ``ParameterManager`` class.
        """
        return self.__parameter_manager


class RootSystem(ParametricSystem):
    """Class responsible for creation and operations on project system."""

    def __init__(
        self,
        uid: str,
        osl_server: OslServer,
    ):
        """Create a new instance of RootSystem.

        Parameters
        ----------
        uid: str
            Uid.
        osl_server: TcpOslServer
            Connection to python class.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        super().__init__(
            uid=uid,
            osl_server=osl_server,
        )

    def create_design(
        self, parameters: Union[Dict[str, float], Iterable[DesignParameter]] = None
    ) -> Design:
        """Create a new instance of ``Design`` class.

        Parameters
        ----------
        parameters: Union[Dict[str, float], Iterable[DesignParameter]], optional
            Dictionary of parameters and it's values {'parname': value, ...}
            or iterable of DesignParameters.

        Returns
        -------
        Design
            Instance of ``Design`` class.
        """
        return Design(parameters)

    def evaluate_design(self, design: Design) -> Tuple[dict, dict]:
        """Evaluate given design.

        Parameters
        ----------
        design: Design
            Instance of ``Design`` class with defined parameters.

        Returns
        -------
        Tuple[Dict, Dict]
            0: Design parameters.
            1: Responses.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        message, is_valid, missing_parameters = self.validate_design(design)
        if not is_valid:
            self._osl_server._logger.warning(message)

        evaluate_dict = {}
        for name, parameter in design.parameters.items():
            evaluate_dict[name] = parameter.reference_value

        output_dict = self._osl_server.evaluate_design(evaluate_dict=evaluate_dict)
        design._receive_results(output_dict[0])

        for parameter in missing_parameters:
            position = output_dict[0]["result_design"]["parameter_names"].index(parameter)
            design.set_parameter(
                parameter,
                output_dict[0]["result_design"]["parameter_values"][position],
                False,
            )
            self._osl_server._logger.debug(f"Design parameter {parameter} was added.")

        return (design.parameters, design.responses)

    def evaluate_multiple_designs(self, designs: Iterable[Design]) -> Tuple[Tuple[dict, dict], ...]:
        """Evaluate multiple given designs.

        Parameters
        ----------
        designs: Iterable[Design]
            Iterable of ``Design`` class instances with defined parameters.

        Returns
        -------
        multiple_design_output: Tuple[Tuple[Dict, Dict], ...]
            Tuple[Dict, Dict]:
                0: Design parameters.
                1: Responses.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        multiple_design_output = []
        for design in designs:
            design_output = self.evaluate_design(design)
            multiple_design_output.append(design_output)
        return tuple(multiple_design_output)

    def get_reference_design(self) -> Design:
        """Get design with reference values of parameters.

        Returns
        -------
        Design
            Instance of `Design` class with defined parameters and reference values.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pm = self.parameter_manager
        parameters = pm.get_parameters()
        return Design(parameters=parameters)

    def validate_design(self, design: Design) -> Tuple[str, bool, List]:
        """Compare parameters defined in given design and optiSLang project.

        Parameters
        ----------
        design: Design
            Instance of ``Design`` class with defined parameters.

        Returns
        -------
        Tuple[str, bool, List]
            0: str, Message describing differences.
            1: bool, True if there are not any missing or redundant parameters.
            2: List, Missing parameters.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        design_parameters = design.parameters
        defined_parameters = self.parameter_manager.get_parameters_names()
        # compare design with defined parameters
        missing_params = list(set(defined_parameters) - set(design_parameters.keys()))
        redundant_params = list(set(design_parameters.keys()) - set(defined_parameters))
        missing_params.sort()
        redundant_params.sort()
        if missing_params or redundant_params:
            message = (
                f"Parameters {missing_params} not defined in design, values set to reference."
                f"Parameters {redundant_params} are not defined in project and weren't used."
            )
            is_valid = False
        else:
            message = "Valid design."
            is_valid = True
        return (message, is_valid, missing_params)
