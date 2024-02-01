# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
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

"""Create workflow."""
###############################################################################
# (c) 2021 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.

# create direct optimization using evolutionary algorithm flow for oscillator python example

# in batch:
#      optislang --new oscillator_py.opf --python oscillator_optimization_ea.py --run --batch

# in optiSlang:
#      open optiSLang and use 'run script file...' in optiSlang python console

# find a description of the oscillator example in optiSLang tutorial section
###############################################################################

###############################################################################
# Import needed modules
###############################################################################
import os

import PyNOA
from py_os_criterion import DesignStatus, PyOSCriterion, PyOSCriterionContainer

###############################################################################
# Create EA and PostProcessing
###############################################################################
EA = actors.EAActor("Evolutionary Algorithm")
EA.auto_save_mode = AS_ACTOR_FINISHED
add_actor(EA)

post_proc = actors.PostprocessingActor("PostProcessing")
add_actor(post_proc)

connect(EA, "OMDBPath", post_proc, "IMDBPath")

###############################################################################
# Create oscillator example @ example_system
###############################################################################
# get example path "OSL_EXAMPLES": .\pyoptislang\src\ansys\optislang\core\examples
example_system = EA
path = os.path.join(
    os.environ["OSL_EXAMPLES"], "00_run_script", "oscillator", "scripts", "_create_oscillator.py"
)
exec(open(path).read())
EA = example_system

###############################################################################
# Setup EA
###############################################################################
settings = EA.optimizer_settings
settings.set_start_pop_size(20)
settings.set_number_of_parents(10)
EA.optimizer_settings = settings

###############################################################################
# Setup Criteria
###############################################################################
criteria_exprs = PyOSCriterionContainer()
criteria_exprs.add("Objective", PyOSCriterion(DesignStatus.MIN, "x_max"))
criteria_exprs.add("Constraint", PyOSCriterion(DesignStatus.LESSEQUAL, "omega_damped", "8.0"))
EA.criteria = criteria_exprs

###############################################################################
# Setup Postprocessing
###############################################################################
post_proc.pp_mode = actors.PP3_AUTOMATIC
post_proc.show_pp_during_run = False
post_proc.show_reduced_pp_when_avaiable = False
post_proc.wait_for_pp_to_finish = True
post_proc.force_classic = False
