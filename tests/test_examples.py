from contextlib import nullcontext as does_not_raise
import pathlib

import matplotlib.pyplot as plt
import pytest

pytestmark = pytest.mark.local_osl

run_python_script_examples_dir = (
    pathlib.Path(__file__).parents[1] / "examples" / "run_python_script"
)

run_python_script_examples = [
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


@pytest.mark.parametrize("example_script", run_python_script_examples)
def test_run_python_script_example(example_script):
    """ """
    with does_not_raise() as dnr:
        exec(run_python_script_examples_dir.joinpath(example_script).open().read())
    assert dnr is None


@pytest.mark.skip(reason="Execution modifies working tree")
def test_01_ten_bar_truss_evaluate_design(monkeypatch):
    """Test 01_ten_bar_truss_evaluate_design.py."""
    with does_not_raise() as dnr:
        monkeypatch.setattr(plt, "show", lambda: None)

        file = (
            pathlib.Path(__file__).parents[1]
            / "examples"
            / "evaluate_design"
            / "01_ten_bar_truss.py"
        )

        exec(file.open().read())
        assert dnr is None
