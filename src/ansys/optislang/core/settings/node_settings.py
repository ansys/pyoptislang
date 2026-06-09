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

"""Base settings class hierarchy and NODE-category leaf classes.

Class hierarchy::

    GeneralNodeSettings
      +-- CommonNodeSettings
            +-- EnvironmentNodeSettings
                  +-- EtkNodeSettings
                  +-- ProcessBaseSettings

Each leaf class corresponds to a specific node type from the
``properties.json`` schema under the ``NODE`` category.
"""

from __future__ import annotations

from typing import Any, Optional

from ansys.optislang.core.settings.enums import (
    AutoSaveMode,
    CommandInterpretion,
    Comparison,
    DataFormat,
    EnvironmentMode,
    ForcedTimeDefinitionStyle,
    MopModelComplexity,
    MopSettingsType,
    MopVariableReduction,
    MonitoringMode,
    PostprocessingMode,
    ReadFailureTreatment,
    ReadMode,
    WriteFailureTreatment,
)
from ansys.optislang.core.settings.primitives import (
    HeaderSequence,
    SplitPath,
    VariantValue,
)
from ansys.optislang.core.settings.types import (
    EnumSetting,
    ModelSetting,
    PathSetting,
    SettingModel,
    TypedSetting,
)


# ===================================================================
# region Base class chain
# ===================================================================


class GeneralNodeSettings(SettingModel):
    """Minimal settings shared by every optiSLang node.

    Contains the 5 properties present on every single node type across
    all categories (NODE, SYSTEM, PARAMETRIC_SYSTEM, INTEGRATION_NODE).

    The descriptor system on ``SettingModel`` ensures that each property
    is validated on assignment and serialized via ``to_dict()``.
    """

    auto_save_mode: EnumSetting[AutoSaveMode] = EnumSetting(
        "AutoSaveMode", AutoSaveMode, AutoSaveMode.NO_AUTO_SAVE
    )
    max_runtime: TypedSetting[int] = TypedSetting("MaxRuntime", int, -1)
    read_mode: EnumSetting[ReadMode] = EnumSetting(
        "ReadMode", ReadMode, ReadMode.READ_AND_WRITE_MODE
    )
    starting_delay: TypedSetting[int] = TypedSetting("StartingDelay", int, 0)
    stop_after_execution: TypedSetting[bool] = TypedSetting("StopAfterExecution", bool, False)


class CommonNodeSettings(GeneralNodeSettings):
    """Extended base adding the 10 properties shared by all NODE-category nodes.

    Inherits the 5 from ``GeneralNodeSettings`` and adds execution,
    retry, and remote-profile settings.
    """

    allow_space_in_file_path: TypedSetting[bool] = TypedSetting(
        "AllowSpaceInFilePath", bool, False
    )
    auto_save_on_nth_design_collected: TypedSetting[int] = TypedSetting(
        "AutoSaveOnNTHDesignCollected", int, 1
    )
    delay_before_execution: TypedSetting[int] = TypedSetting("DelayBeforeExecution", int, 0)
    enable_remote_substitution: TypedSetting[bool] = TypedSetting(
        "EnableRemoteSubstitution", bool, False
    )
    execution_options: TypedSetting[int] = TypedSetting("ExecutionOptions", int, 1)
    forward_hpc_license_context_environment: TypedSetting[bool] = TypedSetting(
        "ForwardHPCLicenseContextEnvironment", bool, False
    )
    remote_profile_id: TypedSetting[str] = TypedSetting("RemoteProfileID", str, "")
    retry_count: TypedSetting[int] = TypedSetting("RetryCount", int, 0)
    retry_delay: TypedSetting[int] = TypedSetting("RetryDelay", int, 0)
    retry_enable: TypedSetting[bool] = TypedSetting("RetryEnable", bool, False)


