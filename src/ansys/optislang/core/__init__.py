"""
optiSLang.

core
"""

import os
import sys

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version(__name__.replace(".", "-"))

IRON_PYTHON = sys.platform == "cli"
WINDOWS = os.name == "nt"
LINUX = os.name == "posix"
PY3 = sys.version_info[0] >= 3

from ansys.optislang.core.osl_process import OslServerProcess
