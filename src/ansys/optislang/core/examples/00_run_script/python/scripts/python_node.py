"""Create python2 node."""
###############################################################################
# (c) 2021 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.
#
# Create a Python2 node and add some source code. Add and remove parameters and
# responses. Add internal variables.
###############################################################################

from py_os_design import *

# Set up Parametric System and insert Python integration actor
param_system = actors.ParametricSystemActor("System")
add_actor(param_system)

pyactor = actors.Python2Actor("Python2")
param_system.add_actor(pyactor)

connect(param_system, "IODesign", pyactor, "IDesign")
connect(pyactor, "ODesign", param_system, "IIDesign")

# Set content of python actor
pyactor.source = "parameter_1 = 5.\nresponse_1 = parameter_1\npython_variable = 5.*parameter_1"

# Add parameters
pyactor.add_parameter("parameter_1", PyOSDesignEntry(5.0))
pyactor.add_parameter("temporary_parameter", PyOSDesignEntry(5.0))
# Remove parameters
pyactor.remove_parameter("temporary_parameter")

# Add responses
pyactor.add_response(
    ("response_2", PyOSDesignEntry(5.0)),
    actors.DerivedLocation("response_2", "parameter_1*response_1"),
)
pyactor.add_response(("response_1", PyOSDesignEntry(5.0)))
pyactor.add_response(("g", PyOSDesignEntry(5.0)))
# Remove responses
pyactor.remove_response("g")

# Add_expression/register_as_internal_location
# both lead to the same
pyactor.register_as_internal_location(
    "python_variable", "internal_from_py_source", PyOSDesignEntry(5.0)
)
pyactor.add_expression("c2", "internal_from_py_source_2", PyOSDesignEntry(5.0))
pyactor.register_as_internal_location(
    actors.DerivedLocation("d", "parameter_1 * response_1"), "d", PyOSDesignEntry(5.0)
)
pyactor.add_expression(
    actors.DerivedLocation("d2", "parameter_1 * response_1"), "d2", PyOSDesignEntry(5.0)
)
pyactor.register_as_internal_location(
    actors.DerivedLocation("f", "parameter_1 * response_1"), "f", PyOSDesignEntry(5.0)
)

# Remove expression/internal_location
pyactor.unregister_from_internal_locations("f")
pyactor.remove_expression("d2")

# Get parameters and print their names and values
params = PyOSDesignPoint()
pyactor.get_parameter(params)
print("Parameters:")
for name, value in params:
    print(name, value.get_scalar())

# Get responses and print their names and values
# Note that response values are updated after running the system
responses = PyOSDesignPoint()
pyactor.get_responses(responses)
print("Responses:")
for name, value in responses:
    print(name, value.get_scalar())
