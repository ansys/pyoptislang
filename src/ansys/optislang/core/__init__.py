"""
optiSLang.

core
"""

import logging
import os
import sys

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

from ansys.optislang.core.logging import OslLogger

LOG = OslLogger(loglevel=logging.ERROR, log_to_file=False, log_to_stdout=True)
LOG.logger.debug("Loaded logging module as LOG")

__version__ = importlib_metadata.version(__name__.replace(".", "-"))

IRON_PYTHON = sys.platform == "cli"
WINDOWS = os.name == "nt"
LINUX = os.name == "posix"
PY3 = sys.version_info[0] >= 3

from ansys.optislang.core.osl_process import OslServerProcess, ServerNotification
