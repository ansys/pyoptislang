"""Download files from repository."""

import os
from pathlib import Path
from typing import Tuple

import ansys.optislang.core.examples as examples

# TODO: implement automatic download from online repository
# EXAMPLE_REPO = "https://github.com/pyansys/pyoptislang/tree/main/examples/files"


def _download_file(scriptname: str) -> Tuple[Path, ...]:
    """Check if file exists, otherwise download it. Return path to file then."""
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
    """Insert name of the example script (without ``.py``) and get local_path."""
    if examples.example_files[scriptname] is not None:
        file_path = _download_file(scriptname)
    else:
        file_path = None

    script_path = _download_script(scriptname)

    return (script_path, file_path)
