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

    num_dimensions: TypedSetting[int] = TypedSetting("num_dimensions", int, 0)
    num_discretization: TypedSetting[int] = TypedSetting("num_discretization", int, 100)
    sampling_method: EnumSetting[SamplingType] = EnumSetting(
        "sampling_method", SamplingType, SamplingType.ADVANCEDLATINHYPER
    )


# endregion


# region settings

AUTO_SAVE_MODE: EnumSetting[AutoSaveMode] = EnumSetting(
    "AutoSaveMode",
    AutoSaveMode,
    default=AutoSaveMode.NO_AUTO_SAVE,
)
INSTANT_VARIABLE_UPDATE = TypedSetting("InstantVariableUpdate", bool, True)
MAX_RUNTIME: TypedSetting[numbers.Number] = TypedSetting("MaxRuntime", numbers.Number, -1)
MDB_PATH: PathSetting = PathSetting("MDBPath", export_mode=SerializationMode.PATH_DICT)
PATH: PathSetting = PathSetting("Path", export_mode=SerializationMode.PATH_DICT)
READ_MODE: EnumSetting[ReadMode] = EnumSetting(
    "ReadMode", ReadMode, default=ReadMode.READ_AND_WRITE_MODE
)
SHOW_PP_ON_TERMINATION = TypedSetting("ShowPPOnTermination", bool, False)
SENSITIVITY_ALGORITHM_SETTINGS: ModelSetting[SensitivityAlgorithmSettings] = ModelSetting(
    "AlgorithmSettings", SensitivityAlgorithmSettings
)
STARTING_DELAY: TypedSetting[numbers.Number] = TypedSetting("StartingDelay", numbers.Number, 0.0)
STOP_AFTER_EXECUTION: TypedSetting[bool] = TypedSetting("StopAfterExecution", bool, False)
UPDATE_RESULT_FILE: ChoiceSetting[str] = ChoiceSetting(
    "UpdateResultFile", ["never", "every_design", "every_iteration", "at_end"], "never"
)

# endregion
