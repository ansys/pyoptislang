# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
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

# create parametric system for oscillator python example

# in batch:
#      optislang --new oscillator_py.opf --python oscillator_system_python.py --run --batch

# in optiSlang:
#      open optiSLang and use 'run script file...' in optiSlang python console

# find a description of the oscillator example in optiSLang tutorial section.
###############################################################################


###############################################################################
# Import needed modules
###############################################################################
import os

from dynardo_py_algorithms import ParameterType, RandomVariableType
from py_os_criterion import DesignStatus, PyOSCriterion, PyOSCriterionContainer
from py_os_design import PyOSDesignEntry, create_nvp_design_entry
from py_os_parameter import PyParameter
from stdcpp_python_export import double_list_to_vec

###############################################################################
# Create ParametricSystem and add python2-knot
###############################################################################
para_system = actors.ParametricSystemActor("oscillator")
add_actor(para_system)

py2 = actors.PythonActor("oscillator.py")
para_system.add_actor(py2)

connect(para_system, "IODesign", py2, "IDesign")
connect(py2, "ODesign", para_system, "IIDesign")

###############################################################################
# Setup python2-knot
###############################################################################
# get example path "OSL_EXAMPLES": .\pyoptislang\src\ansys\optislang\core\examples
path = os.path.join(
    os.environ["OSL_EXAMPLES"], "00_run_script", "oscillator", "files", "oscillator.py"
)
py2.path = Path(path)

py2.add_parameter("m", PyOSDesignEntry(1.0))
py2.add_parameter("k", PyOSDesignEntry(20.0))
py2.add_parameter("D", PyOSDesignEntry(0.02))
py2.add_parameter("Ekin", PyOSDesignEntry(10.0))

py2.add_response(create_nvp_design_entry("omega_damped", PyOSDesignEntry(4.47124)))
py2.add_response(create_nvp_design_entry("x_max", PyOSDesignEntry(0.62342)))

###############################################################################
# Setup ParameterManager
###############################################################################
params = para_system.parameter_manager

params.set_parameter_type("m", ParameterType.MIXED)
params.set_parameter_type("k", ParameterType.MIXED)
params.set_parameter_type("D", ParameterType.STOCHASTIC)
params.set_parameter_type("Ekin", ParameterType.STOCHASTIC)

params.set_bounds("m", PyOSDesignEntry(0.1), PyOSDesignEntry(5.0))
params.set_bounds("k", PyOSDesignEntry(10.0), PyOSDesignEntry(50.0))

params.set_ran_type("m", RandomVariableType.NORMAL)
params.set_ran_type("k", RandomVariableType.NORMAL)
params.set_ran_type("D", RandomVariableType.NORMAL)
params.set_ran_type("Ekin", RandomVariableType.NORMAL)

params.set_ran_parameters("m", double_list_to_vec([1.0, 0.02]))
params.set_ran_parameters("k", double_list_to_vec([20.0, 1.0]))
params.set_ran_parameters("D", double_list_to_vec([0.02, 0.002]))
params.set_ran_parameters("Ekin", double_list_to_vec([10.0, 1.0]))

para_system.parameter_manager = params

###############################################################################
# Setup Criteria
###############################################################################
criteria_exprs = PyOSCriterionContainer()
criteria_exprs.add("Objective", PyOSCriterion(DesignStatus.MIN, "x_max"))
criteria_exprs.add("Constraint", PyOSCriterion(DesignStatus.LESSEQUAL, "omega_damped", "8.0"))
para_system.criteria = criteria_exprs
