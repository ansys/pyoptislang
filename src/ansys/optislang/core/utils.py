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

"""Utitilies module."""
from __future__ import annotations

import collections
from enum import Enum, EnumMeta
import os
from pathlib import Path
import re
from typing import DefaultDict, Dict, Iterable, Iterator, List, Optional, OrderedDict, Tuple, Union

from ansys.optislang.core import FIRST_SUPPORTED_VERSION

VersionMapping = Dict[int, Path]


def enum_from_str(
    string: str,
    enum_class: EnumMeta,
    replace: Optional[Tuple[str, str]] = None,
    upper_case: bool = True,
) -> Enum:
    """Convert string to enumeration.

    Parameters
    ----------
    string: str
        String to be converted.
    enum_class: Enum
        Enumeration type, upper case enumeration items are expected.
    replace: Optional[Tuple[str, str]], optional
        Characters to be replaced in given ``string``.
            Tuple[0]: Replace from.
            Tuple[1]: Replace to.
    upper_case: bool, optional
        Whether string should be converted to upper_case. Defaults to `True`.

    Returns
    -------
    Enum
        Instance of given enumeration type.

    Raises
    ------
    TypeError
        Raised when the type of the ``string`` or the enum_class is invalid.
    ValueError
        Raised when the value for the ``string`` is invalid.
    """
    if not isinstance(string, str):
        raise TypeError(f"String was expected, but `{type(string)}` was given.")
    if not issubclass(enum_class, Enum):
        raise TypeError(f"Enumeration class was expected, but `{type(enum_class)}` was given.")
    if replace is not None:
        string = string.replace(replace[0], replace[1])
    if upper_case:
        string = string.upper()
    try:
        return enum_class[string]
    except:
        raise ValueError(f"{string} is not a member of {enum_class.__name__}.")


def get_osl_exec(osl_version: Optional[Union[int, str]] = None) -> Optional[Tuple[int, Path]]:
    """Get the path to the optiSLang executable file.

    Parameters
    ----------
    osl_version : Optional[Union[int, str]], optional
        optiSLang version in a three-digit format like this ``221``. The default
        is ``None``, in which case the latest installed version is used.

    Returns
    -------
    Optional[Tuple[int, pathlib.Path]]
        optiSLang version and path to the corresponding executable file, if it exists.
        If both Ansys and standalone installations are present, the latest Ansys
        installation is returned. If no executable file is found for a specified
        version, ``None`` is returned.

    Raises
    ------
    NotImplementedError
        Raised when the operating system is not supported.
    """
    osl_execs = find_all_osl_exec()
    if len(osl_execs) == 0:
        return None

    if isinstance(osl_version, str):
        try:
            osl_version = int(osl_version)
        except ValueError:
            return None

    if osl_version is not None:
        return (osl_version, osl_execs[osl_version][0]) if osl_version in osl_execs else None
    else:
        # It is assumed that the first item corresponds to the latest optiSLang version
        osl_version = next(iter(osl_execs.keys()))
        return (osl_version, osl_execs[osl_version][0])


def find_all_osl_exec() -> OrderedDict[int, Tuple[Path, ...]]:
    """Find all optiSLang executable files.

    Returns
    -------
    OrderedDict[int, Tuple[Path, ...]]
        Ordered dictionary of found optiSLang executables. The dictionary key corresponds
        to the optiSLang version and value to the tuple of the optiSLang executable paths.
        Ansys installations are first in the tuple, followed by standalone installations.
        The dictionary is sorted by the version number in descending order.

    Raises
    ------
    NotImplementedError
        Raised when the operating system is not supported.
    """
    # windows
    if os.name == "nt":
        return _find_all_osl_exec_in_windows()
    # linux
    elif os.name == "posix":
        return _find_all_osl_exec_in_posix()
    # another os
    else:
        raise NotImplementedError(f"Unsupported OS {os.name}.")


def get_osl_opx_import_script(osl_executable: Optional[Union[str, Path]] = None) -> Optional[Path]:
    """Get the path to the optiSLang OPX import script file.

    Parameters
    ----------
    osl_executable : Optional[Union[str, pathlib.Path]], optional
        optiSLang executable path to use as a reference for locating the import script file.
        The default is ``None``, in which case the default optiSLang executable file is used.

    Returns
    -------
    Optional[Path]
        Path to the optiSLang OPX import script file, if location succeeded,
        ``None`` is returned otherwise.

    Raises
    ------
    NotImplementedError
        Raised when the operating system is not supported.
    """
    if osl_executable is None:
        installed_version = get_osl_exec()
        if installed_version is not None:
            osl_executable = installed_version[1]

    if osl_executable is not None:
        osl_opx_import_script_path = (
            Path(osl_executable).parent / "tools" / "import" / "opx" / "convert_opx_to_opf.py"
        )
        if osl_opx_import_script_path.is_file():
            return osl_opx_import_script_path

    return None


