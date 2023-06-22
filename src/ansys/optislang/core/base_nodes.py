"""Contains abstract base classes ``Node``, ``System``, ``ParametricSystem`` and ``RootSystem``."""
from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Any, Tuple, Union

from ansys.optislang.core.utils import enum_from_str

if TYPE_CHECKING:
    from ansys.optislang.core.managers import CriteriaManager, ParameterManager, ResponseManager
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
        return enum_from_str(string=string.upper(), enum_class=__class__, replace=(" ", "_"))


class NodeType(Enum):
    """Provides node type options.

    Builtin nodes: 0-999
    Integration plugins: 1000-1999
    Python based algorithm plugins: 2000-2999
    Python based integration plugins: 3000-3999
    Python based MOP node plugins: 4000-4999
    Python based node plugins: 5000-5999
    Algorithm plugins: 6000-6999
    """

    # TODO: test
    # built-in nodes 0-999
    ProEParameterize = 0
    ParameterSet = 1
    Mopsolver = 2
    BashScript = 3
    Sum = 4
    ProEProcess = 5
    Compare = 6
    ETKAsciiOutput = 7
    Calculator = 8
    Variable = 9
    SIMPLEX = 10
    AnsysAPDLParameterize = 11
    Parameterize = 12
    CatiaParameterize = 13
    VCollabProcess = 14
    Mathcad = 15
    PSO = 16
    LSDynaParameterize = 17
    MultiplasParameterize = 18
    TaggedParametersParameterize = 19
    Monitoring = 20
    Stringlist = 21
    PMOPPostprocessing = 22
    VariantMonitoring = 23
    Postprocessing = 24
    String = 25
    Path = 26
    ETKAbaqus = 27
    ScriptFile = 28
    Matlab = 29
    CFturboInput = 30
    AMOP = 31
    Sensitivity = 32
    Robustness = 33
    Excel = 34
    Parameter = 35
    Mop = 36
    SDI = 37
    PMop = 38
    PMopsolver = 39
    ETKComplete = 40
    ETKAnsys = 41
    EA = 42
    ReliabilityFORM = 43
    NOA2 = 44
    PythonScript = 45
    NLPQLP = 46
    ARSM = 47
    Memetic = 48
    OOCalc = 49
    ETKAdams = 50
    ETKMadymo = 51
    ETKEdyson = 52
    Designexport = 53
    ETKMidas = 54
    SoSPostprocessing = 55
    Octave = 56
    Objectives = 57
    Constraints = 58
    Variables = 59
    CalculatorSet = 60
    AnsysWorkbench = 61
    Criteria = 62
    Process = 63
    AbaqusProcess = 64
    CatiaProcess = 65
    AppendDesignsToBinFile = 66
    BatchScript = 67
    PerlScript = 68
    SolverTemplate = 69
    ParametricSystem = 70
    SimulationX = 71
    DesignExport = 72
    DPS = 73
    DesignImport = 74
    MergeDesigns = 75
    Wait = 76
    While = 77
    File = 78
    Reevaluate = 79
    FloEFDInput = 80
    DataExport = 81
    ReliabilityMC = 82
    ReliabilityAS = 83
    ReliabilityDS = 84
    ReliabilityARSM = 85
    ReliabilityAsym = 86
    ReliabilityISPUD = 87
    DataImport = 88
    ASCMOsolver = 89
    IntegrationPlugin = 90
    AlgorithmSystemPlugin = 91
    TurboOptInput = 92
    PDM = 93
    PDMReceive = 94
    PDMSend = 95
    Python2 = 96
    SoSGenerate = 97
    DataMining = 98
    AmesimInput = 99
    SimPackInput = 100
    CetolInput = 101
    ETKAMESim = 102
    Custom = 103
    ETKLSDYNA = 104
    ETKFloEFD = 105
    ETKCFturbo = 106
    ETKSimPack = 107
    ETKTurboOpt = 108
    ETKExtOut = 109
    ETKCetol = 110
    CustomIntegration = 111
    CustomAlgorithm = 112
    CustomETKIntegration = 113
    CustomMop = 114
    RunnableSystem = 115

    # integration plugins 1000-1999
    awb2_plugin = 1000
    discovery_plugin = 1001
    lsdyna_plugin = 1002
    optislang_node = 1003
    spaceclaim_plugin = 1004
    speos_plugin = 1005

    # python based algorithm plugins 2000-2999
    BASS = 2000
    DXAMO = 2001
    DXASO = 2002
    DXMISQP = 2003
    DXUPEGO = 2004
    GLAD = 2005
    OCO = 2006
    PIBO = 2007
    Replace_constant_parameter = 2008
    Unigene_EA = 2009
    while_loop = 2010

    # python based integration plugins 3000-3999
    AEDT2 = 3000
    AEDT2_lsdso = 3001
    ANSA_input = 3002
    ANSA_output = 3003
    AmplitudesFromField_SoS = 3004
    AxSTREAM = 3005
    CAD_CATIA = 3006
    CAD_Creo = 3007
    CAD_Inventor = 3008
    CAD_NX = 3009
    CAESES_input = 3010
    CFX_Partitioner = 3011  # `-` symbol was replaced for `_`
    CFX_Partitioner_v3 = 3012  # `-` symbol was replaced for `_`
    CFX_Pre = 3013  # `-` symbol was replaced for `_`
    CFX_Pre_v3 = 3014  # `-` symbol was replaced for `_`
    CFX_Solver = 3015  # `-` symbol was replaced for `_`
    CFX_Solver_v3 = 3016  # `-` symbol was replaced for `_`
    CFturbo_input = 3017
    COMSOL2 = 3018
    COMSOL_input = 3019
    COMSOL_output = 3020
    Convert_OMDB_to_BIN_SoS = 3021
    DPF = 3022
    ETK_nD = 3023
    FMU_SoS = 3024
    Field_Data_Collector = 3025
    Field_MOP_2D_Nested_DOE_SoS = 3026
    Field_MOP_ANSYSMECH_SoS = 3027
    FloEFD_input = 3028
    FloEFD_output = 3029
    Fluent = 3030
    Fluent_mesher = 3031
    Fluent_solver = 3032
    Flux_input = 3033
    GTSUITE_input = 3034
    GTSUITE_output = 3035
    Generate_SoS = 3036
    GeoDict_input = 3037
    GeoDict_output = 3038
    IPG_Automotive = 3039
    JMAG_Designer_input = 3040
    JMAG_Designer_output = 3041
    JMAG_Designer_solve = 3042
    JSON_input = 3043
    JSON_output = 3044
    KULI = 3045
    Lumerical = 3046
    META_output = 3047
    Matlab_mat_input = 3048
    Matlab_mat_output = 3049
    ModelCenter = 3050
    MotorCAD_input = 3051
    MotorCAD_output = 3052
    MotorCAD_solve = 3053
    NASTRAN = 3054
    OpticStudio = 3055
    PuTTY_SSH = 3056
    ROCKY_input = 3057
    ROCKY_output = 3058
    SPEOSCore = 3059
    SPEOS_Report_Reader = 3060
    SimulationX_SXOA = 3061
    Viewer_SoS = 3062
    VirtualLab_input = 3063
    VirtualLab_output = 3064
    ZEMAX = 3065
    ZEMAX_input = 3066
    ZEMAX_output = 3067
    ZEMAX_solve = 3068
    optislang_omdb = 3069

    # python based MOP node plugins 4000-4999
    MOP = 4000

    # python based node plugins 5000-5999

    # algorithm plugins 6000-6999

    @staticmethod
    def from_str(string: str) -> Union[NodeType, str]:
        """Convert string to an instance of the ``NodeType`` class.

        Parameters
        ----------
        string: str
            String to be converted.

        Returns
        -------
        Union[NodeType, str]
            Instance of the ``NodeType`` class for supported nodes, ``string`` otherwise.

        Raises
        ------
        TypeError
            Raised when an invalid type of ``string`` is given.
        """
        return enum_from_str(string=string, enum_class=__class__, replace=("-", "_"))

    @staticmethod
    def get_subtype(
        node_type_value: int,
    ) -> Tuple[Union[str, None], Union[str, None], Union[str, None], Union[str, None]]:
        """Get node subtype from type.

        Parameters
        ----------
        type_ : int
            Value of NodeType enumeration item.

        Returns
        -------
        Tuple[Union[str, None], Union[str, None], Union[str, None], Union[str, None]]
            algorithm_type, integration_type, mop_node_type, node_type
        """
        algorithm_type, integration_type, mop_node_type, node_type = None, None, None, None
        if node_type_value < 1000:
            pass
        elif 1000 <= node_type_value < 2000:
            integration_type = "integration_plugin"
        elif 2000 <= node_type_value < 3000:
            algorithm_type = "python_based_algorithm_plugin"
        elif 3000 <= node_type_value < 4000:
            integration_type = "python_based_integration_plugin"
        elif 4000 <= node_type_value < 5000:
            mop_node_type = "python_based_mop_node_plugin"
        elif 5000 <= node_type_value < 6000:
            node_type = "python_based_node_plugin"
        elif 6000 <= node_type_value < 7000:
            algorithm_type = "algorithm_plugin"
        else:
            raise ValueError(
                f"Unsupported value of node_type_value: ``{node_type_value}``."
                "Integer in range <0, 7000) was expected."
            )

        return algorithm_type, integration_type, mop_node_type, node_type

    def to_str(self) -> str:
        """Convert enumeration item to string..

        Returns
        -------
        str
            Item converted to str.
        """
        # fix name of cfx items
        if 3011 <= self.value <= 3016:
            return self.name.replace("_", "-")
        else:
            return self.name


