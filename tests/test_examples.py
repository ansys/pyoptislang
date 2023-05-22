from contextlib import nullcontext as does_not_raise
import os
import pathlib
import time

import matplotlib.pyplot as plt
import pytest

pytestmark = pytest.mark.local_osl

pytest_path = __file__

run_python_script_examples_dir = os.path.join(
    pathlib.Path(__file__).parents[1], "examples", "run_python_script"
)
run_python_script_example_files_paths = []
for file in os.listdir(run_python_script_examples_dir):
    if file.endswith(".py"):
        run_python_script_example_files_paths.append(
            os.path.join(run_python_script_examples_dir, file)
        )


def test_01_ten_bar_truss():
    """Test 01_1_ten_bar_truss.py."""
    with does_not_raise() as dnr:
        name = "01_ten_bar_truss"
        file = list(filter(lambda path: name in path, run_python_script_example_files_paths))[0]
        exec(open(file).read())
        time.sleep(5)
    assert dnr is None


def test_02_1_oscillator_robustness():
    """Test 02_1_oscillator_robustness.py."""
    with does_not_raise() as dnr:
        name = "02_1_oscillator_robustness"
        file = list(filter(lambda path: name in path, run_python_script_example_files_paths))[0]
        exec(open(file).read())
        time.sleep(5)
    assert dnr is None


def test_02_2_oscillator_python_system():
    """Test 02_2_oscillator_python_system.py."""
    with does_not_raise() as dnr:
        name = "02_2_oscillator_python_system"
        file = list(filter(lambda path: name in path, run_python_script_example_files_paths))[0]
        exec(open(file).read())
        time.sleep(5)
    assert dnr is None


def test_02_3_oscillator_optimization_on_EA():
    """Test 02_3_oscillator_optimization_on_EA.py."""
    with does_not_raise() as dnr:
        name = "02_3_oscillator_optimization_on_EA"
        file = list(filter(lambda path: name in path, run_python_script_example_files_paths))[0]
        exec(open(file).read())
        time.sleep(5)
    assert dnr is None


def test_02_4_oscillator_MOP_sensitivity_and_optimization():
    """Test 02_4_oscillator_MOP_sensitivity_and_optimization.py."""
    with does_not_raise() as dnr:
        name = "02_4_oscillator_MOP_sensitivity_and_optimization"
        file = list(filter(lambda path: name in path, run_python_script_example_files_paths))[0]
        exec(open(file).read())
        time.sleep(5)
    assert dnr is None


def test_02_5_oscillator_calibration_systems():
    """Test 02_5_oscillator_calibration_systems.py."""
    with does_not_raise() as dnr:
        name = "02_5_oscillator_calibration_systems"
        file = list(filter(lambda path: name in path, run_python_script_example_files_paths))[0]
        exec(open(file).read())
        time.sleep(5)
    assert dnr is None


def test_03_etk_abaqus():
    """Test 03_etk_abaqus.py."""
    with does_not_raise() as dnr:
        name = "03_etk_abaqus"
        file = list(filter(lambda path: name in path, run_python_script_example_files_paths))[0]
        exec(open(file).read())
        time.sleep(5)
    assert dnr is None


def test_04_python_node_and_help():
    """Test 04_python_node_and_help.py."""
    with does_not_raise() as dnr:
        name = "04_python_node_and_help"
        file = list(filter(lambda path: name in path, run_python_script_example_files_paths))[0]
        exec(open(file).read())
        time.sleep(5)
    assert dnr is None


def test_05_optimizer_settings():
    """Test 05_optimizer_settings.py."""
    with does_not_raise() as dnr:
        name = "05_optimizer_settings"
        file = list(filter(lambda path: name in path, run_python_script_example_files_paths))[0]
        exec(open(file).read())
        time.sleep(5)
    assert dnr is None


def test_06_sensitivity_settings():
    """Test 06_sensitivity_settings.py."""
    with does_not_raise() as dnr:
        name = "06_sensitivity_settings"
        file = list(filter(lambda path: name in path, run_python_script_example_files_paths))[0]
        exec(open(file).read())
        time.sleep(5)
    assert dnr is None


def test_07_simple_calculator():
    """Test 07_simple_calculator.py."""
    with does_not_raise() as dnr:
        name = "07_simple_calculator"
        file = list(filter(lambda path: name in path, run_python_script_example_files_paths))[0]
        exec(open(file).read())
        time.sleep(5)
    assert dnr is None


evaluate_design_examples_dir = os.path.join(
    pathlib.Path(__file__).parents[1], "examples", "evaluate_design"
)
evaluate_design_example_files_paths = []
for file in os.listdir(evaluate_design_examples_dir):
    if file.endswith(".py"):
        evaluate_design_example_files_paths.append(os.path.join(evaluate_design_examples_dir, file))


def test_01_ten_bar_truss_evaluate_design(monkeypatch):
    """Test 01_ten_bar_truss_evaluate_design.py."""
    with does_not_raise() as dnr:
        name = "01_ten_bar_truss"
        file = list(filter(lambda path: name in path, evaluate_design_example_files_paths))[0]
        monkeypatch.setattr(plt, "show", lambda: None)
        exec(open(file).read())
        time.sleep(5)
    assert dnr is None
