# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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
.. _ref_optimization_on_mop:

Optimization on MOP with proxy solver
=====================================

This example demonstrates how to create and execute optimization on MOP using ``ParametricDesignStudyManager``

It creates multiple parametric systems using ``ProxySolver`` and ``Mopsolver`` nodes as solvers and then runs the created design study.
"""

#########################################################
# Perform required imports
# ------------------------
# Perform the required imports.


from math import sin
from pathlib import Path

import ansys.optislang.core.node_types as nt
from ansys.optislang.core.project_parametric import (
    Design,
    DesignVariable,
    ObjectiveCriterion,
    OptimizationParameter,
    Response,
)
from ansys.optislang.parametric.design_study import ParametricDesignStudyManager
from ansys.optislang.parametric.design_study_templates import (
    GeneralAlgorithmTemplate,
    OptimizationOnMOPTemplate,
    ProxySolverNodeSettings,
)

#########################################################
# Create template inputs
# ----------------------
# Define template inputs, that are used by the parametric design study manager
# to create and execute the design study.


project_path = Path().cwd() / "design_manager_example.opf"
parameters = [
    OptimizationParameter(name=f"X{i}", reference_value=0.0, range=(-3.14, 3.14))
    for i in range(1, 6)
]
responses = [Response(name="Y", reference_value=0.0)]


def callback(designs: list[Design]) -> list[Design]:
    """Calculate coupled function for provided designs."""
    results_designs = []
    for design in designs:
        X1 = design.parameters[design.parameters_names.index("X1")].value
        X2 = design.parameters[design.parameters_names.index("X2")].value
        X3 = design.parameters[design.parameters_names.index("X3")].value
        X4 = design.parameters[design.parameters_names.index("X4")].value
        X5 = design.parameters[design.parameters_names.index("X5")].value

        Y = 0.5 * X1 + X2 + 0.5 * X1 * X2 + 5 * sin(X3) + 0.2 * X4 + 0.1 * X5
        id = design.id

        # create instance of design with new values
        output_design = Design(
            responses=[DesignVariable("Y", Y)],
            design_id=id,
        )
        results_designs.append(output_design)
    return results_designs


solver_settings = ProxySolverNodeSettings(callback=callback, multi_design_launch_num=-1)

#########################################################
# Create AMOP template
# --------------------
# Define template that will be transformed into an AMOP system with proxy solver.

amop_template = GeneralAlgorithmTemplate(
    parameters=parameters,
    criteria=[],
    responses=responses,
    algorithm_type=nt.AMOP,
    solver_type=nt.ProxySolver,
    solver_settings=solver_settings,
)


#########################################################
# Create AMOP system
# ------------------
# Instantiate parametric design study manager, create and execute the design study.

design_study_manager = ParametricDesignStudyManager(project_path=project_path)
study = design_study_manager.create_design_study(template=amop_template)
study.execute()
design_study_manager.save()


#########################################################
# Create Optimization on MOP
# --------------------------
# Create optimization with MOP solver and validation system, execute.
# Database from the previous design study is used as an input for the MOP Solver.

criteria = [ObjectiveCriterion("minY", expression="Y")]
amop_system = study.managed_instances[0].instance

optimization_template = OptimizationOnMOPTemplate(
    parameters=parameters,
    criteria=criteria,
    responses=responses,
    mop_predecessor=amop_system,
    callback=callback,
)

optimization_study = design_study_manager.create_design_study(optimization_template)
optimization_study.execute()
design_study_manager.save()

#########################################################
# Stop and cancel project
# ~~~~~~~~~~~~~~~~~~~~~~~
# Stop and cancel the project.

design_study_manager.optislang.dispose()


#########################################################
# View generated workflow
# -----------------------
# This image shows the generated workflow.
#
# .. image:: ../../_static/02_optimization_on_mop.png
#  :width: 1200
#  :alt: Result of script.
