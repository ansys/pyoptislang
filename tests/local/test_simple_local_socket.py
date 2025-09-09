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

"""Simple test of the local socket implementation with proper imports."""

import threading
import time

from ansys.optislang.core import utils
from ansys.optislang.core.tcp.local_socket import (
    LocalClientSocket,
    LocalServerSocket,
)


def test_simple_communication():
    """Test basic client-server communication."""
    # Generate server ID
    server_id = utils.generate_local_server_id()

    # Create server
    server = LocalServerSocket()
    server.bind_and_listen(server_id)

    success = False
    error_msg = None

    def server_handler():
        nonlocal success, error_msg
        try:
            client, addr = server.accept(timeout=10.0)

            # Receive data
            data = client.recv(1024)

            # Send response
            response = b"Hello from server!"
            bytes_sent = client.send(response)

            client.close()
            success = True

        finally:
            server.close()

    # Start server in thread
    server_thread = threading.Thread(target=server_handler)
    server_thread.start()

    # Give server time to start
    time.sleep(1.0)

    try:
        # Create client and connect
        client = LocalClientSocket()
        client.connect(server_id, timeout=5.0)

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

    if error_msg:
        raise Exception(error_msg)

    if not success:
        raise Exception("Server did not complete successfully")
