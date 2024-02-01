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

import pathlib

import matplotlib.pyplot as plt
import pytest

from ansys.optislang.core import examples

pytestmark = pytest.mark.local_osl


@pytest.fixture(
    params=[
        "01_ten_bar_truss.py",
        "02_1_oscillator_robustness.py",
        "02_2_oscillator_python_system.py",
        "02_3_oscillator_optimization_on_EA.py",
        "02_4_oscillator_MOP_sensitivity_and_optimization.py",
        "02_5_oscillator_calibration_systems.py",
        "03_etk_abaqus.py",
        # The use of "help" function (intended for interactive use) in this example,
        # leads to a straying osl process. Deactivate this test for now.
        # "04_python_node_and_help.py",
        "05_optimizer_settings.py",
        "06_sensitivity_settings.py",
        "07_simple_calculator.py",
    ]
)
def run_python_script_example_source(request):
    """Source of a run_python_script example."""
    exampe_file = (
        pathlib.Path(__file__).parents[1] / "examples" / "run_python_script" / request.param
    )
    with exampe_file.open() as f:
        src = f.read()
    return src


@pytest.fixture(params=["01_ten_bar_truss.py"])
def evaluate_design_example_source(request):
    """Source of an evaluate_design example."""
    exampe_file = pathlib.Path(__file__).parents[1] / "examples" / "evaluate_design" / request.param
    with exampe_file.open() as f:
        src = f.read()
    return src


def test_run_python_script_example(run_python_script_example_source):
    """Test run_python_script examples."""
    exec(run_python_script_example_source)


def test_evaluate_design_01_ten_bar_truss(
    monkeypatch, tmp_example_project, evaluate_design_example_source
):
    """Test evaluate_design examples."""
    # Suppress plotting
    monkeypatch.setattr(plt, "show", lambda: None)

    # Ensure temporary project file within the example script
    project_file = (None, (tmp_example_project("ten_bar_truss"),))
    monkeypatch.setattr(examples, "get_files", lambda _: project_file)

    exec(evaluate_design_example_source)
