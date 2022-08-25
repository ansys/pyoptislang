"""Module that returns paths to examples."""

import inspect
import os

module_path = os.path.dirname(inspect.getfile(inspect.currentframe()))


def join_path(module_path, folder, filename, type_):
    """Join module_path and file, return path."""
    return os.path.join(module_path, folder, type_, filename)


# dictionary of files, that must be available to run scripts
example_files = {
    "ansys_workbench_portscan": None,
    "arsm_ten_bar_truss": (
        join_path(module_path, r"00_run_script\ten_bar_truss", "ten_bar_truss.s", "files"),
        join_path(module_path, r"00_run_script\ten_bar_truss", "ten_bar_truss.out", "files"),
    ),
    "ansys_workbench_ten_bar_truss": (
        join_path(module_path, r"00_run_script\ten_bar_truss", "ten_bar_truss_apdl.wbpz", "files")
    ),
    "ten_bar_modify_parameters": None,
    "ten_bar_truss_lc2": (
        join_path(module_path, r"00_run_script\ten_bar_truss", "ten_bar_truss2.s", "files"),
        join_path(module_path, r"00_run_script\ten_bar_truss", "ten_bar_truss2.out", "files"),
    ),
    "oscillatorcalibration_system_ascii": (
        join_path(module_path, r"00_run_script\oscillator", "_create_oscillator.py", "scripts"),
        join_path(module_path, r"00_run_script\oscillator", "oscillator.s", "files"),
        join_path(module_path, r"00_run_script\oscillator", "oscillator.bat", "files"),
        join_path(module_path, r"00_run_script\oscillator", "oscillator.sh", "files"),
        join_path(module_path, r"00_run_script\oscillator", "oscillator_signal.txt", "files"),
        join_path(module_path, r"00_run_script\oscillator", "oscillator_reference.txt", "files"),
    ),
    "oscillatorcalibration_system_python": (
        join_path(module_path, r"00_run_script\oscillator", "_create_oscillator.py", "scripts"),
        join_path(module_path, r"00_run_script\oscillator", "oscillator_reference.txt", "files"),
    ),
    "oscillator_optimization_ea": (
        join_path(module_path, r"00_run_script\oscillator", "_create_oscillator.py", "scripts")
    ),
    "oscillator_optimization_on_mop": (
        join_path(module_path, r"00_run_script\oscillator", "_create_oscillator.py", "scripts")
    ),
    "oscillator_robustness_arsm": (
        join_path(module_path, r"00_run_script\oscillator", "_create_oscillator.py", "scripts")
    ),
    "oscillator_sensitivity_mop": (
        join_path(module_path, r"00_run_script\oscillator", "_create_oscillator.py", "scripts")
    ),
    "oscillator_system_python": (
        join_path(module_path, r"00_run_script\oscillator", "_create_oscillator.py", "scripts")
    ),
    "create_all_possible_nodes": None,
    "etk_abaqus": (
        join_path(module_path, r"00_run_script\etk_abaqus", "oscillator.inp", "files"),
        join_path(module_path, r"00_run_script\etk_abaqus", "oscillator.odb", "files"),
    ),
    "python_help": None,
    "python_node": None,
    "optimizer_settings": None,
    "sensitivity_settings": None,
    "simple_calculator": None,
}

# dictionary of scripts to be run
example_scripts = {
    "ansys_workbench_portscan": join_path(
        module_path, r"00_run_script", "ansys_workbench_portscan.py", "scripts"
    ),
    "arsm_ten_bar_truss": join_path(
        module_path, r"00_run_script\ten_bar_truss", "arsm_ten_bar_truss.py", "scripts"
    ),
    "ansys_workbench_ten_bar_truss": join_path(
        module_path, r"00_run_script\ten_bar_truss", "ansys_workbench_ten_bar_truss.py", "scripts"
    ),
    "ten_bar_modify_parameters": join_path(
        module_path, r"00_run_script\ten_bar_truss", "ten_bar_modify_parameters.py", "scripts"
    ),
    "ten_bar_truss_lc2": join_path(
        module_path, r"00_run_script\ten_bar_truss", "ten_bar_truss_lc2.py", "scripts"
    ),
    "oscillatorcalibration_system_ascii": join_path(
        module_path, r"00_run_script\oscillator", "oscillatorcalibration_system_ascii.py", "scripts"
    ),
    "oscillatorcalibration_system_python": join_path(
        module_path,
        r"00_run_script\oscillator",
        "oscillatorcalibration_system_python.py",
        "scripts",
    ),
    "oscillator_optimization_ea": join_path(
        module_path, r"00_run_script\oscillator", "oscillator_optimization_ea.py", "scripts"
    ),
    "oscillator_optimization_on_mop": join_path(
        module_path, r"00_run_script\oscillator", "oscillator_optimization_on_mop.py", "scripts"
    ),
    "oscillator_robustness_arsm": join_path(
        module_path, r"00_run_script\oscillator", "oscillator_robustness_arsm.py", "scripts"
    ),
    "oscillator_sensitivity_mop": join_path(
        module_path, r"00_run_script\oscillator", "oscillator_sensitivity_mop.py", "scripts"
    ),
    "oscillator_system_python": join_path(
        module_path, r"00_run_script\oscillator", "oscillator_system_python.py", "scripts"
    ),
    "create_all_possible_nodes": join_path(
        module_path, r"00_run_script", "create_all_possible_nodes.py", "scripts"
    ),
    "etk_abaqus": join_path(module_path, r"00_run_script\etk_abaqus", "etk_abaqus.py", "scripts"),
    "python_help": join_path(module_path, r"00_run_script\python", "python_help.py", "scripts"),
    "python_node": join_path(module_path, r"00_run_script\python", "python_node.py", "scripts"),
    "optimizer_settings": join_path(
        module_path, r"00_run_script", "optimizer_settings.py", "scripts"
    ),
    "sensitivity_settings": join_path(
        module_path, r"00_run_script", "sensitivity_settings.py", "scripts"
    ),
    "simple_calculator": join_path(
        module_path, r"00_run_script", "simple_calculator.py", "scripts"
    ),
}
