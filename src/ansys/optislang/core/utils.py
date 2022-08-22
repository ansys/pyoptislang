"""Utitilies module."""
import collections
from glob import glob
import os
import re
from typing import Dict, Iterable, OrderedDict, Tuple, Union


def get_osl_exec(osl_version: Union[int, str, None] = None) -> Union[Tuple[int, str], None]:
    """Return path to the optiSLang executable file.

    Parameters
    ----------
    osl_version : int, str, None, optional
        optiSLang version (e.g. 221). If ``None``, the latest available version is assumed.
        Defaults to ``None``.

    Returns
    -------
    Tuple[int, str], None
        optiSLang version and path to the corresponding executable, if exists. If both ANSYS
        and standalone installations are present, ANSYS installation is returned. If no executable
        is found for specified version, returns ``None``.

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
        # It is assumed that the first item corresponds to the latest optiSLang
        osl_version = next(iter(osl_execs.keys()))
        return (osl_version, osl_execs[osl_version][0])


def find_all_osl_exec() -> OrderedDict[int, Tuple[str, ...]]:
    """Find available optiSLang executables.

    Returns
    -------
    OrderedDict[int, Tuple[str, ...]]
        Ordered dictionary of found optiSLang executables. The dictionary key corresponds
        to the optiSLang version and value to the tuple of optiSLang executable paths (ansys
        installation is first in the tuple, standalone installations then). The dictionary is
        sorted by the version number in descending order.

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


