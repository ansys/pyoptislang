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

"""Enum definitions for optiSLang node settings.

Each enum corresponds to a ``{enum: [...], value: ...}`` structure in the
optiSLang JSON properties schema.  The enum members preserve the exact
string values used in the JSON transport layer.
"""

from __future__ import annotations

from enum import Enum


# ---------------------------------------------------------------------------
# region General / shared enums
# ---------------------------------------------------------------------------


class AutoSaveMode(str, Enum):
    """Auto-save trigger mode for node execution."""

    NO_AUTO_SAVE = "no_auto_save"
    AS_ACTOR_FINISHED = "as_actor_finished"
    AS_PSS_NTH_DESIGN_COLLECTED = "as_pss_nth_design_collected"
    AS_ALGO_ITERATION_FINISHED = "as_algo_iteration_finished"


class ReadMode(str, Enum):
    """Read/write mode for node data access."""

    READ_AND_WRITE_MODE = "read_and_write_mode"
    CLASSIC_REEVALUATE_MODE = "classic_reevaluate_mode"


class EnvironmentMode(str, Enum):
    """Strategy for merging environment variables."""

    MERGE = "merge"
    REPLACE = "replace"


class CommandInterpretion(str, Enum):
    """How the command string is interpreted by the process node."""

    SHELL = "shell"
    DIRECT = "direct"


# endregion

# ---------------------------------------------------------------------------
# region Data import / export enums
# ---------------------------------------------------------------------------


class DataFormat(str, Enum):
    """File format for design import/export."""

    CSV = "csv"
    JSON = "json"
    EXCEL = "excel"


class WriteFailureTreatment(str, Enum):
    """Behaviour when a data-export write operation fails."""

    STOP = "stop"
    CONTINUE = "continue"


class ReadFailureTreatment(str, Enum):
    """Behaviour when a data-import read operation fails."""

    STOP = "stop"
    CONTINUE = "continue"


class Comparison(str, Enum):
    """Comparison operator for the Compare node."""

    EQUAL = "equal"
    NOT_EQUAL = "not_equal"
    LESS = "less"
    LESS_EQUAL = "less_equal"
    GREATER = "greater"
    GREATER_EQUAL = "greater_equal"


# endregion

# ---------------------------------------------------------------------------
# region MOP / surrogate enums
# ---------------------------------------------------------------------------


class MopModelComplexity(str, Enum):
    """Complexity level for automatic MOP model selection."""

    MOP_SIMPLE_MODEL = "mop_simple_model"
    MOP_BALANCED_MODEL = "mop_balanced_model"
    MOP_COMPLEX_MODEL = "mop_complex_model"
    MOP_COMPLEX_MODEL_WITH_EXTERNALS = "mop_complex_model_with_externals"
    MOP_POLY_DLN = "mop_poly_dln"
    MOP_MLS = "mop_mls"
    MOP_ISO_KRIGING = "mop_iso_kriging"
    MOP_GARS = "mop_gars"


class MopSettingsType(str, Enum):
    """Which settings block governs MOP training."""

    MOP_AUTOMATIC_SETTINGS = "mop_automatic_settings"
    MOP_ADVANCED_CLASSICAL_SETTINGS = "mop_advanced_classical_settings"
    MOP_ADVANCED_SETTINGS = "mop_advanced_settings"


class MopVariableReduction(str, Enum):
    """Variable-reduction strategy for automatic MOP."""

    MOP_NO_REDUCTION = "mop_no_reduction"
    MOP_FILTER_UNIMPORTANT = "mop_filter_unimportant"
    MOP_FILTER_MINOR_IMPORTANT = "mop_filter_minor_important"
    MOP_USER_DEFINED = "mop_user_defined"


class MopExtrapolationType(str, Enum):
    """Extrapolation behaviour for MOP models."""

    NONE = "none"
    LINEAR = "linear"
    CONSTANT = "constant"


class MopTestingType(str, Enum):
    """Cross-validation strategy for MOP training."""

    CROSSVALIDATION = "crossvalidation"
    LEAVEONEOUT = "leaveoneout"


# endregion

# ---------------------------------------------------------------------------
# region Postprocessing enums
# ---------------------------------------------------------------------------


class MonitoringMode(str, Enum):
    """Monitoring visualisation mode for postprocessing."""

    PP4_AUTOMATIC = "pp4_automatic"
    PP4_STATISTICS = "pp4_statistics"
    PP4_RELI = "pp4_reli"
    PP4_OPT = "pp4_opt"
    PP4_APPROX = "pp4_approx"


class PostprocessingMode(str, Enum):
    """Postprocessing analysis mode."""

    AUTOMATIC = "automatic"
    OPTIMIZATION = "optimization"
    APPROXIMATION = "approximation"
    STATISTICS = "statistics"


# endregion

# ---------------------------------------------------------------------------
# region Wait / variant enums
# ---------------------------------------------------------------------------


class ForcedTimeDefinitionStyle(str, Enum):
    """Time-definition style for the Wait node."""

    UNSPECIFIED = "unspecified"
    ABSOLUTE_TIMEOUT = "absolute_timeout"
    TIME_SINCE_EPOCH = "time_since_epoch"
    USER_INTERACTION = "user_interaction"


