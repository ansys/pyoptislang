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

# create parametric system for oscillator calibration python example

# in batch:
#      optislang --new oscillator_py.opf --python oscillatorcalibration_system_python.py
#           --no-run --batch

# in optiSlang:
#      open optiSLang and paste the content to optiSLang python console

# find a description of the oscillator calibration example in optiSLang tutorial section
###############################################################################
import os

from py_os_design import PyOSDesignEntry
from pyvariant import VariantD

###############################################################################
# Create ParametricSystem, TextOutput and InPath
###############################################################################
# get example path "OSL_EXAMPLES": .\pyoptislang\src\ansys\optislang\core\examples
os.path.join(
    os.environ["OSL_EXAMPLES"], "00_run_script", "oscillator", "scripts", "_create_oscillator.py"
)
example_path = os.path.join(os.environ["OSL_EXAMPLES"], "00_run_script", "oscillator", "files")
system = actors.ParametricSystemActor("OscillatorCalibration")
add_actor(system)

text_out = actors.ETKTextOutputActor("Text Output")
system.add_actor(text_out)

path_act = actors.PathActor("InPath")
system.add_actor(path_act)

text_path = Path(os.path.join(example_path, "oscillator_reference.txt"))
path_act.path = text_path

connect(text_out, "ODesign", system, "IIDesign")
connect(path_act, "OPath", text_out, "IPath")

###############################################################################
# Create oscillator example @ example_system
###############################################################################
example_system = system
path = os.path.join(
    os.environ["OSL_EXAMPLES"], "00_run_script", "oscillator", "scripts", "_create_oscillator.py"
)
exec(open(path).read())

###############################################################################
# Setup TextOutput
###############################################################################

#### output slot 'time_ref'

# set up repeated marker
# marker - offset: 0, increment: 1, repetitions: 1
regex_repeater_args = actors.ETKTextOutputActor.RepeaterArgs(0, 1, 1)
# set up LineReader with repeater
# line - offset: 2, increment: 1, repetitions: 1
line_repeater_args = actors.ETKTextOutputActor.RepeaterArgs(2, 1, 0)
# set up TokenReader with repeater
# token - offset: 0, increment: 1, repetitions: 1
token_repeater_args = actors.ETKTextOutputActor.RepeaterArgs(0, 1, 1)
# create output variable
etk_var = actors.ETKTextOutputActor.TextOutputVariable(
    text_path,
    "time_ref",
    line_repeater_args,
    token_repeater_args,
    True,
    regex_repeater_args,
    "time",
    "time",
)
# add response 'time_ref'
text_out.add_output(etk_var)


#### output slot 'disp_ref'
# set up repeated marker
regex_repeater_args = actors.ETKTextOutputActor.RepeaterArgs(0, 1, 1)
# set up LineReader with repeater
line_repeater_args = actors.ETKTextOutputActor.RepeaterArgs(2, 1, 0)
# set up TokenReader with repeater
token_repeater_args = actors.ETKTextOutputActor.RepeaterArgs(1, 1, 1)
# create output variable
etk_var = actors.ETKTextOutputActor.TextOutputVariable(
    text_path,
    "disp_ref",
    line_repeater_args,
    token_repeater_args,
    True,
    regex_repeater_args,
    "displacement",
    "displacement",
)
# add response 'disp_ref'
text_out.add_output(etk_var)


###############################################################################
# Setup Python node
###############################################################################
tmp_vec = PyOSDesignEntry(VariantD(list(range(0, 70))))
tmp_val = PyOSDesignEntry(5.0)

# add input slots
py2 = system.find_actor("oscillator.py")
py2.add_input_slot(py2.SlotType.DESIGNENTRY, "time_ref")
py2.add_input_slot(py2.SlotType.DESIGNENTRY, "disp_ref")
connect(text_out, "time_ref", py2, "time_ref")
connect(text_out, "disp_ref", py2, "disp_ref")

# create calculator expressions
disp_time_exp = actors.DerivedLocation("disp_time", "xydata(time, x_values)")
disp_time_ref_exp = actors.DerivedLocation("disp_time_ref", "xydata(time_ref, disp_ref)")
disp_signals_exp = actors.DerivedLocation(
    "disp_signals", "$SIG_DIFF_EUCLID(disp_time, disp_time_ref)"
)
max_disp0_exp = actors.DerivedLocation("max_disp0", "$SIG_MAX_Y(disp_time)")
max_disp2_exp = actors.DerivedLocation("max_disp2", "$SIG_MAX_Y_SLOT(disp_time, 2, 10)")
max_disp4_exp = actors.DerivedLocation("max_disp4", "$SIG_MAX_Y_SLOT(disp_time, 4, 10)")
max_disp6_exp = actors.DerivedLocation("max_disp6", "$SIG_MAX_Y_SLOT(disp_time, 6, 10)")
max_disp8_exp = actors.DerivedLocation("max_disp8", "$SIG_MAX_Y_SLOT(disp_time, 8, 10)")

# add variables
py2.register_as_internal_location("time", "time", tmp_vec)
py2.register_as_internal_location("x_values", "x_values", tmp_vec)
py2.register_as_internal_location(disp_time_exp, "disp_time", tmp_vec)
py2.register_as_internal_location(disp_time_ref_exp, "disp_time_ref", tmp_vec)
py2.register_as_internal_location(disp_signals_exp, "disp_signals", tmp_vec)
py2.register_as_internal_location(max_disp0_exp, "max_disp0", tmp_val)
py2.register_as_internal_location(max_disp2_exp, "max_disp2", tmp_val)
py2.register_as_internal_location(max_disp4_exp, "max_disp4", tmp_val)
py2.register_as_internal_location(max_disp6_exp, "max_disp6", tmp_val)
py2.register_as_internal_location(max_disp8_exp, "max_disp8", tmp_val)

# add them to responses
py2.add_response(("disp_time", PyOSDesignEntry()), disp_time_exp)
py2.add_response(("disp_time_ref", PyOSDesignEntry()), disp_time_ref_exp)
py2.add_response(("disp_signals", PyOSDesignEntry()), disp_signals_exp)
py2.add_response(("max_disp0", PyOSDesignEntry()), max_disp0_exp)
py2.add_response(("max_disp2", PyOSDesignEntry()), max_disp2_exp)
py2.add_response(("max_disp4", PyOSDesignEntry()), max_disp4_exp)
py2.add_response(("max_disp6", PyOSDesignEntry()), max_disp6_exp)
py2.add_response(("max_disp8", PyOSDesignEntry()), max_disp8_exp)
