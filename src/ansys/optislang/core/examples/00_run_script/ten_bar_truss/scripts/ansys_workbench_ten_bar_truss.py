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

"""Create workbench node."""
###############################################################################
# (c) 2021 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.

# Create a project with workbench node
# use installed example ten_bar_truss_apdl
# you can select your type of connection
# * connect to running project - lines 30ff
#   * need a running project !!!
# * open project - lines 40 ff

# For more information see ascii based (ten bar truss) examples
# run
#    help(actors.AnsysWorkbenchActor)
# or contact dynardo support
#    +49 (0)3643 9008 - 32
#    support@dynardo.de
###############################################################################

pss = actors.ParametricSystemActor()
add_actor(pss)

from py_os_design import *
from py_os_parameter import *

params = PyParameterManager()
for i in range(1, 11):
    params.add_deterministic_continuous_parameter("AREA%02d" % i, 0.1, 20, 10, 0)
pss.parameter_manager = params


### Workbench ###
wb = actors.AnsysWorkbenchActor()
pss.add_actor(wb)

connect(pss, "IODesign", wb, "IDesign")
connect(wb, "ODesign", pss, "IIDesign")

### WB connect to running ten_bar_truss example ###
# ~ projects=wb.get_network_projects(2)
# ~ for pr in  projects : print pr.GetHost() ,pr.GetName()
# ~ matching_pr=[ x for x in projects if "ten_bar_truss" in x.GetName() ]
# ~ wb.set_connection(matching_pr[0]) # for this example ... take the first match


### Or open ###
import os

# get example path .\pyoptislang\src\ansys\optislang\core\examples\00_run_script\..
#                   ..ten_bar_truss\files\ten_bar_truss_apdl.wbpz
example_path = os.path.join(
    os.environ["OSL_EXAMPLES"], "00_run_script", "ten_bar_truss", "files", "ten_bar_truss_apdl.wbpz"
)


wb.path_to_project = Path(example_path)
wb.ensure_valid_connection()
wb.open_project()
wb.close_project()

for i in range(0, wb.get_num_inputs()):
    wb.add_parameter(wb.get_input_name(i), wb.get_input_value(i))
for i in range(0, wb.get_num_outputs()):
    wb.add_response(wb.get_output_name(i), wb.get_output_value(i))
