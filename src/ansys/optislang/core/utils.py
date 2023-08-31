"""Utitilies module."""
from __future__ import annotations

import collections
from enum import Enum
import os
from pathlib import Path
import re
from typing import Dict, Iterable, Optional, OrderedDict, Tuple, Union

from ansys.optislang.core import FIRST_SUPPORTED_VERSION


def enum_from_str(
    string: str, enum_class: Enum, replace: Union[Tuple[str, str], None] = None
) -> Enum:
    """Convert string to enumeration.

    Parameters
    ----------
    string: str
        String to be converted.
    enum_class: Enum
        Enumeration type, upper case enumeration items are expected.
    replace: Union[Tuple[str, str], None], optional
        Characters to be replaced in given ``string``.
            Tuple[0]: Replace from.
            Tuple[1]: Replace to.

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
    string = string.upper()
    if replace is not None:
        string = string.replace(replace[0], replace[1])
    try:
        enum_type = enum_class[string]
        return enum_type
    except:
        raise ValueError(f"``{string}`` not available in ``{enum_class.__name__}``.")


def get_osl_exec(osl_version: Union[int, str, None] = None) -> Union[Tuple[int, Path], None]:
    """Get the path to the optiSLang executable file.

    Parameters
    ----------
    osl_version : int, str, None, optional
        optiSLang version in a three-digit format like this ``221``. The default
        is ``None``, in which case the latest installed version is used.

    Returns
    -------
    Tuple[int, pathlib.Path], None
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

    if osl_version is not None:
        osl_version = _try_cast_str_to_int(osl_version)
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


def get_osl_opx_import_script(osl_executable: Union[str, Path] = None) -> Optional[Path]:
    """Get the path to the optiSLang OPX import script file.

    Parameters
    ----------
    osl_executable : Union[str, pathlib.Path], optional
        optiSLang executable path to use as a reference for locating the import script file.
        The default is ``None``, in which case the default optiSLang executable file is used.

    Returns
    -------
    Tuple[int, pathlib.Path], None
        Path to the optiSLang OPX import script file, if location succeeded,
        ``None`` is returned otherwise.

    Raises
    ------
    NotImplementedError
        Raised when the operating system is not supported.
    """
    if osl_executable is None:
        osl_executable = get_osl_exec()[1]

    if osl_executable is not None:
        osl_opx_import_script_path = (
            osl_executable.parent / "tools" / "import" / "opx" / "convert_opx_to_opf.py"
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
            _find_ansys_osl_execs_in_windows_envars(),
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
        [_find_ansys_osl_execs_in_posix(), _find_standalone_osl_execs_in_posix()]
    )

    return _sort_osl_execs(all_osl_execs)


def _find_ansys_osl_execs_in_windows_envars() -> Dict[int, Path]:
    """Find optiSLang executable files based on environmental variables on Windows.

    The Ansys ``AWP_ROOT`` environment variable is used to determine the root directory of the Ansys
    installation.

    Returns
    -------
    Dict[int, pathlib.Path]
        Dictionary of found optiSLang executables. The dictionary key is an optiSLang version.
        The dictionary value is a path to the corresponding optiSLang executable file.
    """
    osl_execs = {}
    awp_root_envars = _get_environ_vars(pattern=f"^AWP_ROOT.*")
    for awp_root_key, awp_root_value in awp_root_envars.items():
        osl_exec_path = Path(awp_root_value) / "optiSLang" / "optislang.com"
        if osl_exec_path.is_file():
            ansys_version = _try_cast_str_to_int(awp_root_key[-3:])
            if ansys_version >= FIRST_SUPPORTED_VERSION:
                osl_execs[ansys_version] = osl_exec_path
    return osl_execs


def _find_ansys_osl_execs_in_windows_program_files() -> Dict[int, Path]:
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
        ansys_version = _try_cast_str_to_int(ansys_version_dir.name[1:])
        if ansys_version >= FIRST_SUPPORTED_VERSION:
            osl_exec_path = ansys_version_dir / "optiSLang" / "optislang.com"
            if osl_exec_path.is_file():
                osl_execs[ansys_version] = osl_exec_path
    return osl_execs


def _find_standalone_osl_execs_in_windows() -> Dict[int, Path]:
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
                        ansys_version = _try_cast_str_to_int(match[0][2:4] + match[0][6])
                        if ansys_version >= FIRST_SUPPORTED_VERSION:
                            osl_execs[ansys_version] = osl_exec_path
    return osl_execs


def _find_ansys_osl_execs_in_posix() -> Dict[int, Path]:
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
            ansys_version = _try_cast_str_to_int(ansys_version_dir.name[1:])
            if ansys_version >= FIRST_SUPPORTED_VERSION:
                osl_exec_path = ansys_version_dir / "optiSLang" / "optislang"
                if osl_exec_path.is_file():
                    osl_execs[ansys_version] = osl_exec_path
    return osl_execs


def _find_standalone_osl_execs_in_posix() -> Dict[int, Path]:
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
                    ansys_version = _try_cast_str_to_int(match[0][2:4] + match[0][5])
                    if ansys_version >= FIRST_SUPPORTED_VERSION:
                        osl_execs[ansys_version] = osl_exec_path
    return osl_execs


def _merge_osl_exec_dicts(
    osl_execs_dicts: Iterable[Dict[int, Path]]
) -> Dict[int, Tuple[Path, ...]]:
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
    osl_execs_merged = {}
    for osl_execs in osl_execs_dicts:
        for osl_version, exec_path in osl_execs.items():
            if osl_version not in osl_execs_merged:
                osl_execs_merged[osl_version] = [exec_path]
            else:
                if exec_path not in osl_execs_merged[osl_version]:
                    osl_execs_merged[osl_version].append(exec_path)

    # convert list of version to tuple
    for osl_version, execs_paths in osl_execs_merged.items():
        osl_execs_merged[osl_version] = tuple(execs_paths)

    return osl_execs_merged


def _sort_osl_execs(osl_execs: Dict[int, Tuple[str, ...]]) -> OrderedDict[int, Tuple[str, ...]]:
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


def _get_environ_vars(pattern: str = ".*") -> Dict:
    """Get a dictionary of matching environment variables.

    Parameters
    ----------
    pattern: str, optional
        Regular expression pattern to use for searching environment variables.

    Returns
    -------
    dict
        Dictionary of matching environment variables.
    """
    sys_vars = os.environ.copy()
    dictionary = {}
    for varname, value in sys_vars.items():
        varname_match = re.search(pattern, varname)
        if varname_match:
            dictionary[varname] = value
    return dictionary


def _try_cast_str_to_int(str_value: str) -> Union[int, str]:
    """Try to parse a string value to an integer.

    Parameters
    ----------
    str_value : str
        String value.

    Returns
    -------
    Union[int, str]
        Returns the string value as an integer if the string value can
        be parsed. Otherwise, the string value itself is returned.
    """
    try:
        return int(str_value)
    except:
        return str_value
