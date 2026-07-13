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

"""Module for input/output functionality."""

from __future__ import annotations

from enum import Enum


# region enums
class AutoSaveMode(str, Enum):
    """Enum for auto-save mode options."""

    NO_AUTO_SAVE = "no_auto_save"
    AS_ACTOR_FINISHED = "as_actor_finished"
    AS_PSS_NTH_DESIGN_COLLECTED = "as_pss_nth_design_collected"
    AS_ALGO_ITERATION_FINISHED = "as_algo_iteration_finished"


class ReadMode(str, Enum):
    """Enum for read mode options."""

    READ_AND_WRITE_MODE = "read_and_write_mode"
    CLASSIC_REEVALUATE_MODE = "classic_reevaluate_mode"


# endregion
