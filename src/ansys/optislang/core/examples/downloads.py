"""Download files from repository."""

import os
from pathlib import Path
from typing import Tuple

import ansys.optislang.core.examples as examples

# TODO: implement automatic download from online repository
# EXAMPLE_REPO = "https://github.com/ansys/pyoptislang/tree/main/examples/files"


def _download_files(scriptname: str) -> Tuple[Path, ...]:
    """Check if files exists, otherwise download them. Return path to files then."""
    # check if file was downloaded
    for file_path in examples.example_files[scriptname]:
        if not file_path.is_file():
            NotImplementedError("Automatic download not implemented.")

    return examples.example_files[scriptname]


def _download_script(scriptname: str) -> Path:
    """Check if file exists, otherwise download it. Return path to file then."""
    # check if script was downloaded, download it if not
    local_path = examples.example_scripts[scriptname]

    if not local_path.is_file():
        NotImplementedError("Automatic download not implemented.")

    return local_path


def get_files(scriptname: str) -> Tuple[Path, Tuple[Path, ...]]:
    """Get tuple of files necessary for running example.

    Parameters
    ----------
    scriptname: str
        Name of the example script (without ``.py``).

    Returns
    -------
    Tuple[Path, Tuple[Path, ...]]
        Tuple[0]: path to script
        Tuple[1]: tuple of paths to files necessary for running script
    """
    if examples.example_files[scriptname] is not None:
        file_path = _download_files(scriptname)
    else:
        file_path = None

    if examples.example_scripts[scriptname] is not None:
        script_path = _download_script(scriptname)
    else:
        script_path = None

    return (script_path, file_path)
