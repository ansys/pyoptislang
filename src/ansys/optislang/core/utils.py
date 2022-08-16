"""Utitilies module."""
import collections
from glob import glob
import os
import re
from typing import Dict, OrderedDict, Tuple, Union


def get_osl_exec(osl_version: Union[int, str] = None) -> Union[Tuple[int, str], None]:
    """Return path to the optiSLang executable file.

    Parameters
    ----------
    osl_version : int, str, None, optional
        optiSLang version (e.g. 221). If ``None``, the latest available version is assumed.
        Defaults to ``None``.

    Returns
    -------
    Tuple[int, str], None
        optiSLang version and path to the corresponding executable, if exists (if both ansys
        and standalone installations are present, returns ansys installation); Otherwise, ``None``.
    """
    osl_versions = find_all_osl_exec()
    if len(osl_versions) == 0:
        return None

    if osl_version is not None:
        osl_version = _try_parse_str_to_int(osl_version)
        return (osl_version, osl_versions[osl_version][0]) if osl_version in osl_versions else None
    else:
        # It is assumed that the first item corresponds to the latest optiSLang
        osl_version = next(iter(osl_versions.keys()))
        return (osl_version, osl_versions[osl_version][0])


def find_all_osl_exec() -> OrderedDict[int, Tuple[str, ...]]:
    """Find available optiSLang applications.

    Tries to find paths to available optiSLang executables.

    Returns
    -------
    OrderedDict[int, Tuple[str, ...]]
        Ordered dictionary of found optiSLang applications. The dictionary key corresponds
        to the optiSLang version and value to the tuple of optiSLang executable paths (ansys
        installation is first in the tuple, standalone installations then). The dictionary is
        sorted by the version number in descending order.

    Raises
    ------
    NotImplementedError
        Raised when the operating system is not supported.
    """
    # TODO: Support search for standalone optiSLang as well
    osl_versions = {}
    # windows
    if os.name == "nt":
        # Get all AWP_ROOT system variables which determine the root directory
        # of Ansys installation.
        awp_root_envars = _get_environ_vars(pattern=f"^AWP_ROOT.*")
        for awp_root_key, awp_root_value in awp_root_envars.items():
            file_path = os.path.join(awp_root_value, "optiSlang", "optislang.com")
            if os.path.isfile(file_path):
                ansys_version = _try_parse_str_to_int(awp_root_key[-3:])
                osl_versions[ansys_version] = [file_path]

        # Check also standard Ansys installation directories (in Program Files)
        program_files_path = os.environ.get("ProgramFiles", "C:\\Program Files")
        for ans_path in glob(os.path.join(program_files_path, "ANSYS Inc", "v*")):
            ansys_version = _try_parse_str_to_int(ans_path[-3:])
            # Check only those that were not found using AWP_ROOT environment variables.
            if ansys_version not in osl_versions:
                file_path = os.path.join(ans_path, "optiSLang", "optislang.com")
                if os.path.isfile(file_path):
                    osl_versions[ansys_version] = [file_path]

        # And standalone Optislang installations (in Program Files if Dynardo folder exists).
        # if there are both standalone and ansys installation, version will be appended to list
        path = os.path.join(program_files_path, "Dynardo", "Ansys optiSLang")
        if os.path.isdir(path):
            for ver in glob(os.path.join(path, "*")):
                file_path = os.path.join(path, ver, "optislang.com")
                if os.path.isfile(file_path):
                    # convert version fmt "yyyy Rx" to "yyx"
                    conv_fmt = _try_parse_str_to_int(ver[-5:-3] + ver[-1:])
                    if conv_fmt not in osl_versions.keys():
                        osl_versions[conv_fmt] = [file_path]
                    else:
                        osl_versions[conv_fmt].append(file_path)

    # linux
    elif os.name == "posix":
        base_path = None
        for ans_path in ["/usr/ansys_inc", "/ansys_inc"]:
            if os.path.isdir(ans_path):
                base_path = ans_path
        if base_path is not None:
            for ans_path in glob(os.path.join(base_path, "v*")):
                ansys_version = _try_parse_str_to_int(ans_path[-3:])
                # TODO: optislang or another executable?
                file_path = os.path.join(ans_path, "optiSLang", "optislang")
                if os.path.isfile(file_path):
                    osl_versions[ansys_version] = [file_path]
        # check for standalone Optislang installations (in opt\dynardo\... if exists).
        # if there are both standalone and ansys installation, version will be appended to list
        path = "/opt/dynardo"
        if os.path.isdir(path):
            for ver in glob(os.path.join(path, "*")):
                file_path = os.path.join(path, ver, "optislang")
                if os.path.isfile(file_path):
                    # convert version fmt "yyyy Rx" to "yyx"
                    conv_fmt = _try_parse_str_to_int(ver[-4:-2] + ver[-1:])
                    if conv_fmt not in osl_versions.keys():
                        osl_versions[conv_fmt] = [file_path]
                    else:
                        osl_versions[conv_fmt].append(file_path)

    # another os
    else:
        raise NotImplementedError(f"Unsupported OS {os.name}.")

    # convert list of version to tuple
    for ver, paths in osl_versions.items():
        osl_versions[ver] = tuple(paths)
    return collections.OrderedDict(sorted(osl_versions.items(), reverse=True))


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


def _try_parse_str_to_int(str_value: str) -> Union[int, str]:
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
