"""This module contains available node types."""

from __future__ import annotations

from enum import Enum

from ansys.optislang.core.utils import enum_from_str


class AddinType(Enum):
    """Provides ``AddinType`` options."""

    BUILT_IN = 0
    ALGORITHM_PLUGIN = 1
    INTEGRATION_PLUGIN = 2
    PYTHON_BASED_ALGORITHM_PLUGIN = 3
    PYTHON_BASED_INTEGRATION_PLUGIN = 4
    PYTHON_BASED_MOP_NODE_PLUGIN = 5
    PYTHON_BASED_NODE_PLUGIN = 6

    @staticmethod
    def from_str(string: str) -> AddinType:
        """Convert string to an instance of the ``AddinType`` class.

        Parameters
        ----------
        string: str
            String to be converted.

        Returns
        -------
        AddinType
            Instance of the ``AddinType`` class.

        Raises
        ------
        TypeError
            Raised when an invalid type of ``string`` is given.
        ValueError
            Raised when an invalid value of ``string`` is given.
        """
        return enum_from_str(string=string, enum_class=__class__, replace=(" ", "_"))


class NodeType:
    """Class containing information about node type."""

    def __init__(self, id: str, subtype: AddinType):
        """Create an instance of the ``NodeType`` class.

        Parameters
        ----------
        id : str
            Type of node.
        subtype : AddinType
            Subtype of node.
        """
        self.__id = id
        self.__subtype = subtype

    def __str__(self):
        """Return formatted string."""
        return f"type: {self.id}, subtype: {self.subtype}"

    def __eq__(self, other: NodeType) -> bool:
        """Compare properties of two instances of the ``NodeType`` class.

        Parameters
        ----------
        other: NodeType
            Criterion for comparison.

        Returns
        -------
        bool
            ``True`` if all properties match; ``False`` otherwise.
        """
        if type(self) == type(other):
            checks = {}
            checks["id"] = self.id == other.id
            checks["subtype"] = self.subtype == other.subtype
            return False not in checks.values()
        else:
            return False

    @property
    def id(self) -> str:
        """Type of node.

        Returns
        -------
        str
            Type of node.
        """
        return self.__id

    @property
    def subtype(self) -> AddinType:
        """Subtype of node.

        Returns
        -------
        AddinType
            Instance of the ``AddinType`` class.
        """
        return self.__subtype


