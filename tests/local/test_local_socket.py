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

"""
Test script for local socket implementation with timeout testing.
"""

import threading
import time

from ansys.optislang.core.tcp.local_socket import (
    LocalClientSocket,
    LocalServerSocket,
    generate_local_server_id,
)


def test_basic_communication():
    """Test basic local socket communication."""

    # Generate server ID
    server_id = generate_local_server_id()

    # Create server
    server = LocalServerSocket()
    server.bind_and_listen(server_id)

    def server_handler():
        try:
            server_client, addr = server.accept(timeout=5.0)

            # Receive data on server side
            received = server_client.recv(1024)

            # Send response back
            response = b"Server response"
            server_client.send(response)
            server_client.close()

        finally:
            server.close()

    # Start server in thread
    import threading

    server_thread = threading.Thread(target=server_handler)
    server_thread.start()

    # Give server time to start
    time.sleep(0.5)

    try:
        # Create client
        client = LocalClientSocket()
        client.connect(server_id, timeout=5.0)

        # Test sending data
        test_msg = b"Hello, local socket!"
        sent = client.send(test_msg)

        # Receive response
        response = client.recv(1024)

        client.close()

    finally:
        server_thread.join()


def test_timeout_functionality():
    """Test timeout functionality."""
    # Test connection timeout to non-existent server
    non_existent_id = generate_local_server_id()

    client = LocalClientSocket()
    try:
        start_time = time.time()
        try:
            client.connect(non_existent_id, timeout=1.0)
            assert False, "Connection should have timed out"
        except (ConnectionRefusedError, TimeoutError) as e:
            elapsed = time.time() - start_time

        # Test accept timeout
        server_id = generate_local_server_id()
        server = LocalServerSocket()
        try:
            server.bind_and_listen(server_id)

            start_time = time.time()
            try:
                server.accept(timeout=1.0)
                assert False, "Accept should have timed out"
            except TimeoutError as e:
                elapsed = time.time() - start_time

        finally:
            server.close()

    finally:
        client.close()


def test_concurrent_connections():
    """Test multiple concurrent connections."""
    server_id = generate_local_server_id()

    server = LocalServerSocket()
    server_running = threading.Event()
    test_results = []

    def server_thread():
        """Server thread function."""
        try:
            server.bind_and_listen(server_id)
            server_running.set()

            # Accept multiple connections
            for i in range(3):
                try:
                    client, addr = server.accept(timeout=5.0)

                    # Echo back the received data
                    data = client.recv(1024)
                    client.send(data)
                    client.close()
                    test_results.append(True)

                except Exception as e:
                    test_results.append(False)

        except Exception as e:
            test_results.append(False)

    # Start server thread
    server_thread_obj = threading.Thread(target=server_thread)
    server_thread_obj.start()

    # Wait for server to start
    server_running.wait(timeout=5.0)
    time.sleep(0.1)  # Give server a moment to be ready

    # Create multiple client connections
    for i in range(3):
        try:
            client = LocalClientSocket()
            client.connect(server_id, timeout=5.0)

            test_msg = f"Message from client {i+1}".encode()
            client.send(test_msg)

            response = client.recv(1024)
            if response == test_msg:
                test_results.append(True)
            else:
                test_results.append(False)

            client.close()

        except Exception as e:
            test_results.append(False)

    # Wait for server thread to complete
    server_thread_obj.join(timeout=10.0)
    server.close()

    success_count = sum(test_results)
    total_expected = 6  # 3 server accepts + 3 client communications

    assert (
        success_count == total_expected
    ), f"Expected {total_expected} successful operations, got {success_count}"
