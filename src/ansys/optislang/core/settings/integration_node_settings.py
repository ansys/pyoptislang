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

"""INTEGRATION_NODE-category settings classes.

These classes cover the 131 integration node types.  Most (81) use the
standard ETK pattern and are instantiated directly as ``EtkNodeSettings``.
The remaining nodes fall into pattern groups with additional properties.

Pattern groups::

    EtkNodeSettings           -- 81 standard ETK nodes (no leaf class needed)
    EtkFileNodeSettings       -- 16 ETK-file nodes (File path instead of Path)
    ParameterizeNodeSettings  -- 7 parameterize nodes
    ScriptNodeSettings        -- BashScript, BatchScript, PerlScript
    PythonScriptNodeSettings  -- PythonScript (adds python_location)
    ProcessIntegrationNodeSettings -- CatiaProcess, ProEProcess
    MatlabNodeSettings        -- Matlab, Octave
    ExcelNodeSettings         -- Excel (shares SpreadsheetNodeSettings)
    DiscoveryPluginNodeSettings -- discovery_plugin
    AbaqusProcessNodeSettings -- AbaqusProcess
    HpsNodeSettings           -- HPS
    MopsolverNodeSettings     -- Mopsolver
    Python2NodeSettings       -- Python2
    Awb2PluginNodeSettings    -- awb2_plugin
    OptislangNodeSettings     -- optislang_node (snake_case keys)
"""

from __future__ import annotations

from ansys.optislang.core.settings.enums import (
    AbaqusAnalysisType,
    AbaqusExecutionMode,
)
from ansys.optislang.core.settings.node_settings import (
    EnvironmentNodeSettings,
    EtkNodeSettings,
    ProcessBaseSettings,
    SpreadsheetNodeSettings,
)
from ansys.optislang.core.settings.types import (
    PathSetting,
    TypedSetting,
)


# ===================================================================
# region ETK-file pattern (16 nodes)
# ===================================================================


class EtkFileNodeSettings(EnvironmentNodeSettings):
    """ETK nodes that use a ``File`` path instead of the standard ``Path``.

    Used by: ETKAbaqus, ETKAdams, ETKAMESim, ETKAnsys, ETKCetol,
    ETKCFturbo, ETKComplete, ETKEdyson, ETKExtOut, ETKFloEFD,
    ETKLSDYNA, ETKMadymo, ETKMidas, ETKSimPack, ETKTurboOpt,
    ETKAnsysDpf.
    """

    file: PathSetting = PathSetting("File", export_mode="dict")


class EtkAsciiOutputNodeSettings(EtkFileNodeSettings):
    """Settings for ETKAsciiOutput (ETK-file + MaxParallel)."""

    max_parallel: TypedSetting[int] = TypedSetting("MaxParallel", int, 1)


# endregion

# ===================================================================
# region Parameterize pattern (7 nodes)
# ===================================================================


class ParameterizeNodeSettings(EnvironmentNodeSettings):
    """Settings for parameterize-type nodes.

    Used by: Parameterize, AnsysAPDLParameterize, CatiaParameterize,
    LSDynaParameterize, MultiplasParameterize, ProEParameterize,
    TaggedParametersParameterize.
    """

    file_path: PathSetting = PathSetting("FilePath", export_mode="dict")
    content_encoding: TypedSetting[str] = TypedSetting("ContentEncoding", str, "")
    file_content: TypedSetting[str] = TypedSetting("FileContent", str, "")
    max_parallel: TypedSetting[int] = TypedSetting("MaxParallel", int, 1)
    store_content: TypedSetting[bool] = TypedSetting("StoreContent", bool, True)


# endregion

# ===================================================================
# region Script pattern (BashScript, BatchScript, PerlScript)
# ===================================================================


class ScriptNodeSettings(ProcessBaseSettings):
    """Settings for script-based integration nodes.

    Inherits ``ProcessBaseSettings`` (consolidated process base) and
    adds script-specific properties.

    Used by: BashScript, BatchScript, PerlScript.
    """

    script_path: PathSetting = PathSetting("ScriptPath", export_mode="dict")
    content: TypedSetting[str] = TypedSetting("Content", str, "")


class PythonScriptNodeSettings(ScriptNodeSettings):
    """Settings for the PythonScript integration node."""

    python_location: TypedSetting[str] = TypedSetting("PythonLocation", str, "")


# endregion

# ===================================================================
# region Process-no-script (CatiaProcess, ProEProcess)
# ===================================================================


class ProcessIntegrationNodeSettings(ProcessBaseSettings):
    """Settings for process-based integration nodes without a script.

    Used by: CatiaProcess, ProEProcess.
    """

    pass


# endregion

# ===================================================================
# region Matlab / Octave
# ===================================================================


