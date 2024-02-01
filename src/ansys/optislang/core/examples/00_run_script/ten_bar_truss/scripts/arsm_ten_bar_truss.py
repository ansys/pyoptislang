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

# create ARSM ten_bar_truss flow in batch
# optislang --new ten_bar_arsm.opf --python arsm_ten_bar_truss.py --no-run --batch
# start optiSLang
# optislang ten_bar_arsm.opf

# or open optiSLang, choose "Run script file" from Python console's context menu
# and browse for this file

# find a description of the ten bar truss example in optiSLang tutorial section
###############################################################################

# define and add a new ARSM node
arsm = actors.ARSMActor("ARSM")
add_actor(arsm)

# define 10 cross sectional area to be input parameter with
# * range [0.1,20]
# * reference value = 10
# add them to the new parameter manager
# set this parameter manager at ARSM node
from py_os_parameter import *

params = PyParameterManager()
for i in range(1, 11):
    params.add_deterministic_continuous_parameter("area%02d" % i, 0.1, 20, 10, 0)
arsm.parameter_manager = params

# use installed example
import os

# get example path .\pyoptislang\src\ansys\optislang\core\examples
example_path = os.path.join(os.environ["OSL_EXAMPLES"], "00_run_script", "ten_bar_truss", "files")

### TextInput ###
# create a new TextInput node
infile = actors.TextInputActor("infile")
# add the node to ARSM System
arsm.add_actor(infile)
# set path of reference input file
infile.file_path = Path(os.path.join(example_path, r"ten_bar_truss.s"))
# import the content
infile.set_content()
# define location of the 10 input parameter
for i in range(0, 10):
    infile.add_parameter(actors.TextInputActor.Parameter("area%02d" % (i + 1), 24 + i, 20, 8))
# connect to get design from ARSM
connect(arsm, "IODesign", infile, "IDesign")

### Process ###
# create a new Process node
process = actors.ProcessActor("process")
# add the node to ARSM system
arsm.add_actor(process)
# process needs no distinct working directory
process.distinct_working_directory = False
# define command and arguments
slang_executable = os.environ["OPTISLANG_HOME"] + "/slang/bin/slang"
process.command = slang_executable
argv = WStrList()
argv.push_back("-b")
argv.push_back("ten_bar_truss.s")
process.arguments = argv
# set maximum number of parallel runs
process.max_parallel = 4

# define the list of input files
in_file_map = actors.ProcessActor.InputFilesList()
in_file_map.push_back(
    actors.ProcessActor.InputFileMapping(Path("ten_bar_truss.s"), "ten_bar_truss.s")
)
process.input_files = in_file_map
# connect TextInput path to process
connect(infile, "OPath", process, "ten_bar_truss.s")
connect(infile, "ODesign", process, "IDesign")

# define the list of output files
out_file_map = actors.ProcessActor.OutputFilesList()
out_file_map.push_back(
    actors.ProcessActor.OutputFileMapping(Path("ten_bar_truss.out"), "ten_bar_truss.out")
)
process.output_files = out_file_map


### TextOutput ###
# create a new TextOutput node
outfile = actors.ETKTextOutputActor("outfile")
# add the node to ARSM system
arsm.add_actor(outfile)
# connect process output path to TextOutput node
connect(process, "ten_bar_truss.out", outfile, "IPath")
connect(process, "ODesign", outfile, "IDesign")

# set path of reference file
output_file_name = "ten_bar_truss.out"
output_file_ref_path = os.path.join(example_path, output_file_name)
outfile.file = ProvidedPath(SplittedPath(example_path, output_file_name))

# Output: mass
# set up simple LineReader with repeater
# line - offset: 1, increment: 1, repetitions: 1
line_repeater_args = actors.ETKTextOutputActor.RepeaterArgs(1, 1, 1)
# set up TokenReade with repeater
# token - offset: 0, increment: 1, repetitions: 1
token_repeater_args = actors.ETKTextOutputActor.RepeaterArgs(0, 1, 1)
# create output variable
etk_var = actors.ETKTextOutputActor.TextOutputVariable(
    outfile.path, "mass", line_repeater_args, token_repeater_args
)
# add the response "mass"
outfile.add_response(etk_var)

# Output: stress
# set up repeated marker
# marker - offset: 0, increment: 1, repetitions: 10
regex_repeater_args = actors.ETKTextOutputActor.RepeaterArgs(0, 1, 10)
# set up LineReader with repeater
# line - offset: 1, increment: 1, repetitions: 1
line_repeater_args = actors.ETKTextOutputActor.RepeaterArgs(1, 1, 1)
# set up TokenReader with repeater
# token - offset: 0, increment: 1, repetitions: 1
token_repeater_args = actors.ETKTextOutputActor.RepeaterArgs(0, 1, 1)
# create output variable
etk_var = actors.ETKTextOutputActor.TextOutputVariable(
    outfile.path,
    "stress",
    line_repeater_args,
    token_repeater_args,
    True,
    regex_repeater_args,
    "Stress element",
    "Stress element",
)
# add the response "stress"
outfile.add_response(etk_var)


# connect to send back design
connect(outfile, "ODesign", arsm, "IIDesign")

### Criteria ###
# define criteria
from py_os_criterion import *

criteria_exprs = PyOSCriterionContainer()
# add an objective: mass is to be minimized
criteria_exprs.add("obj", PyOSCriterion(MIN, "mass"))
# add a constraint: maximum absolute stress should be less or equal 25000
criteria_exprs.add("c", PyOSCriterion(LESSEQUAL, "max(abs(stress))", "25000"))
# set criteria at the ARSM node
arsm.criteria = criteria_exprs
