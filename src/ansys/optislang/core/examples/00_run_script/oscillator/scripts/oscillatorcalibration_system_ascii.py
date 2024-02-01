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
# create parametric system for oscillator calibration ascii example
#
# in batch:
#      optislang --new oscillator_ascii.opf --python oscillatorcalibration_system_ascii.py
#           --no-run --batch
#
# in optiSlang:
#      open optiSLang and paste the content to optiSLang python console
#
# find a description of the oscillator calibration example in optiSLang tutorial section
###############################################################################

###############################################################################
# Import needed modules
###############################################################################
import os

from py_file_access import *
from py_os_design import PyOSDesignEntry
from py_os_parameter import PyParameter
from pyvariant import VariantD
from stdcpp_python_export import WStrList

###############################################################################
# Create System
###############################################################################
system = actors.ParametricSystemActor("OscillatorCalibration")
add_actor(system)

# text-input
# get example path "OSL_EXAMPLES": .\pyoptislang\src\ansys\optislang\core\examples
input_file = os.path.join(
    os.environ["OSL_EXAMPLES"], "00_run_script", "oscillator", "files", "oscillator.s"
)
text_in = actors.TextInputActor("oscillator.s")
text_in.file_path = Path(input_file)
text_in.add_parameter(actors.TextInputActor.Parameter("D", 28, 15, 8))
text_in.add_parameter(actors.TextInputActor.Parameter("Ekin", 29, 18, 9))
text_in.add_parameter(actors.TextInputActor.Parameter("k", 26, 15, 9))
text_in.add_parameter(actors.TextInputActor.Parameter("m", 25, 15, 8))
system.add_actor(text_in)

# solver
solver_file = "oscillator.sh"
solver = actors.BashScriptActor("Solver")
# WINDOWS
if not os.sep == "/":
    solver_file = "oscillator.bat"
if not os.sep == "/":
    solver = actors.BatchScriptActor("Solver")
example_files = os.path.join(os.environ["OSL_EXAMPLES"], "00_run_script", "oscillator", "files")
script_content = open(os.path.join(example_files, solver_file)).read()
env_var = WStrList()
env_var.push_back("INPUT_FILE1=%s" % (os.path.basename(input_file)))
solver.environment = env_var
solver.content = script_content
system.add_actor(solver)

output_file_name = "oscillator_signal.txt"
text_out_sig = actors.ETKTextOutputActor("Signal.txt")
text_out_sig.file = ProvidedPath(SplittedPath(example_files, output_file_name))
system.add_actor(text_out_sig)

# reference-output
reference_file = os.path.join(example_files, "oscillator_reference.txt")
text_out_ref = actors.ETKTextOutputActor("Reference.txt")
text_out_ref.file = ProvidedPath(reference_file)
system.add_actor(text_out_ref)

# calculator
calc = actors.CalculatorSetActor("Calculator")
calc.add_input_slot(calc.SlotType.DESIGNENTRY, "time")
calc.add_input_slot(calc.SlotType.DESIGNENTRY, "disp")
calc.add_input_slot(calc.SlotType.DESIGNENTRY, "time_ref")
calc.add_input_slot(calc.SlotType.DESIGNENTRY, "disp_ref")
system.add_actor(calc)

# connect(path_act_sig,  'OPath',        text_out_sig,   'IPath')
connect(system, "IODesign", text_in, "IDesign")
connect(text_in, "ODesign", solver, "IDesign")
connect(solver, "ODesign", text_out_sig, "IDesign")
connect(text_out_ref, "ODesign", system, "IIDesign")
connect(text_out_sig, "ODesign", calc, "IDesign")
connect(calc, "ODesign", system, "IIDesign")

###############################################################################
# Setup TextOutput - Signal
###############################################################################

#### output slot 'time_ref'
# set up repeated marker
# marker - offset: 0, increment: 1, repetitions: 1
regex_repeater_args = actors.ETKTextOutputActor.RepeaterArgs(0, 1, 1)
# set up LineReader with repeater
# line - offset: 2, increment: 1, repetitions: 0
line_repeater_args = actors.ETKTextOutputActor.RepeaterArgs(2, 1, 0)
# set up TokenReader with repeater
# token - offset: 0, increment: 1, repetitions: 1
token_repeater_args = actors.ETKTextOutputActor.RepeaterArgs(0, 1, 1)
# create output variable
etk_var = actors.ETKTextOutputActor.TextOutputVariable(
    text_out_sig.path,
    "time",
    line_repeater_args,
    token_repeater_args,
    True,
    regex_repeater_args,
    "time",
    "time",
)
# add response 'time_ref'
text_out_sig.add_output(etk_var)


#### output slot 'disp_ref'
# set up repeated marker
# marker - offset: 0, increment: 1, repetitions: 1
regex_repeater_args = actors.ETKTextOutputActor.RepeaterArgs(0, 1, 1)
# set up LineReader with repeater
# line - offset: 2, increment: 1, repetitions: 0
line_repeater_args = actors.ETKTextOutputActor.RepeaterArgs(2, 1, 0)
# set up TokenReader with repeater
# token - offset: 0, increment: 1, repetitions: 1
token_repeater_args = actors.ETKTextOutputActor.RepeaterArgs(1, 1, 1)
# create output variable
etk_var = actors.ETKTextOutputActor.TextOutputVariable(
    text_out_sig.path,
    "disp",
    line_repeater_args,
    token_repeater_args,
    True,
    regex_repeater_args,
    "displacement",
    "displacement",
)
# add response 'time_ref'
text_out_sig.add_output(etk_var)


