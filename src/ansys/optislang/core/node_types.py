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

"""This module contains available node types."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from ansys.optislang.core.nodes import NodeClassType
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

    @classmethod
    def from_str(cls, string: str) -> AddinType:
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
        return enum_from_str(string=string, enum_class=cls, replace=(" ", "_"))


class NodeType:
    """Class containing information about node type."""

    def __init__(self, id: str, subtype: AddinType, osl_class_type: Optional[NodeClassType] = None):
        """Create an instance of the ``NodeType`` class.

        Parameters
        ----------
        id : str
            Type of node.
        subtype : AddinType
            Subtype of node.
        osl_class_type: Optional[NodeClassType], optional
            Type of class that should be created, by default ``None``.
        """
        self.__id = id
        self.__subtype = subtype
        self.__osl_class_type = osl_class_type

    def __repr__(self):
        """Return formatted string."""
        return (
            f"<NodeType id={self.id}, subtype={self.subtype}, osl_class_type={self.osl_class_type}>"
        )

    def __str__(self):
        """Return formatted string."""
        return f"type: {self.id}, subtype: {self.subtype}, osl_class_type:{self.osl_class_type}"

    def __eq__(self, other: object) -> bool:
        """Object comparison."""
        if not isinstance(other, NodeType):
            return NotImplemented
        return self.id == other.id and self.subtype == other.subtype

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
    def osl_class_type(self) -> Optional[NodeClassType]:
        """Type of node class.

        Returns
        -------
        Optional[NodeClassType]
            Instance of the ``NodeClassType`` class, ``None`` if not specified.
        """
        return self.__osl_class_type

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
AbaqusProcess = NodeType(
    id="AbaqusProcess", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
AmesimInput = NodeType(
    id="AmesimInput", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
AnsysAPDLParameterize = NodeType(
    id="AnsysAPDLParameterize",
    subtype=AddinType.BUILT_IN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
AnsysWorkbench = NodeType(
    id="AnsysWorkbench", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
AppendDesignsToBinFile = NodeType(
    id="AppendDesignsToBinFile", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
ASCMOsolver = NodeType(
    id="ASCMOsolver", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
BashScript = NodeType(
    id="BashScript", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
BatchScript = NodeType(
    id="BatchScript", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
Calculator = NodeType(
    id="Calculator", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
CalculatorSet = NodeType(
    id="CalculatorSet", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
CatiaParameterize = NodeType(
    id="CatiaParameterize",
    subtype=AddinType.BUILT_IN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
CatiaProcess = NodeType(
    id="CatiaProcess", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
CetolInput = NodeType(
    id="CetolInput", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
CFturboInput = NodeType(
    id="CFturboInput", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
Compare = NodeType(
    id="Compare",
    subtype=AddinType.BUILT_IN,
    osl_class_type=NodeClassType.NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
Custom = NodeType(id="Custom", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
CustomETKIntegration = NodeType(
    id="CustomETKIntegration",
    subtype=AddinType.BUILT_IN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
CustomIntegration = NodeType(
    id="CustomIntegration",
    subtype=AddinType.BUILT_IN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
CustomMop = NodeType(id="CustomMop", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
DataExport = NodeType(
    id="DataExport", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
DataImport = NodeType(
    id="DataImport", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
DataMining = NodeType(
    id="DataMining", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
DesignExport = NodeType(
    id="DesignExport", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
DesignImport = NodeType(
    id="DesignImport", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
DPS = NodeType(id="DPS", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
ETKAbaqus = NodeType(
    id="ETKAbaqus", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
ETKAdams = NodeType(
    id="ETKAdams", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
ETKAMESim = NodeType(
    id="ETKAMESim", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
ETKAnsys = NodeType(
    id="ETKAnsys", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
ETKAsciiOutput = NodeType(
    id="ETKAsciiOutput", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
ETKCetol = NodeType(
    id="ETKCetol", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
ETKCFturbo = NodeType(
    id="ETKCFturbo", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
ETKComplete = NodeType(
    id="ETKComplete", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
ETKEdyson = NodeType(
    id="ETKEdyson", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
ETKExtOut = NodeType(
    id="ETKExtOut", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
ETKFloEFD = NodeType(
    id="ETKFloEFD", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
ETKLSDYNA = NodeType(
    id="ETKLSDYNA", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
ETKMadymo = NodeType(
    id="ETKMadymo", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
ETKMidas = NodeType(
    id="ETKMidas", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
ETKSimPack = NodeType(
    id="ETKSimPack", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
ETKTurboOpt = NodeType(
    id="ETKTurboOpt", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
Excel = NodeType(
    id="Excel", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
FloEFDInput = NodeType(
    id="FloEFDInput", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
IntegrationPlugin = NodeType(
    id="IntegrationPlugin",
    subtype=AddinType.BUILT_IN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
LSDynaParameterize = NodeType(
    id="LSDynaParameterize",
    subtype=AddinType.BUILT_IN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
Matlab = NodeType(
    id="Matlab", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
Mop = NodeType(id="Mop", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
Mopsolver = NodeType(
    id="Mopsolver", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
MultiplasParameterize = NodeType(
    id="MultiplasParameterize", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
Octave = NodeType(
    id="Octave", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
OOCalc = NodeType(id="OOCalc", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
Parameterize = NodeType(
    id="Parameterize", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
Path = NodeType(id="Path", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
PDM = NodeType(id="PDM", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
PDMReceive = NodeType(
    id="PDMReceive", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
PDMSend = NodeType(
    id="PDMSend", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
PerlScript = NodeType(
    id="PerlScript", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
PMop = NodeType(id="PMop", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
PMOPPostprocessing = NodeType(
    id="PMOPPostprocessing", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
PMopsolver = NodeType(
    id="PMopsolver", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
Postprocessing = NodeType(
    id="Postprocessing", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
Process = NodeType(id="Process", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
ProEParameterize = NodeType(
    id="ProEParameterize", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
ProEProcess = NodeType(
    id="ProEProcess", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
ProxySolver = NodeType(
    id="ProxySolver", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.PROXY_SOLVER
)
"""Class :py:class:`~ansys.optislang.core.nodes.ProxySolver` is created from this node type."""
Python2 = NodeType(
    id="Python2", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
PythonScript = NodeType(
    id="PythonScript", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
SimPackInput = NodeType(
    id="SimPackInput", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
SimulationX = NodeType(
    id="SimulationX", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
SolverTemplate = NodeType(
    id="SolverTemplate", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
SoSGenerate = NodeType(
    id="SoSGenerate", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
SoSPostprocessing = NodeType(
    id="SoSPostprocessing", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
String = NodeType(id="String", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE)
TaggedParametersParameterize = NodeType(
    id="TaggedParametersParameterize",
    subtype=AddinType.BUILT_IN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
TurboOptInput = NodeType(
    id="TurboOptInput", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.INTEGRATION_NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
Variable = NodeType(id="Variable", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
VariantMonitoring = NodeType(
    id="VariantMonitoring", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
VCollabProcess = NodeType(
    id="VCollabProcess", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE
)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
Wait = NodeType(id="Wait", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.NODE)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
# endregion
# region Integration plugins
awb2_plugin = NodeType(
    id="awb2_plugin",
    subtype=AddinType.INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
discovery_plugin = NodeType(
    id="discovery_plugin",
    subtype=AddinType.INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
lsdyna_plugin = NodeType(
    id="lsdyna_plugin",
    subtype=AddinType.INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
optislang_node = NodeType(
    id="optislang_node",
    subtype=AddinType.INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
spaceclaim_plugin = NodeType(
    id="spaceclaim_plugin",
    subtype=AddinType.INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
speos_plugin = NodeType(
    id="speos_plugin",
    subtype=AddinType.INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
# endregion
# region Python based integration plugins
AEDT2 = NodeType(
    id="AEDT2",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
AEDT2_lsdso = NodeType(
    id="AEDT2_lsdso",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
ANSA_input = NodeType(
    id="ANSA_input",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
ANSA_output = NodeType(
    id="ANSA_output",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
AmplitudesFromField_SoS = NodeType(
    id="AmplitudesFromField_SoS",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
AxSTREAM = NodeType(
    id="AxSTREAM",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
CAD_CATIA = NodeType(
    id="CAD_CATIA",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
CAD_Creo = NodeType(
    id="CAD_Creo",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
CAD_Inventor = NodeType(
    id="CAD_Inventor",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
CAD_NX = NodeType(
    id="CAD_NX",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
CAESES_input = NodeType(
    id="CAESES_input",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
CFX_Partitioner = NodeType(
    id="CFX-Partitioner",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
CFX_Partitioner_v3 = NodeType(
    id="CFX-Partitioner-v3",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
CFX_Pre = NodeType(
    id="CFX-Pre",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
CFX_Pre_v3 = NodeType(
    id="CFX-Pre-v3",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
CFX_Solver = NodeType(
    id="CFX-Solver",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
CFX_Solver_v3 = NodeType(
    id="CFX-Solver-v3",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
CFturbo_input = NodeType(
    id="CFturbo_input",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
COMSOL2 = NodeType(
    id="COMSOL2",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
COMSOL_input = NodeType(
    id="COMSOL_input",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
COMSOL_output = NodeType(
    id="COMSOL_output",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
Convert_OMDB_to_BIN_SoS = NodeType(
    id="Convert_OMDB_to_BIN_SoS",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
ETK_nD = NodeType(
    id="ETK_nD",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
FMU_SoS = NodeType(
    id="FMU_SoS",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
Field_Data_Collector = NodeType(
    id="Field_Data_Collector",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
Field_MOP_2D_Nested_DOE_SoS = NodeType(
    id="Field_MOP_2D_Nested_DOE_SoS",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
Field_MOP_ANSYSMECH_SoS = NodeType(
    id="Field_MOP_ANSYSMECH_SoS",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
FloEFD_input = NodeType(
    id="FloEFD_input",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
FloEFD_output = NodeType(
    id="FloEFD_output",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
Fluent = NodeType(
    id="Fluent",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
Fluent_mesher = NodeType(
    id="Fluent_mesher",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
Fluent_solver = NodeType(
    id="Fluent_solver",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
Flux_input = NodeType(
    id="Flux_input",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
GTSUITE_input = NodeType(
    id="GTSUITE_input",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
GTSUITE_output = NodeType(
    id="GTSUITE_output",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
Generate_SoS = NodeType(
    id="Generate_SoS",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
GeoDict_input = NodeType(
    id="GeoDict_input",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
GeoDict_output = NodeType(
    id="GeoDict_output",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
IPG_Automotive = NodeType(
    id="IPG_Automotive",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
JMAG_Designer_input = NodeType(
    id="JMAG_Designer_input",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
JMAG_Designer_output = NodeType(
    id="JMAG_Designer_output",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
JMAG_Designer_solve = NodeType(
    id="JMAG_Designer_solve",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
JSON_input = NodeType(
    id="JSON_input",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
JSON_output = NodeType(
    id="JSON_output",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
KULI = NodeType(
    id="KULI",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
Lumerical = NodeType(
    id="Lumerical",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
META_output = NodeType(
    id="META_output",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
Matlab_mat_input = NodeType(
    id="Matlab_mat_input",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
Matlab_mat_output = NodeType(
    id="Matlab_mat_output",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
ModelCenter = NodeType(
    id="ModelCenter",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
MotorCAD_input = NodeType(
    id="MotorCAD_input",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
MotorCAD_output = NodeType(
    id="MotorCAD_output",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
MotorCAD_solve = NodeType(
    id="MotorCAD_solve",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
NASTRAN = NodeType(
    id="NASTRAN",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
OpticStudio = NodeType(
    id="OpticStudio",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
PuTTY_SSH = NodeType(
    id="PuTTY_SSH",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
ROCKY_input = NodeType(
    id="ROCKY_input",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
ROCKY_output = NodeType(
    id="ROCKY_output",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
SPEOSCore = NodeType(
    id="SPEOSCore",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
SPEOS_Report_Reader = NodeType(
    id="SPEOS_Report_Reader",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
SimulationX_SXOA = NodeType(
    id="SimulationX_SXOA",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
Viewer_SoS = NodeType(
    id="Viewer_SoS",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
VirtualLab_input = NodeType(
    id="VirtualLab_input",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
VirtualLab_output = NodeType(
    id="VirtualLab_output",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
ZEMAX = NodeType(
    id="ZEMAX",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
ZEMAX_input = NodeType(
    id="ZEMAX_input",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
ZEMAX_output = NodeType(
    id="ZEMAX_output",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
ZEMAX_solve = NodeType(
    id="ZEMAX_solve",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
optislang_omdb = NodeType(
    id="optislang_omdb",
    subtype=AddinType.PYTHON_BASED_INTEGRATION_PLUGIN,
    osl_class_type=NodeClassType.INTEGRATION_NODE,
)
"""Class :py:class:`~ansys.optislang.core.nodes.IntegrationNode` is created from this node type."""
# endregion
# region Python based MOP node plugins
MOP = NodeType(id="MOP", subtype=AddinType.PYTHON_BASED_MOP_NODE_PLUGIN)
"""Class :py:class:`~ansys.optislang.core.nodes.Node` is created from this node type."""
# endregion
# endregion
# region SYSTEMS
# region Builtins
System = NodeType(id="System", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.SYSTEM)
"""Class :py:class:`~ansys.optislang.core.nodes.System` is created from this node type.
note:: Creation of this specific node is not supported."""
While = NodeType(id="While", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.SYSTEM)
"""Class :py:class:`~ansys.optislang.core.nodes.System` is created from this node type."""
# endregion
# endregion
# region PARAMETRIC SYSTEMS
# region Builtins
AlgorithmSystemPlugin = NodeType(
    id="AlgorithmSystemPlugin",
    subtype=AddinType.BUILT_IN,
    osl_class_type=NodeClassType.PARAMETRIC_SYSTEM,
)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
AMOP = NodeType(
    id="AMOP", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.PARAMETRIC_SYSTEM
)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
ARSM = NodeType(
    id="ARSM", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.PARAMETRIC_SYSTEM
)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
CustomAlgorithm = NodeType(
    id="CustomAlgorithm", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.PARAMETRIC_SYSTEM
)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
EA = NodeType(id="EA", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.PARAMETRIC_SYSTEM)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
Memetic = NodeType(
    id="Memetic", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.PARAMETRIC_SYSTEM
)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
NLPQLP = NodeType(
    id="NLPQLP", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.PARAMETRIC_SYSTEM
)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
NOA2 = NodeType(
    id="NOA2", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.PARAMETRIC_SYSTEM
)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
ParametricSystem = NodeType(
    id="ParametricSystem",
    subtype=AddinType.BUILT_IN,
    osl_class_type=NodeClassType.PARAMETRIC_SYSTEM,
)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
PSO = NodeType(id="PSO", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.PARAMETRIC_SYSTEM)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
Reevaluate = NodeType(
    id="Reevaluate", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.PARAMETRIC_SYSTEM
)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
ReliabilityARSM = NodeType(
    id="ReliabilityARSM", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.PARAMETRIC_SYSTEM
)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
ReliabilityAS = NodeType(
    id="ReliabilityAS", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.PARAMETRIC_SYSTEM
)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
ReliabilityDS = NodeType(
    id="ReliabilityDS", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.PARAMETRIC_SYSTEM
)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
ReliabilityFORM = NodeType(
    id="ReliabilityFORM", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.PARAMETRIC_SYSTEM
)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
ReliabilityISPUD = NodeType(
    id="ReliabilityISPUD",
    subtype=AddinType.BUILT_IN,
    osl_class_type=NodeClassType.PARAMETRIC_SYSTEM,
)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
ReliabilityMC = NodeType(
    id="ReliabilityMC", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.PARAMETRIC_SYSTEM
)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
Robustness = NodeType(
    id="Robustness", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.PARAMETRIC_SYSTEM
)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
SDI = NodeType(id="SDI", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.PARAMETRIC_SYSTEM)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
Sensitivity = NodeType(
    id="Sensitivity", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.PARAMETRIC_SYSTEM
)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
SIMPLEX = NodeType(
    id="SIMPLEX", subtype=AddinType.BUILT_IN, osl_class_type=NodeClassType.PARAMETRIC_SYSTEM
)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
# endregion
# region Python based algorithm plugins
BASS = NodeType(
    id="BASS",
    subtype=AddinType.PYTHON_BASED_ALGORITHM_PLUGIN,
    osl_class_type=NodeClassType.PARAMETRIC_SYSTEM,
)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
DXAMO = NodeType(
    id="DXAMO",
    subtype=AddinType.PYTHON_BASED_ALGORITHM_PLUGIN,
    osl_class_type=NodeClassType.PARAMETRIC_SYSTEM,
)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
DXASO = NodeType(
    id="DXASO",
    subtype=AddinType.PYTHON_BASED_ALGORITHM_PLUGIN,
    osl_class_type=NodeClassType.PARAMETRIC_SYSTEM,
)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
DXMISQP = NodeType(
    id="DXMISQP",
    subtype=AddinType.PYTHON_BASED_ALGORITHM_PLUGIN,
    osl_class_type=NodeClassType.PARAMETRIC_SYSTEM,
)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
DXUPEGO = NodeType(
    id="DXUPEGO",
    subtype=AddinType.PYTHON_BASED_ALGORITHM_PLUGIN,
    osl_class_type=NodeClassType.PARAMETRIC_SYSTEM,
)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
GLAD = NodeType(
    id="GLAD",
    subtype=AddinType.PYTHON_BASED_ALGORITHM_PLUGIN,
    osl_class_type=NodeClassType.PARAMETRIC_SYSTEM,
)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
OCO = NodeType(
    id="OCO",
    subtype=AddinType.PYTHON_BASED_ALGORITHM_PLUGIN,
    osl_class_type=NodeClassType.PARAMETRIC_SYSTEM,
)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
PIBO = NodeType(
    id="PIBO",
    subtype=AddinType.PYTHON_BASED_ALGORITHM_PLUGIN,
    osl_class_type=NodeClassType.PARAMETRIC_SYSTEM,
)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
Replace_constant_parameter = NodeType(
    id="Replace_constant_parameter",
    subtype=AddinType.PYTHON_BASED_ALGORITHM_PLUGIN,
    osl_class_type=NodeClassType.PARAMETRIC_SYSTEM,
)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
Unigene_EA = NodeType(
    id="Unigene_EA",
    subtype=AddinType.PYTHON_BASED_ALGORITHM_PLUGIN,
    osl_class_type=NodeClassType.PARAMETRIC_SYSTEM,
)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
while_loop = NodeType(
    id="while_loop",
    subtype=AddinType.PYTHON_BASED_ALGORITHM_PLUGIN,
    osl_class_type=NodeClassType.PARAMETRIC_SYSTEM,
)
"""Class :py:class:`~ansys.optislang.core.nodes.ParametricSystem` is created from this node type."""
# endregion
# endregion


def get_node_type_from_str(node_id: str) -> NodeType:
    """Create instance of ``NodeType`` from string.

    Parameters
    ----------
    node_id: str
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
    module_constants = {
        key: value
        for key, value in globals().items()
        if not (callable(value) or isinstance(value, type) or key.startswith("__"))
    }
    module_constants.pop("annotations")

    if module_constants.get(node_id, None) is not None:
        return module_constants[node_id]
    elif node_id in customs.keys():
        id_ = node_id[:-1]
        subtype = AddinType.BUILT_IN
    else:
        was_found = False
        for custom in customs.keys():
            if node_id.startswith(custom):
                id_ = node_id.replace(custom, "")
                subtype = customs[custom]  # type: ignore
                was_found = True
                break
        if not was_found:
            id_ = node_id
            subtype = AddinType.BUILT_IN
    return NodeType(id=id_, subtype=subtype)