class EnvironmentNodeSettings(CommonNodeSettings):
    """Adds environment and execution-policy properties.

    Used by nodes that support custom environment variables,
    distinct working directories, and execution policies.
    """

    distinct_working_directory: TypedSetting[bool] = TypedSetting(
        "DistinctWorkingDirectory", bool, False
    )
    environment: TypedSetting[list] = TypedSetting("Environment", list, [])
    environment_mode: EnumSetting[EnvironmentMode] = EnumSetting(
        "EnvironmentMode", EnvironmentMode, EnvironmentMode.MERGE
    )
    error_code: TypedSetting[int] = TypedSetting("ErrorCode", int, 0)
    execution_policy: TypedSetting[Optional[Any]] = TypedSetting("ExecutionPolicy", object, None)
    instant_variable_update: TypedSetting[bool] = TypedSetting("InstantVariableUpdate", bool, True)
    visible_pages_override: TypedSetting[int] = TypedSetting("VisiblePagesOverride", int, -1)


class EtkNodeSettings(EnvironmentNodeSettings):
    """ETK-pattern node settings.

    Adds properties for ETK-based solver integrations that communicate
    via the optiSLang ETK interface (ModifyingSettings, Settings, etc.).
    """

    max_parallel: TypedSetting[int] = TypedSetting("MaxParallel", int, 1)
    multi_design_launch_num: TypedSetting[int] = TypedSetting("MultiDesignLaunchNum", int, 1)
    modifying_settings: TypedSetting[dict] = TypedSetting("ModifyingSettings", dict, {})
    non_modifying_settings: TypedSetting[dict] = TypedSetting("NonModifyingSettings", dict, {})
    settings: ModelSetting[HeaderSequence] = ModelSetting("Settings", HeaderSequence)
    usage: TypedSetting[list] = TypedSetting("Usage", list, [])


class ProcessBaseSettings(EnvironmentNodeSettings):
    """Consolidated base for process-like nodes.

    Shared by ``Process``, ``SolverTemplate``, ``VCollabProcess`` (NODE),
    and ``ScriptNode``, ``ProcessIntegration`` (INTEGRATION_NODE).
    Eliminates duplication of 14+ identical properties.
    """

    arguments: TypedSetting[list] = TypedSetting("Arguments", list, [])
    command: TypedSetting[str] = TypedSetting("Command", str, "")
    command_interpretion: EnumSetting[CommandInterpretion] = EnumSetting(
        "CommandInterpretion", CommandInterpretion, CommandInterpretion.SHELL
    )
    enable_multi_design_launch: TypedSetting[bool] = TypedSetting(
        "EnableMultiDesignLaunch", bool, False
    )
    ignore_exit_code: TypedSetting[bool] = TypedSetting("IgnoreExitCode", bool, False)
    ignore_global_dop: TypedSetting[bool] = TypedSetting("IgnoreGlobalDOP", bool, False)
    input_files: TypedSetting[list] = TypedSetting("InputFiles", list, [])
    max_parallel: TypedSetting[int] = TypedSetting("MaxParallel", int, 1)
    multi_design_launch_num: TypedSetting[int] = TypedSetting("MultiDesignLaunchNum", int, 1)
    output_files: TypedSetting[list] = TypedSetting("OutputFiles", list, [])
    polling_interval: TypedSetting[int] = TypedSetting("PollingInterval", int, 30)
    prepend_project_bin_to_path: TypedSetting[bool] = TypedSetting(
        "PrependProjectBinToPATH", bool, False
    )
    reconnect_timeout: TypedSetting[int] = TypedSetting("ReconnectTimeout", int, 240)
    remove_remote_design_dir: TypedSetting[bool] = TypedSetting(
        "RemoveRemoteDesignDir", bool, False
    )
    shared_remote_folder: TypedSetting[str] = TypedSetting("SharedRemoteFolder", str, "")
    use_shared_location: TypedSetting[bool] = TypedSetting("UseSharedLocation", bool, False)
    working_dir: TypedSetting[str] = TypedSetting("WorkingDir", str, "")


# endregion

