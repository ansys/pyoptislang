"""Contains classes for a node, system, parametric system, and root system."""
from __future__ import annotations

import copy
from enum import Enum
import logging
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Tuple, Union

from deprecated import deprecated

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
        # TODO: IF `CFX` in name, replace `_` with `-` when creating node
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


class Node:
    """Provides for creating and operating on nodes."""

    def __init__(
        self,
        uid: str,
        osl_server: OslServer,
        type_: Union[NodeType, str],
        logger=None,
    ) -> None:
        """Create a ``Node`` instance.

        Parameters
        ----------
        uid: str
            Unique ID of the node.
        osl_server: OslServer
            Object providing access to the optiSLang server.
        type_: Union[NodeType, str]
            Instance of the ``NodeType`` class for supported nodes, ``string`` otherwise.
        logger: Any, optional
            Object for logging. If ``None``, standard logging object is used. Defaults to ``None``.
        """
        self._osl_server = osl_server
        self.__uid = uid
        self.__type = type_
        self._logger = logging.getLogger(__name__) if logger is None else logger

    def __str__(self):
        """Return formatted string."""
        type_ = self.type.name if isinstance(type_, NodeType) else type_
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
    def type(self) -> Union[NodeType, str]:
        """Type of the node.

        Returns
        -------
        Union[NodeType, str]
            Instance of the ``NodeType`` class for supported nodes, ``string`` otherwise.
        """
        # TODO: test
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
        # TODO: test
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
        # TODO: test
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

    def get_connections(self, slot_type: SlotType, slot_name: str = None) -> Tuple[Edge]:
        """Get connections of a given direction and slot.

        Parameters
        ----------
        slot_type: SlotType
            Slot type.
        slot_name : str, optional
            _description_, by default None

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
        # TODO: test
        project_tree = self._osl_server.get_full_project_tree_with_properties()
        connections = project_tree.get("projects", [{}])[0].get("connections")
        direction = SlotType.to_dir_str(type_=slot_type)
        filtered_connections = __class__._filter_connections(
            connections=connections, uid=self.uid, direction=direction
        )
        edges = []
        for connection in filtered_connections:
            edges.append(
                self._create_edge_from_dict(
                    project_tree=project_tree["projects"][0]["system"], connection=connection
                )
            )
        return tuple(edges)

    def get_input_slots(self) -> Tuple[InputSlot, ...]:
        """Get node's input slots.

        Returns
        -------
        Tuple[Slot,...]
            Tuple of defined input slots.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        # TODO: test
        return self._get_slots(type_=SlotType.INPUT)

    def get_input_connections(self) -> Tuple[Edge]:
        """Get nodes input connections.

        Returns
        -------
        Tuple[Edge]
            Nodes input connections.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        # TODO: test
        return self.get_connections(slot_type=SlotType.INPUT)

    def get_output_connections(self) -> Tuple[Edge]:
        """Get nodes output connections.

        Returns
        -------
        Tuple[Edge]
            Nodes output connections.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
        """
        # TODO: test
        return self.get_connections(slot_type=SlotType.OUTPUT)

    def get_output_slots(self) -> Tuple[OutputSlot, ...]:
        """Get node's output slots.

        Returns
        -------
        Tuple[Slot,...]
            Tuple of defined output slots.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        # TODO: test
        return self._get_slots(type_=SlotType.OUTPUT)

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

    def get_ancestors(self) -> Tuple[Node, ...]:
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
        if isinstance(self, RootSystem):
            self._logger.warning(
                "``RootSystem`` doesn't have any ancestors, empty tuple will be returned."
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
        return self._osl_server.get_actor_properties(self.uid)

    def get_slot(self, name: str, type_: SlotType) -> Slot:
        """Get current node's slot of a given type and name.

        Parameters
        ----------
        name : str
            Slot name.
        type_ : SlotType
            Slot type.

        Returns
        -------
        Slot
            Specified slot.

        Raises
        ------
        NameError
            Raised when slot for given combination of ``name`` and ``type_`` could not be found.
        """
        # TODO: test
        slots = self._get_slots(type_=type_, name=name)
        if len(slots) > 1:
            self._logger.error("Multiple slots with the same name and type were found.")
        if len(slots) > 0:
            return slots[0]
        else:
            raise NameError(f"Slot of type: ``{type_}`` and name: ``{name}`` could not be found.")

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

    @deprecated(version="0.2.1", reason="Use ``Node.type`` instead.")
    def get_type(self) -> Union[NodeType, str]:
        """Get the type of the node.

        Returns
        -------
        Union[NodeType,str]
            Type of the node, ``NodeType`` is returned for supported nodes, ``string`` otherwise.

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
        actor_type = NodeType.from_str(actor_info["type"])
        if isinstance(actor_type, str):
            self._logger.warning(f"Node type ``{actor_type}`` is not fully supported.")
        return actor_type

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

    def _get_slots(self, type_: SlotType, name: Union[str, None] = None) -> Tuple[Slot, ...]:
        """Get current node's slots of given type and optionally name.

        Parameters
        ----------
        type_: SlotType
            Type of slots to be returned.
        name : Union[str, None], optional
            Slot name.

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
        info = self._get_info()
        key = type_.name.lower() + "_slots"
        slots_dict_list = info.get(key)
        slots_list = []
        for slot_dict in slots_dict_list:
            if name is not None and name != slot_dict["name"]:
                continue
            slots_list.append(
                Slot.create_slot(
                    osl_server=self._osl_server,
                    node=self,
                    name=slot_dict["name"],
                    type_=type_,
                    type_hint=slot_dict["type"],
                )
            )
        return tuple(slots_list)

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
        # TODO: replace query after dictionary extension
        info = self._osl_server.get_actor_info(connection["receiving_uuid"])
        if True in [item["name"] == rec_slot_name for item in info["input_slots"]]:
            rec_slot_type = SlotType.INPUT
        elif True in [item["name"] == rec_slot_name for item in info.get("inner_input_slots", [])]:
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
        # TODO: replace query after dictionary extension
        info = self._osl_server.get_actor_info(connection["sending_uuid"])
        if True in [item["name"] == sen_slot_name for item in info["output_slots"]]:
            sen_slot_type = SlotType.OUTPUT
        elif True in [item["name"] == sen_slot_name for item in info.get("inner_output_slots", [])]:
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
            type_ = node["type"]
            if kind == "actor":
                nodes_list.append(
                    Node(uid=uid, osl_server=self._osl_server, type_=type_, logger=self._logger)
                )
            elif kind == "system":
                if node["is_parametric_system"]:
                    nodes_list.append(
                        ParametricSystem(
                            uid=uid, osl_server=self._osl_server, type_=type_, logger=self._logger
                        )
                    )
                else:
                    nodes_list.append(
                        System(
                            uid=uid, osl_server=self._osl_server, type_=type_, logger=self._logger
                        )
                    )
            elif kind == "root_system":
                nodes_list.append(
                    RootSystem(uid=node["uid"], osl_server=self._osl_server, logger=self._logger)
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
        node: Union[Node, None] = None,
    ) -> Slot:
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
        Slot
            Instance of the Slot class.
        """
        if uid == self.uid:
            node = self
        elif uid == project_tree["uid"]:
            node = RootSystem(uid=uid, osl_server=self._osl_server, logger=self._logger)
        else:
            node_dict = self.__class__._find_node_with_uid(
                uid=uid,
                tree=project_tree,
                properties_dicts_list=[],
                current_depth=1,
                max_search_depth=float("inf"),
            )
            node = self._create_nodes_from_properties_dicts(properties_dicts_list=node_dict)[0]
        return Slot.create_slot(
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

    @staticmethod
    def _filter_connections(
        connections: List[dict], uid: str, direction: str, slot_name: Union[str, None] = None
    ) -> Tuple[dict]:
        """Filter list of connections to by given node, slot type and optionally slot name.

        Parameters
        ----------
        connections : List[dict]
            List of connections.
        uid: str
            Node uid.
        direction: str
            Direction type, either 'receiving' or 'sending'.
        slot_name: Union[str, None], optional
            Name of the slot.

        Returns
        -------
        Tuple[dict]
            Tuple of filtered connections dictionaries.
        """
        filtered_connections = []
        uid_key = direction + "_uuid"
        if slot_name:
            slot_name_key = slot_name + "_slot"
        for connection in connections:
            if connection[uid_key] != uid:
                continue
            if slot_name is not None and connection[slot_name_key] != slot_name:
                continue
            filtered_connections.append(connection)
        return tuple(filtered_connections)

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


class System(Node):
    """Provides for creating and operatating on a system."""

    def __init__(
        self,
        uid: str,
        osl_server: OslServer,
        type_: Union[NodeType, str],
        logger=None,
    ) -> None:
        """Create a ``System`` instance.

        Parameters
        ----------
        uid: str
            Unique ID.
        osl_server: OslServer
            Object providing access to the optiSLang server.
        type_: Union[NodeType, str]
            Instance of the ``NodeType`` class for supported nodes, ``string`` otherwise.
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
        type_: Union[NodeType, str],
        name: Union[str, None] = None,
        design_flow: Union[DesignFlow, None] = None,
        algorithm_type: Union[str, None] = None,
        integration_type: Union[str, None] = None,
        mop_node_type: Union[str, None] = None,
        node_type: Union[str, None] = None,
    ) -> Node:
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
        # TODO: test
        if isinstance(type_, NodeType):
            if type_ == NodeType.RunnableSystem:
                raise ValueError(
                    "Creation of RootSystem (NodeType.RunnableSystem) is not supported."
                )
            algorithm_type, integration_type, mop_node_type, node_type = NodeType.get_subtype(
                type_.value
            )
            type_ = type_.name
            if "CFX" in type_:
                type_ = type_.replace("_", "-")
        elif not isinstance(type_, str):
            raise TypeError(
                f"Invalid type of ``type_: {type(type_)}``, "
                "``NodeType`` or ``str`` was expected."
            )
        design_flow_name = design_flow.name.lower() if design_flow is not None else None
        uid = self._osl_server.create_node(
            type_=type_,
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
        return self._create_nodes_from_properties_dicts([info])

    def delete_children_nodes(self) -> None:
        """Delete all children nodes from active project.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        # TODO: test
        nodes = self.get_nodes()
        for node in nodes:
            node.delete()

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

    def get_inner_input_slots(self) -> Tuple[Slot, ...]:
        """Get node's inner input slots.

        Returns
        -------
        Tuple[Slot,...]
            Tuple of defined inner input slots.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self._get_slots(type_=SlotType.INNER_INPUT)

    def get_inner_output_slots(self) -> Tuple[Slot, ...]:
        """Get node's inner output slots.

        Returns
        -------
        Tuple[Slot,...]
            Tuple of defined inner output slots.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self._get_slots(type_=SlotType.INNER_OUTPUT)

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


class ParametricSystem(System):
    """Provides methods to obtain data from a parametric system."""

    def __init__(
        self,
        uid: str,
        osl_server: OslServer,
        type_: Union[NodeType, str],
        logger=None,
    ) -> None:
        """Create a parametric system.

        Parameters
        ----------
        uid: str
            Unique ID.
        osl_server: OslServer
            Object providing access to the optiSLang server.
        type_: Union[NodeType, str]
            Instance of the ``NodeType`` class for supported nodes, ``string`` otherwise.
        logger: Any, optional
            Object for logging. If ``None``, standard logging object is used. Defaults to ``None``.
        """
        super().__init__(
            uid=uid,
            osl_server=osl_server,
            type_=type_,
            logger=logger,
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


class RootSystem(ParametricSystem):
    """Provides for creating and operating on a project system."""

    def __init__(
        self,
        uid: str,
        osl_server: OslServer,
        logger=None,
    ) -> None:
        """Create a ``RootSystem`` system.

        Parameters
        ----------
        uid: str
            Unique ID.
        osl_server: OslServer
            Object providing access to the optiSLang server.
        logger: Any, optional
            Object for logging. If ``None``, standard logging object is used. Defaults to ``None``.
        """
        super().__init__(
            uid=uid,
            osl_server=osl_server,
            type_=NodeType.RunnableSystem,
            logger=logger,
        )

    def delete(self) -> None:
        """Delete current node and it's children from active project.

        Raises
        ------
        NotImplementedError
            Raised always.
        """
        # TODO: test
        raise NotImplementedError("``RootSystem`` cannot be deleted.")

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


# TODO: test
class Slot:
    """Provides for creating and operating on slots."""

    def __init__(
        self,
        osl_server: OslServer,
        node: Node,
        name: str,
        type_: SlotType,
        type_hint: Union[str, None] = None,
    ) -> None:
        """Create a ``Slot`` instance.

        Parameters
        ----------
        osl_server: OslServer
            Object providing access to the optiSLang server.
        node : Node
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
        """Get slot name."""
        return self.__name

    @property
    def node(self) -> Node:
        """Get node to which the slot belongs."""
        return self.__node

    @property
    def type(self) -> SlotType:
        """Get slot type."""
        return self.__type

    @property
    def type_hint(self) -> Union[str, None]:
        """Get type hint."""
        return self.__type_hint

    def get_connections(self) -> Tuple[Edge]:
        """Get connections for current slot.

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
        osl_server: OslServer,
        node: Node,
        name: str,
        type_: SlotType,
        type_hint: Union[str, None] = None,
    ) -> Slot:
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
        Union[InputSlot, OutputSlot]
            Instance of InputSlot or OutputSlot.
        """
        if type_ == SlotType.INPUT:
            return InputSlot(
                osl_server=osl_server, node=node, name=name, type_=type_, type_hint=type_hint
            )
        elif type_ == SlotType.INNER_INPUT:
            return InnerInputSlot(
                osl_server=osl_server, node=node, name=name, type_=type_, type_hint=type_hint
            )
        elif type_ == SlotType.OUTPUT:
            return OutputSlot(
                osl_server=osl_server, node=node, name=name, type_=type_, type_hint=type_hint
            )
        elif type_ == SlotType.INNER_OUTPUT:
            return InnerOutputSlot(
                osl_server=osl_server, node=node, name=name, type_=type_, type_hint=type_hint
            )
        else:
            raise TypeError(
                f"Type of ``type_`` = ``SlotType`` was expected, but ``{type(type_)}`` was given."
            )

    @staticmethod
    def _create_connection_script(from_slot: Slot, to_slot: Slot) -> str:
        """Create optiSLang python script for slot connection.

        Parameters
        ----------
        from_slot : Slot
            Sending slot.
        to_slot : Slot
            Receiving slot.

        Returns
        -------
        str
            Python script for slot connection.
        """
        # TODO: Remove this, after server command `connect_nodes` is fixed (works for inner slots).
        if isinstance(from_slot.node, RootSystem):
            from_actor_script = "from_actor = project.get_root_system()\n"
        else:
            from_actor_script = __class__._create_find_actor_script(
                slot=from_slot, name="from_actor"
            )

        if isinstance(to_slot.node, RootSystem):
            to_actor_script = "to_actor = project.get_root_system()"
        else:
            to_actor_script = __class__._create_find_actor_script(slot=to_slot, name="to_actor")

        final_script = (
            f"{from_actor_script}\n"
            f"{to_actor_script}\n"
            f"connect(from_actor=from_actor, from_slot='{from_slot.name}', "
            f"to_actor=to_actor, to_slot='{to_slot.name}')\n"
        )
        return final_script

    @staticmethod
    def _create_find_actor_script(slot: Slot, name: str):
        actor_ancestors = slot.node.get_ancestors()
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
        actor_script += f"   if str(child.uuid)=='{slot.node.uid}': {name} = child\n"
        return actor_script


# TODO: test
class InputSlot(Slot):
    """Provides for creating and operating on input slots."""

    def __init__(
        self,
        osl_server: OslServer,
        node: Node,
        name: str,
        type_: SlotType,
        type_hint: Union[str, None] = None,
    ) -> None:
        """Create a ``InputSlot`` instance.

        Parameters
        ----------
        osl_server: OslServer
            Object providing access to the optiSLang server.
        node : Node
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

    def connect_from(self, from_slot: Slot) -> Edge:
        """Connect slot from another slot.

        Parameters
        ----------
        from_slot: Slot
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
        if not isinstance(from_slot, (InnerInputSlot, InnerOutputSlot)):
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
        """Remove all connections for given slot.

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
class OutputSlot(Slot):
    """Provides for creating and operating on output slots."""

    def __init__(
        self,
        osl_server: OslServer,
        node: Node,
        name: str,
        type_: SlotType,
        type_hint: Union[str, None] = None,
    ) -> None:
        """Create a ``OutputSlot`` instance.

        Parameters
        ----------
        osl_server: OslServer
            Object providing access to the optiSLang server.
        node : Node
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

    def connect_to(self, to_slot: Slot) -> Edge:
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
        if not isinstance(to_slot, (InnerInputSlot, InnerOutputSlot)):
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
        """Remove all connections for given slot.

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
class InnerInputSlot(Slot):
    """Provides for creating and operating on inner input slots."""

    def __init__(
        self,
        osl_server: OslServer,
        node: Node,
        name: str,
        type_: SlotType,
        type_hint: Union[str, None] = None,
    ) -> None:
        """Create a ``InnerInputSlot`` instance.

        Parameters
        ----------
        osl_server: OslServer
            Object providing access to the optiSLang server.
        node : Node
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

    def connect_from(self, from_slot: Slot) -> Edge:
        """Connect slot from another slot.

        Parameters
        ----------
        from_slot: Slot
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
class InnerOutputSlot(Slot):
    """Provides for creating and operating on inner output slots."""

    def __init__(
        self,
        osl_server: OslServer,
        node: Node,
        name: str,
        type_: SlotType,
        type_hint: Union[str, None] = None,
    ) -> None:
        """Create a ``InnerOutputSlot`` instance.

        Parameters
        ----------
        osl_server: OslServer
            Object providing access to the optiSLang server.
        node : Node
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

    def connect_to(self, to_slot: Slot) -> Edge:
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
        python_script = self.__class__._create_connection_script(from_slot=self, to_slot=to_slot)
        self._osl_server.run_python_script(script=python_script)
        return Edge(from_slot=self, to_slot=to_slot)


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
