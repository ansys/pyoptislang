#!/usr/bin/env python3

# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""Test timeout functionality of the overlapped I/O implementation."""

import sys
import threading
import time

import pytest

from ansys.optislang.core import utils
from ansys.optislang.core.tcp.local_socket import (
    LocalClientSocket,
    LocalServerSocket,
)


def test_connection_timeout():
    """Test connection timeout when server doesn't exist."""
    # Try to connect to non-existent server
    non_existent_id = utils.generate_local_server_id()
    client = LocalClientSocket()

    start_time = time.time()
    try:
        client.connect(non_existent_id, timeout=1.5)
        assert False, "Should have timed out"
    except (ConnectionRefusedError, TimeoutError) as e:
        elapsed = time.time() - start_time
        assert elapsed <= 2.0, f"Timeout took {elapsed}s, expected ~1.5s maximum"
    finally:
        client.close()


@pytest.mark.skipif(
    sys.platform != "win32" and sys.version_info < (3, 10), reason="Fails for Python 3.9 on Linux"
)
def test_accept_timeout():
    """Test accept timeout when no client connects."""
    server_id = utils.generate_local_server_id()
    server = LocalServerSocket()
    server.bind_and_listen(server_id)

    start_time = time.time()
    try:
        server.accept(timeout=1.5)
        assert False, "Should have timed out"
    except TimeoutError as e:
        elapsed = time.time() - start_time
        assert 1.0 <= elapsed <= 2.0, f"Accept timeout took {elapsed}s, expected ~1.5s"
    finally:
        server.close()


@pytest.mark.skipif(
    sys.platform != "win32" and sys.version_info < (3, 10), reason="Fails for Python 3.9 on Linux"
)
def test_send_recv_timeout():
    """Test send/recv timeout functionality."""
    server_id = utils.generate_local_server_id()
    server = LocalServerSocket()
    server.bind_and_listen(server_id)

    def slow_server():
        try:
            client, addr = server.accept(timeout=5.0)
            # Don't read anything, just sleep to cause client recv timeout
            time.sleep(3.0)
            client.close()
        finally:
            server.close()

    server_thread = threading.Thread(target=slow_server)
    server_thread.start()

    time.sleep(0.5)  # Let server start

    try:
        client = LocalClientSocket()
        client.connect(server_id, timeout=5.0)

        # Send data
        message = b"Hello"
        client.send(message)

        # Try to receive with timeout (server won't send anything)
        start_time = time.time()
        try:
            client.recv_with_timeout(1024, timeout=1.5)
            assert False, "Should have timed out"
        except TimeoutError as e:
            elapsed = time.time() - start_time
            assert 1.0 <= elapsed <= 2.0, f"Recv timeout took {elapsed}s, expected ~1.5s"

        client.close()

    finally:
        server_thread.join()


def test_overlapped_io_robustness():
    """Test the robustness of overlapped I/O under concurrent operations."""
    server_id = utils.generate_local_server_id()
    server = LocalServerSocket()
    server.bind_and_listen(server_id)

    results = []

    def robust_server():
        try:
            for i in range(3):
                client, addr = server.accept(timeout=10.0)

                # Handle each client quickly with timeouts
                try:
                    data = client.recv_with_timeout(1024, timeout=2.0)
                    response = f"Response {i+1}".encode()
                    client.send_with_timeout(response, timeout=2.0)
                    results.append(i + 1)
                finally:
                    client.close()

        finally:
            server.close()

    server_thread = threading.Thread(target=robust_server)
    server_thread.start()

    time.sleep(0.5)

    # Create multiple clients quickly
    client_threads = []

    def client_worker(client_id):
        client = LocalClientSocket()
        client.connect(server_id, timeout=5.0)

        message = f"Message from client {client_id}".encode()
        client.send_with_timeout(message, timeout=2.0)

        response = client.recv_with_timeout(1024, timeout=3.0)

        client.close()

    # Start multiple clients
    for i in range(3):
        thread = threading.Thread(target=client_worker, args=(i + 1,))
        thread.start()
        client_threads.append(thread)
        time.sleep(0.2)  # Slight delay between clients

    # Wait for all clients
    for thread in client_threads:
        thread.join()

    server_thread.join()

    assert len(results) == 3, f"Expected 3 handled connections, got {len(results)}"