def _find_all_osl_exec_in_windows() -> OrderedDict[int, Tuple[str, ...]]:
    """Find all optiSLang executables on Windows operating system.

    Returns
    -------
    OrderedDict[int, Tuple[str, ...]]
        Ordered dictionary of found optiSLang executables. The dictionary key corresponds
        to the optiSLang version and value to the tuple of optiSLang executable paths.
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


def _find_all_osl_exec_in_posix() -> OrderedDict[int, Tuple[str, ...]]:
    """Find all optiSLang executables on POSIX compliant operating systems.

    Returns
    -------
    OrderedDict[int, Tuple[str, ...]]
        Ordered dictionary of found optiSLang executables. The dictionary key corresponds
        to the optiSLang version and value to the tuple of optiSLang executable paths.
        The dictionary is sorted by the version number in descending order.
    """
    all_osl_execs = _merge_osl_exec_dicts(
        [_find_ansys_osl_execs_in_posix(), _find_standalone_osl_execs_in_posix()]
    )

    return _sort_osl_execs(all_osl_execs)


def _find_ansys_osl_execs_in_windows_envars() -> Dict[int, str]:
    """Find optiSLang executables based on environmental variables on Windows operating system.

    Ansys AWP_ROOT environment variable is used to determine the root directory of the ANSYS
    installation.

    Returns
    -------
    Dict[int, str]
        Dictionary of found optiSLang executables. Dictionary key is an optiSLang version and
        dictionary value is a path to the corresponding optiSLang executable.
    """
    osl_execs = {}
    awp_root_envars = _get_environ_vars(pattern=f"^AWP_ROOT.*")
    for awp_root_key, awp_root_value in awp_root_envars.items():
        osl_exec_path = os.path.join(awp_root_value, "optiSlang", "optislang.com")
        if os.path.isfile(osl_exec_path):
            ansys_version = _try_cast_str_to_int(awp_root_key[-3:])
            osl_execs[ansys_version] = osl_exec_path
    return osl_execs


def _find_ansys_osl_execs_in_windows_program_files() -> Dict[int, str]:
    """Find optiSLang executables in Program Files directory on Windows operating system.

    Search is performed in standard installation directory of ANSYS products.

    Returns
    -------
    Dict[int, str]
        Dictionary of found optiSLang executables. Dictionary key is an optiSLang version and
        dictionary value is a path to the corresponding optiSLang executable.
    """
    osl_execs = {}
    program_files_path = _get_program_files_path()
    for ansys_version_dir in glob(os.path.join(program_files_path, "ANSYS Inc", "v*")):
        ansys_version = _try_cast_str_to_int(ansys_version_dir[-3:])
        osl_exec_path = os.path.join(ansys_version_dir, "optiSLang", "optislang.com")
        if os.path.isfile(osl_exec_path):
            osl_execs[ansys_version] = osl_exec_path
    return osl_execs


def _find_standalone_osl_execs_in_windows() -> Dict[int, str]:
    """Find executables of standalone optiSLang installations on Windows operating system.

    Returns
    -------
    Dict[int, str]
        Dictionary of found optiSLang executables. Dictionary key is an optiSLang version and
        dictionary value is a path to the corresponding optiSLang executable.
    """
    osl_execs = {}
    root_install_dir = os.path.join(_get_program_files_path(), "Dynardo", "Ansys optiSLang")
    if os.path.isdir(root_install_dir):
        for osl_version_dir in glob(os.path.join(root_install_dir, "*")):
            osl_exec_path = os.path.join(root_install_dir, osl_version_dir, "optislang.com")
            if os.path.isfile(osl_exec_path):
                # convert version fmt "yyyy Rx" to "yyx"
                ansys_version = _try_cast_str_to_int(osl_version_dir[-5:-3] + osl_version_dir[-1:])
                osl_execs[ansys_version] = osl_exec_path
    return osl_execs


def _find_ansys_osl_execs_in_posix() -> Dict[int, str]:
    """Find optiSLang executables in default ANSYS paths on POSIX compliant operating systems.

    Search is performed in standard installation paths of ANSYS products.

    Returns
    -------
    Dict[int, str]
        Dictionary of found optiSLang executables. Dictionary key is an optiSLang version and
        dictionary value is a path to the corresponding optiSLang executable.
    """
    osl_execs = {}
    base_path = None
    for ansys_dir in ["/usr/ansys_inc", "/ansys_inc"]:
        if os.path.isdir(ansys_dir):
            base_path = ansys_dir
    if base_path is not None:
        for ansys_version_dir in glob(os.path.join(base_path, "v*")):
            ansys_version = _try_cast_str_to_int(ansys_version_dir[-3:])
            osl_exec_path = os.path.join(ansys_version_dir, "optiSLang", "optislang")
            if os.path.isfile(osl_exec_path):
                osl_execs[ansys_version] = osl_exec_path
    return osl_execs


def _find_standalone_osl_execs_in_posix() -> Dict[int, str]:
    """Find executables of standalone optiSLang installations on POSIX compliant operating systems.

    Returns
    -------
    Dict[int, str]
        Dictionary of found optiSLang executables. Dictionary key is an optiSLang version and
        dictionary value is a path to the corresponding optiSLang executable.
    """
    osl_execs = {}
    root_install_dir = "/opt/dynardo"
    if os.path.isdir(root_install_dir):
        for osl_version_dir in glob(os.path.join(root_install_dir, "*")):
            osl_exec_path = os.path.join(root_install_dir, osl_version_dir, "optislang")
            if os.path.isfile(osl_exec_path):
                # convert version fmt "yyyy Rx" to "yyx"
                ansys_version = _try_cast_str_to_int(osl_version_dir[-4:-2] + osl_version_dir[-1:])
                osl_execs[ansys_version] = osl_exec_path
    return osl_execs


def _merge_osl_exec_dicts(osl_execs_dicts: Iterable[Dict[int, str]]) -> Dict[int, Tuple[str, ...]]:
    """Merge dictionaries of optiSLang executables into one dictionary.

    Parameters
    ----------
    osl_execs_dicts : Iterable[Dict[int, str]]
        Iterable of dictionaries of optiSLang executables. In each dictionary, key is an optiSLang
        version and value is a corresponding path to the optiSLang executable.

    Returns
    -------
    Dict[int, Tuple[str, ...]]
        Merged dictionary in which the key is an optiSLang version and value is a tuple of paths
        to the corresponding optiSLang executables.
    """
    osl_execs_merged = {}
    for osl_execs in osl_execs_dicts:
        for osl_version, exec_path in osl_execs.items():
            if osl_version not in osl_execs_dicts:
                osl_execs_merged[osl_version] = [exec_path]
            else:
                osl_execs_merged[osl_version].append(exec_path)

    # convert list of version to tuple
    for osl_version, execs_paths in osl_execs_merged.items():
        osl_execs_merged[osl_version] = tuple(execs_paths)

    return osl_execs_merged


def _sort_osl_execs(osl_execs: Dict[int, Tuple[str, ...]]) -> OrderedDict[int, Tuple[str, ...]]:
    """Sort dictionary of optiSLang executables according to the version in descending order.

    Parameters
    ----------
    osl_execs : Dict[int, Tuple[str, ...]]
        Dictionary of optiSLang executables. Dictionary key is an optiSLang version and value is
        a tuple of paths to the optiSLang executables.

    Returns
    -------
    OrderedDict[int, Tuple[str, ...]]
        Sorted ordered dictionary of optiSLang executables. Dictionary key is an optiSLang version
        and value is a tuple of paths to the optiSLang executables.
    """
    return collections.OrderedDict(sorted(osl_execs.items(), reverse=True))


def _get_program_files_path() -> str:
    """Get the "Program Files" directory path on Windows operating system.

    Returns
    -------
    str
        Path to the "Program Files" directory.
    """
    return os.environ.get("ProgramFiles", "C:\\Program Files")


def _get_environ_vars(pattern: str = ".*") -> Dict:
    """Return dict of matching environment variables.

    Parameters
    ----------
    pattern: str, optional
        Regular expression pattern used to search environment variables.

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
    """Try to parse string value to integer.

    Parameters
    ----------
    str_value : str
        String value to be parsed to integer.

    Returns
    -------
    Union[int, str]
        Returns value as integer, if it can be parsed; Otherwise, the value as string is returned.
    """
    try:
        return int(str_value)
    except:
        return str_value
