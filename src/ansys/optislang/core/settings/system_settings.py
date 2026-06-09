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

"""SYSTEM and PARAMETRIC_SYSTEM category settings classes.

Class hierarchy::

    CommonNodeSettings
      +-- WhileSystemSettings                    (SYSTEM)
      +-- ParametricSystemSettings               (PARAMETRIC_SYSTEM base)
            +-- RootSystemSettings               (ROOT_SYSTEM)
            +-- AlgorithmNodeSettings            (algorithm nodes)
            |     +-- NOA2Settings
            +-- SamplingAlgorithmSettings        (sampling nodes)
            |     +-- SensitivitySettings
            |     +-- RobustnessSettings
            |     +-- ReevaluateSettings
            |     +-- ParametricServiceSettings
            +-- ARSMSettings
            +-- AMOPSettings
            +-- ReliabilityBaseSettings
                  +-- ReliabilityFORMSettings
                  +-- ReliabilityISPUDSettings
"""

from __future__ import annotations

from typing import Any, Optional

from ansys.optislang.core.settings.enums import (
    AlgorithmType,
    AutoSaveMode,
    DirectoryCleanupStrategy,
    MopSettingsType,
    ParameterMergingMode,
    ReevaluateDepParHandling,
    ReevaluateResultFileType,
    ReliabilityFORMType,
    ReliabilityISPUDType,
    UpdateResultFile,
)
from ansys.optislang.core.settings.primitives import (
    HeaderSequence,
    SamplingSettings,
)
from ansys.optislang.core.settings.node_settings import CommonNodeSettings
from ansys.optislang.core.settings.types import (
    EnumSetting,
    ModelSetting,
    TypedSetting,
)


# ===================================================================
# region SYSTEM
# ===================================================================


class WhileSystemSettings(CommonNodeSettings):
    """Settings for the While system node.

    Note: ``condition`` and ``manual_max_parallel`` are ``bool`` in the
    JSON schema (values ``false``), not ``str`` or ``int``.
    """

    condition: TypedSetting[bool] = TypedSetting("Condition", bool, False)
    manual_max_parallel: TypedSetting[bool] = TypedSetting("ManualMaxParallel", bool, False)
    max_parallel: TypedSetting[int] = TypedSetting("MaxParallel", int, 1)


# endregion

# ===================================================================
# region PARAMETRIC_SYSTEM base
# ===================================================================


