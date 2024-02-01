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
#
# (c) 2021 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.
#
# create optimization on mop flow for oscillator python example
#
# Requirements:
#      calculated example oscillator_sensitivity_mop.py in project oscillator_py.opf is needed!
#
# in batch:
#      optislang oscillator_py.opf --python oscillator_optimization_on_mop.py --run --batch
#
# in optiSlang:
#      open optiSLang and use 'run script file...' in optiSlang python console
#
# find a description of the oscillator example in optiSLang tutorial section
###############################################################################

###############################################################################
# Import needed modules
###############################################################################
import os

from py_os_criterion import DesignStatus, PyOSCriterion, PyOSCriterionContainer
from py_osl3binfile import BinfilePath

try:
    test = find_actor("MOP")
except:
    raise Exception("MOP node not found. Run oscillator_sensitivity_mop.py first.")


###############################################################################
# Create NLPQL, MOPSolver and ParametricSystem
###############################################################################
nlpql = actors.NLPQLPActor("NLPQL")
nlpql.auto_save_mode = AS_ACTOR_FINISHED
add_actor(nlpql)

mop_solver = actors.MOPSolverActor("MOP Solver")
nlpql.add_actor(mop_solver)

validator_system = actors.SensitivityActor("Oscillator")
validator_system.dynamic_sampling = False
validator_system.solve_start_designs_again = True
add_actor(validator_system)

post_proc_opt = actors.PostprocessingActor("PostProcessing_Optimization")
add_actor(post_proc_opt)

append_node = actors.DataMiningActor()
add_actor(append_node)
append_node.init_append_best_designs()

mop = find_actor("MOP")
sensi = find_actor("Sensitivity")
connect(mop, "OParameterManager", nlpql, "IParameterManager")
connect(mop, "OMDBPath", mop_solver, "IMDBPath")
connect(nlpql, "IODesign", mop_solver, "IDesign")
connect(mop_solver, "ODesign", nlpql, "IIDesign")
connect(sensi, "OBestDesigns", nlpql, "IStartDesigns")
connect(nlpql, "OCriteria", validator_system, "ICriteria")
connect(nlpql, "OBestDesigns", validator_system, "IStartDesigns")

connect(nlpql, "OMDBPath", append_node, "IMDBPath")
connect(validator_system, "ODesigns", append_node, "IDesigns")

connect(append_node, "OValidatedMDBPath", post_proc_opt, "IMDBPath")

###############################################################################
# Create oscillator example @ example_system
###############################################################################
# get example path "OSL_EXAMPLES": .\pyoptislang\src\ansys\optislang\core\examples
example_system = validator_system
path = os.path.join(
    os.environ["OSL_EXAMPLES"], "00_run_script", "oscillator", "scripts", "_create_oscillator.py"
)
exec(open(path).read())
validator_system = example_system

###############################################################################
# Setup MOPSolver
###############################################################################
mop_solver.mdb_path = BinfilePath("MOP.omdb")
mop_solver.initialize_solver(mop_solver.mdb_path)
mop_solver.register_available_parameters()
mop_solver.register_available_responses()

###############################################################################
# Setup Criteria
###############################################################################
criteria_exprs = PyOSCriterionContainer()
criteria_exprs.add("Objective", PyOSCriterion(DesignStatus.MIN, "x_max"))
criteria_exprs.add("Constraint", PyOSCriterion(DesignStatus.LESSEQUAL, "omega_damped", "8.0"))

nlpql.criteria = criteria_exprs
nlpql.parameter_manager = find_actor("Sensitivity").parameter_manager
nlpql.solve_start_designs_again = True

###############################################################################
# Setup Postprocessing
###############################################################################
post_proc_opt.pp_mode = actors.PP3_AUTOMATIC
post_proc_opt.show_pp_during_run = False
post_proc_opt.show_reduced_pp_when_avaiable = False
post_proc_opt.wait_for_pp_to_finish = True
