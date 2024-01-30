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