class ParametricSystemSettings(CommonNodeSettings):
    """Base settings for all parametric system nodes.

    Contains the ~30 properties shared across all 34 parametric system
    types (AMOP, ARSM, EA, Sensitivity, Robustness, etc.).
    """

    # --- Design directory management ---
    at_end_cleanup_design_directory_if_failed: TypedSetting[bool] = TypedSetting(
        "AtEndCleanupDesignDirectoryIfFailed", bool, False
    )
    at_end_cleanup_design_directory_if_succeeded: TypedSetting[bool] = TypedSetting(
        "AtEndCleanupDesignDirectoryIfSucceeded", bool, False
    )
    at_end_design_dir_cleanup_failed_filter: TypedSetting[Optional[Any]] = TypedSetting(
        "AtEndDesignDirCleanupFailedFilter", object, None
    )
    at_end_design_dir_cleanup_strategy_failed: EnumSetting[DirectoryCleanupStrategy] = EnumSetting(
        "AtEndDesignDirCleanupStrategyFailed",
        DirectoryCleanupStrategy,
        DirectoryCleanupStrategy.ALL,
    )
    at_end_design_dir_cleanup_strategy_succeeded: EnumSetting[
        DirectoryCleanupStrategy
    ] = EnumSetting(
        "AtEndDesignDirCleanupStrategySucceeded",
        DirectoryCleanupStrategy,
        DirectoryCleanupStrategy.ALL,
    )
    at_end_design_dir_cleanup_succeeded_filter: TypedSetting[Optional[Any]] = TypedSetting(
        "AtEndDesignDirCleanupSucceededFilter", object, None
    )
    at_end_remove_design_directory_if_empty: TypedSetting[bool] = TypedSetting(
        "AtEndRemoveDesignDirectoryIfEmpty", bool, True
    )
    at_start_remove_design_directory: TypedSetting[bool] = TypedSetting(
        "AtStartRemoveDesignDirectory", bool, False
    )
    design_directory_format_override: TypedSetting[str] = TypedSetting(
        "DesignDirectoryFormatOverride", str, ""
    )
    use_design_directory_format_override: TypedSetting[bool] = TypedSetting(
        "UseDesignDirectoryFormatOverride", bool, False
    )
    use_working_directory_override: TypedSetting[bool] = TypedSetting(
        "UseWorkingDirectoryOverride", bool, False
    )
    working_directory_override: TypedSetting[str] = TypedSetting(
        "WorkingDirectoryOverride", str, ""
    )

    # --- Criteria / parameters ---
    criteria: ModelSetting[HeaderSequence] = ModelSetting("Criteria", HeaderSequence)
    criteria_import_file: TypedSetting[str] = TypedSetting("CriteriaImportFile", str, "")
    current_predefined_setting: TypedSetting[str] = TypedSetting(
        "CurrentPredefinedSetting", str, "User Defined"
    )
    design_point_tolerance: TypedSetting[float] = TypedSetting(
        "DesignPointTolerance", float, 2.220446049250313e-13
    )
    parameter_manager: TypedSetting[dict] = TypedSetting("ParameterManager", dict, {})
    parameter_merging_mode: EnumSetting[ParameterMergingMode] = EnumSetting(
        "ParameterMergingMode", ParameterMergingMode, ParameterMergingMode.PREFER_PROPERTY
    )
    parametric_import_file: TypedSetting[str] = TypedSetting("ParametricImportFile", str, "")
    prefer_criteria_from_slot: TypedSetting[bool] = TypedSetting(
        "PreferCriteriaFromSlot", bool, False
    )

    # --- Execution ---
    manual_max_parallel: TypedSetting[bool] = TypedSetting("ManualMaxParallel", bool, False)
    manual_seed_value: TypedSetting[int] = TypedSetting("ManualSeedValue", int, 0)
    max_parallel: TypedSetting[int] = TypedSetting("MaxParallel", int, 1)
    use_manual_seed: TypedSetting[bool] = TypedSetting("UseManualSeed", bool, False)

    # --- File registration ---
    register_avz_files: TypedSetting[bool] = TypedSetting("RegisterAVZFiles", bool, False)
    register_cax_files: TypedSetting[bool] = TypedSetting("RegisterCAXFiles", bool, False)
    register_custom_files: TypedSetting[bool] = TypedSetting("RegisterCustomFiles", bool, False)
    register_images: TypedSetting[bool] = TypedSetting("RegisterImages", bool, False)
    registered_file_filter: TypedSetting[Optional[Any]] = TypedSetting(
        "RegisteredFileFilter", object, None
    )

    # --- Solve behaviour ---
    solve_reference_design_point: TypedSetting[bool] = TypedSetting(
        "SolveReferenceDesignPoint", bool, False
    )
    solve_start_designs_again: TypedSetting[bool] = TypedSetting(
        "SolveStartDesignsAgain", bool, False
    )
    solve_twice: TypedSetting[bool] = TypedSetting("SolveTwice", bool, False)
    solve_violated: TypedSetting[bool] = TypedSetting("SolveViolated", bool, True)
    start_designs: TypedSetting[list] = TypedSetting("StartDesigns", list, [])

    # --- Postprocessing ---
    show_pp_on_termination: TypedSetting[bool] = TypedSetting("ShowPPOnTermination", bool, False)
    show_pp_when_available: TypedSetting[bool] = TypedSetting("ShowPPWhenAvailable", bool, False)

    # --- Result file ---
    update_result_file: EnumSetting[UpdateResultFile] = EnumSetting(
        "UpdateResultFile", UpdateResultFile, UpdateResultFile.EVERY_ITERATION
    )
    write_osl3_bin_file_default: TypedSetting[bool] = TypedSetting(
        "WriteOSL3BinFileDefault", bool, False
    )

    # --- Auto-save override (PS default differs from NODE default) ---
    DEFAULTS = {
        "auto_save_mode": AutoSaveMode.AS_PSS_NTH_DESIGN_COLLECTED,
    }