# ===================================================================
# region NODE — no-env, no-ETK (inherit CommonNodeSettings)
# ===================================================================


class AppendDesignsToBinFileNodeSettings(CommonNodeSettings):
    """Settings for the AppendDesignsToBinFile node."""

    pass


class CompareNodeSettings(CommonNodeSettings):
    """Settings for the Compare node."""

    comparison: EnumSetting[Comparison] = EnumSetting(
        "Comparison", Comparison, Comparison.EQUAL
    )


class DataExportNodeSettings(CommonNodeSettings):
    """Settings for the DataExport node."""

    failure_treatment: EnumSetting[WriteFailureTreatment] = EnumSetting(
        "FailureTreatment", WriteFailureTreatment, WriteFailureTreatment.STOP
    )
    path: ModelSetting[SplitPath] = ModelSetting("Path", SplitPath)


class DataImportNodeSettings(CommonNodeSettings):
    """Settings for the DataImport node."""

    failure_treatment: EnumSetting[ReadFailureTreatment] = EnumSetting(
        "FailureTreatment", ReadFailureTreatment, ReadFailureTreatment.STOP
    )
    path: ModelSetting[SplitPath] = ModelSetting("Path", SplitPath)


class DesignExportNodeSettings(CommonNodeSettings):
    """Settings for the DesignExport node."""

    mdb_path: PathSetting = PathSetting("MDBPath", export_mode="dict")
    out_path: PathSetting = PathSetting("OutPath", export_mode="dict")
    export_format: EnumSetting[DataFormat] = EnumSetting(
        "ExportFormat", DataFormat, DataFormat.CSV
    )
    csv_delimiter: TypedSetting[str] = TypedSetting("CSVDelimiter", str, ",")
    json_legacy_mode: TypedSetting[bool] = TypedSetting("JSONLegacyMode", bool, False)
    json_prettified_mode: TypedSetting[bool] = TypedSetting("JSONPrettifiedMode", bool, False)
    json_signal_data: TypedSetting[bool] = TypedSetting("JSONSignalData", bool, False)


class DesignImportNodeSettings(CommonNodeSettings):
    """Settings for the DesignImport node."""

    in_path: PathSetting = PathSetting("InPath", export_mode="dict")
    settings_file_path: PathSetting = PathSetting("SettingsFilePath", export_mode="dict")
    import_format: EnumSetting[DataFormat] = EnumSetting(
        "ImportFormat", DataFormat, DataFormat.CSV
    )
    sheet_name: TypedSetting[str] = TypedSetting("SheetName", str, "")
    import_settings: TypedSetting[bool] = TypedSetting("ImportSettings", bool, False)
    import_settings_file: TypedSetting[bool] = TypedSetting("ImportSettingsFile", bool, False)
    dimension_settings: TypedSetting[list] = TypedSetting("DimensionSettings", list, [])


class StringNodeSettings(CommonNodeSettings):
    """Settings for the String node."""

    string: TypedSetting[str] = TypedSetting("String", str, "")


class VariableNodeSettings(CommonNodeSettings):
    """Settings for the Variable node.

    ``variant`` is truly untyped (can be null, scalar, string, etc.).
    """

    variant: TypedSetting[Optional[Any]] = TypedSetting("Variant", object, None)


class VariantMonitoringNodeSettings(CommonNodeSettings):
    """Settings for the VariantMonitoring node."""

    pass


class PMOPPostprocessingNodeSettings(CommonNodeSettings):
    """Settings for the PMOPPostprocessing node."""

    pass


# endregion

# ===================================================================
# region NODE — EnvironmentNodeSettings subclasses
# ===================================================================


class ASCMOsolverNodeSettings(EnvironmentNodeSettings):
    """Settings for the ASCMOsolver node."""

    pass


class PMopsolverNodeSettings(EnvironmentNodeSettings):
    """Settings for the PMopsolver node."""

    pass


