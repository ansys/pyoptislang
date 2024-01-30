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

"""Modify workflow."""
###############################################################################
# (c) 2021 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.
#
# modify flow created by arsm_ten_bar_truss.py
# in batch
# optislang ten_bar_arsm.opf --python ten_bar_truss_lc2.py --no-run --batch
# start optiSLang
# optislang ten_bar_arsm.opf

# or open optiSLang, in Python console select "Run script file" and browse
# for this file

# find a description of the ten bar truss example in optiSLang tutorial section
# this script is related to the ten_bar_truss_advanced example
# see arsm_ten_bar_truss.py for previous steps
###############################################################################

### ARSM node ###
# get the ARSM node
arsm = find_actor("ARSM")

# use installed example
import os

# get example path .\pyoptislang\src\ansys\optislang\core\examples
example_path = os.path.join(os.environ["OSL_EXAMPLES"], "00_run_script", "ten_bar_truss", "files")

### TextInput ###
# create a new TextInput node
infile_lc2 = actors.TextInputActor("infile_lc2")
# add the node to ARSM System
arsm.add_actor(infile_lc2)
# set path of reference input file
infile_lc2.file_path = Path(os.path.join(example_path, "ten_bar_truss2.s"))
# import the content
infile_lc2.set_content()
# define location of the 10 input parameter
for i in range(0, 10):
    infile_lc2.add_parameter(actors.TextInputActor.Parameter("area%02d" % (i + 1), 24 + i, 20, 8))
# connect to get design from ARSM
connect(arsm, "IODesign", infile_lc2, "IDesign")


### Process ###
# create a new Process node for load case 2
process_lc2 = actors.ProcessActor("process_lc2")
# add the node to ARSM system
arsm.add_actor(process_lc2)
# process needs no distinct working directory
process_lc2.distinct_working_directory = False
# define command and arguments
slang_executable = os.environ["OPTISLANG_HOME"] + "/slang/bin/slang"
process_lc2.command = slang_executable
argv = WStrList()
argv.push_back("-b")
argv.push_back("ten_bar_truss2.s")
process_lc2.arguments = argv
# set maximum number of parallel runs
process_lc2.max_parallel = 2

# define the list of input files
in_file_map = actors.ProcessActor.InputFilesList()
in_file_map.push_back(
    actors.ProcessActor.InputFileMapping(Path("ten_bar_truss2.s"), "ten_bar_truss2.s")
)
process_lc2.input_files = in_file_map
# connect TextInput path to process
connect(infile_lc2, "OPath", process_lc2, "ten_bar_truss2.s")
connect(infile_lc2, "ODesign", process_lc2, "IDesign")

# define the list of output files
out_file_map = actors.ProcessActor.OutputFilesList()
out_file_map.push_back(
    actors.ProcessActor.OutputFileMapping(Path("ten_bar_truss2.out"), "ten_bar_truss2.out")
)
process_lc2.output_files = out_file_map


### TextOutput ###
# create a new TextOutput node
outfile_lc2 = actors.ETKTextOutputActor("outfile_lc2")
# add the node to ARSM system
arsm.add_actor(outfile_lc2)
# connect process output path to TextOutput node
connect(process_lc2, "ten_bar_truss2.out", outfile_lc2, "IPath")
connect(process_lc2, "ODesign", outfile_lc2, "IDesign")

# set path of reference file
output_lc2_file_name = "ten_bar_truss2.out"
output_lc2_file_ref_path = os.path.join(example_path, output_lc2_file_name)
outfile_lc2.file = ProvidedPath(output_lc2_file_ref_path)


# Output: stress (of load case 2)
# set up repeated marker
# marker - offset: 0, increment: 1, repetitions: 1
regex_repeater_args = actors.ETKTextOutputActor.RepeaterArgs(0, 1, 10)
# set up LineReader with repeater
# line - offset: 2, increment: 1, repetitions: 0
line_repeater_args = actors.ETKTextOutputActor.RepeaterArgs(1, 1, 1)
# set up TokenReader with repeater
# token - offset: 1, increment: 1, repetitions: 1
token_repeater_args = actors.ETKTextOutputActor.RepeaterArgs(0, 1, 1)
# create output variable
etk_var = actors.ETKTextOutputActor.TextOutputVariable(
    outfile_lc2.path,
    "stress_lc2",
    line_repeater_args,
    token_repeater_args,
    True,
    regex_repeater_args,
    "Stress element",
    "Stress element",
)
# add response "time_ref"
outfile_lc2.add_response(etk_var)


# connect to send back design
connect(outfile_lc2, "ODesign", arsm, "IIDesign")


### Criteria modification ###
from py_os_criterion import *

# get the criteria of ARSM node
criteria_exprs = arsm.criteria
# add a constraint: maximum absolute stress should be less or equal 35000
criteria_exprs.add("c_lc2", PyOSCriterion(LESSEQUAL, "max(abs(stress_lc2))", "35000"))
# set criteria at the ARSM node
arsm.criteria = criteria_exprs