class RootSystemSettings(ParametricSystemSettings):
    """Settings for the root system (all_nodes)."""

    pass


# endregion

# ===================================================================
# region Algorithm nodes (consolidated base)
# ===================================================================


class AlgorithmNodeSettings(ParametricSystemSettings):
    """Base for algorithm-based parametric systems.

    Covers: BASS, DLS, DXAMO, DXASO, DXMISQP, DXUPEGO, GLAD, OCO,
    PIBO, Replace_constant_parameter, Unigene_EA, while_loop,
    CustomAlgorithm, AlgorithmSystemPlugin, EA, Memetic, NLPQLP,
    PSO, SDI, SIMPLEX.

    Algorithm-specific ``Settings`` and ``OptimizerSettings`` are left
    as opaque payloads in ``additional_settings``.
    """

    algo_log_file_path: TypedSetting[str] = TypedSetting(
        "AlgoLogFilePath", str, "message_log.txt"
    )
    minimum_designs_to_show_pp: TypedSetting[int] = TypedSetting(
        "MinimumDesignsToShowPP", int, 1
    )
    show_algo_messages_in_project_log: TypedSetting[bool] = TypedSetting(
        "ShowAlgoMessagesInProjectLog", bool, False
    )
    write_algo_log_file: TypedSetting[bool] = TypedSetting("WriteAlgoLogFile", bool, True)


class NOA2Settings(AlgorithmNodeSettings):
    """Settings for the NOA2 parametric system."""

    algorithm_type: EnumSetting[AlgorithmType] = EnumSetting(
        "AlgorithmType", AlgorithmType, AlgorithmType.NOA
    )


# --- Thin leaf classes for specific algorithm nodes ---


class BASSSettings(AlgorithmNodeSettings):
    """Settings for the BASS parametric system."""

    pass


class DLSSettings(AlgorithmNodeSettings):
    """Settings for the DLS parametric system."""

    pass


class DXAMOSettings(AlgorithmNodeSettings):
    """Settings for the DXAMO parametric system."""

    pass


class DXASOSettings(AlgorithmNodeSettings):
    """Settings for the DXASO parametric system."""

    pass


class DXMISQPSettings(AlgorithmNodeSettings):
    """Settings for the DXMISQP parametric system."""

    pass


class DXUPEGOSettings(AlgorithmNodeSettings):
    """Settings for the DXUPEGO parametric system."""

    pass


class EASettings(AlgorithmNodeSettings):
    """Settings for the EA (Evolutionary Algorithm) parametric system."""

    pass


class GLADSettings(AlgorithmNodeSettings):
    """Settings for the GLAD parametric system."""

    pass


class MemeticSettings(AlgorithmNodeSettings):
    """Settings for the Memetic parametric system."""

    pass


class NLPQLPSettings(AlgorithmNodeSettings):
    """Settings for the NLPQLP parametric system."""

    pass


class PSOSettings(AlgorithmNodeSettings):
    """Settings for the PSO (Particle Swarm Optimization) parametric system."""

    pass


class SDISettings(AlgorithmNodeSettings):
    """Settings for the SDI parametric system."""

    pass


class SIMPLEXSettings(AlgorithmNodeSettings):
    """Settings for the SIMPLEX parametric system."""

    pass


class CustomAlgorithmSettings(AlgorithmNodeSettings):
    """Settings for the CustomAlgorithm parametric system."""

    pass


class AlgorithmSystemPluginSettings(AlgorithmNodeSettings):
    """Settings for the AlgorithmSystemPlugin parametric system."""

    pass


class OCOSettings(AlgorithmNodeSettings):
    """Settings for the OCO parametric system."""

    pass


class PIBOSettings(AlgorithmNodeSettings):
    """Settings for the PIBO parametric system."""

    pass


class ReplaceConstantParameterSettings(AlgorithmNodeSettings):
    """Settings for the Replace_constant_parameter parametric system."""

    pass


class UnigeneEASettings(AlgorithmNodeSettings):
    """Settings for the Unigene_EA parametric system."""

    pass