###############################################################################
# Setup TextOutput - Reference
###############################################################################

#### output slot 'time_ref'
# set up repeated marker
# marker - offset: 0, increment: 1, repetitions: 1
regex_repeater_args = actors.ETKTextOutputActor.RepeaterArgs(0, 1, 1)
# set up LineReader with repeater
# line - offset: 2, increment: 1, repetitions: 0
line_repeater_args = actors.ETKTextOutputActor.RepeaterArgs(2, 1, 0)
# set up TokenReader with repeater
# token - offset: 0, increment: 1, repetitions: 1
token_repeater_args = actors.ETKTextOutputActor.RepeaterArgs(0, 1, 1)
# create output variable
etk_var = actors.ETKTextOutputActor.TextOutputVariable(
    text_out_ref.path,
    "time_ref",
    line_repeater_args,
    token_repeater_args,
    True,
    regex_repeater_args,
    "time",
    "time",
)
# add response 'time_ref'
text_out_ref.add_output(etk_var)


#### output slot 'disp_ref'
# set up repeated marker
# marker - offset: 0, increment: 1, repetitions: 1
regex_repeater_args = actors.ETKTextOutputActor.RepeaterArgs(0, 1, 1)
# set up LineReader with repeater
# line - offset: 2, increment: 1, repetitions: 0
line_repeater_args = actors.ETKTextOutputActor.RepeaterArgs(2, 1, 0)
# set up TokenReader with repeater
# token - offset: 1, increment: 1, repetitions: 1
token_repeater_args = actors.ETKTextOutputActor.RepeaterArgs(1, 1, 1)
# create output variable
etk_var = actors.ETKTextOutputActor.TextOutputVariable(
    text_out_ref.path,
    "disp_ref",
    line_repeater_args,
    token_repeater_args,
    True,
    regex_repeater_args,
    "displacement",
    "displacement",
)
# add response 'time_ref'
text_out_ref.add_output(etk_var)


connect(text_out_sig, "time", calc, "time")
connect(text_out_sig, "disp", calc, "disp")
connect(text_out_ref, "time_ref", calc, "time_ref")
connect(text_out_ref, "disp_ref", calc, "disp_ref")

###############################################################################
# Setup Calculator
###############################################################################
tmp_vec = PyOSDesignEntry(VariantD(list(range(0, 70))))
tmp_val = PyOSDesignEntry(0.0)

# create expressions -name              -expression
calc.add_expression("disp_time", "xydata(time,disp)", True)
calc.add_expression("disp_time_ref", "xydata(time_ref,disp_ref)", True)
calc.add_expression("disp_signals", "$SIG_DIFF_EUCLID(disp_time,disp_time_ref)", True)
calc.add_expression("max_disp0", "$SIG_MAX_Y(disp_time)", True)
calc.add_expression("max_disp2", "$SIG_MAX_Y_SLOT(disp_time,2,10)", True)
calc.add_expression("max_disp4", "$SIG_MAX_Y_SLOT(disp_time,4,10)", True)
calc.add_expression("max_disp6", "$SIG_MAX_Y_SLOT(disp_time,6,10)", True)
calc.add_expression("max_disp8", "$SIG_MAX_Y_SLOT(disp_time,8,10)", True)

# add responses
calc.add_response("disp_time", "xydata(time,disp)", tmp_vec)
calc.add_response("disp_time_ref", "xydata(time_ref,disp_ref)", tmp_vec)
calc.add_response("disp_signals", "$SIG_DIFF_EUCLID(disp_time,disp_time_ref)", tmp_vec)
calc.add_response("max_disp0", "$SIG_MAX_Y(disp_time)", tmp_val)
calc.add_response("max_disp2", "$SIG_MAX_Y_SLOT(disp_time,2,10)", tmp_val)
calc.add_response("max_disp4", "$SIG_MAX_Y_SLOT(disp_time,4,10)", tmp_val)
calc.add_response("max_disp6", "$SIG_MAX_Y_SLOT(disp_time,6,10)", tmp_val)
calc.add_response("max_disp8", "$SIG_MAX_Y_SLOT(disp_time,8,10)", tmp_val)

###############################################################################
# Setup ParameterManager
###############################################################################
params = system.parameter_manager
params.add_parameter("m")
params.add_parameter("k")
params.add_parameter("D")
params.add_parameter("Ekin")
params.set_bounds("m", PyOSDesignEntry(0.1), PyOSDesignEntry(5.0))
params.set_bounds("k", PyOSDesignEntry(10.0), PyOSDesignEntry(50.0))
params.set_bounds("D", PyOSDesignEntry(0.01), PyOSDesignEntry(0.05))
params.set_bounds("Ekin", PyOSDesignEntry(10.0), PyOSDesignEntry(100.0))
params.set_reference_value("m", PyOSDesignEntry(1.0))
params.set_reference_value("k", PyOSDesignEntry(20.0))
params.set_reference_value("D", PyOSDesignEntry(0.02))
params.set_reference_value("Ekin", PyOSDesignEntry(10.0))
system.parameter_manager = params