class CalculatorNodeSettings(EnvironmentNodeSettings):
    """Settings for the Calculator node."""

    expression: TypedSetting[str] = TypedSetting("Expression", str, "")


class DpsNodeSettings(EnvironmentNodeSettings):
    """Settings for the DPS (Design Point Service) node."""

    config: TypedSetting[int] = TypedSetting("Config", int, 0)
    max_submission_batch_size: TypedSetting[int] = TypedSetting("MaxSubmissionBatchSize", int, 1)
    project: TypedSetting[str] = TypedSetting("Project", str, "")
    url: TypedSetting[str] = TypedSetting("Url", str, "")
    user: TypedSetting[str] = TypedSetting("User", str, "")
    refresh_token: TypedSetting[str] = TypedSetting("RefreshToken", str, "")
    output_files_to_fetch: TypedSetting[list] = TypedSetting("OutputFilesToFetch", list, [])


class WaitNodeSettings(CommonNodeSettings):
    """Settings for the Wait node.

    ``AbsoluteTimeout`` and ``TimeSinceEpoch`` are modeled as
    ``VariantValue`` SettingModels containing a kind discriminator
    and a complex scalar payload.
    """

    error_code: TypedSetting[int] = TypedSetting("ErrorCode", int, 0)
    forced_time_definition_style: EnumSetting[ForcedTimeDefinitionStyle] = EnumSetting(
        "ForcedTimeDefinitionStyle",
        ForcedTimeDefinitionStyle,
        ForcedTimeDefinitionStyle.UNSPECIFIED,
    )
    instruction_text: TypedSetting[str] = TypedSetting("InstructionText", str, "")
    absolute_timeout: ModelSetting[VariantValue] = ModelSetting("AbsoluteTimeout", VariantValue)
    time_since_epoch: ModelSetting[VariantValue] = ModelSetting("TimeSinceEpoch", VariantValue)


# endregion

# ===================================================================
# region NODE — ETK-pattern (EtkNodeSettings subclasses)
# ===================================================================


class AmesimInputNodeSettings(EtkNodeSettings):
    """Settings for the AmesimInput node."""

    pass


class CFturboInputNodeSettings(EtkNodeSettings):
    """Settings for the CFturboInput node."""

    pass


class CetolInputNodeSettings(EtkNodeSettings):
    """Settings for the CetolInput node."""

    pass


class CustomNodeSettings(EtkNodeSettings):
    """Settings for the Custom node."""

    pass


class CustomMopNodeSettings(EtkNodeSettings):
    """Settings for the CustomMop node."""

    responses: ModelSetting[HeaderSequence] = ModelSetting("Responses", HeaderSequence)


class MopInputNodeSettings(EtkNodeSettings):
    """Settings for the MopInput node (ModifyingSettings is opaque)."""

    pass


class PathNodeSettings(EtkNodeSettings):
    """Settings for the Path node (ETK variant with path property)."""

    pass


class SoSGenerateNodeSettings(EtkNodeSettings):
    """Settings for the SoSGenerate node."""

    pass


# endregion

# ===================================================================
# region NODE — MOP training
# ===================================================================