class WhileLoopSettings(AlgorithmNodeSettings):
    """Settings for the while_loop parametric system."""

    pass


# endregion

# ===================================================================
# region Sampling algorithms (consolidated base)
# ===================================================================


class SamplingAlgorithmSettings(ParametricSystemSettings):
    """Consolidated base for sampling-based parametric systems.

    Covers: Sensitivity, Robustness, Reevaluate, ParametricService.
    Eliminates duplication of 9 shared properties.
    """

    algo_log_file_path: TypedSetting[str] = TypedSetting(
        "AlgoLogFilePath", str, "message_log.txt"
    )
    algorithm_settings: ModelSetting[SamplingSettings] = ModelSetting(
        "AlgorithmSettings", SamplingSettings
    )
    dynamic_sampling_desired: TypedSetting[bool] = TypedSetting(
        "DynamicSamplingDesired", bool, True
    )
    minimum_designs_to_show_pp: TypedSetting[int] = TypedSetting(
        "MinimumDesignsToShowPP", int, 1
    )
    preserve_start_design_hids: TypedSetting[bool] = TypedSetting(
        "PreserveStartDesignHIDs", bool, False
    )
    save_design_points: TypedSetting[bool] = TypedSetting("SaveDesignPoints", bool, True)
    show_algo_messages_in_project_log: TypedSetting[bool] = TypedSetting(
        "ShowAlgoMessagesInProjectLog", bool, False
    )
    write_algo_log_file: TypedSetting[bool] = TypedSetting("WriteAlgoLogFile", bool, True)
    write_design_start_set_flag: TypedSetting[bool] = TypedSetting(
        "WriteDesignStartSetFlag", bool, False
    )


class SensitivitySettings(SamplingAlgorithmSettings):
    """Settings for the Sensitivity parametric system."""

    pass


class RobustnessSettings(SamplingAlgorithmSettings):
    """Settings for the Robustness parametric system."""

    solve_nominal_design_point: TypedSetting[bool] = TypedSetting(
        "SolveNominalDesignPoint", bool, False
    )


class ReevaluateSettings(SamplingAlgorithmSettings):
    """Settings for the Reevaluate parametric system."""

    reevaluate_adapt_bounds: TypedSetting[bool] = TypedSetting(
        "ReevaluateAdaptBounds", bool, False
    )
    reevaluate_dep_par_handling: EnumSetting[ReevaluateDepParHandling] = EnumSetting(
        "ReevaluateDepParHandling",
        ReevaluateDepParHandling,
        ReevaluateDepParHandling.KEEP,
    )
    reevaluate_design_dir_format: TypedSetting[str] = TypedSetting(
        "ReevaluateDesignDirFormat", str, ""
    )
    reevaluate_design_dir_path: TypedSetting[str] = TypedSetting(
        "ReevaluateDesignDirPath", str, ""
    )
    reevaluate_input_file_path: TypedSetting[str] = TypedSetting(
        "ReevaluateInputFilePath", str, ""
    )
    reevaluate_merge_input_data: TypedSetting[bool] = TypedSetting(
        "ReevaluateMergeInputData", bool, False
    )
    reevaluate_merge_output_data: TypedSetting[bool] = TypedSetting(
        "ReevaluateMergeOutputData", bool, False
    )
    reevaluate_result_file_type: EnumSetting[ReevaluateResultFileType] = EnumSetting(
        "ReevaluateResultFileType",
        ReevaluateResultFileType,
        ReevaluateResultFileType.CSV,
    )
    reevaluate_use_input_file: TypedSetting[bool] = TypedSetting(
        "ReevaluateUseInputFile", bool, False
    )
    reevaluate_design_numbers: TypedSetting[list] = TypedSetting(
        "ReevaluateDesignNumbers", list, []
    )


class ParametricServiceSettings(SamplingAlgorithmSettings):
    """Settings for the ParametricService parametric system.

    Thin leaf that only overrides defaults from the sampling base.
    """

    DEFAULTS = {
        "dynamic_sampling_desired": False,
        "save_design_points": False,
    }


# endregion

# ===================================================================
# region ARSM
# ===================================================================


