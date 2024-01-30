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

"""Create simple calculator."""
###############################################################################
# (c) 2021 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.

# This example serves to show the principle of optiSLang

# Nodes (or Actors in Python-Script) symbolize
#   * an operation
#   * a task
#   * an algorithm

# Edges (or Connections in Python-Script) symbolize
#   * the data flow
#       * which data is received from prior node
#       * which data is sended to successive node
#   * the scheduling
#       * defines predecessors and successors of a node

# paste this into the Python console and run it

# This example creates a simple flow of 4 nodes:

#    A(12.0)  ---\
#                 | --->  A + B*2  ---> Result
#    B( 3.0)  ---/
###############################################################################

# import needed dynardo python module
from py_os_design import *
from pyvariant import VariantD

### Variable node A ###
# create variable node A
a = actors.VariableActor("A")  # set name "A"
# add the variable to the scenery/flow
add_actor(a)
# set the value 12.0 at node A
# (value needs to be converted from standard python to dynardo design entry)
a.variant = PyOSDesignEntry(12.0)

### Variable node B ###
# create variable node B
b = actors.VariableActor("B")
# add the variable to the scenery/flow
add_actor(b)
# set the value 3.0 at node B
vec = [1, 2, 3, 4, 5]

b.variant = PyOSDesignEntry(VariantD(vec))


### Calculator node ###
# create calculator node
calc_actor = actors.CalculatorSetActor()  # use standard name
# add the calculator to the scenery/flow
add_actor(calc_actor)
# add 2 input slots (left hand side)
# to receive values of A and B
calc_actor.add_input_slot(Actor.SlotType.DESIGNENTRY, "A")
calc_actor.add_input_slot(Actor.SlotType.DESIGNENTRY, "B")
# define the formula "A + B * 2" and add it as an output
calc_actor.add_output("result", "A+B[0]*2")
calc_actor.add_output("result2", "A+B*2")

### Variable node Result ###
# you can also print some output to the python console
print("Creating and adding a node to show the result")
# create variable node result
r = actors.Python2Actor("result")

# py actor source text
r_text = "import os\n\n"
r_text = r_text + ("#open result.txt in DESIGN_DIR and write value of result to it.\n")
# open file
r_text = r_text + ("res_file=open(os.path.join(DESIGN_DIR,'result.txt'),'w')\n")
# write result
r_text = r_text + ("res_file.write('Result: '+str(result))\n")
# close file
r_text = r_text + ("res_file.close()")
# py actor source
r.source = r_text

# ~ r.source =("import os\n\nres_file=open(os.path.join(DESIGN_DIR,'out.txt'),'w')
#                   \nres_file.write(str(result))\nres_file.close()")

# add input slot to receive result
r.add_input_slot(Actor.SlotType.DESIGNENTRY, "result")

# add the variable to the scenery/flow
add_actor(r)

# add monitoring node
r2 = actors.VariantMonitoringActor("result2")
# add the variable to the scenery/flow
add_actor(r2)
# add input slot to receive result2
r2.add_input_slot(Actor.SlotType.DESIGNENTRY, "result2")

# now open the monitoring context menu (right click)
# and select "Pin Preview"


print("All nodes are created, added and set up")
print("Now nodes need to be connected")

########################################################################
### Connections ###

# Connect variable A and Calculator
connect(a, "OVar", calc_actor, "A")
# Connect variable B and Calculator
connect(b, "OVar", calc_actor, "B")
# Connect variable Calculator and result
connect(calc_actor, "result", r, "result")
# Connect variable Calculator and result2
connect(calc_actor, "result2", r2, "result2")

###
# scheduling:
# -> when A and B are processed calculator starts evaluation
# -> when calculator is processed - results come up in result node
#
# data flow:
# when A is processed
# -> A sends its result (12.0) at output slot (right hand side)
# -> data flows to calculator (edge)
# -> calculator receives data at input slot (left hand side)
# same for B -> calculator
# same for calculator -> result
