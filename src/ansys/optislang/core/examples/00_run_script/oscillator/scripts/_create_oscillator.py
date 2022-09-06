"""Create oscillator node and its physics."""
###############################################################################
# (c) 2021 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.
#
###############################################################################
# Import needed modules
###############################################################################
import os

from dynardo_py_algorithms import DOETYPES, ParameterType, RandomVariableType
import py_doe_settings
from py_os_criterion import DesignStatus, PyOSCriterion, PyOSCriterionContainer
from py_os_design import PyOSDesignEntry, create_nvp_design_entry
from py_os_parameter import PyParameter
from stdcpp_python_export import double_list_to_vec

###############################################################################
# Create connections between system and python node
###############################################################################
py2 = actors.PythonActor("oscillator.py")
example_system.add_actor(py2)

connect(example_system, "IODesign", py2, "IDesign")
connect(py2, "ODesign", example_system, "IIDesign")

###############################################################################
# Setup python node
###############################################################################

# get example path "OSL_EXAMPLES": .\pyoptislang\src\ansys\optislang\core\examples
py2.path = Path(
    os.path.join(
        os.environ["OSL_EXAMPLES"], "00_run_script", "oscillator", "files", "oscillator.py"
    )
)

py2.add_parameter("m", PyOSDesignEntry(1.0))
py2.add_parameter("k", PyOSDesignEntry(20.0))
py2.add_parameter("D", PyOSDesignEntry(0.02))
py2.add_parameter("Ekin", PyOSDesignEntry(10.0))

py2.max_parallel = 4

py2.add_response(create_nvp_design_entry("omega_damped", PyOSDesignEntry(4.47124)))
py2.add_response(create_nvp_design_entry("x_max", PyOSDesignEntry(0.62342)))

###############################################################################
# Setup ParameterManager
###############################################################################
params = example_system.parameter_manager

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

example_system.parameter_manager = params

###############################################################################
# Setup Criteria
###############################################################################
criteria_exprs = PyOSCriterionContainer()
criteria_exprs.add("Objective", PyOSCriterion(DesignStatus.MIN, "x_max"))
criteria_exprs.add("Constraint", PyOSCriterion(DesignStatus.LESSEQUAL, "omega_damped", "8.0"))
example_system.criteria = criteria_exprs
