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

"""Reusable SettingModel definitions and shared primitive setting instances.

This module contains:

- **SettingModel classes** that represent structured JSON sub-objects
  (e.g. ``HeaderSequence``, ``SplitPath``, ``VariantValue``).
- **Shared primitive instances** that are referenced by multiple settings
  classes to avoid duplication.
"""

from __future__ import annotations

from ansys.optislang.core.settings.enums import (
    AutoSaveMode,
    MopTestingType,
    ReadMode,
    SamplingType,
    VariantKind,
)
from ansys.optislang.core.settings.types import (
    EnumSetting,
    ModelSetting,
    PathSetting,
    SettingModel,
    TypedSetting,
)


# ===================================================================
# region SettingModel definitions
# ===================================================================


class SamplingSettings(SettingModel):
    """DOE / sensitivity sampling configuration.

    Represents the ``AlgorithmSettings`` or ``DOESettings`` JSON object
    containing sampling method, discretisation count, and seed.
    """

    num_dimensions: TypedSetting[int] = TypedSetting("num_dimensions", int, 0)
    num_discretization: TypedSetting[int] = TypedSetting("num_discretization", int, 100)
    sampling_method: EnumSetting[SamplingType] = EnumSetting(
        "sampling_method", SamplingType, SamplingType.ADVANCEDLATINHYPER
    )
    seed: TypedSetting[int] = TypedSetting("seed", int, 0)


class HeaderSequence(SettingModel):
    """Generic header + sequence container.

    Represents the ``{header: int, sequence: list}`` JSON structure used
    by ``Settings``, ``Responses``, ``Criteria``, and ``NominalDesignPoint``.
    """

    header: TypedSetting[int] = TypedSetting("header", int, 0)
    sequence: TypedSetting[list] = TypedSetting("sequence", list, [])


class SplitPath(SettingModel):
    """Head/tail path pair without base-path mode.

    Represents the ``{head: str, tail: str}`` JSON structure used by
    ``DataExport.Path`` and ``DataImport.Path``.
    """

    head: TypedSetting[str] = TypedSetting("head", str, "")
    tail: TypedSetting[str] = TypedSetting("tail", str, "")


class ComplexScalar(SettingModel):
    """Complex number with real and imaginary parts.

    Represents ``{imag: float, real: float}`` inside variant values.
    """

    imag: TypedSetting[float] = TypedSetting("imag", float, 0.0)
    real: TypedSetting[float] = TypedSetting("real", float, 0.0)


class VariantValue(SettingModel):
    """Typed variant value with kind discriminator.

    Represents structures like ``Wait.AbsoluteTimeout``::

        {
            "kind": {"enum": [...], "value": "scalar"},
            "scalar": {"imag": 0.0, "real": 0.0}
        }

    The ``kind`` field determines which payload field is active.
    Currently only ``scalar`` is modeled; additional variant payloads
    (``bool``, ``vector``, etc.) can be added when encountered.
    """

    kind: EnumSetting[VariantKind] = EnumSetting("kind", VariantKind, VariantKind.SCALAR)
    scalar: ModelSetting[ComplexScalar] = ModelSetting("scalar", ComplexScalar)


