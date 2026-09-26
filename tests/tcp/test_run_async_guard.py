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

"""Unit tests for the ``run_async`` (long running operation) server-version guard.

These tests exercise ``TcpOslServer._check_run_async_supported`` in isolation, without
connecting to a live optiSLang server, so they are intentionally *not* marked
``local_osl``.
"""

import pytest

from ansys.optislang.core.errors import OslVersionError
from ansys.optislang.core.osl_server import OslVersion
import ansys.optislang.core.tcp.osl_server as tos


def _make_guarded_server(version: OslVersion, version_string: str) -> tos.TcpOslServer:
    """Build a bare ``TcpOslServer`` with only the version attributes populated.

    ``__new__`` is used to avoid the network/server side-effects of ``__init__``; only
    the private version attributes read by the guard are set.
    """
    server = tos.TcpOslServer.__new__(tos.TcpOslServer)
    # Name-mangled private attributes read by ``_check_run_async_supported``.
    setattr(server, "_TcpOslServer__osl_version", version)
    setattr(server, "_TcpOslServer__osl_version_string", version_string)
    return server


@pytest.mark.parametrize(
    "version, version_string",
    [
        (OslVersion(25, 1, 0, 0), "25.1.0"),
        (OslVersion(26, 1, 0, 0), "26.1.0"),
        (OslVersion(27, 0, 0, 0), "27.0.0"),
    ],
)
def test_run_async_guard_raises_on_old_server(version, version_string):
    server = _make_guarded_server(version, version_string)
    with pytest.raises(OslVersionError) as exc_info:
        server._check_run_async_supported("evaluate_design")
    message = str(exc_info.value)
    assert "evaluate_design" in message
    assert "27.1" in message
    assert version_string in message


@pytest.mark.parametrize(
    "version, version_string",
    [
        (OslVersion(27, 1, 0, 0), "27.1.0"),
        (OslVersion(27, 2, 0, 0), "27.2.0"),
        (OslVersion(28, 0, 0, 0), "28.0.0"),
    ],
)
def test_run_async_guard_passes_on_supported_server(version, version_string):
    server = _make_guarded_server(version, version_string)
    # Should not raise.
    server._check_run_async_supported("evaluate_design")


def test_run_async_guard_passes_on_unknown_version():
    # A ``None`` major version means the version could not be determined; the guard must
    # not block in that case (backward compatibility).
    server = _make_guarded_server(OslVersion(None, None, None, None), "unknown")
    server._check_run_async_supported("reset")


def test_run_async_guard_includes_feature_name():
    server = _make_guarded_server(OslVersion(26, 1, 0, 0), "26.1.0")
    with pytest.raises(OslVersionError) as exc_info:
        server._check_run_async_supported("run_python_script")
    assert "run_python_script" in str(exc_info.value)