class MatlabNodeSettings(EnvironmentNodeSettings):
    """Settings for Matlab and Octave integration nodes."""

    file_path: PathSetting = PathSetting("FilePath", export_mode="dict")
    auto_detect_force_real: TypedSetting[bool] = TypedSetting("AutoDetectForceReal", bool, False)
    batch_mode_user_args: TypedSetting[str] = TypedSetting("BatchModeUserArgs", str, "")
    batch_mode_args: TypedSetting[list] = TypedSetting("BatchModeArgs", list, [])
    free_on_finished: TypedSetting[bool] = TypedSetting("FreeOnFinished", bool, True)
    max_parallel: TypedSetting[int] = TypedSetting("MaxParallel", int, 1)
    pre_command: TypedSetting[str] = TypedSetting("PreCommand", str, "")
    save: TypedSetting[bool] = TypedSetting("Save", bool, False)
    save_inputs: TypedSetting[bool] = TypedSetting("SaveInputs", bool, False)
    save_outputs: TypedSetting[bool] = TypedSetting("SaveOutputs", bool, False)
    startup_timeout: TypedSetting[int] = TypedSetting("StartupTimeout", int, 120)
    use_batch_mode: TypedSetting[bool] = TypedSetting("UseBatchMode", bool, False)
    version: TypedSetting[str] = TypedSetting("Version", str, "")
    write_output_logfile: TypedSetting[bool] = TypedSetting("WriteOutputLogfile", bool, False)


# endregion

# ===================================================================
# region Excel
# ===================================================================


class ExcelNodeSettings(SpreadsheetNodeSettings):
    """Settings for the Excel integration node.

    Inherits ``SpreadsheetNodeSettings`` (shared with OOCalc).
    """

    pass


# endregion

# ===================================================================
# region Discovery plugin
# ===================================================================


class DiscoveryPluginNodeSettings(EnvironmentNodeSettings):
    """Settings for the discovery_plugin integration node."""

    file_path: PathSetting = PathSetting("FilePath", export_mode="dict")
    max_parallel: TypedSetting[int] = TypedSetting("MaxParallel", int, 1)


# endregion

# ===================================================================
# region Abaqus
# ===================================================================


class AbaqusProcessNodeSettings(EnvironmentNodeSettings):
    """Settings for the AbaqusProcess integration node."""

    file_path: PathSetting = PathSetting("FilePath", export_mode="dict")
    analysis_type: TypedSetting[str] = TypedSetting("AnalysisType", str, "standard")
    cpus: TypedSetting[int] = TypedSetting("Cpus", int, 1)
    execution_mode: TypedSetting[str] = TypedSetting("ExecutionMode", str, "interactive")
    job_name: TypedSetting[str] = TypedSetting("JobName", str, "")
    max_parallel: TypedSetting[int] = TypedSetting("MaxParallel", int, 1)
    scratch_dir: TypedSetting[str] = TypedSetting("ScratchDir", str, "")


# endregion

# ===================================================================
# region HPS
# ===================================================================


class HpsNodeSettings(EnvironmentNodeSettings):
    """Settings for the HPS integration node."""

    max_parallel: TypedSetting[int] = TypedSetting("MaxParallel", int, 1)


# endregion

# ===================================================================
# region Mopsolver
# ===================================================================


class MopsolverNodeSettings(EnvironmentNodeSettings):
    """Settings for the Mopsolver integration node."""

    max_parallel: TypedSetting[int] = TypedSetting("MaxParallel", int, 1)


# endregion

# ===================================================================
# region Python2
# ===================================================================


class Python2NodeSettings(EnvironmentNodeSettings):
    """Settings for the Python2 integration node."""

    file_path: PathSetting = PathSetting("FilePath", export_mode="dict")
    max_parallel: TypedSetting[int] = TypedSetting("MaxParallel", int, 1)


# endregion

# ===================================================================
# region awb2_plugin
# ===================================================================


class Awb2PluginNodeSettings(EnvironmentNodeSettings):
    """Settings for the awb2_plugin integration node."""

    file_path: PathSetting = PathSetting("FilePath", export_mode="dict")
    max_parallel: TypedSetting[int] = TypedSetting("MaxParallel", int, 1)


# endregion

# ===================================================================
# region optislang_node (snake_case property names)
# ===================================================================


class OptislangNodeSettings(EnvironmentNodeSettings):
    """Settings for the optislang_node integration plugin.

    Note: This node uses lowercase snake_case property names in JSON,
    unlike all other nodes.  The ``TypedSetting`` names preserve the
    exact JSON keys.
    """

    file_path: PathSetting = PathSetting("file_path", export_mode="dict")
    max_parallel: TypedSetting[int] = TypedSetting("max_parallel", int, 1)


# endregion

# ===================================================================
# region Proxy solver
# ===================================================================


class ProxySolverSettings(EnvironmentNodeSettings):
    """Settings for the ProxySolver node."""

    multi_design_launch_num: TypedSetting[int] = TypedSetting("MultiDesignLaunchNum", int, 1)


# endregion
