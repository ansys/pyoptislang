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

import importlib.metadata
import os
import sys

from ansys.optislang.core.logging import OslLogger

LOG = OslLogger(loglevel="ERROR", log_to_file=False, log_to_stdout=True)
LOG.logger.debug("Loaded logging module as LOG")

__version__ = importlib.metadata.version(__name__.replace(".", "-"))

IRON_PYTHON = sys.platform == "cli"
PY3 = sys.version_info[0] >= 3
# First supported version of optiSLang: 2023R1
FIRST_SUPPORTED_VERSION = 231

from ansys.optislang.core.optislang import Optislang
from ansys.optislang.core.osl_process import OslServerProcess, ServerNotification

# Setup data directory
try:
    import importlib.util

    if spec := importlib.util.find_spec("ansys.optislang.core"):
        if spec.origin:
            user_data_path = os.path.dirname(spec.origin)
            if not os.path.exists(user_data_path):
                os.makedirs(user_data_path)

            local_examples_path = os.path.join(user_data_path, "examples")
            if not os.path.exists(local_examples_path):
                os.makedirs(local_examples_path)

            os.environ["OSL_EXAMPLES"] = local_examples_path
except Exception as e:
    LOG.logger.warning(f"Could not set up path to examples: {e}")
    pass
