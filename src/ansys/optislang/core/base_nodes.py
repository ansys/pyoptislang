"""Contains abstract base classes ``Node``, ``System``, ``ParametricSystem`` and ``RootSystem``."""
from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Any, Tuple, Union

from ansys.optislang.core.utils import enum_from_str

if TYPE_CHECKING:
    from ansys.optislang.core.managers import CriteriaManager, ParameterManager, ResponseManager
    from ansys.optislang.core.node_types import NodeType
    from ansys.optislang.core.osl_server import OslServer
    from ansys.optislang.core.project_parametric import Design


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


class SlotType(Enum):
    """Provides slot type options."""

    INPUT = 0
    OUTPUT = 1
    INNER_INPUT = 2
    INNER_OUTPUT = 3

    @staticmethod
    def from_str(string: str) -> SlotType:
        """Convert string to an instance of the ``SlotType`` class.

        Parameters
        ----------
        string: str
            String to be converted.

        Returns
        -------
        SlotType
            Instance of the ``SlotType`` class.

        Raises
        ------
        TypeError
            Raised when an invalid type of ``string`` is given.
        """
        return enum_from_str(string=string, enum_class=__class__, replace=(" ", "_"))

    @staticmethod
    def to_dir_str(type_: SlotType) -> str:
        """Convert string to an instance of the ``SlotType`` class.

        Parameters
        ----------
        string: str
            String to be converted.

        Returns
        -------
        SlotType
            Instance of the ``SlotType`` class.

        Raises
        ------
        TypeError
            Raised when an invalid type of ``string`` is given.
        ValueError
            Raised when an invalid value of ``string`` is given.
        """
        if not isinstance(type_, SlotType):
            raise TypeError(f"Unsupported type of type_: ``{type(type_)}``.")
        if type_ in [SlotType.INPUT, SlotType.INNER_INPUT]:
            return "receiving"
        elif type_ in [SlotType.OUTPUT, SlotType.INNER_OUTPUT]:
            return "sending"
        else:
            raise ValueError(f"Unsupported value of type_: ``{type_}``.")


class Node(ABC):
    """Base class for classes which provide for creating and operating on nodes."""

    @abstractmethod
    def __init__(self):  # pragma: no cover
        """``Node`` class is an abstract base class and cannot be instantiated."""
        pass

    @property
    @abstractmethod
    def uid(self) -> str:  # pragma: no cover
        """Unique ID of the node.

        Returns
        -------
        str
            Unique ID of the node.
        """
        pass

    @property
    @abstractmethod
    def type(self) -> NodeType:  # pragma: no cover
        """Type of the node.

        Returns
        -------
        NodeType
            Instance of the ``NodeType`` class.
        """
        pass

    @abstractmethod
    def delete(self) -> None:  # pragma: no cover
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
        pass

    @abstractmethod
    def exists(self) -> bool:  # pragma: no cover
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
        pass

    @abstractmethod
    def get_connections(
        self, slot_type: Union[SlotType, None] = None, slot_name: Union[str, None] = None
    ) -> Tuple[Edge]:  # pragma: no cover
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
        pass

    @abstractmethod
    def get_name(self) -> str:  # pragma: no cover
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
        pass

    @abstractmethod
    def get_ancestors(self) -> Tuple[Node, ...]:  # pragma: no cover
        """Get tuple of ordered ancestors starting from root system at position 0.

        Returns
        -------
        Tuple[Node, ...]
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
        pass

    @abstractmethod
    def get_parent(self) -> Node:  # pragma: no cover
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
        pass

    @abstractmethod
    def get_parent_name(self) -> str:  # pragma: no cover
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
        pass

    @abstractmethod
    def get_property(self) -> Any:  # pragma: no cover
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
        pass

    @abstractmethod
    def get_slots(
        self, type_: Union[SlotType, None] = None, name: Union[str, None] = None
    ) -> Tuple[Slot, ...]:  # pragma: no cover
        """Get current node's slots of given type and name.

        Parameters
        ----------
        type_: Union[SlotType, None], optional
            Type of slots to be returned, by default ``None``.
        name : Union[str, None], optional
            Slot name, by default ``None``.

        Returns
        -------
        Tuple[Slot, ...]
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
        pass

    @abstractmethod
    def get_status(self) -> str:  # pragma: no cover
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
        pass

    @abstractmethod
    def set_property(self, name: str, value: Any) -> None:  # pragma: no cover
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
        pass


