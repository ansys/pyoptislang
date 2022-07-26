"""Find optislang module."""
from collections import OrderedDict
from glob import glob
import os
import re


def get_osl_executable(osl_version=None):
    """Return path to optiSLang executable file (by default the latest available version).

    Parameters
    ----------
    osl_version : str, optional
        Version of optiSLang, e.g. "221".
    Returns
    -------
    path: str
        Path of the specified optiSLang version.
    """
    # TODO: Must work for standalone optiSLang as well
    # windows
    if os.name == "nt":
        # find all ansys system variables, optiSLang installed in AWP_ROOT on windows
        installed_versions = _get_system_vars(pattern="^AWP_ROOT.*")
        if not installed_versions:
            raise FileNotFoundError(
                f"No version of ansys was found, please specify direct path of executable."
            )
        if osl_version:
            version = "AWP_ROOT" + osl_version
            if version in installed_versions:
                path = os.path.join(installed_versions[version], "optiSlang", "optislang.exe")
                if os.path.isfile(path):
                    return path
                else:
                    raise FileNotFoundError(
                        f"Optislang not installed in this version: {osl_version}"
                    )
            else:
                raise FileNotFoundError(
                    f"This version of ansys is not defined in system variables: {osl_version}"
                )
        else:
            # sort installed versions from the highest number
            installed_versions = OrderedDict(reversed(sorted(installed_versions.items())))
            for version in list(installed_versions.keys()):
                path = os.path.join(installed_versions[version], "optiSlang", "optislang.exe")
                if os.path.isfile(path):
                    return path

            raise FileNotFoundError(
                "No version of optiSLang was found, please specify direct path of executable."
            )

    # linux
    elif os.name == "posix":
        base_path = None
        for path in ["/usr/ansys_inc", "/ansys_inc"]:
            if os.path.isdir(path):
                base_path = path
        if osl_version:
            dir_path = os.path.join(base_path, "v" + osl_version)
            if not os.path.exists(dir_path):
                raise FileNotFoundError(f"Ansys not installed in this version: {osl_version}")

            file_path = os.path.join(dir_path, "optiSLang", "optislang")
            if not os.path.isfile(file_path):
                raise FileNotFoundError(f"Optislang not installed in this version: {osl_version}")

            return file_path
        else:
            paths = sorted(glob(os.path.join(base_path, "v*")), reverse=True)
            for path in paths:
                file_path = os.path.join(path, "optiSLang", "optislang")
                if os.path.isfile(file_path):
                    return file_path
            raise FileNotFoundError(
                "No version of optislang was found, please specify direct path of executable."
            )

    # another os
    else:
        raise OSError(f"Unsupported OS {os.name}")


def _get_system_vars(pattern=".*"):
    """Return dict of matching system variables.

    Parameters
    ----------
    pattern: str, optional
        regex template

    Returns
    -------
    installed_versions: dict
        Dictionary of matching system variables.
    """
    sys_vars = os.environ.copy()
    dictionary = {}
    for varname, value in sys_vars.items():
        varname_match = re.search(pattern, varname)
        if varname_match:
            dictionary[varname] = value
    return dictionary
