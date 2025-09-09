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

"""Direct test of local_socket module without circular imports."""

import threading
import time

from ansys.optislang.core.tcp.local_socket import (
    LocalClientSocket,
    LocalServerSocket,
    generate_local_server_id,
)


def test_basic_communication():
    """Test basic client-server communication."""

    # Generate server ID
    server_id = generate_local_server_id()

    # Create server
    server = LocalServerSocket()
    server.bind_and_listen(server_id)

    def server_handler():
        try:
            client, addr = server.accept(timeout=5.0)

            # Receive data
            data = client.recv(1024)

            # Send response
            response = b"Hello from server!"
            client.send(response)

            client.close()
        finally:
            server.close()

    # Start server in thread
    server_thread = threading.Thread(target=server_handler)
    server_thread.start()

    # Give server time to start
    time.sleep(0.5)

    try:
        # Create client and connect
        client = LocalClientSocket()
        client.connect(server_id, timeout=2.0)

        # Send message
        message = b"Hello from client!"
        bytes_sent = client.send(message)

        # Receive response
        response = client.recv(1024)

        client.close()

        # Verify response
        assert response == b"Hello from server!", f"Expected 'Hello from server!', got {response}"

    finally:
        server_thread.join()


def test_timeout_functionality():
    """Test timeout functionality."""

    # Test connection timeout
    non_existent_id = generate_local_server_id()
    client = LocalClientSocket()

    start_time = time.time()
    try:
        client.connect(non_existent_id, timeout=1.0)
        assert False, "Should have timed out"
    except (ConnectionRefusedError, TimeoutError):
        elapsed = time.time() - start_time
        assert elapsed <= 1.5, f"Timeout took {elapsed}s, expected ~1.0s maximum"

    # Test accept timeout
    server_id = generate_local_server_id()
    server = LocalServerSocket()
    server.bind_and_listen(server_id)

    start_time = time.time()
    try:
        server.accept(timeout=1.0)
        assert False, "Should have timed out"
    except TimeoutError:
        elapsed = time.time() - start_time
        assert 0.8 <= elapsed <= 1.5, f"Accept timeout took {elapsed}s, expected ~1.0s"
    finally:
        server.close()


def test_concurrent_connections():
    """Test multiple concurrent connections."""

    server_id = generate_local_server_id()
    server = LocalServerSocket()
    server.bind_and_listen(server_id)

    connections_handled = []

    def server_handler():
        try:
            for i in range(3):
                client, addr = server.accept(timeout=5.0)

                # Handle connection in separate thread
                def handle_client(client_conn, conn_id):
                    data = client_conn.recv(1024)
                    response = f"Response {conn_id}".encode()
                    client_conn.send(response)
                    connections_handled.append(conn_id)
                    client_conn.close()

                thread = threading.Thread(target=handle_client, args=(client, i + 1))
                thread.start()

        finally:
            server.close()

    # Start server
    server_thread = threading.Thread(target=server_handler)
    server_thread.start()

    time.sleep(0.5)

    # Create multiple clients
    clients = []

    for i in range(3):
        client = LocalClientSocket()
        client.connect(server_id, timeout=2.0)
        client.send(f"Message {i+1}".encode())

        response = client.recv(1024)

        client.close()
        clients.append(client)

    # Wait for server to finish
    server_thread.join()

    # Verify all connections were handled
    assert (
        len(connections_handled) == 3
    ), f"Expected 3 connections, handled {len(connections_handled)}"
