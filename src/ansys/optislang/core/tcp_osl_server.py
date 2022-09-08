"""Contains classes for plain TCP/IP communication with server."""

from datetime import datetime
import json
import logging
import os
import select
import socket
import struct
import threading
import time
from typing import Dict, Sequence, Tuple, Union
import uuid

from ansys.optislang.core import server_commands as commands
from ansys.optislang.core import server_queries as queries
from ansys.optislang.core.encoding import force_bytes, force_text
from ansys.optislang.core.errors import (
    ConnectionEstablishedError,
    ConnectionNotEstablishedError,
    EmptyResponseError,
    OslCommandError,
    OslCommunicationError,
    ResponseFormatError,
)
from ansys.optislang.core.osl_process import OslServerProcess
from ansys.optislang.core.osl_server import OslServer


def _get_current_timeout(initial_timeout: Union[float, None], start_time: float) -> None:
    """Get actual timeout value.

    The function will raise a timeout exception if the timeout has expired.

    Parameters
    ----------
    initial_timeout : float, None
        Initial timeout value. For non-zero value, the new timeout value is computed.
        If the timeout period value has elapsed, the timeout exception is raised.
        For zero value, the non-blocking mode is assumed and zero value is returned.
        For ``None``, the blocking mode is assumed and ``None`` is returned.
    start_time : float
        The time when the initial time out starts to count down. It is defined in seconds
        since the epoch as a floating point number.

    Raises
    ------
    TimeoutError
        Raised when the timeout expires.
    """
    if initial_timeout != 0 and initial_timeout is not None:
        elapsed_time = time.time() - start_time
        remaining_timeout = initial_timeout - elapsed_time
        if remaining_timeout <= 0:
            raise TimeoutError("Timeout has expired.")
        return remaining_timeout
    else:
        return initial_timeout


