"""Module that returns paths to examples."""

import inspect
import os

module_path = os.path.dirname(inspect.getfile(inspect.currentframe()))

# dictionary of files, that must be available to run scripts
example_files = {
    "ansys_workbench_portscan": None,
    "arsm_ten_bar_truss": (
        os.path.join(module_path, "00_run_script", "ten_bar_truss", "files", "ten_bar_truss.s"),
        os.path.join(module_path, "00_run_script", "ten_bar_truss", "files", "ten_bar_truss.out"),
    ),
    "ansys_workbench_ten_bar_truss": (
        os.path.join(
            module_path, "00_run_script", "ten_bar_truss", "files", "ten_bar_truss_apdl.wbpz"
        )
    ),
    "ten_bar_modify_parameters": None,
    "ten_bar_truss_lc2": (
        os.path.join(module_path, "00_run_script", "ten_bar_truss", "files", "ten_bar_truss2.s"),
        os.path.join(module_path, "00_run_script", "ten_bar_truss", "files", "ten_bar_truss2.out"),
    ),
    "oscillatorcalibration_system_ascii": (
        os.path.join(
            module_path, "00_run_script", "oscillator", "scripts", "_create_oscillator.py"
        ),
        os.path.join(module_path, "00_run_script", "oscillator", "files", "oscillator.s"),
        os.path.join(module_path, "00_run_script", "oscillator", "files", "oscillator.bat"),
        os.path.join(module_path, "00_run_script", "oscillator", "files", "oscillator.sh"),
        os.path.join(module_path, "00_run_script", "oscillator", "files", "oscillator_signal.txt"),
        os.path.join(
            module_path, "00_run_script", "oscillator", "files", "oscillator_reference.txt"
        ),
    ),
    "oscillatorcalibration_system_python": (
        os.path.join(
            module_path, "00_run_script", "oscillator", "scripts", "_create_oscillator.py"
        ),
        os.path.join(
            module_path, "00_run_script", "oscillator", "files", "oscillator_reference.txt"
        ),
    ),
    "oscillator_optimization_ea": (
        os.path.join(module_path, "00_run_script", "oscillator", "scripts", "_create_oscillator.py")
    ),
    "oscillator_optimization_on_mop": (
        os.path.join(module_path, "00_run_script", "oscillator", "scripts", "_create_oscillator.py")
    ),
    "oscillator_robustness_arsm": (
        os.path.join(module_path, "00_run_script", "oscillator", "scripts", "_create_oscillator.py")
    ),
    "oscillator_sensitivity_mop": (
        os.path.join(module_path, "00_run_script", "oscillator", "scripts", "_create_oscillator.py")
    ),
    "oscillator_system_python": (
        os.path.join(module_path, "00_run_script", "oscillator", "scripts", "_create_oscillator.py")
    ),
    "create_all_possible_nodes": None,
    "etk_abaqus": (
        os.path.join(module_path, "00_run_script", "etk_abaqus", "files", "oscillator.inp"),
        os.path.join(module_path, "00_run_script", "etk_abaqus", "files", "oscillator.odb"),
    ),
    "python_help": None,
    "python_node": None,
    "optimizer_settings": None,
    "sensitivity_settings": None,
    "simple_calculator": None,
}

# dictionary of scripts to be run
example_scripts = {
    "ansys_workbench_portscan": os.path.join(
        module_path, "00_run_script", "scripts", "ansys_workbench_portscan.py"
    ),
    "arsm_ten_bar_truss": os.path.join(
        module_path, "00_run_script", "ten_bar_truss", "scripts", "arsm_ten_bar_truss.py"
    ),
    "ansys_workbench_ten_bar_truss": os.path.join(
        module_path, "00_run_script", "ten_bar_truss", "scripts", "ansys_workbench_ten_bar_truss.py"
    ),
    "ten_bar_modify_parameters": os.path.join(
        module_path, "00_run_script", "ten_bar_truss", "scripts", "ten_bar_modify_parameters.py"
    ),
    "ten_bar_truss_lc2": os.path.join(
        module_path, "00_run_script", "ten_bar_truss", "scripts", "ten_bar_truss_lc2.py"
    ),
    "oscillatorcalibration_system_ascii": os.path.join(
        module_path,
        "00_run_script",
        "oscillator",
        "scripts",
        "oscillatorcalibration_system_ascii.py",
    ),
    "oscillatorcalibration_system_python": os.path.join(
        module_path,
        "00_run_script",
        "oscillator",
        "scripts",
        "oscillatorcalibration_system_python.py",
    ),
    "oscillator_optimization_ea": os.path.join(
        module_path, "00_run_script", "oscillator", "scripts", "oscillator_optimization_ea.py"
    ),
    "oscillator_optimization_on_mop": os.path.join(
        module_path, "00_run_script", "oscillator", "scripts", "oscillator_optimization_on_mop.py"
    ),
    "oscillator_robustness_arsm": os.path.join(
        module_path, "00_run_script", "oscillator", "scripts", "oscillator_robustness_arsm.py"
    ),
    "oscillator_sensitivity_mop": os.path.join(
        module_path, "00_run_script", "oscillator", "scripts", "oscillator_sensitivity_mop.py"
    ),
    "oscillator_system_python": os.path.join(
        module_path, "00_run_script", "oscillator", "scripts", "oscillator_system_python.py"
    ),
    "create_all_possible_nodes": os.path.join(
        module_path, "00_run_script", "scripts", "create_all_possible_nodes.py"
    ),
    "etk_abaqus": os.path.join(
        module_path, "00_run_script", "etk_abaqus", "scripts", "etk_abaqus.py"
    ),
    "python_help": os.path.join(
        module_path, "00_run_script", "python", "scripts", "python_help.py"
    ),
    "python_node": os.path.join(
        module_path, "00_run_script", "python", "scripts", "python_node.py"
    ),
    "optimizer_settings": os.path.join(
        module_path, "00_run_script", "scripts", "optimizer_settings.py"
    ),
    "sensitivity_settings": os.path.join(
        module_path, "00_run_script", "scripts", "sensitivity_settings.py"
    ),
    "simple_calculator": os.path.join(
        module_path, "00_run_script", "scripts", "simple_calculator.py"
    ),
}
