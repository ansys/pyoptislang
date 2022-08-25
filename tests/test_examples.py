from contextlib import nullcontext as does_not_raise
import os
import pathlib

import pytest

pytestmark = pytest.mark.local_osl
pytest_path = __file__
examples_dir = os.path.join(pathlib.Path(__file__).parents[1], "examples")
example_files_paths = []
for file in os.listdir(examples_dir):
    if file.endswith(".py"):
        example_files_paths.append(os.path.join(examples_dir, file))


def setup_function(function):
    """Rewrite ``__file__`` attribute in order to save files in correct directory."""
    global name
    name = function.__name__[5:]
    global __file__
    __file__ = os.path.join(examples_dir, name + ".py")


def teardown_function(function):
    """Rewrite ``__file__`` attribute to original value."""
    global __file__
    __file__ = pytest_path


def test_01_1_ten_bar_truss():
    """Test 01_1_ten_bar_truss.py."""
    with does_not_raise() as dnr:
        file = list(filter(lambda path: name in path, example_files_paths))[0]
        exec(open(file).read())
    assert dnr is None


def test_01_2_ten_bar_truss():
    """Test 01_2_ten_bar_truss.py."""
    with does_not_raise() as dnr:
        file = list(filter(lambda path: name in path, example_files_paths))[0]
        exec(open(file).read())
    assert dnr is None


def test_02_1_oscillator_robustness():
    """Test 02_1_oscillator_robustness.py."""
    with does_not_raise() as dnr:
        file = list(filter(lambda path: name in path, example_files_paths))[0]
        exec(open(file).read())
    assert dnr is None


def test_02_2_oscillator_python_system():
    """Test 02_2_oscillator_python_system.py."""
    with does_not_raise() as dnr:
        file = list(filter(lambda path: name in path, example_files_paths))[0]
        exec(open(file).read())
    assert dnr is None


def test_02_3_oscillator_optimization_on_EA():
    """Test 02_3_oscillator_optimization_on_EA.py."""
    with does_not_raise() as dnr:
        file = list(filter(lambda path: name in path, example_files_paths))[0]
        exec(open(file).read())
    assert dnr is None


def test_02_4_oscillator_MOP_sensitivity_and_optimization():
    """Test 02_4_oscillator_MOP_sensitivity_and_optimization.py."""
    with does_not_raise() as dnr:
        file = list(filter(lambda path: name in path, example_files_paths))[0]
        exec(open(file).read())
    assert dnr is None


def test_02_5_oscillator_calibration_systems():
    """Test 02_5_oscillator_calibration_systems.py."""
    with does_not_raise() as dnr:
        file = list(filter(lambda path: name in path, example_files_paths))[0]
        exec(open(file).read())
    assert dnr is None


def test_03_etk_abaqus():
    """Test 03_etk_abaqus.py."""
    with does_not_raise() as dnr:
        file = list(filter(lambda path: name in path, example_files_paths))[0]
        exec(open(file).read())
    assert dnr is None


def test_04_python_node_and_help():
    """Test 04_python_node_and_help.py."""
    with does_not_raise() as dnr:
        file = list(filter(lambda path: name in path, example_files_paths))[0]
        exec(open(file).read())
    assert dnr is None


def test_05_optimizer_settings():
    """Test 05_optimizer_settings.py."""
    with does_not_raise() as dnr:
        file = list(filter(lambda path: name in path, example_files_paths))[0]
        exec(open(file).read())
    assert dnr is None


def test_06_sensitivity_settings():
    """Test 06_sensitivity_settings.py."""
    with does_not_raise() as dnr:
        file = list(filter(lambda path: name in path, example_files_paths))[0]
        exec(open(file).read())
    assert dnr is None


def test_07_simple_calculator():
    """Test 07_simple_calculator.py."""
    with does_not_raise() as dnr:
        file = list(filter(lambda path: name in path, example_files_paths))[0]
        exec(open(file).read())
    assert dnr is None


def test_08_ansys_workbench_portscan():
    """Test 08_ansys_workbench_portscan.py."""
    with does_not_raise() as dnr:
        file = list(filter(lambda path: name in path, example_files_paths))[0]
        exec(open(file).read())
    assert dnr is None