# region NODES
# region Builtins
ProEParameterize = NodeType(id="ProEParameterize", subtype=AddinType.BUILT_IN)
ParameterSet = NodeType(id="ParameterSet", subtype=AddinType.BUILT_IN)
Mopsolver = NodeType(id="Mopsolver", subtype=AddinType.BUILT_IN)
BashScript = NodeType(id="BashScript", subtype=AddinType.BUILT_IN)
Sum = NodeType(id="Sum", subtype=AddinType.BUILT_IN)
ProEProcess = NodeType(id="ProEProcess", subtype=AddinType.BUILT_IN)
Compare = NodeType(id="Compare", subtype=AddinType.BUILT_IN)
ETKAsciiOutput = NodeType(id="ETKAsciiOutput", subtype=AddinType.BUILT_IN)
Calculator = NodeType(id="Calculator", subtype=AddinType.BUILT_IN)
Variable = NodeType(id="Variable", subtype=AddinType.BUILT_IN)
AnsysAPDLParameterize = NodeType(id="AnsysAPDLParameterize", subtype=AddinType.BUILT_IN)
Parameterize = NodeType(id="Parameterize", subtype=AddinType.BUILT_IN)
CatiaParameterize = NodeType(id="CatiaParameterize", subtype=AddinType.BUILT_IN)
VCollabProcess = NodeType(id="VCollabProcess", subtype=AddinType.BUILT_IN)
Mathcad = NodeType(id="Mathcad", subtype=AddinType.BUILT_IN)
LSDynaParameterize = NodeType(id="LSDynaParameterize", subtype=AddinType.BUILT_IN)
MultiplasParameterize = NodeType(id="MultiplasParameterize", subtype=AddinType.BUILT_IN)
TaggedParametersParameterize = NodeType(
    id="TaggedParametersParameterize", subtype=AddinType.BUILT_IN
)
Monitoring = NodeType(id="Monitoring", subtype=AddinType.BUILT_IN)
PMOPPostprocessing = NodeType(id="PMOPPostprocessing", subtype=AddinType.BUILT_IN)
VariantMonitoring = NodeType(id="VariantMonitoring", subtype=AddinType.BUILT_IN)
Postprocessing = NodeType(id="Postprocessing", subtype=AddinType.BUILT_IN)
String = NodeType(id="String", subtype=AddinType.BUILT_IN)
Path = NodeType(id="Path", subtype=AddinType.BUILT_IN)
ETKAbaqus = NodeType(id="ETKAbaqus", subtype=AddinType.BUILT_IN)
ScriptFile = NodeType(id="ScriptFile", subtype=AddinType.BUILT_IN)
Matlab = NodeType(id="Matlab", subtype=AddinType.BUILT_IN)
CFturboInput = NodeType(id="CFturboInput", subtype=AddinType.BUILT_IN)
Excel = NodeType(id="Excel", subtype=AddinType.BUILT_IN)
Parameter = NodeType(id="Parameter", subtype=AddinType.BUILT_IN)
Mop = NodeType(id="Mop", subtype=AddinType.BUILT_IN)
PMop = NodeType(id="PMop", subtype=AddinType.BUILT_IN)
PMopsolver = NodeType(id="PMopsolver", subtype=AddinType.BUILT_IN)
ETKComplete = NodeType(id="ETKComplete", subtype=AddinType.BUILT_IN)
ETKAnsys = NodeType(id="ETKAnsys", subtype=AddinType.BUILT_IN)
PythonScript = NodeType(id="PythonScript", subtype=AddinType.BUILT_IN)
OOCalc = NodeType(id="OOCalc", subtype=AddinType.BUILT_IN)
ETKAdams = NodeType(id="ETKAdams", subtype=AddinType.BUILT_IN)
ETKMadymo = NodeType(id="ETKMadymo", subtype=AddinType.BUILT_IN)
ETKEdyson = NodeType(id="ETKEdyson", subtype=AddinType.BUILT_IN)
Designexport = NodeType(id="Designexport", subtype=AddinType.BUILT_IN)
ETKMidas = NodeType(id="ETKMidas", subtype=AddinType.BUILT_IN)
SoSPostprocessing = NodeType(id="SoSPostprocessing", subtype=AddinType.BUILT_IN)
Octave = NodeType(id="Octave", subtype=AddinType.BUILT_IN)
CalculatorSet = NodeType(id="CalculatorSet", subtype=AddinType.BUILT_IN)
AnsysWorkbench = NodeType(id="AnsysWorkbench", subtype=AddinType.BUILT_IN)
Criteria = NodeType(id="Criteria", subtype=AddinType.BUILT_IN)
Process = NodeType(id="Process", subtype=AddinType.BUILT_IN)
AbaqusProcess = NodeType(id="AbaqusProcess", subtype=AddinType.BUILT_IN)
CatiaProcess = NodeType(id="CatiaProcess", subtype=AddinType.BUILT_IN)
AppendDesignsToBinFile = NodeType(id="AppendDesignsToBinFile", subtype=AddinType.BUILT_IN)
BatchScript = NodeType(id="BatchScript", subtype=AddinType.BUILT_IN)
PerlScript = NodeType(id="PerlScript", subtype=AddinType.BUILT_IN)
SolverTemplate = NodeType(id="SolverTemplate", subtype=AddinType.BUILT_IN)
SimulationX = NodeType(id="SimulationX", subtype=AddinType.BUILT_IN)
DesignExport = NodeType(id="DesignExport", subtype=AddinType.BUILT_IN)
DPS = NodeType(id="DPS", subtype=AddinType.BUILT_IN)
DesignImport = NodeType(id="DesignImport", subtype=AddinType.BUILT_IN)
MergeDesigns = NodeType(id="MergeDesigns", subtype=AddinType.BUILT_IN)
Wait = NodeType(id="Wait", subtype=AddinType.BUILT_IN)
FloEFDInput = NodeType(id="FloEFDInput", subtype=AddinType.BUILT_IN)
DataExport = NodeType(id="DataExport", subtype=AddinType.BUILT_IN)
DataImport = NodeType(id="DataImport", subtype=AddinType.BUILT_IN)
ASCMOsolver = NodeType(id="ASCMOsolver", subtype=AddinType.BUILT_IN)
IntegrationPlugin = NodeType(id="IntegrationPlugin", subtype=AddinType.BUILT_IN)
TurboOptInput = NodeType(id="TurboOptInput", subtype=AddinType.BUILT_IN)
PDM = NodeType(id="PDM", subtype=AddinType.BUILT_IN)
PDMReceive = NodeType(id="PDMReceive", subtype=AddinType.BUILT_IN)
PDMSend = NodeType(id="PDMSend", subtype=AddinType.BUILT_IN)
Python2 = NodeType(id="Python2", subtype=AddinType.BUILT_IN)
SoSGenerate = NodeType(id="SoSGenerate", subtype=AddinType.BUILT_IN)
DataMining = NodeType(id="DataMining", subtype=AddinType.BUILT_IN)
AmesimInput = NodeType(id="AmesimInput", subtype=AddinType.BUILT_IN)
SimPackInput = NodeType(id="SimPackInput", subtype=AddinType.BUILT_IN)
CetolInput = NodeType(id="CetolInput", subtype=AddinType.BUILT_IN)
ETKAMESim = NodeType(id="ETKAMESim", subtype=AddinType.BUILT_IN)
Custom = NodeType(id="Custom", subtype=AddinType.BUILT_IN)
ETKLSDYNA = NodeType(id="ETKLSDYNA", subtype=AddinType.BUILT_IN)
ETKFloEFD = NodeType(id="ETKFloEFD", subtype=AddinType.BUILT_IN)
ETKCFturbo = NodeType(id="ETKCFturbo", subtype=AddinType.BUILT_IN)
ETKSimPack = NodeType(id="ETKSimPack", subtype=AddinType.BUILT_IN)
ETKTurboOpt = NodeType(id="ETKTurboOpt", subtype=AddinType.BUILT_IN)
ETKExtOut = NodeType(id="ETKExtOut", subtype=AddinType.BUILT_IN)
ETKCetol = NodeType(id="ETKCetol", subtype=AddinType.BUILT_IN)
CustomIntegration = NodeType(id="CustomIntegration", subtype=AddinType.BUILT_IN)
CustomETKIntegration = NodeType(id="CustomETKIntegration", subtype=AddinType.BUILT_IN)
CustomMop = NodeType(id="CustomMop", subtype=AddinType.BUILT_IN)
# endregion
# region Integration plugins
awb2_plugin = NodeType(id="awb2_plugin", subtype=AddinType.INTEGRATION_PLUGIN)
discovery_plugin = NodeType(id="discovery_plugin", subtype=AddinType.INTEGRATION_PLUGIN)
lsdyna_plugin = NodeType(id="lsdyna_plugin", subtype=AddinType.INTEGRATION_PLUGIN)
optislang_node = NodeType(id="optislang_node", subtype=AddinType.INTEGRATION_PLUGIN)
spaceclaim_plugin = NodeType(id="spaceclaim_plugin", subtype=AddinType.INTEGRATION_PLUGIN)
speos_plugin = NodeType(id="speos_plugin", subtype=AddinType.INTEGRATION_PLUGIN)
# endregion
# region Python based integration plugins
AEDT2 = NodeType(id="AEDT2", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
AEDT2_lsdso = NodeType(id="AEDT2_lsdso", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
ANSA_input = NodeType(id="ANSA_input", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
ANSA_output = NodeType(id="ANSA_output", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
AmplitudesFromField_SoS = NodeType(
    id="AmplitudesFromField_SoS", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN
)
AxSTREAM = NodeType(id="AxSTREAM", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
CAD_CATIA = NodeType(id="CAD_CATIA", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
CAD_Creo = NodeType(id="CAD_Creo", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
CAD_Inventor = NodeType(id="CAD_Inventor", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
CAD_NX = NodeType(id="CAD_NX", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
CAESES_input = NodeType(id="CAESES_input", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
CFX_Partitioner = NodeType(id="CFX-Partitioner", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
CFX_Partitioner_v3 = NodeType(
    id="CFX-Partitioner-v3", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN
)
CFX_Pre = NodeType(id="CFX-Pre", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
CFX_Pre_v3 = NodeType(id="CFX-Pre-v3", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
CFX_Solver = NodeType(id="CFX-Solver", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
CFX_Solver_v3 = NodeType(id="CFX-Solver-v3", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
CFturbo_input = NodeType(id="CFturbo_input", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
COMSOL2 = NodeType(id="COMSOL2", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
COMSOL_input = NodeType(id="COMSOL_input", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
COMSOL_output = NodeType(id="COMSOL_output", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
Convert_OMDB_to_BIN_SoS = NodeType(
    id="Convert_OMDB_to_BIN_SoS", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN
)
DPF = NodeType(id="DPF", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
ETK_nD = NodeType(id="ETK_nD", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
FMU_SoS = NodeType(id="FMU_SoS", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
Field_Data_Collector = NodeType(
    id="Field_Data_Collector", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN
)
Field_MOP_2D_Nested_DOE_SoS = NodeType(
    id="Field_MOP_2D_Nested_DOE_SoS", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN
)
Field_MOP_ANSYSMECH_SoS = NodeType(
    id="Field_MOP_ANSYSMECH_SoS", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN
)
FloEFD_input = NodeType(id="FloEFD_input", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
FloEFD_output = NodeType(id="FloEFD_output", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
Fluent = NodeType(id="Fluent", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
Fluent_mesher = NodeType(id="Fluent_mesher", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
Fluent_solver = NodeType(id="Fluent_solver", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
Flux_input = NodeType(id="Flux_input", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
GTSUITE_input = NodeType(id="GTSUITE_input", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
GTSUITE_output = NodeType(id="GTSUITE_output", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
Generate_SoS = NodeType(id="Generate_SoS", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
GeoDict_input = NodeType(id="GeoDict_input", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
GeoDict_output = NodeType(id="GeoDict_output", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
IPG_Automotive = NodeType(id="IPG_Automotive", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
JMAG_Designer_input = NodeType(
    id="JMAG_Designer_input", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN
)
JMAG_Designer_output = NodeType(
    id="JMAG_Designer_output", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN
)
JMAG_Designer_solve = NodeType(
    id="JMAG_Designer_solve", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN
)
JSON_input = NodeType(id="JSON_input", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
JSON_output = NodeType(id="JSON_output", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
KULI = NodeType(id="KULI", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
Lumerical = NodeType(id="Lumerical", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
META_output = NodeType(id="META_output", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
Matlab_mat_input = NodeType(
    id="Matlab_mat_input", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN
)
Matlab_mat_output = NodeType(
    id="Matlab_mat_output", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN
)
ModelCenter = NodeType(id="ModelCenter", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
MotorCAD_input = NodeType(id="MotorCAD_input", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
MotorCAD_output = NodeType(id="MotorCAD_output", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
MotorCAD_solve = NodeType(id="MotorCAD_solve", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
NASTRAN = NodeType(id="NASTRAN", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
OpticStudio = NodeType(id="OpticStudio", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
PuTTY_SSH = NodeType(id="PuTTY_SSH", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
ROCKY_input = NodeType(id="ROCKY_input", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
ROCKY_output = NodeType(id="ROCKY_output", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
SPEOSCore = NodeType(id="SPEOSCore", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
SPEOS_Report_Reader = NodeType(
    id="SPEOS_Report_Reader", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN
)
SimulationX_SXOA = NodeType(
    id="SimulationX_SXOA", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN
)
Viewer_SoS = NodeType(id="Viewer_SoS", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
VirtualLab_input = NodeType(
    id="VirtualLab_input", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN
)
VirtualLab_output = NodeType(
    id="VirtualLab_output", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN
)
ZEMAX = NodeType(id="ZEMAX", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
ZEMAX_input = NodeType(id="ZEMAX_input", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
ZEMAX_output = NodeType(id="ZEMAX_output", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
ZEMAX_solve = NodeType(id="ZEMAX_solve", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
optislang_omdb = NodeType(id="optislang_omdb", subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN)
# endregion
# region Python based MOP node plugins
MOP = NodeType(id="MOP", subtype=AddinType.PYTHON_BASED_MOP_NODE_PLUGIN)
# endregion
# endregion

# region SYSTEMS
# region Builtins
While = NodeType(id="While", subtype=AddinType.BUILT_IN)
# endregion
# endregion

# region PARAMETRIC SYSTEMS
# region Builtins
SIMPLEX = NodeType(id="SIMPLEX", subtype=AddinType.BUILT_IN)
PSO = NodeType(id="PSO", subtype=AddinType.BUILT_IN)
AMOP = NodeType(id="AMOP", subtype=AddinType.BUILT_IN)
Sensitivity = NodeType(id="Sensitivity", subtype=AddinType.BUILT_IN)
Robustness = NodeType(id="Robustness", subtype=AddinType.BUILT_IN)
SDI = NodeType(id="SDI", subtype=AddinType.BUILT_IN)
EA = NodeType(id="EA", subtype=AddinType.BUILT_IN)
ReliabilityFORM = NodeType(id="ReliabilityFORM", subtype=AddinType.BUILT_IN)
NOA2 = NodeType(id="NOA2", subtype=AddinType.BUILT_IN)
NLPQLP = NodeType(id="NLPQLP", subtype=AddinType.BUILT_IN)
ARSM = NodeType(id="ARSM", subtype=AddinType.BUILT_IN)
Memetic = NodeType(id="Memetic", subtype=AddinType.BUILT_IN)
ParametricSystem = NodeType(id="ParametricSystem", subtype=AddinType.BUILT_IN)
Reevaluate = NodeType(id="Reevaluate", subtype=AddinType.BUILT_IN)
ReliabilityMC = NodeType(id="ReliabilityMC", subtype=AddinType.BUILT_IN)
ReliabilityAS = NodeType(id="ReliabilityAS", subtype=AddinType.BUILT_IN)
ReliabilityDS = NodeType(id="ReliabilityDS", subtype=AddinType.BUILT_IN)
ReliabilityARSM = NodeType(id="ReliabilityARSM", subtype=AddinType.BUILT_IN)
ReliabilityAsym = NodeType(id="ReliabilityAsym", subtype=AddinType.BUILT_IN)
ReliabilityISPUD = NodeType(id="ReliabilityISPUD", subtype=AddinType.BUILT_IN)
AlgorithmSystemPlugin = NodeType(id="AlgorithmSystemPlugin", subtype=AddinType.BUILT_IN)
CustomAlgorithm = NodeType(id="CustomAlgorithm", subtype=AddinType.BUILT_IN)
# endregion
# region Python based algorithm plugins
BASS = NodeType(id="BASS", subtype=AddinType.PYTHON_BASED_ALGORITHM_PLUGIN)
DXAMO = NodeType(id="DXAMO", subtype=AddinType.PYTHON_BASED_ALGORITHM_PLUGIN)
DXASO = NodeType(id="DXASO", subtype=AddinType.PYTHON_BASED_ALGORITHM_PLUGIN)
DXMISQP = NodeType(id="DXMISQP", subtype=AddinType.PYTHON_BASED_ALGORITHM_PLUGIN)
DXUPEGO = NodeType(id="DXUPEGO", subtype=AddinType.PYTHON_BASED_ALGORITHM_PLUGIN)
GLAD = NodeType(id="GLAD", subtype=AddinType.PYTHON_BASED_ALGORITHM_PLUGIN)
OCO = NodeType(id="OCO", subtype=AddinType.PYTHON_BASED_ALGORITHM_PLUGIN)
PIBO = NodeType(id="PIBO", subtype=AddinType.PYTHON_BASED_ALGORITHM_PLUGIN)
Replace_constant_parameter = NodeType(
    id="Replace_constant_parameter", subtype=AddinType.PYTHON_BASED_ALGORITHM_PLUGIN
)
Unigene_EA = NodeType(id="Unigene_EA", subtype=AddinType.PYTHON_BASED_ALGORITHM_PLUGIN)
while_loop = NodeType(id="while_loop", subtype=AddinType.PYTHON_BASED_ALGORITHM_PLUGIN)
# endregion
# endregion