class MopNodeSettings(EnvironmentNodeSettings):
    """Settings for the Mop (MOP training) node."""

    mdb_path: PathSetting = PathSetting("MDBPath", export_mode="dict")
    max_parallel: TypedSetting[int] = TypedSetting("MaxParallel", int, 1)
    multi_design_launch_num: TypedSetting[int] = TypedSetting("MultiDesignLaunchNum", int, 1)
    model_complexity: EnumSetting[MopModelComplexity] = EnumSetting(
        "ModelComplexity", MopModelComplexity, MopModelComplexity.MOP_BALANCED_MODEL
    )
    settings_type: EnumSetting[MopSettingsType] = EnumSetting(
        "SettingsType", MopSettingsType, MopSettingsType.MOP_AUTOMATIC_SETTINGS
    )
    variable_reduction: EnumSetting[MopVariableReduction] = EnumSetting(
        "VariableReduction", MopVariableReduction, MopVariableReduction.MOP_FILTER_MINOR_IMPORTANT
    )
    adapt_bounds_safety_factor: TypedSetting[float] = TypedSetting(
        "AdaptBoundsSafetyFactor", float, 0.0
    )
    adapt_bounds_to_sampling: TypedSetting[bool] = TypedSetting(
        "AdaptBoundsToSampling", bool, True
    )
    cv_value_suffix: TypedSetting[str] = TypedSetting("CVValueSuffix", str, "_cv")
    export_fmu: TypedSetting[bool] = TypedSetting("ExportFMU", bool, False)
    num_responses_parallel: TypedSetting[int] = TypedSetting("NumResponsesParallel", int, 4)
    show_algo_messages_in_project_log: TypedSetting[bool] = TypedSetting(
        "ShowAlgoMessagesInProjectLog", bool, False
    )
    show_pp_when_available: TypedSetting[bool] = TypedSetting("ShowPPWhenAvailable", bool, False)
    use_incomplete_designs: TypedSetting[bool] = TypedSetting("UseIncompleteDesigns", bool, True)
    write_algo_log_file: TypedSetting[bool] = TypedSetting("WriteAlgoLogFile", bool, False)
    write_cv_values_to_omdb: TypedSetting[bool] = TypedSetting(
        "WriteCVValuesToOMDB", bool, False
    )
    write_function_string: TypedSetting[bool] = TypedSetting("WriteFunctionString", bool, False)
    responses: ModelSetting[HeaderSequence] = ModelSetting("Responses", HeaderSequence)
    parameter_manager: TypedSetting[dict] = TypedSetting("ParameterManager", dict, {})
    mop_settings: TypedSetting[list] = TypedSetting("Settings", list, [])


class PMopNodeSettings(EnvironmentNodeSettings):
    """Settings for the PMop node."""

    mdb_path: PathSetting = PathSetting("MDBPath", export_mode="dict")
    adapt_bounds_safety_factor: TypedSetting[float] = TypedSetting(
        "AdaptBoundsSafetyFactor", float, 0.0
    )
    adapt_bounds_to_sampling: TypedSetting[bool] = TypedSetting(
        "AdaptBoundsToSampling", bool, True
    )
    export_fmu: TypedSetting[bool] = TypedSetting("ExportFMU", bool, False)
    show_algo_messages_in_project_log: TypedSetting[bool] = TypedSetting(
        "ShowAlgoMessagesInProjectLog", bool, False
    )
    show_pp_when_available: TypedSetting[bool] = TypedSetting("ShowPPWhenAvailable", bool, False)
    use_incomplete_designs: TypedSetting[bool] = TypedSetting("UseIncompleteDesigns", bool, True)
    write_algo_log_file: TypedSetting[bool] = TypedSetting("WriteAlgoLogFile", bool, False)
    responses: ModelSetting[HeaderSequence] = ModelSetting("Responses", HeaderSequence)
    parameter_manager: TypedSetting[dict] = TypedSetting("ParameterManager", dict, {})


# endregion

# ===================================================================
# region NODE — Postprocessing
# ===================================================================