class ARSMSettings(ParametricSystemSettings):
    """Settings for the ARSM parametric system.

    Has its own DOE settings and nested optimizer settings (opaque).
    """

    algo_log_file_path: TypedSetting[str] = TypedSetting(
        "AlgoLogFilePath", str, "message_log.txt"
    )
    doe_settings: ModelSetting[SamplingSettings] = ModelSetting("DOESettings", SamplingSettings)
    minimum_designs_to_show_pp: TypedSetting[int] = TypedSetting(
        "MinimumDesignsToShowPP", int, 1
    )
    show_algo_messages_in_project_log: TypedSetting[bool] = TypedSetting(
        "ShowAlgoMessagesInProjectLog", bool, False
    )
    write_algo_log_file: TypedSetting[bool] = TypedSetting("WriteAlgoLogFile", bool, True)


# endregion

# ===================================================================
# region AMOP
# ===================================================================


class AMOPSettings(ParametricSystemSettings):
    """Settings for the AMOP parametric system.

    Algorithm-specific settings (AMopSettings, MOPAdvancedSettings,
    MOPAutomaticSettings) are left as opaque payloads.
    """

    algo_log_file_path: TypedSetting[str] = TypedSetting(
        "AlgoLogFilePath", str, "message_log.txt"
    )
    minimum_designs_to_show_pp: TypedSetting[int] = TypedSetting(
        "MinimumDesignsToShowPP", int, 1
    )
    settings_type: EnumSetting[MopSettingsType] = EnumSetting(
        "SettingsType", MopSettingsType, MopSettingsType.MOP_AUTOMATIC_SETTINGS
    )
    show_algo_messages_in_project_log: TypedSetting[bool] = TypedSetting(
        "ShowAlgoMessagesInProjectLog", bool, False
    )
    write_algo_log_file: TypedSetting[bool] = TypedSetting("WriteAlgoLogFile", bool, True)


# endregion

# ===================================================================
# region Reliability (consolidated base)
# ===================================================================


class ReliabilityBaseSettings(ParametricSystemSettings):
    """Consolidated base for reliability analysis parametric systems.

    Covers: ReliabilityARSM, ReliabilityAS, ReliabilityDS,
    ReliabilityFORM, ReliabilityISPUD, ReliabilityMC.
    """

    algo_log_file_path: TypedSetting[str] = TypedSetting(
        "AlgoLogFilePath", str, "message_log.txt"
    )
    minimum_designs_to_show_pp: TypedSetting[int] = TypedSetting(
        "MinimumDesignsToShowPP", int, 1
    )
    show_algo_messages_in_project_log: TypedSetting[bool] = TypedSetting(
        "ShowAlgoMessagesInProjectLog", bool, False
    )
    solve_nominal_design_point: TypedSetting[bool] = TypedSetting(
        "SolveNominalDesignPoint", bool, False
    )
    write_algo_log_file: TypedSetting[bool] = TypedSetting("WriteAlgoLogFile", bool, True)


class ReliabilityFORMSettings(ReliabilityBaseSettings):
    """Settings for the ReliabilityFORM parametric system."""

    reliability_form_type: EnumSetting[ReliabilityFORMType] = EnumSetting(
        "ReliabilityFORMType", ReliabilityFORMType, ReliabilityFORMType.HLRF
    )


class ReliabilityISPUDSettings(ReliabilityBaseSettings):
    """Settings for the ReliabilityISPUD parametric system."""

    reliability_ispud_type: EnumSetting[ReliabilityISPUDType] = EnumSetting(
        "ReliabilityISPUDType", ReliabilityISPUDType, ReliabilityISPUDType.ISPUD
    )


class ReliabilityARSMSettings(ReliabilityBaseSettings):
    """Settings for the ReliabilityARSM parametric system."""

    pass


class ReliabilityASSettings(ReliabilityBaseSettings):
    """Settings for the ReliabilityAS parametric system."""

    pass


class ReliabilityDSSettings(ReliabilityBaseSettings):
    """Settings for the ReliabilityDS parametric system."""

    pass


class ReliabilityMCSettings(ReliabilityBaseSettings):
    """Settings for the ReliabilityMC parametric system."""

    pass


# endregion
