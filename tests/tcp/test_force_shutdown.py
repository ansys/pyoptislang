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

"""Unit tests for the wait before a forced shutdown terminates the local optiSLang process.

These tests exercise ``TcpOslServer.shutdown`` and ``_force_shutdown_local_process`` with a
fake process, without starting optiSLang, so they are intentionally *not* marked ``local_osl``.
"""

import logging
import time

import pytest

import ansys.optislang.core.tcp.osl_server as tos


class _FakeProcess:
    """Stands in for ``OslServerProcess``: exits by itself after ``exits_after`` seconds."""

    def __init__(self, exits_after: float = float("inf")):
        self._exits_at = time.monotonic() + exits_after
        self.terminated = False

    def is_running(self) -> bool:
        return not self.terminated and time.monotonic() < self._exits_at

    def terminate(self) -> None:
        self.terminated = True


def _make_server(process: _FakeProcess) -> tos.TcpOslServer:
    """Build a bare ``TcpOslServer`` that owns ``process`` and records the commands it sends.

    ``__new__`` is used to avoid the network/server side-effects of ``__init__``; only the
    private attributes read by ``shutdown`` are set.
    """
    server = tos.TcpOslServer.__new__(tos.TcpOslServer)
    server._logger = logging.getLogger(__name__)
    # Name-mangled private attributes read by ``shutdown``.
    setattr(server, "_TcpOslServer__osl_process", process)
    setattr(server, "_TcpOslServer__password", None)
    setattr(server, "_TcpOslServer__listeners", {})
    setattr(server, "_TcpOslServer__listeners_registration_thread", None)
    setattr(
        server,
        "_TcpOslServer__timeouts_register",
        server._TcpOslServer__get_default_timeouts_register(),
    )
    setattr(
        server,
        "_TcpOslServer__max_request_attempts_register",
        server._TcpOslServer__get_default_max_request_attempts_register(),
    )
    server.sent_commands = []
    server.send_command = lambda command, **kwargs: server.sent_commands.append(command)
    return server


def test_default_wait_leaves_time_to_exit():
    # optiSLang needs 1 to 3 s to send its usage data and release its licenses.
    assert tos.TcpOslServer._SHUTDOWN_WAIT >= 15


def test_process_that_exits_in_time_is_not_terminated():
    process = _FakeProcess(exits_after=0.2)
    server = _make_server(process)
    start = time.monotonic()
    server._force_shutdown_local_process(terminate_after=5)
    assert not process.terminated
    assert time.monotonic() - start < 2


def test_process_still_running_is_terminated_after_the_wait():
    process = _FakeProcess()
    server = _make_server(process)
    start = time.monotonic()
    server._force_shutdown_local_process(terminate_after=0.3)
    elapsed = time.monotonic() - start
    assert process.terminated
    assert 0.3 <= elapsed < 2


def test_wait_without_terminate_after_is_the_default(monkeypatch):
    monkeypatch.setattr(tos.TcpOslServer, "_SHUTDOWN_WAIT", 0.3)
    process = _FakeProcess()
    server = _make_server(process)
    start = time.monotonic()
    server._force_shutdown_local_process()
    assert process.terminated
    assert 0.3 <= time.monotonic() - start < 2


def test_shutdown_passes_terminate_after_on():
    process = _FakeProcess()
    server = _make_server(process)
    start = time.monotonic()
    server.shutdown(force=True, terminate_after=0.3)
    elapsed = time.monotonic() - start
    assert len(server.sent_commands) == 1
    assert process.terminated
    assert 0.3 <= elapsed < 2


def test_shutdown_without_force_does_not_wait_or_terminate():
    process = _FakeProcess()
    server = _make_server(process)
    server.shutdown(terminate_after=0.3)
    assert len(server.sent_commands) == 1
    assert not process.terminated


def test_negative_terminate_after_is_rejected_before_shutting_down():
    process = _FakeProcess()
    server = _make_server(process)
    with pytest.raises(ValueError):
        server.shutdown(force=True, terminate_after=-1)
    assert server.sent_commands == []
    assert not process.terminated