class System(Node):
    """Base class for classes which provide for creating and operating on a system."""

    @abstractmethod
    def __init__(self):  # pragma: no cover
        """``System`` class is an abstract base class and cannot be instantiated."""
        pass

    @abstractmethod
    def create_node(
        self,
        type_: NodeType,
        name: Union[str, None] = None,
        design_flow: Union[DesignFlow, None] = None,
    ) -> Node:  # pragma: no cover
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
        Node
            Instance of the created node.

        Raises
        ------
        TypeError
            Raised when unsupported type of type_ is given.
        ValueError
            Raised when unsupported value of type_ is given.
        """
        pass

    @abstractmethod
    def delete_children_nodes(self) -> None:  # pragma: no cover
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
        pass

    @abstractmethod
    def find_node_by_uid(
        self, uid: str, search_depth: int = 1
    ) -> Union[Node, None]:  # pragma: no cover
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
        pass

    @abstractmethod
    def find_nodes_by_name(
        self, name: str, search_depth: int = 1
    ) -> Tuple[Node, ...]:  # pragma: no cover
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
        pass

    @abstractmethod
    def get_nodes(self) -> Tuple[Node, ...]:  # pragma: no cover
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
        pass


class ParametricSystem(System):
    """Base class for classes which provide for creating and operating on a parametric system."""

    @abstractmethod
    def __init__(self):  # pragma: no cover
        """``ParametricSystem`` class is an abstract base class and cannot be instantiated."""
        pass

    @property
    @abstractmethod
    def criteria_manager(self) -> CriteriaManager:  # pragma: no cover
        """Criteria manager of the current system.

        Returns
        -------
        CriteriaManager
            Instance of the ``CriteriaManager`` class.
        """
        pass

    @property
    @abstractmethod
    def parameter_manager(self) -> ParameterManager:  # pragma: no cover
        """Parameter manager of the current system.

        Returns
        -------
        ParameterManager
            Instance of the ``ParameterManager`` class.
        """
        pass

    @property
    @abstractmethod
    def response_manager(self) -> ResponseManager:  # pragma: no cover
        """Response manager of the current system.

        Returns
        -------
        ResponseManager
            Instance of the ``ResponseManager`` class.
        """
        pass


class RootSystem(ParametricSystem):
    """Base class for classes which provide for creating and operating on a project system."""

    @abstractmethod
    def __init__(self):  # pragma: no cover
        """``Rootsystem`` class is an abstract base class and cannot be instantiated."""
        pass

    @abstractmethod
    def evaluate_design(self, design: Design) -> Design:  # pragma: no cover
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
        pass

    @abstractmethod
    def get_reference_design(self) -> Design:  # pragma: no cover
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
        pass

    @abstractmethod
    def get_missing_parameters_names(self, design: Design) -> Tuple[str, ...]:  # pragma: no cover
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
        pass

    @abstractmethod
    def get_undefined_parameters_names(self, design: Design) -> Tuple[str, ...]:  # pragma: no cover
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
        pass


class Slot(ABC):
    """Provides for creating and operating on slots."""

    @abstractmethod
    def __init__(self):  # pragma: no cover
        """``Slot`` class is an abstract base class and cannot be instantiated."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:  # pragma: no cover
        """Get slot name.

        Returns
        -------
        str
            Slot name.
        """
        pass

    @property
    @abstractmethod
    def node(self) -> Node:  # pragma: no cover
        """Get node to which the slot belongs.

        Returns
        -------
        Node
            Node to which the slot belongs.
        """
        pass

    @property
    @abstractmethod
    def type(self) -> SlotType:  # pragma: no cover
        """Get slot type.

        Returns
        -------
        SlotType
            Type of current slot.
        """
        pass

    @property
    @abstractmethod
    def type_hint(self) -> Union[str, None]:  # pragma: no cover
        """Get type hint.

        Returns
        -------
        Union[str, None]
            Data type of the current slot, ``None`` if not specified.
        """
        pass

    @abstractmethod
    def get_connections(self) -> Tuple[Edge]:  # pragma: no cover
        """Get connections for the current slot.

        Returns
        -------
        Tuple[Edge]
            Tuple with connections of the current slot.
        """
        pass

    @abstractmethod
    def get_type_hint(self) -> str:  # pragma: no cover
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
        pass

    @staticmethod
    @abstractmethod
    def create_slot(
        osl_server: OslServer,
        node: Node,
        name: str,
        type_: SlotType,
        type_hint: Union[str, None] = None,
    ) -> Slot:  # pragma: no cover
        """Create instance of new slot.

        Parameters
        ----------
        osl_server: OslServer
            Object providing access to the optiSLang server.
        node : Node
            Node to which slot belongs to.
        name : str
            Slot name.
        type_ : SlotType
            Slot type.
        type_hint : Union[str, None], optional
            Slot's expected data type, by default None.

        Returns
        -------
        Slot
            Instance of InputSlot, OutputSlot, InnerInputSlot or InnerOutputSlot class.
        """
        pass