class TcpClient:
    r"""Client of the plain TCP/IP communication.

    Parameters
    ----------
    socket: socket.SocketType, None, optional
        Client socket.
    logger: Any, optional
        Object for logging. If ``None``, standard logging object is used. Defaults to ``None``.

    Examples
    --------
    Connect to the plain TCP/IP server with IP address of localhost and port 49690. Send
    the following message:
    '{ "What": "SYSTEMS_STATUS_INFO" }'

    >>> from ansys.optislang.core.tcp import TcpClient
    >>> client = TcpClient()
    >>> client.connect('127.0.0.1', 49690)
    >>> client.send_msg('{ "What": "SYSTEMS_STATUS_INFO" }')
    """

    _BUFFER_SIZE = pow(2, 12)
    # Response size in bytes. Value is assumed to be binary 64Bit unsigned integer.
    _RESPONSE_SIZE_BYTES = 8

    def __init__(self, socket: Union[socket.SocketType, None] = None, logger=None) -> None:
        """Initialize a new instance of the ``TcpClient`` class."""
        self.__socket = socket

        if logger is None:
            self._logger = logging.getLogger(__name__)
        else:
            self._logger = logger

    @property
    def remote_address(self) -> Union[Tuple[str, int], None]:
        """Get the remote address of the connection.

        Returns
        -------
        Tuple(str, int), None
            Remote host address which consists of IP address and port number, if connection is
            established; ``None`` otherwise.
        """
        if self.__socket is None:
            return None

        return self.__socket.getpeername()

    @property
    def local_address(self) -> Union[Tuple[str, int], None]:
        """Get the local address of the connection.

        Returns
        -------
        Tuple(str, int), None
            Local host address which consists of IP address and port number, if connection is
            established; ``None`` otherwise.
        """
        if self.__socket is None:
            return None

        return self.__socket.getsockname()

    @property
    def is_connected(self) -> bool:
        """Determine whether the connection has been established.

        Returns
        -------
        bool
            True if the connection has been established; False otherwise.
        """
        return self.__socket is not None

    def connect(self, host: str, port: int, timeout: Union[float, None] = 2) -> None:
        """Connect to the plain TCP/IP server.

        Parameters
        ----------
        host : str
            A string representation of an IPv4/v6 address or domain name.
        port : int
            A numeric port number.
        timeout : Union[float, None], optional
            Timeout in seconds to establish a connection. If a non-zero value is given,
            the function will raise a timeout exception if the timeout period value has elapsed
            before the operation has completed. If zero is given, the non-blocking mode is used.
            If ``None`` is given, the blocking mode is used. Defaults to 2 s.

        Raises
        ------
        ConnectionEstablishedError
            Raised when the connection is already established.
        ConnectionRefusedError
            Raised when the connection cannot be established.
        """
        if self.is_connected:
            raise ConnectionEstablishedError("Connection is already established.")

        start_time = time.time()

        for af, socktype, proto, canonname, sa in socket.getaddrinfo(
            host, port, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE
        ):
            try:
                self.__socket = socket.socket(af, socktype, proto)
            except OSError as ex:
                self.__socket = None
                continue
            self.__socket.settimeout(_get_current_timeout(timeout, start_time))
            try:
                self.__socket.connect(sa)
            except OSError:
                self.__socket.close()
                self.__socket = None
                continue

        if self.__socket is None:
            raise ConnectionRefusedError(
                f"Connection could not be established to host {host} and port {port}."
            )

        self._logger.info("Connection has been established to host %s and port %d.", host, port)

    def disconnect(self) -> None:
        """Disconnect from the server."""
        if self.is_connected:
            self.__socket.close()
            self.__socket = None

    def send_msg(self, msg: str, timeout: Union[float, None] = 5) -> None:
        """Send message to the server.

        Parameters
        ----------
        msg : str
            Message to send.
        timeout : Union[float, None], optional
            Timeout in seconds to send a message. If a non-zero value is given,
            the function will raise a timeout exception if the timeout period value has elapsed
            before the operation has completed. If zero is given, the non-blocking mode is used.
            If ``None`` is given, the blocking mode is used. Defaults to 5 s.

        Raises
        ------
        ConnectionNotEstablishedError
            Raised when the connection has not been established before function call.
        TimeoutError
            Raised when the timeout period value has elapsed before the operation has completed.
        OSError
            Raised when an error occurs while sending data.
        """
        if not self.is_connected:
            raise ConnectionNotEstablishedError(
                "Cannot send message. Connection is not established."
            )

        self._logger.debug("Sending message to %s. Message: %s", self.__socket.getpeername(), msg)
        data = force_bytes(msg)
        data_len = len(data)

        header = struct.pack("!QQ", data_len, data_len)

        self.__socket.settimeout(timeout)
        self.__socket.sendall(header + data)

    def send_file(self, file_path: str, timeout: Union[float, None] = 5) -> None:
        """Send content of the file to the server.

        Parameters
        ----------
        file_path : str
            Path to the file whose content is to be sent to the server.
        timeout : Union[float, None], optional
            Timeout in seconds to send the buffer of the read part of the file. If a non-zero value
            is given, the function will raise a timeout exception if the timeout period value
            has elapsed before the operation has completed. If zero is given, the non-blocking mode
            is used. If ``None`` is given, the blocking mode is used. Defaults to 5 s.
        Raises
        ------
        ConnectionNotEstablishedError
            Raised when the connection has not been established before function call.
        FileNotFoundError
            Raised when the specified file does exist.
        TimeoutError
            Raised when the timeout period value has elapsed before the operation has completed.
        OSError
            Raised when an error occurs while sending data.
        """
        if not self.is_connected:
            raise ConnectionNotEstablishedError("Cannot send file. Connection is not established.")
        if not os.path.isfile(file_path):
            raise FileNotFoundError(
                "Cannot send file. The file does not exist. File path: %s", file_path
            )

        self._logger.debug(
            "Sending file to %s. File path: %s", self.__socket.getpeername(), file_path
        )
        file_size = os.path.getsize(file_path)

        header = struct.pack("!QQ", file_size, file_size)

        with open(file_path, "rb") as file:
            self.__socket.settimeout(timeout)
            self.__socket.sendall(header)
            load = file.read(self.__class__._BUFFER_SIZE)
            while load:
                self.__socket.send(load)
                load = file.read(self.__class__._BUFFER_SIZE)

    def receive_msg(self, timeout: Union[float, None] = 5) -> str:
        """Receive message from the server.

        Parameters
        ----------
        timeout : Union[float, None], optional
            Timeout in seconds to receive a message. The function will raise a timeout exception
            if the timeout period value has elapsed before the operation has completed. If ``None``
            is given, the blocking mode is used. Defaults to 5 s.

        Returns
        -------
        str
            Received message from the server.

        Raises
        ------
        ConnectionNotEstablishedError
            Raised when the connection has not been established before function call.
        EmptyResponseError
            Raised when the empty message is received.
        ResponseFormatError
            Raised when the format of the received message is not valid.
        TimeoutError
            Raised when the timeout period value has elapsed before the operation has completed.
        ValueError
            Raised if the timeout value is a number not greater than zero.
        """
        if not self.is_connected:
            raise ConnectionNotEstablishedError(
                "Cannot receive message. Connection is not established."
            )

        if isinstance(timeout, float) and timeout <= 0:
            raise ValueError("Timeout value must be greater than zero or None.")

        start_time = time.time()

        msg_len = self._recv_response_length(timeout)
        if msg_len == 0:
            raise EmptyResponseError("The empty message has been received.")

        remain_timeout = _get_current_timeout(timeout, start_time)
        data = self._receive_bytes(msg_len, remain_timeout)
        if len(data) != msg_len:
            raise ResponseFormatError("Received data does not match declared data size.")

        return force_text(data)

    def receive_file(self, file_path: str, timeout: Union[float, None] = 5) -> None:
        """Receive file from the server.

        Parameters
        ----------
        file_path : str
            Path where the received file is to be saved.
        timeout : Union[float, None], optional
            Timeout in seconds to receive a buffer of the file part. The function will raise
            a timeout exception if the timeout period value has elapsed before the operation
            has completed. If ``None`` is given, the blocking mode is used. Defaults to 5 s.

        Raises
        ------
        ConnectionNotEstablishedError
            Raised when the connection has not been established before function call.
        EmptyResponseError
            Raised when the empty message is received.
        ResponseFormatError
            Raised when the format of the received data is not valid.
        TimeoutError
            Raised when the timeout period value has elapsed before the operation has completed.
        ValueError
            Raised if the timeout value is a number not greater than zero.
        OSError
            Raised when the file cannot be opened.
        """
        if not self.is_connected:
            raise ConnectionNotEstablishedError(
                "Cannot receive file. Connection is not established."
            )

        start_time = time.time()

        file_len = self._recv_response_length(timeout)
        if file_len == 0:
            raise EmptyResponseError("The empty file has been received.")

        remain_timeout = _get_current_timeout(timeout, start_time)
        self._fetch_file(file_len, file_path, remain_timeout)
        if os.path.getsize(file_path) != file_len:
            raise ResponseFormatError("Received data does not match declared data size.")

    def _recv_response_length(self, timeout: Union[float, None]) -> int:
        """Receive length of the response.

        Parameters
        ----------
        timeout : Union[float, None], optional
            Timeout in seconds to receive the response length. The function will raise a timeout
            exception if the timeout period value has elapsed before the operation has completed.
            If ``None`` is given, the blocking mode is used.

        Returns
        -------
        int
            Length of the response to be received.

        Raises
        ------
        TimeoutError
            Raised when the timeout period value has elapsed before the operation has completed.
        ResponseFormatError
            Raised when the response length specification is invalid.
        ValueError
            Raised if the timeout value is a number not greater than zero.
        """
        if isinstance(timeout, float) and timeout <= 0:
            raise ValueError("Timeout value must be greater than zero or None.")

        start_time = time.time()
        self.__socket.settimeout(timeout)

        response_len = -1
        bytes_to_receive = self.__class__._RESPONSE_SIZE_BYTES
        # read from socket until response size (twice) has been received
        while True:
            try:
                # Test if we will be able to read something from the connection.
                readable_sockets, _, _ = select.select([self.__socket], [], [], 1)
                if self.__socket in readable_sockets:
                    # Read and convert response size. Assume server sent response size twice.
                    # Sizes need to match.
                    response_len_1 = struct.unpack("!Q", self.__socket.recv(bytes_to_receive))[0]
                    response_len_2 = struct.unpack("!Q", self.__socket.recv(bytes_to_receive))[0]
                    if response_len_1 != response_len_2:
                        raise ResponseFormatError("The message size values do not match.")

                    response_len = response_len_1
                if response_len >= 0:
                    break
            except Exception as e:
                self._logger.debug(e)
                pass
            now = time.time()
            elapsed = now - start_time
            if timeout is not None and elapsed > timeout:
                raise TimeoutError("Time to receive message length has expired.")

        return response_len

    def _receive_bytes(self, count: int, timeout: Union[float, None]) -> bytes:
        """Receive specified number of bytes from the server.

        Parameters
        ----------
        count : int
            Number of bytes to be received from the server.
        timeout : Union[float, None], optional
            Timeout in seconds to receive specified number of bytes. The function will raise
            a timeout exception if the timeout period value has elapsed before the operation
            has completed. If ``None`` is given, the blocking mode is used.

        Returns
        -------
        bytes
            Received bytes.

        Raises
        ------
        TimeoutError
            Raised when the timeout period value has elapsed before the operation has completed.
        ValueError
            Raised when the number of bytes is not greater than zero.
            -or-
            Raised if the timeout value is a number not greater than zero.
        """
        if count <= 0:
            raise ValueError("Number of bytes must be greater than zero.")
        if isinstance(timeout, float) and timeout <= 0:
            raise ValueError("Timeout value must be greater than zero or None.")

        start_time = time.time()

        received = b""
        received_len = 0
        while received_len < count:
            remain = count - received_len
            if remain > self.__class__._BUFFER_SIZE:
                buff = self.__class__._BUFFER_SIZE
            else:
                buff = remain

            self.__socket.settimeout(_get_current_timeout(timeout, start_time))
            chunk = self.__socket.recv(buff)
            if not chunk:
                break
            received += chunk
            received_len += len(chunk)
        return received

    def _fetch_file(self, file_len: int, file_path: str, timeout: Union[float, None]) -> None:
        """Write received bytes from the server to the file.

        Parameters
        ----------
        file_len : int
            Number of bytes to be written.
        file_path : str
            Path to the file to which the received data is to be written.
        timeout : Union[float, None], optional
            Timeout in seconds to receive bytes from the server and write them to the file.
            The function will raise a timeout exception if the timeout period value has
            elapsed before the operation has completed. If ``None`` is given, the blocking mode
            is used.

        Raises
        ------
        TimeoutError
            Raised when the timeout period value has elapsed before the operation has completed.
        OSError
            Raised when the file cannot be opened.
        ValueError
            Raised if the timeout value is a number not greater than zero.
        """
        if isinstance(timeout, float) and timeout <= 0:
            raise ValueError("Timeout value must be greater than zero or None.")

        start_time = time.time()

        with open(file_path, "wb") as file:
            data_len = 0
            while data_len < file_len:
                remain = file_len - data_len
                if remain > self.__class__._BUFFER_SIZE:
                    buff = self.__class__._BUFFER_SIZE
                else:
                    buff = remain

                self.__socket.settimeout(_get_current_timeout(timeout, start_time))
                chunk = self.__socket.recv(buff)
                if not chunk:
                    break
                file.write(chunk)
                data_len += len(chunk)