def _find_all_osl_exec_in_windows() -> OrderedDict[int, Tuple[Path, ...]]:
    """Find all optiSLang executable files on Windows.

    Returns
    -------
    OrderedDict[int, Tuple[Path, ...]]
        Ordered dictionary of found optiSLang executables. The dictionary key corresponds
        to the optiSLang version and value to the tuple of the optiSLang executable paths.
        The dictionary is sorted by the version number in descending order.
    """
    all_osl_execs = _merge_osl_exec_dicts(
        [
            _find_ansys_osl_execs_in_envars("optislang.com"),
            _find_ansys_osl_execs_in_windows_program_files(),
            _find_standalone_osl_execs_in_windows(),
        ]
    )

    return _sort_osl_execs(all_osl_execs)


def _find_all_osl_exec_in_posix() -> OrderedDict[int, Tuple[Path, ...]]:
    """Find all optiSLang executable files on POSIX-compliant systems.

    Returns
    -------
    OrderedDict[int, Tuple[pathlib.Path, ...]]
        Ordered dictionary of found optiSLang executables. The dictionary key corresponds
        to the optiSLang version and value to the tuple of the optiSLang executable paths.
        The dictionary is sorted by the version number in descending order.
    """
    all_osl_execs = _merge_osl_exec_dicts(
        [
            _find_ansys_osl_execs_in_envars("optislang"),
            _find_ansys_osl_execs_in_posix(),
            _find_standalone_osl_execs_in_posix(),
        ]
    )

    return _sort_osl_execs(all_osl_execs)


def _find_ansys_osl_execs_in_envars(exec_name: str) -> VersionMapping:
    """Find optiSLang executable files based on environmental variables.

    The Ansys ``AWP_ROOT`` environment variable is used to determine the root directory of the Ansys
    installation.

    Parameters
    ----------
    exec_name : str
        optiSLang executable name.

    Returns
    -------
    Dict[int, pathlib.Path]
        Dictionary of found optiSLang executables. The dictionary key is an optiSLang version.
        The dictionary value is a path to the corresponding optiSLang executable file.
    """
    osl_execs = {}
    for version, awp_root_value in iter_awp_roots():
        osl_exec_path = awp_root_value / "optiSLang" / exec_name
        if osl_exec_path.is_file() and version >= FIRST_SUPPORTED_VERSION:
            osl_execs[version] = osl_exec_path
    return osl_execs


def _find_ansys_osl_execs_in_windows_program_files() -> VersionMapping:
    """Find optiSLang executable files in the ``Program Files`` directory on Windows.

    This search is performed in the standard installation directory of Ansys products.

    Returns
    -------
    Dict[int, pathlib.Path]
        Dictionary of found optiSLang executables. The dictionary key is an optiSLang version.
        The dictionary value is a path to the corresponding optiSLang executable file.
    """
    osl_execs = {}
    program_files_path = _get_program_files_path()
    for ansys_version_dir in (program_files_path / "ANSYS Inc").glob("v*/"):
        try:
            ansys_version = int(ansys_version_dir.name[1:])
        except ValueError:
            continue
        if ansys_version >= FIRST_SUPPORTED_VERSION:
            osl_exec_path = ansys_version_dir / "optiSLang" / "optislang.com"
            if osl_exec_path.is_file():
                osl_execs[ansys_version] = osl_exec_path
    return osl_execs


def _find_standalone_osl_execs_in_windows() -> VersionMapping:
    """Find executable files of standalone optiSLang installations on Windows.

    Returns
    -------
    Dict[int, pathlib.Path]
        Dictionary of found optiSLang executables. The dctionary key is an optiSLang version.
        The dictionary value is a path to the corresponding optiSLang executable file.
    """
    osl_execs = {}

    root_install_dirs = [
        _get_program_files_path() / "Dynardo" / "Ansys optiSLang",
        _get_program_files_path() / "Ansys optiSLang",
    ]
    for root_install_dir in root_install_dirs:
        if root_install_dir.is_dir():
            for osl_version_dir in root_install_dir.glob("*/"):
                osl_exec_path = osl_version_dir / "optislang.com"
                if os.path.isfile(osl_exec_path):
                    # convert version fmt "yyyy Rx" to "yyx"
                    # TODO: add '$' at the end of regex pattern to disable dev version
                    match = re.findall("[2][0][1-9][0-9] R[1-9]", str(osl_version_dir))
                    if match:
                        try:
                            ansys_version = int(match[0][2:4] + match[0][6])
                        except ValueError:
                            continue
                        if ansys_version >= FIRST_SUPPORTED_VERSION:
                            osl_execs[ansys_version] = osl_exec_path
    return osl_execs


