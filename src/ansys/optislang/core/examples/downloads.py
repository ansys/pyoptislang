"""Download files from repository."""

import os
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Tuple

from ansys.optislang.core.examples.examples import ExampleFiles, example_files, example_scripts

# TODO: implement automatic download from online repository
# EXAMPLE_REPO = "https://github.com/ansys/pyoptislang/tree/main/examples/files"


def _download_files(scriptname: str) -> Optional[ExampleFiles]:
    """Check if files exists, otherwise download them. Return path to files then."""
    # check if file was downloaded
    file_paths = example_files[scriptname]

    if file_paths is not None:
        for file_path in file_paths:
            if not file_path.is_file():
                NotImplementedError("Automatic download not implemented.")

    return file_paths


def _download_script(scriptname: str) -> Optional[Path]:
    """Check if file exists, otherwise download it. Return path to file then."""
    # check if script was downloaded, download it if not
    script_path = example_scripts[scriptname]

    if script_path is not None and not script_path.is_file():
        NotImplementedError("Automatic download not implemented.")

    return script_path


def get_files(scriptname: str) -> Tuple[Optional[Path], Optional[ExampleFiles]]:
    """Get tuple of files necessary for running example.

    Parameters
    ----------
    scriptname: str
        Name of the example script (without ``.py``).

    Returns
    -------
    Tuple[Optional[Path], Optional[Tuple[Path, ...]]]
        Tuple[0]: path to script
        Tuple[1]: tuple of paths to files necessary for running script
    """
    if example_files[scriptname] is not None:
        file_paths = _download_files(scriptname)
    else:
        file_paths = None

    if example_scripts[scriptname] is not None:
        script_path = _download_script(scriptname)
    else:
        script_path = None

    return script_path, file_paths
