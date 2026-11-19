# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Forced shutdown of a real local optiSLang process.

The default wait of a forced shutdown has to be long enough for optiSLang to finish its own
shutdown, which ends its session properly; a terminated process loses it.
"""

import pytest

from ansys.optislang.core import Optislang, OslServerProcess
from ansys.optislang.core.communication_channels import CommunicationChannel

pytestmark = pytest.mark.local_osl


def test_optislang_exits_by_itself_within_the_default_wait(tmp_example_project, monkeypatch):
    terminated = []
    terminate = OslServerProcess.terminate

    def recording_terminate(self, *args, **kwargs):
        terminated.append(self)
        return terminate(self, *args, **kwargs)

    monkeypatch.setattr(OslServerProcess, "terminate", recording_terminate)

    osl = Optislang(
        project_path=tmp_example_project("calculator_with_params"),
        communication_channel=CommunicationChannel.TCP,
        ini_timeout=90,
    )
    process = osl._Optislang__osl_server._TcpOslServer__osl_process
    osl.application.project.start()
    osl.shutdown(force=True)

    assert not terminated, "optiSLang was terminated instead of exiting by itself"
    assert not process.is_running()
