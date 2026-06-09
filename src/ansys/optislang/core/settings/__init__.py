# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Settings package containing available node settings.

Public API
----------

Enums
    All enum types used in settings (``AutoSaveMode``, ``ReadMode``, etc.)

Descriptor framework
    ``TypedSetting``, ``EnumSetting``, ``PathSetting``, ``ModelSetting``,
    ``SettingModel``, ``ChoiceSetting``, ``SettingProperty``

SettingModels (reusable sub-objects)
    ``SamplingSettings``, ``HeaderSequence``, ``SplitPath``,
    ``ComplexScalar``, ``VariantValue``, ``MopTrainingEntry``

Base classes
    ``GeneralNodeSettings``, ``CommonNodeSettings``,
    ``EnvironmentNodeSettings``, ``EtkNodeSettings``,
    ``ProcessBaseSettings``

NODE settings
    One class per node type (e.g. ``ProcessNodeSettings``,
    ``WaitNodeSettings``, ``MopNodeSettings``, etc.)

INTEGRATION_NODE settings
    Pattern-group classes (e.g. ``ScriptNodeSettings``,
    ``MatlabNodeSettings``, ``ExcelNodeSettings``, etc.)

SYSTEM / PARAMETRIC_SYSTEM settings
    ``WhileSystemSettings``, ``ParametricSystemSettings``,
    ``SensitivitySettings``, ``ARSMSettings``, etc.
"""

# --- Enums ---
from ansys.optislang.core.settings.enums import (  # noqa: F401
    AbaqusAnalysisType,
    AbaqusExecutionMode,
    AlgorithmType,
    AutoSaveMode,
    BasePathMode,
    CommandInterpretion,
    Comparison,
    DataFormat,
    DirectoryCleanupStrategy,
    EnvironmentMode,
    ForcedTimeDefinitionStyle,
    MonitoringMode,
    MopExtrapolationType,
    MopModelComplexity,
    MopSettingsType,
    MopTestingType,
    MopVariableReduction,
    NumericalDifferences,
    ParameterMergingMode,
    PostprocessingMode,
    ReadFailureTreatment,
    ReadMode,
    ReevaluateDepParHandling,
    ReevaluateResultFileType,
    ReliabilityFORMType,
    ReliabilityISPUDType,
    SamplingType,
    UpdateResultFile,
    VariantKind,
    WriteFailureTreatment,
)

# --- Descriptor framework ---
from ansys.optislang.core.settings.types import (  # noqa: F401
    ChoiceSetting,
    EnumSetting,
    ModelSetting,
    PathSetting,
    SettingModel,
    SettingProperty,
    TypedSetting,
)

# --- SettingModels ---
from ansys.optislang.core.settings.primitives import (  # noqa: F401
    ComplexScalar,
    HeaderSequence,
    MopTrainingEntry,
    SamplingSettings,
    SplitPath,
    VariantValue,
)

# --- Base classes ---
from ansys.optislang.core.settings.node_settings import (  # noqa: F401
    CommonNodeSettings,
    EnvironmentNodeSettings,
    EtkNodeSettings,
    GeneralNodeSettings,
    ProcessBaseSettings,
)

# --- NODE settings ---
from ansys.optislang.core.settings.node_settings import (  # noqa: F401
    AmesimInputNodeSettings,
    AppendDesignsToBinFileNodeSettings,
    ASCMOsolverNodeSettings,
    CalculatorNodeSettings,
    CFturboInputNodeSettings,
    CetolInputNodeSettings,
    CompareNodeSettings,
    CustomMopNodeSettings,
    CustomNodeSettings,
    DataExportNodeSettings,
    DataImportNodeSettings,
    DesignExportNodeSettings,
    DesignImportNodeSettings,
    DpsNodeSettings,
    MopInputNodeSettings,
    MopNodeSettings,
    OOCalcNodeSettings,
    PathNodeSettings,
    PMOPPostprocessingNodeSettings,
    PMopNodeSettings,
    PMopsolverNodeSettings,
    PostprocessingNodeSettings,
    ProcessNodeSettings,
    SimulationXNodeSettings,
    SolverTemplateNodeSettings,
    SoSGenerateNodeSettings,
    SoSPostprocessingNodeSettings,
    SpreadsheetNodeSettings,
    StringNodeSettings,
    VariableNodeSettings,
    VariantMonitoringNodeSettings,
    VCollabProcessNodeSettings,
    WaitNodeSettings,
)

# --- INTEGRATION_NODE settings ---
from ansys.optislang.core.settings.integration_node_settings import (  # noqa: F401
    AbaqusProcessNodeSettings,
    Awb2PluginNodeSettings,
    DiscoveryPluginNodeSettings,
    EtkAsciiOutputNodeSettings,
    EtkFileNodeSettings,
    ExcelNodeSettings,
    HpsNodeSettings,
    MatlabNodeSettings,
    MopsolverNodeSettings,
    OptislangNodeSettings,
    ParameterizeNodeSettings,
    ProcessIntegrationNodeSettings,
    ProxySolverSettings,
    Python2NodeSettings,
    PythonScriptNodeSettings,
    ScriptNodeSettings,
)

# --- SYSTEM / PARAMETRIC_SYSTEM settings ---
from ansys.optislang.core.settings.system_settings import (  # noqa: F401
    AlgorithmNodeSettings,
    AlgorithmSystemPluginSettings,
    AMOPSettings,
    ARSMSettings,
    BASSSettings,
    CustomAlgorithmSettings,
    DLSSettings,
    DXAMOSettings,
    DXASOSettings,
    DXMISQPSettings,
    DXUPEGOSettings,
    EASettings,
    GLADSettings,
    MemeticSettings,
    NLPQLPSettings,
    NOA2Settings,
    OCOSettings,
    ParametricServiceSettings,
    ParametricSystemSettings,
    PIBOSettings,
    PSOSettings,
    ReevaluateSettings,
    ReliabilityARSMSettings,
    ReliabilityASSettings,
    ReliabilityBaseSettings,
    ReliabilityDSSettings,
    ReliabilityFORMSettings,
    ReliabilityISPUDSettings,
    ReliabilityMCSettings,
    ReplaceConstantParameterSettings,
    RobustnessSettings,
    RootSystemSettings,
    SamplingAlgorithmSettings,
    SDISettings,
    SensitivitySettings,
    SIMPLEXSettings,
    UnigeneEASettings,
    WhileLoopSettings,
    WhileSystemSettings,
)