class VariantKind(str, Enum):
    """Data-type discriminator for optiSLang variant values."""

    UNINITIALIZED = "uninitialized"
    BOOL = "bool"
    SCALAR = "scalar"
    VECTOR = "vector"
    MATRIX = "matrix"
    SIGNAL = "signal"
    XYDATA = "xydata"


# endregion

# ---------------------------------------------------------------------------
# region Parametric system enums
# ---------------------------------------------------------------------------


class ParameterMergingMode(str, Enum):
    """Strategy for merging parameters from slots and properties."""

    PREFER_PROPERTY = "prefer_property"
    PREFER_SLOT = "prefer_slot"
    MERGE_FROM_SLOT = "merge_from_slot"


class DirectoryCleanupStrategy(str, Enum):
    """Strategy for cleaning up design directories."""

    ALL = "all"
    CUSTOM = "custom"


class UpdateResultFile(str, Enum):
    """When to update the result file during a parametric run."""

    NEVER = "never"
    EVERY_DESIGN = "every_design"
    EVERY_ITERATION = "every_iteration"
    AT_END = "at_end"


class AlgorithmType(str, Enum):
    """Algorithm type selector for NOA2."""

    NOA = "noa"
    ARSM = "arsm"
    NLPQL = "nlpql"
    MEMETIC = "memetic"


# endregion

# ---------------------------------------------------------------------------
# region Sampling enums
# ---------------------------------------------------------------------------


class SamplingType(str, Enum):
    """Sampling method for DOE / sensitivity / robustness."""

    CENTERPOINT = "centerpoint"
    FULLFACTORIAL = "fullfactorial"
    AXIAL = "axial"
    STARPOINTS = "starpoints"
    KOSHAL = "koshal"
    CENTRALCOMPOSITE = "centralcomposite"
    MIXEDTERMS = "mixedterms"
    LATINHYPER = "latinhyper"
    LATINHYPERDETEMINISTIC = "latinhyperdeteministic"
    OPTIMIZEDLATINHYPER = "optimizedlatinhyper"
    ORTHOLATINHYPERDETEMINISTIC = "ortholatinhyperdeteministic"
    SOBOLSEQUENCES = "sobolsequences"
    PLAINMONTECARLO = "plainmontecarlo"
    DOPTIMAL = "doptimal"
    DOPTIMALLINEAR = "doptimallinear"
    DOPTIMALQUADRATIC = "doptimalquadratic"
    DOPTIMALQUADRATICNOMIXED = "doptimalquadraticnomixed"
    KOSHALLINEAR = "koshallinear"
    KOSHALQUADRATIC = "koshalquadratic"
    FEKETE = "fekete"
    BOXBEHNKEN = "boxbehnken"
    FULLCOMBINATORIAL = "fullcombinatorial"
    ADVANCEDLATINHYPER = "advancedlatinhyper"


class NumericalDifferences(str, Enum):
    """Finite-difference scheme for gradient computation."""

    CENTRAL = "central"
    FORWARD = "forward"
    BACKWARD = "backward"
    FOURTH_ORDER = "fourth_order"


# endregion

# ---------------------------------------------------------------------------
# region Reevaluate enums
# ---------------------------------------------------------------------------


class ReevaluateDepParHandling(str, Enum):
    """How dependent parameters are handled during re-evaluation."""

    KEEP = "keep"
    RECALCULATE = "recalculate"


class ReevaluateResultFileType(str, Enum):
    """Result file format for re-evaluation input."""

    CSV = "csv"
    BIN = "bin"
    OMDB = "omdb"


# endregion

# ---------------------------------------------------------------------------
# region Reliability enums
# ---------------------------------------------------------------------------


class ReliabilityFORMType(str, Enum):
    """FORM algorithm variant for reliability analysis."""

    HLRF = "hlrf"
    IHLRF = "ihlrf"


class ReliabilityISPUDType(str, Enum):
    """ISPUD algorithm variant for reliability analysis."""

    ISPUD = "ispud"
    FORM_UNI = "form_uni"


# endregion

# ---------------------------------------------------------------------------
# region Abaqus enums
# ---------------------------------------------------------------------------


class AbaqusAnalysisType(str, Enum):
    """Abaqus analysis type."""

    STANDARD = "standard"
    EXPLICIT = "explicit"


class AbaqusExecutionMode(str, Enum):
    """Abaqus execution mode."""

    INTERACTIVE = "interactive"
    BACKGROUND = "background"


# endregion

# ---------------------------------------------------------------------------
# region Base path mode (used inside PathSetting serialization)
# ---------------------------------------------------------------------------


class BasePathMode(str, Enum):
    """Base-path resolution mode for optiSLang path structures."""

    WORKING_DIR_RELATIVE = "WORKING_DIR_RELATIVE"
    PROJECT_RELATIVE = "PROJECT_RELATIVE"
    PROJECT_WORKING_DIR_RELATIVE = "PROJECT_WORKING_DIR_RELATIVE"
    REFERENCE_FILES_DIR_RELATIVE = "REFERENCE_FILES_DIR_RELATIVE"
    ABSOLUTE_PATH = "ABSOLUTE_PATH"


# endregion