class SlotType(Enum):
    """Provides slot type options."""

    # TODO: test
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
        return enum_from_str(string=string.upper(), enum_class=__class__, replace=(" ", "_"))

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
    def type(self) -> Union[NodeType, str]:  # pragma: no cover
        """Type of the node.

        Returns
        -------
        Union[NodeType, str]
            Instance of the ``NodeType`` class for supported nodes, ``string`` otherwise.
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

        Return
        ------
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
        self, type_: Union[SlotType, None], name: Union[str, None] = None
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
        type_: Union[NodeType, str],
        name: Union[str, None] = None,
        design_flow: Union[DesignFlow, None] = None,
        algorithm_type: Union[str, None] = None,
        integration_type: Union[str, None] = None,
        mop_node_type: Union[str, None] = None,
        node_type: Union[str, None] = None,
    ) -> Node:  # pragma: no cover
        """Create a new node in current system in active project.

        Parameters
        ----------
        type_ : Union[NodeType, str]
            Type of created node.
        name : Union[str, None], optional
            Name of created node, by default None.
        design_flow : Union[DesignFlow, None], optional
            Design flow, by default None.
        algorithm_type : Union[str, None], optional
            Algorithm type, e. g. 'algorithm_plugin'.
            Ignored when ``type(type_) == NodeType``, by default None.
        integration_type : Union[str, None], optional
            Integration type, e. g. 'integration_plugin'.
            Ignored when ``type(type_) == NodeType``, by default None.
        mop_node_type : Union[str, None], optional
            MOP node type, e. g. 'python_based_mop_node_plugin'.
            Ignored when ``type(type_) == NodeType``, by default None.
        node_type: Union[str, None], optional
            Node type, e. g. 'python_based_node_plugin'.
            Ignored when ``type(type_) == NodeType``, by default None.

        Returns
        -------
        Node
            Instance of the created node.
        """

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

        Return
        ------
        str
            Slot name.
        """
        pass

    @property
    @abstractmethod
    def node(self) -> Node:  # pragma: no cover
        """Get node to which the slot belongs.

        Return
        ------
        Node
            Node to which the slot belongs.
        """
        pass

    @property
    @abstractmethod
    def type(self) -> SlotType:  # pragma: no cover
        """Get slot type.

        Return
        ------
        SlotType
            Type of current slot.
        """
        pass

    @property
    @abstractmethod
    def type_hint(self) -> Union[str, None]:  # pragma: no cover
        """Get type hint.

        Return
        ------
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


class TcpOutputSlotProxy(Slot):
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


class TcpInnerInputSlotProxy(Slot):
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
        pass


class TcpInnerOutputSlotProxy(Slot):
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
        pass


# TODO: test
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