def _find_ansys_osl_execs_in_posix() -> VersionMapping:
    """Find optiSLang executable files in default Ansys paths on POSIX-compliant systems.

    This search is performed in standard installation paths of Ansys products.

    Returns
    -------
    Dict[int, pathlib.Path]
        Dictionary of found optiSLang executables. The dictionary key is an optiSLang version.
        The dictionary value is a path to the corresponding optiSLang executable file.
    """
    osl_execs = {}
    base_path = None
    for ansys_dir in [Path("/usr/ansys_inc"), Path("/ansys_inc")]:
        if ansys_dir.is_dir():
            base_path = ansys_dir
    if base_path is not None:
        for ansys_version_dir in base_path.glob("v*/"):
            try:
                ansys_version = int(ansys_version_dir.name[1:])
            except ValueError:
                continue
            if ansys_version >= FIRST_SUPPORTED_VERSION:
                osl_exec_path = ansys_version_dir / "optiSLang" / "optislang"
                if osl_exec_path.is_file():
                    osl_execs[ansys_version] = osl_exec_path
    return osl_execs


def _find_standalone_osl_execs_in_posix() -> VersionMapping:
    """Find the executable files of standalone optiSLang installations on POSIX-compliant systems.

    Returns
    -------
    Dict[int, pathlib.Path]
        Dictionary of found optiSLang executables. The dictionary key is an optiSLang version.
        The dictionary value is a path to the corresponding optiSLang executable file.
    """
    osl_execs = {}
    root_install_dir = Path("/opt/dynardo")
    if root_install_dir.is_dir():
        for osl_version_dir in root_install_dir.glob("*/"):
            osl_exec_path = osl_version_dir / "optislang"
            if osl_exec_path.is_file():
                # convert version fmt "yyyy Rx" to "yyx"
                # TODO: add '$' at the end of regex pattern to disable dev version
                match = re.findall("[2][0][1-9][0-9]R[1-9]", str(osl_version_dir))
                if match:
                    try:
                        ansys_version = int(match[0][2:4] + match[0][5])
                    except ValueError:
                        continue
                    if ansys_version >= FIRST_SUPPORTED_VERSION:
                        osl_execs[ansys_version] = osl_exec_path
    return osl_execs


def _merge_osl_exec_dicts(osl_execs_dicts: Iterable[VersionMapping]) -> Dict[int, Tuple[Path, ...]]:
    """Merge dictionaries of optiSLang executable files into one dictionary.

    Parameters
    ----------
    osl_execs_dicts : Iterable[Dict[int, pathlib.Path]]
        Iterable of dictionaries of optiSLang executable files. In each dictionary,
        the key is an optiSLang version. The value is a corresponding path to the
        optiSLang executable file.

    Returns
    -------
    Dict[int, Tuple[pathlib.Path, ...]]
        Merged dictionary in which the key is an optiSLang version and the value is
        a tuple of paths to the corresponding optiSLang executable files.
    """
    osl_execs_merged: DefaultDict[int, List[Path]] = collections.defaultdict(list)

    for osl_execs in osl_execs_dicts:
        for osl_version, exec_path in osl_execs.items():
            if exec_path not in osl_execs_merged[osl_version]:
                osl_execs_merged[osl_version].append(exec_path)

    return {version: tuple(execs_paths) for version, execs_paths in osl_execs_merged.items()}


def _sort_osl_execs(osl_execs: Dict[int, Tuple[Path, ...]]) -> OrderedDict[int, Tuple[Path, ...]]:
    """Sort the dictionary of optiSLang executable files according to version in descending order.

    Parameters
    ----------
    osl_execs : Dict[int, Tuple[str, ...]]
        Dictionary of optiSLang executables. The dictionary key is an optiSLang version. The
        value is a tuple of paths to the optiSLang executable files.

    Returns
    -------
    OrderedDict[int, Tuple[str, ...]]
        Sorted ordered dictionary of optiSLang executable files. The dictionary key is an optiSLang
        version. The value is a tuple of paths to the optiSLang executable files.
    """
    return collections.OrderedDict(sorted(osl_execs.items(), reverse=True))


def _get_program_files_path() -> Path:
    """Get the path for the ``Program Files`` directory on Windows.

    Returns
    -------
    str
        Path to the ``Program Files`` directory.
    """
    return Path(os.environ.get("ProgramFiles", "C:\\Program Files"))


def iter_awp_roots() -> Iterator[Tuple[int, Path]]:
    """Iterate AWP_ROOTXXX environment variables.

    Yields
    -------
    tuple
        Ansys version and the respective root directory.
    """
    for varname, value in os.environ.copy().items():
        varname_match = re.fullmatch(r"AWP_ROOT([0-9]{3})", varname)
        if varname_match:
            yield int(varname_match.group(1)), Path(value)
