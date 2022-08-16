"""Contains classes for plain TCP/IP communication with server."""

from datetime import datetime
import json
import logging
import os
import socket
import struct
import threading
import time
from typing import Dict, Sequence, Tuple, Union
import uuid

from ansys.optislang.core import IRON_PYTHON
from ansys.optislang.core import server_commands as commands
from ansys.optislang.core import server_queries as queries
from ansys.optislang.core.encoding import force_bytes, force_text
from ansys.optislang.core.errors import (
    ConnectionNotEstablishedError,
    EmptyMessageError,
    MessageFormatError,
    OslCommandError,
    OslCommunicationError,
)
from ansys.optislang.core.osl_process import OslServerProcess
from ansys.optislang.core.osl_server import OslServer


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
    def timeout(self) -> Union[float, None]:
        """Get timeout for operations.

        Returns
        -------
        float, None
            The timeout in seconds (float) associated with socket operations, or ``None`` if
            no timeout is set.
        """
        if self.__socket is None:
            return None

        return self.__socket.gettimeout()

    def connect(self, host: str, port: int, timeout: Union[float, None] = 2) -> None:
        """Connect to the plain TCP/IP server.

        Parameters
        ----------
        host : str
            A string representation of an IPv4/v6 address or domain name.
        port : int
            A numeric port number.
        timeout : float, None, optional
            Timeout in seconds to establish a connection. If a non-zero value is given,
            the function will raise a timeout exception if the timeout period value has elapsed
            before the operation has completed. If zero is given, the non-blocking mode is used.
            If ``None`` is given, the blocking mode is used. Defaults to 2 s.

        Raises
        ------
        ConnectionRefusedError
            Raised when the connection cannot be established.
        """
        for af, socktype, proto, canonname, sa in socket.getaddrinfo(
            host, port, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE
        ):
            try:
                self.__socket = socket.socket(af, socktype, proto)
            except OSError as ex:
                self.__socket = None
                continue
            self.__socket.settimeout(timeout)
            try:
                self.__socket.connect(sa)
            except OSError as ex:
                self.__socket.close()
                self.__socket = None
                continue

        if self.__socket is None:
            raise ConnectionRefusedError(
                f"Connection could not be established to host {host} " f"and port {port}"
            )

        self._logger.info("Connection has been established to host %s and port %d", host, port)

    def disconnect(self) -> None:
        """Disconnect from the server."""
        if self.__socket is not None:
            self.__socket.close()
            self.__socket = None

    def send_msg(self, msg: str, timeout: Union[float, None] = 5) -> None:
        """Send message to the server.

        Parameters
        ----------
        msg : str
            Message to send.
        timeout : float, None, optional
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
        if self.__socket is None:
            raise ConnectionNotEstablishedError(
                "Cannot send message. Connection is not established."
            )

        self._logger.debug("Sending message to %s. Message: %s", self.__socket.getpeername(), msg)
        data = force_bytes(msg)
        data_len = len(data)

        pack_format = "!QQ" if IRON_PYTHON else b"!QQ"
        header = struct.pack(pack_format, data_len, data_len)

        self.__socket.settimeout(timeout)
        self.__socket.sendall(header + data)

    def send_file(self, file_path: str, timeout: Union[float, None] = 5) -> None:
        """Send content of the file to the server.

        Parameters
        ----------
        file_path : str
            Path to the file whose content is to be sent to the server.
        timeout : float, None, optional
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
        if self.__socket is None:
            raise ConnectionNotEstablishedError("Cannot send file. Connection is not established.")
        if not os.path.isfile(file_path):
            raise FileNotFoundError(
                "Cannot send file. The file does not exist. File path: %s", file_path
            )

        self._logger.debug(
            "Sending file to %s. File path: %s", self.__socket.getpeername(), file_path
        )
        file_size = os.path.getsize(file_path)

        pack_format = "!QQ" if IRON_PYTHON else b"!QQ"
        header = struct.pack(pack_format, file_size, file_size)

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
        timeout : float, None, optional
            Timeout in seconds to receive a message. If a non-zero value is given,
            the function will raise a timeout exception if the timeout period value has elapsed
            before the operation has completed. If zero is given, the non-blocking mode is used.
            If ``None`` is given, the blocking mode is used. Defaults to 5 s.

        Returns
        -------
        str
            Received message from the server.

        Raises
        ------
        ConnectionNotEstablishedError
            Raised when the connection has not been established before function call.
        EmptyMessageError
            Raised when the empty message is received.
        MessageFormatError
            Raised when the format of the received message is not valid.
        TimeoutError
            Raised when the timeout period value has elapsed before the operation has completed.
        """
        if self.__socket is None:
            raise ConnectionNotEstablishedError(
                "Cannot receive message. Connection is not established."
            )

        self.__socket.settimeout(timeout)
        msg_len = self._recv_message_length()
        data = self._receive_bytes(msg_len)
        if len(data) != msg_len:
            raise MessageFormatError("Received data does not match declared data size.")

        return force_text(data)

    def receive_file(self, file_path: str, timeout: Union[float, None] = 5) -> None:
        """Receive file from the server.

        Parameters
        ----------
        file_path : str
            Path where the received file is to be saved.
        timeout : float, None, optional
            Timeout in seconds to receive a buffer of the file part. If a non-zero value is given,
            the function will raise a timeout exception if the timeout period value has elapsed
            before the operation has completed. If zero is given, the non-blocking mode is used.
            If ``None`` is given, the blocking mode is used. Defaults to 5 s.

        Raises
        ------
        ConnectionNotEstablishedError
            Raised when the connection has not been established before function call.
        EmptyMessageError
            Raised when the no data is received.
        MessageFormatError
            Raised when the format of the received data is not valid.
        TimeoutError
            Raised when the timeout period value has elapsed before the operation has completed.
        OSError
            Raised when the file cannot be opened.
        """
        if self.__socket is None:
            raise ConnectionNotEstablishedError(
                "Cannot receive file. Connection is not established."
            )

        self.__socket.settimeout(timeout)
        msg_len = self._recv_message_length()
        self._write_bytes(msg_len, file_path)
        if os.path.getsize(file_path) != msg_len:
            raise MessageFormatError("Received data does not match declared data size.")

    def _recv_message_length(self) -> int:
        """Receive length of the message to be received from the server.

        Returns
        -------
        int
            Length of the message to be received.

        Raises
        ------
        EmptyMessageError
            Raised when the empty message is received.
        MessageFormatError
            Raised when the message length specification is invalid.
        """
        header_field_1 = self._receive_bytes(8)
        header_field_2 = self._receive_bytes(8)

        if len(header_field_1) == 0 or len(header_field_2) == 0:
            raise EmptyMessageError("The empty message has been received.")
        if len(header_field_1) != 8 or len(header_field_2) != 8:
            raise MessageFormatError("The message header fields do not match.")

        pack_format = "!Q" if IRON_PYTHON else b"!Q"
        msg_len_1 = struct.unpack(pack_format, header_field_1)[0]
        msg_len_2 = struct.unpack(pack_format, header_field_2)[0]
        if msg_len_1 != msg_len_2:
            raise MessageFormatError("The message size values do not match.")

        return msg_len_1

    def _receive_bytes(self, count: int) -> bytes:
        """Receive specified number of bytes from the server.

        Parameters
        ----------
        count : int
            Number of bytes to be received from the server.

        Returns
        -------
        bytes
            Received bytes.
        """
        data = b""
        data_len = 0
        while data_len < count:
            remain = count - data_len
            if remain > self.__class__._BUFFER_SIZE:
                buff = self.__class__._BUFFER_SIZE
            else:
                buff = remain
            chunk = self.__socket.recv(buff)
            if not chunk:
                break
            data += chunk
            data_len += len(chunk)
        return data

    def _write_bytes(self, count: int, file_path: str) -> None:
        """Write received bytes from the server to the file.

        Parameters
        ----------
        count : int
            Number of bytes to be written.
        file_path : str
            Path to the file to which the received data is to be written.

        Raises
        ------
        OSError
            Raised when the file cannot be opened.
        """
        with open(file_path, "wb") as file:
            data_len = 0
            while data_len < count:
                remain = count - data_len
                if remain > self.__class__._BUFFER_SIZE:
                    buff = self.__class__._BUFFER_SIZE
                else:
                    buff = remain
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
    timeout : float, optional
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
    # TODO: Add example
    """

    _LOCALHOST = "127.0.0.1"
    _PRIVATE_PORTS_RANGE = (49152, 65535)
    _SHUTDOWN_WAIT = 60  # wait for local server to shutdown in second

    def __init__(
        self,
        host: str = None,
        port: int = None,
        executable: str = None,
        project_path: str = None,
        no_save: bool = False,
        timeout: float = 20,
        password: str = None,
        logger=None,
    ) -> None:
        """Initialize a new instance of the ``TcpOslServer`` class."""
        self.__host = host
        self.__port = port

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
            self._start_local(timeout)

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
        """
        return self._send_command(queries.server_info())

    def _get_basic_project_info(self) -> Dict:
        """Get basic project info, like name, location, global settings and status.

        Returns
        -------
        Dict
            Information data as dictionary.
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
        """
        project_info = self._get_basic_project_info()
        if len(project_info["projects"]) == 0:
            return None
        return project_info["projects"][0]["state"]

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
        """
        project_info = self._get_basic_project_info()
        if len(project_info["projects"]) == 0:
            return None
        return project_info["projects"][0]["working_dir"]

    def new(self) -> None:
        """Create a new project.

        Raises
        ------
        NotImplementedError
            Currently, command is not supported in batch mode.
        """
        raise NotImplementedError("Currently, command is not supported in batch mode.")

    def open(self, file_path: str, force: bool, restore: bool, reset: bool) -> None:
        """Open a new project.

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
        """
        self._send_command(commands.reset(password=self.__password))

    def run_python_commands(
        self, script: str, args: Union[Sequence[object], None] = None
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
        """
        responses = self._send_command(commands.run_python_script(script, args, self.__password))
        std_out = ""
        std_err = ""
        for response in responses:
            std_out += response.get("std_out", "")
            std_err += response.get("std_err", "")

        return (std_out, std_err)

    def run_python_script(
        self, script_path: str, args: Union[Sequence[object], None] = None
    ) -> Tuple[str, str]:
        """Read python script from the file, load it in a project context and execute it.

        Parameters
        ----------
        script_path : str
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
        """
        if not os.path.isfile(script_path):
            raise FileNotFoundError("Python script file does not exist.")

        with open(script_path, "r") as file:
            script = file.readlines()

        return self.run_python_commands(script, args)

    def save(self) -> None:
        """Save the changed data and settings of the current project.

        Raises
        ------
        NotImplementedError
            Currently, command is not supported in batch mode.
        """
        raise NotImplementedError("Currently, command is not supported in batch mode.")

    def save_as(self, file_path: str, force: bool, restore: bool, reset: bool) -> None:
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
        """
        self._send_command(commands.save_copy(file_path, self.__password))

    def shutdown(self) -> None:
        """Shutdown the server.

        Stop listening for incoming connections, discard pending requests, and shut down
        the server. Batch mode exclusive: Continue project run until execution finished.
        Terminate optiSLang.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        """
        self._send_command(commands.shutdown(self.__password))

        if self.__osl_process is not None:
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

    def start(self) -> None:
        """Start project execution.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        """
        self._send_command(commands.start(self.__password))

    def stop(self) -> None:
        """Stop project execution.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        """
        self._send_command(commands.stop(self.__password))

    def stop_gently(self) -> None:
        """Stop project execution after the current design is finished.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        """
        self._send_command(commands.stop_gently(self.__password))

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
        """
        self._send_command(commands.unregister_listener(uuid, self.__password))

    def _start_local(self, timeout) -> None:
        """Start local optiSLang server.

        Parameters
        ----------
        timeout : float, optional
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
                args=(listener_socket, timeout),
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

    def _send_command(self, command: str, timeout: Union[float, None] = None) -> Dict:
        """Send command or query to the optiSLang server.

        Parameters
        ----------
        command : str
            Command or query to be executed on optiSLang server.
        timeout : float, None
            Timeout in seconds to send a command. Must be greater than zero or ``None``.
            If ``None``, Defaults to ``None``.

        Returns
        -------
        Dict
            Response from the server.

        Raises
        ------
        RuntimeError
            Raised when the optiSLang server is not started.
        ValueError
            Raised when the timeout is lower than or equal to zero.
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        """
        if self.__host is None or self.__port is None:
            raise RuntimeError("optiSLang server is not started.")
        if timeout is not None and timeout <= 0:
            raise ValueError("timeout must be greater than zero or None.")

        self._logger.debug("Sending command or query to the server: %s", command)
        client = TcpClient(logger=self._logger)
        try:
            client.connect(self.__host, self.__port, timeout)
            client.send_msg(command, timeout)
            response_str = client.receive_msg(timeout)
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
