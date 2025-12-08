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

"""Platform-specific socket implementations for local domain communication."""
from __future__ import annotations

import logging
import os
import socket
import sys
import time
from typing import Optional, Tuple

if sys.platform == "win32":
    import pywintypes
    import win32api
    import win32event
    import win32file
    import win32pipe
    import win32security


class LocalSocket:
    """Platform-specific local domain socket abstraction."""

    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize local socket.

        Parameters
        ----------
        logger : Optional[logging.Logger], optional
            Logger instance. If None, creates a default logger.
        """
        self._logger = logger or logging.getLogger(__name__)
        self._socket: Optional[socket.socket] = None
        self._handle = None
        self._address: Optional[str] = None
        self._timeout: Optional[float] = None  # Store timeout for Windows named pipes

    @property
    def address(self) -> Optional[str]:
        """Get the local address/identifier."""
        return self._address

    @property
    def is_connected(self) -> bool:
        """Check if socket is connected."""
        if sys.platform == "win32":
            return self._handle is not None
        else:
            return self._socket is not None

    def close(self) -> None:
        """Close the socket connection."""
        if sys.platform == "win32":
            if self._handle is not None:
                try:
                    win32api.CloseHandle(self._handle)  # type: ignore[name-defined]
                except Exception as e:
                    self._logger.warning(f"Error closing Windows pipe handle: {e}")
                self._handle = None
        else:
            if self._socket is not None:
                try:
                    self._socket.close()
                except Exception as e:
                    self._logger.warning(f"Error closing Unix socket: {e}")
                self._socket = None


class LocalClientSocket(LocalSocket):
    """Platform-specific local domain client socket."""

    def connect(self, server_id: str, timeout: Optional[float] = 2.0) -> None:
        """Connect to a local server.

        Parameters
        ----------
        server_id : str
            Server identifier (pipe name on Windows, socket path on Linux)
        timeout : Optional[float], optional
            Connection timeout in seconds. Defaults to 2.0.

        Raises
        ------
        ConnectionRefusedError
            If connection cannot be established
        TimeoutError
            If connection times out
        """
        start_time = time.time()

        if sys.platform == "win32":
            self._connect_windows_pipe(server_id, timeout, start_time)
        else:
            self._connect_unix_socket(server_id, timeout, start_time)

        self._address = server_id
        self._logger.debug(f"Connected to local server: {server_id}")

    def _connect_windows_pipe(
        self, pipe_name: str, timeout: Optional[float], start_time: float
    ) -> None:
        """Connect to Windows named pipe with proper timeout handling using overlapped I/O."""
        deadline = start_time + timeout if timeout is not None else None

        while True:
            try:
                # Try to open the pipe with overlapped flag for async operations
                self._handle = win32file.CreateFile(  # type: ignore[name-defined, assignment]
                    pipe_name,
                    win32file.GENERIC_READ | win32file.GENERIC_WRITE,  # type: ignore[name-defined]
                    0,
                    None,
                    win32file.OPEN_EXISTING,  # type: ignore[name-defined]
                    win32file.FILE_FLAG_OVERLAPPED,  # type: ignore[name-defined]
                    None,
                )
                return
            except pywintypes.error as e:  # type: ignore[name-defined]
                if e.winerror == 2:  # File not found (pipe doesn't exist)
                    if deadline and time.time() > deadline:
                        raise ConnectionRefusedError(f"Named pipe {pipe_name} not found")
                    time.sleep(0.1)
                    continue
                elif e.winerror == 231:  # All pipe instances are busy
                    # Use WaitNamedPipe with proper timeout calculation
                    if deadline:
                        remaining_ms = max(0, int((deadline - time.time()) * 1000))
                        if remaining_ms == 0:
                            raise ConnectionRefusedError(f"Named pipe {pipe_name} busy - timeout")
                    else:
                        remaining_ms = 1000  # Default 1 second wait

                    win32pipe.WaitNamedPipe(pipe_name, remaining_ms)  # type: ignore[name-defined]
                else:
                    raise ConnectionRefusedError(f"Cannot connect to named pipe {pipe_name}: {e}")

    def _connect_unix_socket(
        self, socket_path: str, timeout: Optional[float], start_time: float
    ) -> None:
        """Connect to Unix domain socket."""
        try:
            self._socket = socket.socket(
                socket.AF_UNIX,  # type: ignore[attr-defined]
                socket.SOCK_STREAM,
            )
            if timeout is not None:
                remaining_timeout = timeout - (time.time() - start_time)
                if remaining_timeout <= 0:
                    raise TimeoutError("Connection timeout")
                self._socket.settimeout(remaining_timeout)
            self._socket.connect(socket_path)
        except socket.timeout:
            # In Python 3.9, socket.timeout is not a subclass of TimeoutError
            # Convert to TimeoutError for consistency
            if self._socket:
                self._socket.close()
                self._socket = None
            raise TimeoutError("Connection timeout")
        except OSError as e:
            if self._socket:
                self._socket.close()
                self._socket = None
            raise ConnectionRefusedError(f"Cannot connect to Unix socket {socket_path}: {e}")

    def send(self, data: bytes) -> int:
        """Send data through the socket.

        Parameters
        ----------
        data : bytes
            Data to send

        Returns
        -------
        int
            Number of bytes sent
        """
        return self.send_with_timeout(data, self._timeout)

    def send_with_timeout(self, data: bytes, timeout: Optional[float]) -> int:
        """Send data through the socket with timeout support.

        Parameters
        ----------
        data : bytes
            Data to send
        timeout : Optional[float]
            Timeout in seconds, None for blocking

        Returns
        -------
        int
            Number of bytes sent
        """
        if sys.platform == "win32":
            if self._handle is None:
                raise ConnectionError("Not connected")
            try:
                # Create overlapped structure for async operation
                overlapped = pywintypes.OVERLAPPED()  # type: ignore[name-defined]
                overlapped.hEvent = win32event.CreateEvent(  # type: ignore[name-defined]
                    None, True, False, None
                )

                try:
                    # Attempt to write with overlapped I/O
                    win32file.WriteFile(  # type: ignore[name-defined]
                        self._handle, data, overlapped
                    )

                    # Wait for completion with timeout
                    if timeout is not None:
                        timeout_ms = int(timeout * 1000)
                    else:
                        timeout_ms = win32event.INFINITE  # type: ignore[name-defined]

                    wait_result = win32event.WaitForSingleObject(  # type: ignore[name-defined]
                        overlapped.hEvent, timeout_ms
                    )

                    if wait_result == win32event.WAIT_TIMEOUT:  # type: ignore[name-defined]
                        win32file.CancelIo(self._handle)  # type: ignore[name-defined]
                        raise TimeoutError("Send operation timed out")
                    elif wait_result != win32event.WAIT_OBJECT_0:  # type: ignore[name-defined]
                        raise ConnectionError(f"Send wait failed with result: {wait_result}")

                    try:
                        bytes_written = win32file.GetOverlappedResult(  # type: ignore[name-defined]
                            self._handle, overlapped, False
                        )
                    except pywintypes.error as e:  # type: ignore[name-defined]
                        bytes_written = 0
                    return bytes_written
                finally:
                    win32api.CloseHandle(overlapped.hEvent)  # type: ignore[name-defined]

            except pywintypes.error as e:  # type: ignore[name-defined]
                raise ConnectionError(f"Send failed: {e}")
        else:
            if self._socket is None:
                raise ConnectionError("Not connected")
            if timeout is not None:
                original_timeout = self._socket.gettimeout()
                self._socket.settimeout(timeout)
                try:
                    return self._socket.send(data)
                except socket.timeout:
                    # In Python 3.9, socket.timeout is not a subclass of TimeoutError
                    # Convert to TimeoutError for consistency
                    raise TimeoutError("Send operation timed out")
                finally:
                    self._socket.settimeout(original_timeout)
            else:
                return self._socket.send(data)

    def recv(self, bufsize: int) -> bytes:
        """Receive data from the socket.

        Parameters
        ----------
        bufsize : int
            Maximum number of bytes to receive

        Returns
        -------
        bytes
            Received data
        """
        return self.recv_with_timeout(bufsize, self._timeout)

    def recv_with_timeout(self, bufsize: int, timeout: Optional[float]) -> bytes:
        """Receive data from the socket with timeout support.

        Parameters
        ----------
        bufsize : int
            Maximum number of bytes to receive
        timeout : Optional[float]
            Timeout in seconds, None for blocking

        Returns
        -------
        bytes
            Received data
        """
        if sys.platform == "win32":
            if self._handle is None:
                raise ConnectionError("Not connected")
            try:
                # Create overlapped structure for async operation
                overlapped = pywintypes.OVERLAPPED()  # type: ignore[name-defined]
                overlapped.hEvent = win32event.CreateEvent(  # type: ignore[name-defined]
                    None, True, False, None
                )

                try:
                    # Attempt to read with overlapped I/O
                    _, data = win32file.ReadFile(  # type: ignore[name-defined]
                        self._handle, bufsize, overlapped
                    )

                    # Wait for completion with timeout
                    if timeout is not None:
                        timeout_ms = int(timeout * 1000)
                    else:
                        timeout_ms = win32event.INFINITE  # type: ignore[name-defined]

                    wait_result = win32event.WaitForSingleObject(  # type: ignore[name-defined]
                        overlapped.hEvent, timeout_ms
                    )

                    if wait_result == win32event.WAIT_TIMEOUT:  # type: ignore[name-defined]
                        win32file.CancelIo(self._handle)  # type: ignore[name-defined]
                        raise TimeoutError("Receive operation timed out")
                    elif wait_result != win32event.WAIT_OBJECT_0:  # type: ignore[name-defined]
                        raise ConnectionError(f"Receive wait failed with result: {wait_result}")

                    try:
                        bytes_read = win32file.GetOverlappedResult(  # type: ignore[name-defined]
                            self._handle, overlapped, False
                        )
                    except pywintypes.error as e:  # type: ignore[name-defined]
                        bytes_read = 0
                    return data[:bytes_read] if bytes_read < len(data) else data
                finally:
                    win32api.CloseHandle(overlapped.hEvent)  # type: ignore[name-defined]

            except pywintypes.error as e:  # type: ignore[name-defined]
                raise ConnectionError(f"Receive failed: {e}")
        else:
            if self._socket is None:
                raise ConnectionError("Not connected")
            if timeout is not None:
                original_timeout = self._socket.gettimeout()
                self._socket.settimeout(timeout)
                try:
                    return self._socket.recv(bufsize)
                except socket.timeout:
                    # In Python 3.9, socket.timeout is not a subclass of TimeoutError
                    # Convert to TimeoutError for consistency
                    raise TimeoutError("Receive operation timed out")
                finally:
                    self._socket.settimeout(original_timeout)
            else:
                return self._socket.recv(bufsize)

    def settimeout(self, timeout: Optional[float]) -> None:
        """Set socket timeout.

        Parameters
        ----------
        timeout : Optional[float]
            Timeout in seconds, None for blocking
        """
        self._timeout = timeout
        if sys.platform != "win32" and self._socket is not None:
            self._socket.settimeout(timeout)


class LocalServerSocket(LocalSocket):
    """Platform-specific local domain server socket."""

    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize local server socket."""
        super().__init__(logger)

    def bind_and_listen(self, server_id: str, backlog: int = 5) -> None:
        """Bind to address and start listening.

        Parameters
        ----------
        server_id : str
            Server identifier to bind to
        backlog : int, optional
            Maximum number of pending connections. Defaults to 5.
        """
        self._address = server_id

        if sys.platform == "win32":
            self._create_windows_pipe(server_id)
        else:
            self._create_unix_socket(server_id, backlog)

        self._logger.debug(f"Listening on: {server_id}")

    def _create_windows_pipe(self, pipe_name: str) -> None:
        """Create Windows named pipe server with overlapped I/O support."""
        try:
            # Create security descriptor to restrict access to current user
            security_descriptor = win32security.SECURITY_DESCRIPTOR()  # type: ignore[name-defined]
            security_descriptor.SetSecurityDescriptorDacl(1, None, 0)  # type: ignore[arg-type]

            security_attributes = win32security.SECURITY_ATTRIBUTES()  # type: ignore[name-defined]
            security_attributes.SECURITY_DESCRIPTOR = security_descriptor

            self._handle = win32pipe.CreateNamedPipe(  # type: ignore[name-defined, assignment]
                pipe_name,
                win32pipe.PIPE_ACCESS_DUPLEX  # type: ignore[name-defined]
                | win32file.FILE_FLAG_OVERLAPPED,  # type: ignore[name-defined]
                win32pipe.PIPE_TYPE_BYTE  # type: ignore[name-defined]
                | win32pipe.PIPE_READMODE_BYTE  # type: ignore[name-defined]
                | win32pipe.PIPE_WAIT,  # type: ignore[name-defined]
                win32pipe.PIPE_UNLIMITED_INSTANCES,  # type: ignore[name-defined]
                65536,  # out buffer size
                65536,  # in buffer size
                0,  # default timeout
                security_attributes,
            )

            if self._handle == win32file.INVALID_HANDLE_VALUE:  # type: ignore[name-defined]
                raise OSError("Failed to create named pipe")

        except Exception as e:
            raise OSError(f"Cannot create named pipe {pipe_name}: {e}")

    def _create_unix_socket(self, socket_path: str, backlog: int) -> None:
        """Create Unix domain socket server."""
        try:
            # Remove existing socket file if it exists
            if os.path.exists(socket_path):
                os.remove(socket_path)

            self._socket = socket.socket(
                socket.AF_UNIX,  # type: ignore[attr-defined]
                socket.SOCK_STREAM,
            )
            self._socket.bind(socket_path)
            self._socket.listen(backlog)

            # Restrict permissions to current user only
            os.chmod(socket_path, 0o600)

        except OSError as e:
            if self._socket:
                self._socket.close()
                self._socket = None
            raise OSError(f"Cannot create Unix socket {socket_path}: {e}")

    def accept(self, timeout: Optional[float] = None) -> Tuple[LocalClientSocket, str]:
        """Accept a client connection.

        Parameters
        ----------
        timeout : Optional[float], optional
            Accept timeout in seconds

        Returns
        -------
        Tuple[LocalClientSocket, str]
            Client socket and client address
        """
        if sys.platform == "win32":
            return self._accept_windows_pipe(timeout)
        else:
            return self._accept_unix_socket(timeout)

    def _accept_windows_pipe(self, timeout: Optional[float]) -> Tuple[LocalClientSocket, str]:
        """Accept connection on Windows named pipe with proper timeout handling."""
        if self._handle is None:
            raise ConnectionError("Server not listening")

        try:
            # Create overlapped structure for async operation
            overlapped = pywintypes.OVERLAPPED()  # type: ignore[name-defined]
            overlapped.hEvent = win32event.CreateEvent(  # type: ignore[name-defined]
                None, True, False, None
            )

            try:
                # Start asynchronous ConnectNamedPipe operation
                try:
                    win32pipe.ConnectNamedPipe(  # type: ignore[name-defined]
                        self._handle, overlapped
                    )
                except pywintypes.error as e:  # type: ignore[name-defined]
                    if e.winerror != 997:  # ERROR_IO_PENDING
                        # If it's not a pending operation, it might be an immediate connection
                        if e.winerror == 535:  # ERROR_PIPE_CONNECTED
                            # Pipe is already connected (client connected very quickly)
                            pass
                        else:
                            raise ConnectionError(f"ConnectNamedPipe failed: {e}")

                # Wait for the connection with timeout
                if timeout is not None:
                    timeout_ms = int(timeout * 1000)
                else:
                    timeout_ms = win32event.INFINITE  # type: ignore[name-defined]

                wait_result = win32event.WaitForSingleObject(  # type: ignore[name-defined]
                    overlapped.hEvent, timeout_ms
                )

                if wait_result == win32event.WAIT_TIMEOUT:  # type: ignore[name-defined]
                    # Cancel the overlapped operation
                    try:
                        win32file.CancelIo(self._handle)  # type: ignore[name-defined]
                    except Exception:
                        pass
                    raise TimeoutError(f"Accept operation timed out after {timeout} seconds")
                elif wait_result != win32event.WAIT_OBJECT_0:  # type: ignore[name-defined]
                    raise ConnectionError(f"Wait for connection failed with result: {wait_result}")

                # Get the result of the overlapped operation
                try:
                    win32file.GetOverlappedResult(  # type: ignore[name-defined]
                        self._handle, overlapped, False
                    )
                except pywintypes.error as e:  # type: ignore[name-defined]
                    if e.winerror != 535:  # ERROR_PIPE_CONNECTED is expected
                        raise ConnectionError(f"GetOverlappedResult failed: {e}")

                # Create client socket wrapper
                client = LocalClientSocket(self._logger)
                client._handle = self._handle
                client._address = self._address

                # Create new pipe instance for next connection
                self._create_windows_pipe(self._address)

                return client, self._address

            finally:
                win32api.CloseHandle(overlapped.hEvent)  # type: ignore[name-defined]

        except pywintypes.error as e:  # type: ignore[name-defined]
            raise ConnectionError(f"Accept failed: {e}")

    def _accept_unix_socket(self, timeout: Optional[float]) -> Tuple[LocalClientSocket, str]:
        """Accept connection on Unix domain socket."""
        if self._socket is None:
            raise ConnectionError("Server not listening")

        original_timeout = self._socket.gettimeout()
        try:
            if timeout is not None:
                self._socket.settimeout(timeout)

            conn, addr = self._socket.accept()

            # Create client socket wrapper
            client = LocalClientSocket(self._logger)
            client._socket = conn
            client._address = addr

            return client, addr

        except socket.timeout:
            # In Python 3.9, socket.timeout is not a subclass of TimeoutError
            # Convert to TimeoutError for consistency
            raise TimeoutError(f"Accept operation timed out after {timeout} seconds")
        finally:
            self._socket.settimeout(original_timeout)

    def close(self) -> None:
        """Close server socket."""
        super().close()

        # Close any additional pipe instances on Windows
        if sys.platform != "win32":
            # Clean up socket file
            if self._address and os.path.exists(self._address):
                try:
                    os.remove(self._address)
                except Exception as e:
                    self._logger.warning(f"Error removing socket file {self._address}: {e}")