class TcpOslServer(OslServer):
    """Class which provides access to optiSLang server using plain TCP/IP communication protocol.

    For remote connection, it is assumed that the optiSLang server process is already running
    on remote (or local) host. In that case, the host and port must be specified and other
    parameters are ignored.

    Parameters
    ----------
    host : str, optional
        A string representation of an IPv4/v6 address or domain name of running optiSLang server.
        Defaults to ``None``.
    port : int, optional
        A numeric port number of running optiSLang server. Defaults to ``None``.
    executable : str, optional
        Path to the optiSLang executable file which supposed to be executed on localhost.
        It is ignored when the host and port parameters are specified. Defaults to ``None``.
    project_path : str, optional
        Path to the optiSLang project file which is supposed to be used by new local optiSLang
        server. It is ignored when the host and port parameters are specified.
        - If the project file exists, it is opened.
        - If the project file does not exist, a new project is created on the specified path.
        - If the path is None, a new project is created in the temporary directory.
        Defaults to ``None``.
    no_save : bool, optional
        Determines whether not to save the specified project after all other actions are completed.
        It is ignored when the host and port parameters are specified. Defaults to ``False``.
    ini_timeout : float, optional
        Time in seconds to listen to the optiSLang server port. If the port is not listened
        for specified time, the optiSLang server is not started and RuntimeError is raised.
        It is ignored when the host and port parameters are specified. Defaults to 20 s.
    password : str, optional
        The server password. Use when communication with the server requires the request
        to contain a password entry. Defaults to ``None``.
    logger : Any, optional
        Object for logging. If ``None``, standard logging object is used. Defaults to ``None``.

    Raises
    ------
    RuntimeError
        Port listener cannot be started.
        -or-
        optiSLang server port is not listened for specified timeout value.

    Examples
    --------
    Start local optiSLang server, get optiSLang version and shutdown the server.
    >>> from ansys.optislang.core.tcp_osl_server import TcpOslServer
    >>> osl_server = TcpOslServer()
    >>> osl_version = osl_server.get_osl_version()
    >>> print(osl_version)
    >>> osl_server.shutdown()

    Connect to the remote optiSLang server, get optiSLang version and shutdown the server.
    >>> from ansys.optislang.core.tcp_osl_server import TcpOslServer
    >>> host = "192.168.101.1"  # IP address of the remote host
    >>> port = 49200            # Port of the remote optiSLang server
    >>> osl_server = TcpOslServer(host, port)
    >>> osl_version = osl_server.get_osl_version()
    >>> print(osl_version)
    >>> osl_server.shutdown()
    """

    _LOCALHOST = "127.0.0.1"
    _PRIVATE_PORTS_RANGE = (49152, 65535)
    _SHUTDOWN_WAIT = 5  # wait for local server to shutdown in second

    def __init__(
        self,
        host: str = None,
        port: int = None,
        executable: str = None,
        project_path: str = None,
        no_save: bool = False,
        ini_timeout: float = 20,
        password: str = None,
        logger=None,
    ) -> None:
        """Initialize a new instance of the ``TcpOslServer`` class."""
        self.__host = host
        self.__port = port
        self.__timeout = None
        self.__executable = executable

        if logger is None:
            self._logger = logging.getLogger(__name__)
        else:
            self._logger = logger

        self.__project_path = project_path
        self.__no_save = no_save
        self.__password = password
        self.__osl_process = None

        if self.__host is None or self.__port is None:
            self._start_local(ini_timeout)

    def _get_server_info(self) -> Dict:
        """Get information about the application, the server configuration and the open projects.

        Returns
        -------
        Dict
            Information data as dictionary.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self._send_command(queries.server_info())

    def _get_basic_project_info(self) -> Dict:
        """Get basic project info, like name, location, global settings and status.

        Returns
        -------
        Dict
            Information data as dictionary.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self._send_command(queries.basic_project_info())

    def close(self) -> None:
        """Close the current project.

        Raises
        ------
        NotImplementedError
            Currently, command is not supported in batch mode.
        """
        raise NotImplementedError("Currently, command is not supported in batch mode.")

    def get_osl_version(self) -> str:
        """Get version of used optiSLang.

        Returns
        -------
        str
            optiSLang version.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        server_info = self._get_server_info()
        return server_info["application"]["version"]

    def get_project_description(self) -> str:
        """Get description of optiSLang project.

        Returns
        -------
        str
            optiSLang project description. If no project is loaded in the optiSLang,
            returns ``None``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        project_info = self._get_basic_project_info()
        if len(project_info["projects"]) == 0:
            return None
        return project_info["projects"][0]["settings"]["short_description"]

    def get_project_location(self) -> str:
        """Get path to the optiSLang project file.

        Returns
        -------
        str
            Path to the optiSLang project file. If no project is loaded in the optiSLang,
            returns ``None``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        project_info = self._get_basic_project_info()
        if len(project_info["projects"]) == 0:
            return None
        return project_info["projects"][0]["location"]

    def get_project_name(self) -> str:
        """Get name of the optiSLang project.

        Returns
        -------
        str
            Name of the optiSLang project. If no project is loaded in the optiSLang,
            returns ``None``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        project_info = self._get_basic_project_info()
        if len(project_info["projects"]) == 0:
            return None
        return project_info["projects"][0]["name"]

    def get_project_status(self) -> str:
        """Get status of the optiSLang project.

        Returns
        -------
        str
            optiSLang project status. If no project is loaded in the optiSLang,
            returns ``None``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        project_info = self._get_basic_project_info()
        if len(project_info["projects"]) == 0:
            return None
        return project_info["projects"][0]["state"]

    def get_timeout(self) -> Union[float, None]:
        """Get current timeout value for execution of commands.

        Returns
        -------
        timeout: Union[float, None]
            Timeout in seconds to perform commands.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.__timeout

    def get_working_dir(self) -> str:
        """Get path to the optiSLang project working directory.

        Returns
        -------
        str
            Path to the optiSLang project working directory. If no project is loaded
            in the optiSLang, returns ``None``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        project_info = self._get_basic_project_info()
        if len(project_info["projects"]) == 0:
            return None
        return project_info["projects"][0]["working_dir"]

    def new(self) -> None:
        """Create a new project.

        Parameters
        ----------
        timeout : float, None, optional
            Timeout in seconds to perform the command. It must be greater than zero or ``None``.
            The function will raise a timeout exception if the timeout period value has
            elapsed before the operation has completed. If ``None`` is given, the function
            will wait until the function is finished (no timeout exception is raised).
            Defaults to ``None``.

        Raises
        ------
        NotImplementedError
            Currently, command is not supported in batch mode.
        """
        raise NotImplementedError("Currently, command is not supported in batch mode.")

    def open(
        self,
        file_path: str,
        force: bool,
        restore: bool,
        reset: bool,
    ) -> None:
        """Open a new project.

        Parameters
        ----------
        file_path : str
            Path to the optiSLang project file to open.
        force : bool
            # TODO: description of this parameter is missing in ANSYS help
        restore : bool
            # TODO: description of this parameter is missing in ANSYS help
        reset : bool
            # TODO: description of this parameter is missing in ANSYS help
        timeout : float, None, optional
            Timeout in seconds to perform the command. It must be greater than zero or ``None``.
            The function will raise a timeout exception if the timeout period value has
            elapsed before the operation has completed. If ``None`` is given, the function
            will wait until the function is finished (no timeout exception is raised).
            Defaults to ``None``.

        Raises
        ------
        NotImplementedError
            Currently, command is not supported in batch mode.
        """
        raise NotImplementedError("Currently, command is not supported in batch mode.")

    def reset(self):
        """Reset complete project.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self._send_command(commands.reset(password=self.__password))

    def run_python_script(
        self,
        script: str,
        args: Union[Sequence[object], None] = None,
    ) -> Tuple[str, str]:
        """Load a Python script in a project context and execute it.

        Parameters
        ----------
        script : str
            Python commands to be executed on the server.
        args : Sequence[object], None, optional
            Sequence of arguments used in Python script. Defaults to ``None``.

        Returns
        -------
        Tuple[str, str]
            STDOUT and STDERR from executed Python script.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        responses = self._send_command(commands.run_python_script(script, args, self.__password))
        std_out = ""
        std_err = ""
        for response in responses:
            std_out += response.get("std_out", "")
            std_err += response.get("std_err", "")

        return (std_out, std_err)

    def run_python_file(
        self,
        file_path: str,
        args: Union[Sequence[object], None] = None,
    ) -> Tuple[str, str]:
        """Read python script from the file, load it in a project context and execute it.

        Parameters
        ----------
        file_path : str
            Path to the Python script file which content is supposed to be executed on the server.
        args : Sequence[object], None, optional
            Sequence of arguments used in Python script. Defaults to ``None``.

        Returns
        -------
        Tuple[str, str]
            STDOUT and STDERR from executed Python script.

        Raises
        ------
        FileNotFoundError
            Raised when the specified Python script file does not exist.
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError("Python script file does not exist.")

        with open(file_path, "r") as file:
            script = file.read()

        return self.run_python_script(script, args)

    def save(self) -> None:
        """Save the changed data and settings of the current project.

        Raises
        ------
        NotImplementedError
            Currently, command is not supported in batch mode.
        """
        raise NotImplementedError("Currently, command is not supported in batch mode.")

    def save_as(
        self,
        file_path: str,
        force: bool,
        restore: bool,
        reset: bool,
    ) -> None:
        """Save and open the current project at a new location.

        Parameters
        ----------
        file_path : str
            Path where to save the project file.
        force : bool
            # TODO: description of this parameter is missing in ANSYS help
        restore : bool
            # TODO: description of this parameter is missing in ANSYS help
        reset : bool
            # TODO: description of this parameter is missing in ANSYS help

        Raises
        ------
        NotImplementedError
            Currently, command is not supported in batch mode.
        """
        raise NotImplementedError("Currently, command is not supported in batch mode.")

    def save_copy(self, file_path: str) -> None:
        """Save the current project as a copy to a location.

        Parameters
        ----------
        file_path : str
            Path where to save the project copy.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self._send_command(commands.save_copy(file_path, self.__password))

    def set_timeout(self, timeout: Union[float, None] = None) -> None:
        """Set timeout value for execution of commands.

        Parameters
        ----------
        timeout: Union[float, None]
            Timeout in seconds to perform commands, it must be greater than zero or ``None``.
            Another functions will raise a timeout exception if the timeout period value has
            elapsed before the operation has completed. If ``None`` is given, functions
            will wait until they're finished (no timeout exception is raised).
            Defaults to ``None``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        ValueError
            Raised when timeout <= 0.
        TypeError
            Raised when timeout not Union[float, None].
        """
        if timeout is None:
            self.__timeout = timeout
        elif isinstance(timeout, float):
            if timeout > 0:
                self.__timeout = timeout
            else:
                raise ValueError(
                    "Timeout must be float greater than zero or ``None`` but "
                    f"``{timeout}`` was given."
                )
        else:
            raise TypeError(
                "Invalid type of timeout, timeout must be float greater than zero or "
                f"``None`` but {type(timeout)} was given."
            )

    def shutdown(self, force: bool = False) -> None:
        """Shutdown the server.

        Stop listening for incoming connections, discard pending requests, and shut down
        the server. Batch mode exclusive: Continue project run until execution finished.
        Terminate optiSLang.

        Parameters
        ----------
        force : bool, optional
            Determines whether to force shutdown the local optiSLang server. Has no effect when
            the connection is established to the remote optiSLang server. In all cases, it is tried
            to shutdown the optiSLang server process in a proper way. However, if the force
            parameter is ``True``, after a while, the process is forced to terminate and
            no exception is raised. Defaults to ``False``.

        Raises
        ------
        OslCommunicationError
            Raised when the parameter force is ``False`` and an error occurs while communicating
            with server.
        OslCommandError
            Raised when the parameter force is ``False`` and the command or query fails.
        TimeoutError
            Raised when the parameter force is ``False`` and the timeout float value expires.
        """
        try:
            self._send_command(commands.shutdown(self.__password))
        except Exception:
            if not force or self.__osl_process is None:
                raise
        finally:
            if force and self.__osl_process is not None:
                self._force_shutdown_local_process()

    def _force_shutdown_local_process(self):
        """Force shutdown local optiSLang server process.

        It waits a while and then terminates the process.
        """
        start_time = datetime.now()
        while (
            self.__osl_process.is_running()
            and (datetime.now() - start_time).seconds < self.__class__._SHUTDOWN_WAIT
        ):
            time.sleep(0.5)

        if self.__osl_process.is_running():
            self.__osl_process.terminate()
        self.__osl_process = None
        self.__host = None
        self.__port = None

    def start(self, wait_for_finish: bool = True) -> None:
        """Start project execution.

        Parameters
        ----------
        wait_for_finish : bool, optional
            Determines whether this function call should wait on the optiSlang to finish
            the command execution. I.e. don't continue on next line of python script after command
            was successfully sent to optiSLang but wait for execution of flow inside optiSLang.
            Defaults to ``True``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        start_time = time.time()
        self._send_command(commands.start(self.__password))

        if wait_for_finish:
            self._wait_for_finish(_get_current_timeout(self.__timeout, start_time))

    def stop(self, wait_for_finish: bool = True) -> None:
        """Stop project execution.

        Parameters
        ----------
        wait_for_finish : bool, optional
            Determines whether this function call should wait on the optiSlang to finish
            the command execution. I.e. don't continue on next line of python script after command
            was successfully sent to optiSLang but wait for execution of command inside optiSLang.
            Defaults to ``True``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        start_time = time.time()
        status = self.get_project_status()

        not_stopped_states = [
            "IDLE",
            "FINISHED",
            "STOP_REQUESTED",
            "STOPPED",
            "ABORT_REQUESTED",
            "ABORTED",
        ]

        if status not in not_stopped_states:
            self._send_command(commands.stop(self.__password))

            if wait_for_finish:
                self._wait_for_finish(_get_current_timeout(self.__timeout, start_time))

    def stop_gently(self, wait_for_finish: bool = True) -> None:
        """Stop project execution after the current design is finished.

        Parameters
        ----------
        wait_for_finish : bool, optional
            Determines whether this function call should wait on the optiSlang to finish
            the command execution. I.e. don't continue on next line of python script after command
            was successfully sent to optiSLang but wait for execution of command inside optiSLang.
            Defaults to ``True``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        start_time = time.time()
        status = self.get_project_status()

        not_gently_stopped_states = ["IDLE", "FINISHED", "STOPPED", "ABORT_REQUESTED", "ABORTED"]

        if status not in not_gently_stopped_states:
            self._send_command(commands.stop_gently(self.__password))

            if wait_for_finish:
                self._wait_for_finish(_get_current_timeout(self.__timeout, start_time))

    def _unregister_listener(self, uuid: str) -> None:
        """Unregister a listener.

        Parameters
        ----------
        uuid : str
            Specific unique ID for the TCP listener.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self._send_command(commands.unregister_listener(uuid, self.__password))

    def _start_local(self, ini_timeout: float) -> None:
        """Start local optiSLang server.

        Parameters
        ----------
        ini_timeout : Union[float], optional
            Time in seconds to listen to the optiSLang server port. If the port is not listened
            for specified time, the optiSLang server is not started and RuntimeError is raised.

        Raises
        ------
        RuntimeError
            Raised when the optiSLang server is already started.
            -or-
            Port listener cannot be started.
            -or-
            optiSLang server port is not listened for specified timeout value.
        """
        if self.__osl_process is not None:
            raise RuntimeError("optiSLang server is already started.")

        listener_socket = None
        listener_uid = uuid.uuid4()
        try:
            listener_socket = self.__init_port_listener(self.__class__._PRIVATE_PORTS_RANGE)
            if listener_socket is None:
                raise RuntimeError("Cannot start listener of optiSLang server port.")

            listener_thread = threading.Thread(
                target=self.__listen_port,
                name="PyOptiSLang.OslPortListener",
                args=(listener_socket, ini_timeout),
                daemon=True,
            )
            listener_thread.start()

            self.__osl_process = OslServerProcess(
                self.__executable,
                project_path=self.__project_path,
                no_save=self.__no_save,
                password=self.__password,
                listener=(self.__class__._LOCALHOST, listener_socket.getsockname()[1]),
                listener_id=str(listener_uid),
                logger=self._logger,
            )
            self.__osl_process.start()

            listener_thread.join()
        finally:
            if listener_socket is not None:
                listener_socket.close()

        if self.__port is None:
            self.__osl_process.terminate()
            self.__osl_process = None
            raise RuntimeError("Cannot get optiSLang server port.")

        self.__host = self.__class__._LOCALHOST

        try:
            self._unregister_listener(str(listener_uid))
        except Exception as ex:
            self._logger.warn("Cannot unregister port listener: %s", ex)

    def __init_port_listener(self, port_range: Tuple[int, int]) -> socket.socket:
        """Initialize port listener.

        Parameters
        ----------
        port_range : Tuple[int, int]
            Defines the port range for port listener. Defaults to ``None``.

        Returns
        -------
        socket
            Listener socket.
        """
        listener_socket = None
        for port in range(port_range[0], port_range[1] + 1):
            try:
                listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                listener_socket.bind((self.__class__._LOCALHOST, port))
                listener_socket.listen(5)
                self._logger.debug("Listening on port: %d", port)
                break
            except IOError as ex:
                if listener_socket is not None:
                    listener_socket.close()
                    listener_socket = None

        return listener_socket

    def __listen_port(self, listener_socket: socket.socket, timeout: float) -> None:
        """Listen to the optiSLang server port.

        Parameters
        ----------
        listener_socket : socket.socket
            Socket of the port listener.
        timeout : float
            Timeout in seconds for listening port.
        """
        listener_socket.settimeout(timeout)
        start_time = datetime.now()
        while True:
            if (datetime.now() - start_time).seconds > timeout:
                self._logger.info("OptiSLang server port listening timed out.")
                break

            client = None
            try:
                clientsocket, address = listener_socket.accept()
                self._logger.debug("Connection from %s has been established.", address)

                client = TcpClient(clientsocket)
                message = client.receive_msg()
                self._logger.debug("Received message from client: %s", message)

                data_dict = json.loads(message)
                self.__port = int(data_dict["port"])
                self._logger.info("optiSLang server port has been received: %d", self.__port)
                break
            except Exception as ex:
                self._logger.warning(ex)
            finally:
                if client is not None:
                    client.disconnect()

    def _send_command(self, command: str) -> Dict:
        """Send command or query to the optiSLang server.

        Parameters
        ----------
        command : str
            Command or query to be executed on optiSLang server.

        Returns
        -------
        Dict
            Response from the server.

        Raises
        ------
        RuntimeError
            Raised when the optiSLang server is not started.
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout expires.
        """
        if self.__host is None or self.__port is None:
            raise RuntimeError("optiSLang server is not started.")

        start_time = time.time()
        self._logger.debug("Sending command or query to the server: %s", command)
        client = TcpClient(logger=self._logger)
        try:
            client.connect(
                self.__host, self.__port, timeout=_get_current_timeout(self.__timeout, start_time)
            )
            client.send_msg(command, timeout=_get_current_timeout(self.__timeout, start_time))
            response_str = client.receive_msg(
                timeout=_get_current_timeout(self.__timeout, start_time)
            )
        except TimeoutError as ex:
            raise
        except Exception as ex:
            raise OslCommunicationError(
                "An error occurred while communicating with the optiSLang server."
            ) from ex
        finally:
            client.disconnect()

        self._logger.debug("Response received: %s", response_str)
        response = json.loads(response_str)

        if isinstance(response, list):
            for resp_elem in response:
                self.__class__.__check_command_response(resp_elem)
        else:
            self.__class__.__check_command_response(response)

        return response

    @staticmethod
    def __check_command_response(response: Dict) -> None:
        """Check whether the server response for a sent command contains any failure information.

        Parameters
        ----------
        response : Dict
            Server response as dictionary.

        Raises
        ------
        OslCommandError
            Raised when the server response for the sent command contains any failure information.
        """
        if "status" in response and response["status"].lower() == "failure":
            message = None
            if "message" in response:
                message = response["message"]
            if "std_err" in response:
                message += "; " + response["std_err"]
            if message is None:
                message = "Command error: " + str(response)
            raise OslCommandError(message)

    def _wait_for_finish(self, timeout: Union[float, None]) -> None:
        """Wait on optiSLang to finish the project run.

        Parameters
        ----------
        desired_status : str
            The project status to wait for.
        timeout : Union[float, None], optional
            Timeout in seconds to wait on optiSlang to finish the project run. Must be greater
            than zero or ``None``. The function will raise a timeout exception if the timeout
            period value has elapsed before the operation has completed. If ``None`` is given,
            the function will wait until the function is finished (no timeout exception is raised).
            Defaults to ``None``.
        Raises
        ------
        TimeoutError
            Raised when the timeout expires.
        """
        start_time = time.time()
        while True:
            remain_time = _get_current_timeout(timeout, start_time)
            status = self.get_project_status()
            if status == "FINISHED" or status == "STOPPED" or status == "ABORTED":
                return

            self._logger.debug("Waiting for project run to finish...")
            time.sleep(1)
