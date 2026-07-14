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

"""Contains definitions of the TCP settings."""

import numbers

from ansys.optislang.core.nodes import SamplingType
from ansys.optislang.core.settings.types import (
    ChoiceSetting,
    EnumSetting,
    ModelSetting,
    PathSetting,
    SerializationMode,
    SettingModel,
    TypedSetting,
)

from .enums import AutoSaveMode, ReadMode


# region setting models
class SensitivityAlgorithmSettings(SettingModel):
    """Model for sensitivity algorithm settings."""

    num_dimensions: TypedSetting[int] = TypedSetting(
        "num_dimensions", int, 0, doc="Number of dimensions used by the sampling algorithm."
    )
    num_discretization: TypedSetting[int] = TypedSetting(
        "num_discretization",
        int,
        100,
        doc="Number of discretization points used by the sampling algorithm.",
    )
    sampling_method: EnumSetting[SamplingType] = EnumSetting(
        "sampling_method",
        SamplingType,
        SamplingType.ADVANCEDLATINHYPER,
        doc="Sampling method used by the sampling algorithm.",
    )


# endregion


# region settings

AUTO_SAVE_MODE: EnumSetting[AutoSaveMode] = EnumSetting(
    "AutoSaveMode",
    AutoSaveMode,
    default=AutoSaveMode.NO_AUTO_SAVE,
    doc="""Setting for auto-save mode.""",
)
INSTANT_VARIABLE_UPDATE: TypedSetting[bool] = TypedSetting(
    "InstantVariableUpdate", bool, True, doc="""Setting for instant variable update."""
)
MAX_RUNTIME: TypedSetting[numbers.Number] = TypedSetting(
    "MaxRuntime", numbers.Number, -1, doc="""Setting for maximum runtime."""
)
MDB_PATH: PathSetting = PathSetting(
    "MDBPath", export_mode=SerializationMode.PATH_DICT, doc="""Setting for MDB path."""
)
MULTI_DESIGN_LAUNCH_NUM: TypedSetting[int] = TypedSetting(
    "MultiDesignLaunchNum", int, -1, doc="Number of designs to be sent/received in one batch."
)
MULTI_DESIGN_NUM: TypedSetting[int] = TypedSetting(
    "MultiDesignNum", int, -1, doc="Number of designs to be sent/received in one batch."
)

PATH: PathSetting = PathSetting(
    "Path", export_mode=SerializationMode.PATH_DICT, doc="""Setting for general path."""
)
READ_MODE: EnumSetting[ReadMode] = EnumSetting(
    "ReadMode", ReadMode, default=ReadMode.READ_AND_WRITE_MODE, doc="""Setting for read mode."""
)
SHOW_PP_ON_TERMINATION: TypedSetting[bool] = TypedSetting(
    "ShowPPOnTermination",
    bool,
    False,
    doc="""Setting for showing post-processing on termination.""",
)
SENSITIVITY_ALGORITHM_SETTINGS: ModelSetting[SensitivityAlgorithmSettings] = ModelSetting(
    "AlgorithmSettings",
    SensitivityAlgorithmSettings,
    doc="""Setting for sensitivity algorithm settings.""",
)
SOURCE: TypedSetting[str] = TypedSetting("Source", str, r"""""", doc="Python script code.")
STARTING_DELAY: TypedSetting[numbers.Number] = TypedSetting(
    "StartingDelay", numbers.Number, 0.0, doc="""Setting for starting delay."""
)
STOP_AFTER_EXECUTION: TypedSetting[bool] = TypedSetting(
    "StopAfterExecution", bool, False, doc="""Setting for stopping after execution."""
)
UPDATE_RESULT_FILE: ChoiceSetting[str] = ChoiceSetting(
    "UpdateResultFile",
    ["never", "every_design", "every_iteration", "at_end"],
    "never",
    doc="""Setting for updating the result file.""",
)

# endregion