class InputSlot(Slot):
    """Provides for creating and operating on input slots."""

    @abstractmethod
    def __init__(self):  # pragma: no cover
        """``InputSlot`` class is an abstract base class and cannot be instantiated."""
        pass

    @abstractmethod
    def connect_from(self, from_slot: Slot) -> Edge:  # pragma: no cover
        """Connect slot from another slot.

        Parameters
        ----------
        from_slot: Slot
            Sending (output) slot.

        Returns
        -------
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
        pass

    @abstractmethod
    def disconnect(self) -> None:  # pragma: no cover
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
        pass


class OutputSlot(Slot):
    """Provides for creating and operating on output slots."""

    @abstractmethod
    def __init__(self):  # pragma: no cover
        """``OutputSlot`` class is an abstract base class and cannot be instantiated."""
        pass

    @abstractmethod
    def connect_to(self, to_slot: Slot) -> Edge:  # pragma: no cover
        """Connect slot to another slot.

        Parameters
        ----------
        to_slot: Slot
            Receiving (input) slot

        Returns
        -------
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
        pass

    @abstractmethod
    def disconnect(self) -> None:  # pragma: no cover
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
        pass


class InnerInputSlot(Slot):
    """Provides for creating and operating on inner input slots."""

    @abstractmethod
    def __init__(self):  # pragma: no cover
        """``InnerInputSlot`` class is an abstract base class and cannot be instantiated."""
        pass

    @abstractmethod
    def connect_from(self, from_slot: Slot) -> Edge:  # pragma: no cover
        """Connect slot from another slot.

        Parameters
        ----------
        from_slot: Slot
            Sending (output) slot.

        Returns
        -------
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
        pass


class InnerOutputSlot(Slot):
    """Provides for creating and operating on inner output slots."""

    @abstractmethod
    def __init__(self):  # pragma: no cover
        """``InnerOutputSlot`` class is an abstract base class and cannot be instantiated."""
        pass

    @abstractmethod
    def connect_to(self, to_slot: Slot) -> Edge:  # pragma: no cover
        """Connect slot to another slot.

        Parameters
        ----------
        to_slot: Slot
            Receiving (input) slot

        Returns
        -------
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
        pass


class Edge:
    """Provides for creating and operating on connections."""

    def __init__(
        self,
        from_slot: Slot,
        to_slot: Slot,
    ) -> None:
        """Create an ``Edge`` instance.

        Parameters
        ----------
        from_slot: Slot
            Output slot.
        to_slot: Slot
            Input slot.
        """
        if from_slot.type not in [SlotType.INNER_OUTPUT, SlotType.OUTPUT]:
            raise ValueError(
                f"Invalid value of ``from_slot.type``: ``{from_slot.type}``."
                f"``{SlotType.OUTPUT}<or>{SlotType.INNER_OUTPUT}`` was expected."
            )
        self.__from_slot = from_slot
        if to_slot.type not in [SlotType.INNER_INPUT, SlotType.INPUT]:
            raise ValueError(
                f"Invalid value of ``to_slot.type``: ``{to_slot.type}``."
                f"``{SlotType.INPUT}<or>{SlotType.INNER_INPUT}`` was expected."
            )
        self.__to_slot = to_slot

    def __str__(self):
        """Return formatted string."""
        return (
            "From_slot:\n"
            f"   type: {self.from_slot.type.name}\n"
            f"   name: {self.from_slot.name}\n"
            "To_slot:\n"
            f"   type: {self.to_slot.type.name}\n"
            f"   name: {self.to_slot.name}\n"
        )

    @property
    def from_slot(self) -> Slot:
        """Get output slot."""
        return self.__from_slot

    @property
    def to_slot(self) -> Slot:
        """Get input slot."""
        return self.__to_slot

    def exists(self) -> bool:
        """Get info whether connection exists in active project.

        Returns
        -------
        bool
            Whether current connection exists in active project.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        connections = self.from_slot.get_connections()
        for connection in connections:
            if (
                connection.to_slot.node.uid == self.to_slot.node.uid
                and connection.to_slot.name == self.to_slot.name
            ):
                return True
        return False
