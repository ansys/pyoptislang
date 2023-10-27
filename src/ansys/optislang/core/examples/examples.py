"""Module that returns paths to examples."""

import inspect
import os
from pathlib import Path

module_path = Path(inspect.getfile(inspect.currentframe())).parent

# dictionary of files, that must be available to run scripts
example_files = {
    "ansys_workbench_portscan": None,
    "arsm_ten_bar_truss": (
        module_path / "00_run_script" / "ten_bar_truss" / "files" / "ten_bar_truss.s",
        module_path / "00_run_script" / "ten_bar_truss" / "files" / "ten_bar_truss.out",
    ),
    "ansys_workbench_ten_bar_truss": (
        module_path / "00_run_script" / "ten_bar_truss" / "files" / "ten_bar_truss_apdl.wbpz",
    ),
    "ten_bar_modify_parameters": None,
    "ten_bar_truss_lc2": (
        module_path / "00_run_script" / "ten_bar_truss" / "files" / "ten_bar_truss2.s",
        module_path / "00_run_script" / "ten_bar_truss" / "files" / "ten_bar_truss2.out",
    ),
    "oscillatorcalibration_system_ascii": (
        module_path / "00_run_script" / "oscillator" / "scripts" / "_create_oscillator.py",
        module_path / "00_run_script" / "oscillator" / "files" / "oscillator.s",
        module_path / "00_run_script" / "oscillator" / "files" / "oscillator.bat",
        module_path / "00_run_script" / "oscillator" / "files" / "oscillator.sh",
        module_path / "00_run_script" / "oscillator" / "files" / "oscillator_signal.txt",
        module_path / "00_run_script" / "oscillator" / "files" / "oscillator_reference.txt",
    ),
    "oscillatorcalibration_system_python": (
        module_path / "00_run_script" / "oscillator" / "scripts" / "_create_oscillator.py",
        module_path / "00_run_script" / "oscillator" / "files" / "oscillator_reference.txt",
    ),
    "oscillator_optimization_ea": (
        module_path / "00_run_script" / "oscillator" / "scripts" / "_create_oscillator.py",
    ),
    "oscillator_optimization_on_mop": (
        module_path / "00_run_script" / "oscillator" / "scripts" / "_create_oscillator.py",
    ),
    "oscillator_robustness_arsm": (
        module_path / "00_run_script" / "oscillator" / "scripts" / "_create_oscillator.py",
    ),
    "oscillator_sensitivity_mop": (
        module_path / "00_run_script" / "oscillator" / "scripts" / "_create_oscillator.py",
    ),
    "oscillator_system_python": (
        module_path / "00_run_script" / "oscillator" / "scripts" / "_create_oscillator.py",
    ),
    "create_all_possible_nodes": None,
    "etk_abaqus": (
        module_path / "00_run_script" / "etk_abaqus" / "files" / "oscillator.inp",
        module_path / "00_run_script" / "etk_abaqus" / "files" / "oscillator.odb",
    ),
    "python_help": None,
    "python_node": None,
    "optimizer_settings": None,
    "sensitivity_settings": None,
    "simple_calculator": (module_path / "00_run_script" / "files" / "calculator.opf",),
    "calculator_with_params": (
        module_path / "00_run_script" / "files" / "calculator_with_params.opf",
    ),
    "nodes_connection": (module_path / "00_run_script" / "files" / "connect_nodes.opf",),
    "nested_systems": (module_path / "00_run_script" / "files" / "nested_systems.opf",),
    "ten_bar_truss": (module_path / "00_run_script" / "files" / "ten_bar_truss.opf",),
    "omdb_files": (module_path / "00_run_script" / "files" / "omdb_files.opf",),
}

# dictionary of scripts to be run
example_scripts = {
    "ansys_workbench_portscan": module_path
    / "00_run_script"
    / "scripts"
    / "ansys_workbench_portscan.py",
    "arsm_ten_bar_truss": module_path
    / "00_run_script"
    / "ten_bar_truss"
    / "scripts"
    / "arsm_ten_bar_truss.py",
    "ansys_workbench_ten_bar_truss": module_path
    / "00_run_script"
    / "ten_bar_truss"
    / "scripts"
    / "ansys_workbench_ten_bar_truss.py",
    "ten_bar_modify_parameters": module_path
    / "00_run_script"
    / "ten_bar_truss"
    / "scripts"
    / "ten_bar_modify_parameters.py",
    "ten_bar_truss_lc2": module_path
    / "00_run_script"
    / "ten_bar_truss"
    / "scripts"
    / "ten_bar_truss_lc2.py",
    "oscillatorcalibration_system_ascii": module_path
    / "00_run_script"
    / "oscillator"
    / "scripts"
    / "oscillatorcalibration_system_ascii.py",
    "oscillatorcalibration_system_python": module_path
    / "00_run_script"
    / "oscillator"
    / "scripts"
    / "oscillatorcalibration_system_python.py",
    "oscillator_optimization_ea": module_path
    / "00_run_script"
    / "oscillator"
    / "scripts"
    / "oscillator_optimization_ea.py",
    "oscillator_optimization_on_mop": module_path
    / "00_run_script"
    / "oscillator"
    / "scripts"
    / "oscillator_optimization_on_mop.py",
    "oscillator_robustness_arsm": module_path
    / "00_run_script"
    / "oscillator"
    / "scripts"
    / "oscillator_robustness_arsm.py",
    "oscillator_sensitivity_mop": module_path
    / "00_run_script"
    / "oscillator"
    / "scripts"
    / "oscillator_sensitivity_mop.py",
    "oscillator_system_python": module_path
    / "00_run_script"
    / "oscillator"
    / "scripts"
    / "oscillator_system_python.py",
    "create_all_possible_nodes": module_path
    / "00_run_script"
    / "scripts"
    / "create_all_possible_nodes.py",
    "etk_abaqus": module_path / "00_run_script" / "etk_abaqus" / "scripts" / "etk_abaqus.py",
    "python_help": module_path / "00_run_script" / "python" / "scripts" / "python_help.py",
    "python_node": module_path / "00_run_script" / "python" / "scripts" / "python_node.py",
    "optimizer_settings": module_path / "00_run_script" / "scripts" / "optimizer_settings.py",
    "sensitivity_settings": module_path / "00_run_script" / "scripts" / "sensitivity_settings.py",
    "simple_calculator": module_path / "00_run_script" / "scripts" / "simple_calculator.py",
    "calculator_with_params": None,
    "nodes_connection": None,
    "nested_systems": None,
    "ten_bar_truss": None,
    "omdb_files": None,
}