class PostprocessingNodeSettings(CommonNodeSettings):
    """Settings for the Postprocessing and SoSPostprocessing nodes."""

    mdb_path: PathSetting = PathSetting("MDBPath", export_mode="dict")
    template_path: PathSetting = PathSetting("TemplatePath", export_mode="dict")
    text_import_settings_path: PathSetting = PathSetting(
        "TextImportSettingsPath", export_mode="dict"
    )
    custom_command_script: PathSetting = PathSetting("CustomCommandScript", export_mode="dict")
    monitoring_mode: EnumSetting[MonitoringMode] = EnumSetting(
        "MonitoringMode", MonitoringMode, MonitoringMode.PP4_AUTOMATIC
    )
    postprocessing_mode: EnumSetting[PostprocessingMode] = EnumSetting(
        "PostprocessingMode", PostprocessingMode, PostprocessingMode.AUTOMATIC
    )
    force_classic_postprocessing: TypedSetting[bool] = TypedSetting(
        "ForceClassicPostprocessing", bool, False
    )
    show_post_processing_during_run: TypedSetting[bool] = TypedSetting(
        "ShowPostProcessingDuringRun", bool, False
    )
    show_reduced_pp_when_available: TypedSetting[bool] = TypedSetting(
        "ShowReducedPPWhenAvailable", bool, True
    )
    text_import_non_interactive: TypedSetting[bool] = TypedSetting(
        "TextImportNonInteractive", bool, False
    )
    use_custom_command_script: TypedSetting[bool] = TypedSetting(
        "UseCustomCommandScript", bool, False
    )
    use_template: TypedSetting[bool] = TypedSetting("UseTemplate", bool, False)
    wait_for_postprocessing_to_finish: TypedSetting[bool] = TypedSetting(
        "WaitForPostprocessingToFinish", bool, False
    )


class SoSPostprocessingNodeSettings(PostprocessingNodeSettings):
    """Settings for the SoSPostprocessing node (identical to Postprocessing)."""

    pass


# endregion

# ===================================================================
# region NODE — Process family (ProcessBaseSettings subclasses)
# ===================================================================


class ProcessNodeSettings(ProcessBaseSettings):
    """Settings for the Process node."""

    pass


class SolverTemplateNodeSettings(ProcessBaseSettings):
    """Settings for the SolverTemplate node."""

    script_path: PathSetting = PathSetting("ScriptPath", export_mode="dict")
    command_template: TypedSetting[str] = TypedSetting("CommandTemplate", str, "")
    command_template_type: TypedSetting[str] = TypedSetting("CommandTemplateType", str, "")
    content: TypedSetting[str] = TypedSetting("Content", str, "")
    update_command_template: TypedSetting[bool] = TypedSetting(
        "UpdateCommandTemplate", bool, False
    )


class VCollabProcessNodeSettings(ProcessBaseSettings):
    """Settings for the VCollabProcess node."""

    pass


# endregion

# ===================================================================
# region NODE — Spreadsheet (OOCalc / Excel shared base)
# ===================================================================


class SpreadsheetNodeSettings(EnvironmentNodeSettings):
    """Shared base for spreadsheet-based nodes (OOCalc, Excel).

    Consolidates identical properties from OOCalc (NODE) and
    Excel (INTEGRATION_NODE) per Rule 14.
    """

    file_path: PathSetting = PathSetting("FilePath", export_mode="dict")
    auto_calculate: TypedSetting[bool] = TypedSetting("AutoCalculate", bool, True)
    close_after_run: TypedSetting[bool] = TypedSetting("CloseAfterRun", bool, True)
    run_macros_in_design_dir: TypedSetting[bool] = TypedSetting(
        "RunMacrosInDesignDir", bool, False
    )
    save: TypedSetting[bool] = TypedSetting("Save", bool, False)
    show_spreadsheet_tool: TypedSetting[bool] = TypedSetting("ShowSpreadsheetTool", bool, False)
    execute_macros: TypedSetting[list] = TypedSetting("ExecuteMacros", list, [])


class OOCalcNodeSettings(SpreadsheetNodeSettings):
    """Settings for the OOCalc node."""

    pass


# endregion

# ===================================================================
# region NODE — SimulationX
# ===================================================================


class SimulationXNodeSettings(EnvironmentNodeSettings):
    """Settings for the SimulationX node."""

    file_path: PathSetting = PathSetting("FilePath", export_mode="dict")
    pre_command: TypedSetting[str] = TypedSetting("PreCommand", str, "clear all;")
    save: TypedSetting[bool] = TypedSetting("Save", bool, False)
    version: TypedSetting[str] = TypedSetting("Version", str, "")
    write_output_logfile: TypedSetting[bool] = TypedSetting("WriteOutputLogfile", bool, False)


# endregion
