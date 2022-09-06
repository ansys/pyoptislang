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

from ansys.optislang.core.logging import OslLogger

LOG = OslLogger(loglevel="ERROR", log_to_file=False, log_to_stdout=True)
LOG.logger.debug("Loaded logging module as LOG")

__version__ = importlib_metadata.version(__name__.replace(".", "-"))

IRON_PYTHON = sys.platform == "cli"
WINDOWS = os.name == "nt"
LINUX = os.name == "posix"
PY3 = sys.version_info[0] >= 3
# First supported version of optiSLang: 2023R1
FIRST_SUPPORTED_VERSION = 231

from ansys.optislang.core.optislang import Optislang
from ansys.optislang.core.osl_process import OslServerProcess, ServerNotification

# Setup data directory
USER_DATA_PATH = None
LOCAL_DOWNLOADED_EXAMPLES_PATH = None
try:
    import pkgutil

    spec = pkgutil.get_loader("ansys.optislang.core")
    USER_DATA_PATH = os.path.dirname(spec.get_filename())
    if not os.path.exists(USER_DATA_PATH):  # pragma: no cover
        os.makedirs(USER_DATA_PATH)

    LOCAL_DOWNLOADED_EXAMPLES_PATH = os.path.join(USER_DATA_PATH, "examples")
    if not os.path.exists(LOCAL_DOWNLOADED_EXAMPLES_PATH):  # pragma: no cover
        os.makedirs(LOCAL_DOWNLOADED_EXAMPLES_PATH)
    os.environ["OSL_EXAMPLES"] = LOCAL_DOWNLOADED_EXAMPLES_PATH
except:  # pragma: no cover
    pass