class MopTrainingEntry(SettingModel):
    """Single MOP training configuration entry.

    Represents the ~40-field structure found in ``Mop.Settings[]`` and
    ``AMOP.AMopSettings.mop_settings`` / ``MOPAdvancedSettings.pmop_settings``.
    Fields ``custom_settings``, ``custom_usage``, ``osl_variables``, and
    ``important_info`` are schema-less and left to ``additional_settings``.
    """

    coeff_factor_ascmo: TypedSetting[float] = TypedSetting("coeff_factor_ascmo", float, 8.0)
    coeff_factor_kriging: TypedSetting[float] = TypedSetting("coeff_factor_kriging", float, 8.0)
    coeff_factor_mls: TypedSetting[float] = TypedSetting("coeff_factor_mls", float, 8.0)
    coeff_factor_polynomial: TypedSetting[float] = TypedSetting(
        "coeff_factor_polynomial", float, 2.0
    )
    corr_input_check: TypedSetting[float] = TypedSetting("corr_input_check", float, 0.5)
    limits_first: TypedSetting[str] = TypedSetting("limits_first", str, "-inf")
    limits_second: TypedSetting[str] = TypedSetting("limits_second", str, "inf")
    max_cod: TypedSetting[float] = TypedSetting("max_cod", float, 0.05)
    max_coi: TypedSetting[float] = TypedSetting("max_coi", float, 0.05)
    max_input_corr: TypedSetting[float] = TypedSetting("max_input_corr", float, 0.7)
    max_order_mls: TypedSetting[int] = TypedSetting("max_order_mls", int, 2)
    max_order_polynomial: TypedSetting[int] = TypedSetting("max_order_polynomial", int, 2)
    min_input_corr: TypedSetting[float] = TypedSetting("min_input_corr", float, 0.3)
    min_significance: TypedSetting[float] = TypedSetting("min_significance", float, 0.95)
    num_corr_steps: TypedSetting[int] = TypedSetting("num_corr_steps", int, 10)
    step_cod: TypedSetting[float] = TypedSetting("step_cod", float, 0.01)
    step_coi: TypedSetting[float] = TypedSetting("step_coi", float, 0.01)
    step_significance: TypedSetting[float] = TypedSetting("step_significance", float, 0.01)
    testing_type: EnumSetting[MopTestingType] = EnumSetting(
        "testing_type", MopTestingType, MopTestingType.CROSSVALIDATION
    )
    tolerance_cop_model: TypedSetting[float] = TypedSetting("tolerance_cop_model", float, 0.01)
    tolerance_cop_variables: TypedSetting[float] = TypedSetting(
        "tolerance_cop_variables", float, 0.01
    )
    use_adjusted_cod: TypedSetting[bool] = TypedSetting("use_adjusted_cod", bool, True)
    use_adjusted_cop: TypedSetting[bool] = TypedSetting("use_adjusted_cop", bool, False)
    use_ascmo: TypedSetting[bool] = TypedSetting("use_ascmo", bool, False)
    use_box_cox: TypedSetting[bool] = TypedSetting("use_box_cox", bool, True)
    use_cod_filter: TypedSetting[bool] = TypedSetting("use_cod_filter", bool, True)
    use_coi_filter: TypedSetting[bool] = TypedSetting("use_coi_filter", bool, True)
    use_correlation_filter: TypedSetting[bool] = TypedSetting("use_correlation_filter", bool, True)
    use_input_correlation_filter: TypedSetting[bool] = TypedSetting(
        "use_input_correlation_filter", bool, False
    )
    use_interpolation: TypedSetting[bool] = TypedSetting("use_interpolation", bool, False)
    use_kriging: TypedSetting[bool] = TypedSetting("use_kriging", bool, True)
    use_kriging_anisotropic_kernel: TypedSetting[bool] = TypedSetting(
        "use_kriging_anisotropic_kernel", bool, False
    )
    use_limits: TypedSetting[bool] = TypedSetting("use_limits", bool, False)
    use_mls: TypedSetting[bool] = TypedSetting("use_mls", bool, True)
    use_mls_anisotropic_kernel: TypedSetting[bool] = TypedSetting(
        "use_mls_anisotropic_kernel", bool, False
    )
    use_polynomials: TypedSetting[bool] = TypedSetting("use_polynomials", bool, True)
    use_significance_filter: TypedSetting[bool] = TypedSetting(
        "use_significance_filter", bool, True
    )
    use_spearman: TypedSetting[bool] = TypedSetting("use_spearman", bool, False)
    use_uniform_resample: TypedSetting[bool] = TypedSetting("use_uniform_resample", bool, False)


# endregion

# ===================================================================
# region Shared primitive instances
# ===================================================================

# These are reusable SettingProperty instances referenced by multiple
# settings classes.  Defaults are defined here (Rule 10); DEFAULTS
# dicts on classes are used only for overrides.

AUTO_SAVE_MODE: EnumSetting[AutoSaveMode] = EnumSetting(
    "AutoSaveMode", AutoSaveMode, default=AutoSaveMode.NO_AUTO_SAVE
)
READ_MODE: EnumSetting[ReadMode] = EnumSetting(
    "ReadMode", ReadMode, default=ReadMode.READ_AND_WRITE_MODE
)
MAX_RUNTIME: TypedSetting[int] = TypedSetting("MaxRuntime", int, -1)
STARTING_DELAY: TypedSetting[int] = TypedSetting("StartingDelay", int, 0)
STOP_AFTER_EXECUTION: TypedSetting[bool] = TypedSetting("StopAfterExecution", bool, False)
MDB_PATH: PathSetting = PathSetting("MDBPath", export_mode="dict")
PATH: PathSetting = PathSetting("Path", export_mode="dict")
SHOW_PP_ON_TERMINATION: TypedSetting[bool] = TypedSetting("ShowPPOnTermination", bool, False)
INSTANT_VARIABLE_UPDATE: TypedSetting[bool] = TypedSetting("InstantVariableUpdate", bool, True)

SENSITIVITY_ALGORITHM_SETTINGS: ModelSetting[SamplingSettings] = ModelSetting(
    "AlgorithmSettings", SamplingSettings
)

# endregion
