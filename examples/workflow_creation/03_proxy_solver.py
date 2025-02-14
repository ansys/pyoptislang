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

"""
.. _ref_proxy_solver:

Proxy solver
------------

This example demonstrates how to obtain designs from parametric system and process them externally.

It creates a proxy solver node inside parametric system and solves it's designs externally.

This is a unified approach for "optiSLang inside" solutions.
"""

#########################################################
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Perform the required imports.
import time

from ansys.optislang.core import Optislang
import ansys.optislang.core.node_types as node_types
from ansys.optislang.core.nodes import DesignFlow, ParametricSystem, ProxySolverNode
from ansys.optislang.core.project_parametric import (
    ComparisonType,
    ObjectiveCriterion,
    OptimizationParameter,
)
from ansys.optislang.core.utils import find_all_osl_exec

#########################################################
# Create solver
# ~~~~~~~~~~~~~
# Define a simple calculator function to solve the variations


def calculator(hid, X1, X2, X3, X4, X5):
    from math import sin

    Y = 0.5 * X1 + X2 + 0.5 * X1 * X2 + 5 * sin(X3) + 0.2 * X4 + 0.1 * X5
    return Y


def calculate(designs):
    result_design_list = []
    print(f"Calculate {len(designs)} designs")
    for design in designs:
        hid = design["hid"]
        parameters = design["parameters"]
        X1 = 0.0
        X2 = 0.0
        X3 = 0.0
        X4 = 0.0
        X5 = 0.0
        for parameter in parameters:
            if parameter["name"] == "X1":
                X1 = parameter["value"]
            elif parameter["name"] == "X2":
                X2 = parameter["value"]
            elif parameter["name"] == "X3":
                X3 = parameter["value"]
            elif parameter["name"] == "X4":
                X4 = parameter["value"]
            elif parameter["name"] == "X5":
                X5 = parameter["value"]
        Y = calculator(hid, X1, X2, X3, X4, X5)

        result_design = {}
        result_design["hid"] = hid
        responses = [{"name": "Y", "value": Y}]
        result_design["responses"] = responses
        result_design_list.append(result_design)

    print(f"Return {len(result_design_list)} designs")
    return result_design_list


#########################################################
# Create optiSLang instance
# ~~~~~~~~~~~~~~~~~~~~~~~~~
# Find the optiSLang >= 25.1 executable. Initialize the Optislang class instance with the executable.

available_optislang_executables = find_all_osl_exec()
version, executables = available_optislang_executables.popitem(last=False)
if not version >= 251:
    raise KeyError("OptiSLang installation >= 25R1 wasn't found, please specify path manually.")

osl = Optislang(executable=executables[0])

print(f"Using optiSLang version {osl.osl_version_string}")


#########################################################
# Create workflow
# ~~~~~~~~~~~~~~~

root_system = osl.application.project.root_system

# Create the algorithm system of your choice.

algorithm_system: ParametricSystem = root_system.create_node(
    type_=node_types.Sensitivity, name="Sensitivity"
)

num_discretization = 2000

algorithm_settings = algorithm_system.get_property("AlgorithmSettings")
algorithm_settings["num_discretization"] = num_discretization
algorithm_system.set_property("AlgorithmSettings", algorithm_settings)

# Fast running solver settings

algorithm_system.set_property("AutoSaveMode", "no_auto_save")
algorithm_system.set_property("SolveTwice", True)
algorithm_system.set_property("UpdateResultFile", "never")
algorithm_system.set_property("WriteDesignStartSetFlag", False)

# Add the Proxy Solver node and set the desired maximum number of designs you handle in one go.

proxy_solver: ProxySolverNode = algorithm_system.create_node(
    type_=node_types.ProxySolver, name="Calculator", design_flow=DesignFlow.RECEIVE_SEND
)

multi_design_launch_num = 99  # set -1 to solve all designs simultaneously
proxy_solver.set_property("MultiDesignLaunchNum", multi_design_launch_num)
proxy_solver.set_property("ForwardHPCLicenseContextEnvironment", True)

# Load the available parameters and responses.

load_json = {}
load_json["parameters"] = []
load_json["responses"] = []

for i in range(1, 6):
    parameter = {"dir": {"value": "input"}, "name": f"X{i}", "value": 1.0}
    load_json["parameters"].append(parameter)

response = {"dir": {"value": "output"}, "name": "Y", "value": 3.0}
load_json["responses"].append(response)

proxy_solver.load(args=load_json)

# Register parameters and responses to be available in the algorithm system

proxy_solver.register_locations_as_parameter()
proxy_solver.register_locations_as_response()

# Change parameter bounds.

for i in range(1, 6):
    algorithm_system.parameter_manager.modify_parameter(
        OptimizationParameter(name=f"X{i}", reference_value=1.0, range=(-3.14, 3.14))
    )

# Create a criterion in the algorithm system

algorithm_system.criteria_manager.add_criterion(
    ObjectiveCriterion(name="obj", expression="Y", criterion=ComparisonType.MIN)
)


#########################################################
# Optionally save project
# ~~~~~~~~~~~~~~~~~~~~~~~
# If you want to save the project to some desired location,
# uncomment and edit these lines:
#
# .. code:: python
#
#   dir_path = Path(r"<insert-desired-location>")
#   project_name = "proxy_solver_workflow.opf"
#   osl.application.save_as(dir_path / project_name)


#########################################################
# Run workflow
# ~~~~~~~~~~~~
# Run the workflow created by the preceding scripts.

# Start the optiSLang project execution.
osl.application.project.start(wait_for_finished=False)


# Now loop until get_status() returns "Processing done" for the root system. Use the GET_DESIGNS query and the SET_DESIGNS command for the Proxy Solver node to get designs and set responses until the system is done.

while not osl.project.root_system.get_status() == "Processing done":
    design_list = proxy_solver.get_designs()
    if len(design_list):
        responses_dict = calculate(design_list)
        proxy_solver.set_designs(responses_dict)
    # time.sleep(0.1)

print("Solved Successfully!")


#########################################################
# Stop and cancel project
# ~~~~~~~~~~~~~~~~~~~~~~~
# Stop and cancel the project.
osl.dispose()

#########################################################
# View generated workflow
# ~~~~~~~~~~~~~~~~~~~~~~~
# This image shows the generated workflow.
# However, it is important to note, that this workflow is only usable through pyoptislang and cannot be used interactively!
#
# .. image:: ../../_static/03_ProxySolver.png
#  :width: 400
#  :alt: Result of script.
#
