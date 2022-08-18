"""Contains Optislang class which provides python API for optiSLang application."""
from typing import Sequence, Tuple, Union

from ansys.optislang.core import LOG
from ansys.optislang.core.osl_server import OslServer
from ansys.optislang.core.tcp_osl_server import TcpOslServer


class Optislang:
    """Connects to the optiSLang application and provides an API to control it.

    For remote connection, it is assumed that the optiSLang server process is already running
    on remote (or local) host. In that case, the host and port must be specified and parameters
    related to the execution of the new optiSLang server are ignored.

    For execution of optiSLang locally, both host and port parameters must be ``None``. Other
    parameters can be optionally specified.

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
        Time in seconds to connect to the optiSLang server. Defaults to 20 s.
    name : str, optional
        Identifier of the optiSLang instance.
    password : str, optional
        The server password. Use when communication with the server requires the request
        to contain a password entry. Defaults to ``None``.
    loglevel : str, optional
        Logging level. The following options are available:
        - CRITICAL: Log errors which are fatal for the application.
        - ERROR: Log errors which are fatal for some operation, but not for application.
        - WARNING: Log some oddities or potential problems.
        - INFO: Log some useful information that program works as expected.
        - DEBUG: The most grained logging.

    Raises
    ------
    RuntimeError
        Raised when the connection to the optiSLang server cannot be established in specified time.

    Examples
    --------
    Start and connect to the local optiSLang server, get version of used optiSLang, print it
    and shutdown the server.

    >>> from ansys.optislang.core import Optislang
    >>> osl = Optislang()
    >>> osl_version = osl.get_osl_version()
    >>> print(osl_version)
    >>> osl.shutdown()
    """

    def __init__(
        self,
        host: str = None,
        port: int = None,
        executable: str = None,
        project_path: str = None,
        no_save: bool = False,
        timeout: float = 20,
        name: str = None,
        password: str = None,
        loglevel: str = None,
    ) -> None:
        """Initialize a new instance of the ``Optislang`` class."""
        self.__host = host
        self.__port = port
        self.__executable = executable
        self.__project_path = project_path
        self.__no_save = no_save
        self.__timeout = timeout
        self.__name = name
        self.__password = password

        self._logger = LOG.add_instance_logger(self.name, self, loglevel)
        self.__osl_server: OslServer = self.__init_osl_server("tcp")

    def __init_osl_server(self, server_type: str) -> OslServer:
        """Initialize optiSLang server.

        Parameters
        ----------
        server_type : str, optional
            Type of the optiSLang server. The following options are available:
            - "tcp": plain TCP/IP communication protocol is used
            Defaults to "tcp".

        Returns
        -------
        OslServer
            OptiSlang server object.

        Raises
        ------
        NotImplementedError
            Raised when the specified server type is not supported.
        """
        if server_type.lower() == "tcp":
            return TcpOslServer(
                host=self.__host,
                port=self.__port,
                executable=self.__executable,
                project_path=self.__project_path,
                no_save=self.__no_save,
                timeout=self.__timeout,
                password=self.__password,
                logger=self._logger,
            )
        else:
            raise NotImplementedError(f'OptiSLang server of type "{server_type}" is not supported.')

    @property
    def name(self) -> str:
        """Instance unique identifier."""
        if not self.__name:
            if self.__host or self.__port:
                self.__name = f"optiSLang_{self.__host}:{self.__port}"
            else:
                self.__name = f"optiSLang_{id(self)}"
        return self.__name

    def get_osl_version(self, timeout: Union[float, None] = None) -> str:
        """Get version of used optiSLang.

        Parameters
        ----------
        timeout : float, None, optional
            Timeout in seconds to perform the query. It must be greater than zero or ``None``.
            The function will raise a timeout exception if the timeout period value has
            elapsed before the operation has completed. If ``None`` is given, the function
            will wait until the function is finished (no timeout exception is raised).
            Defaults to ``None``.

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
        return self.__osl_server.get_osl_version(timeout)

    def get_project_description(self, timeout: Union[float, None] = None) -> str:
        """Get description of optiSLang project.

        Parameters
        ----------
        timeout : float, None, optional
            Timeout in seconds to perform the query. It must be greater than zero or ``None``.
            The function will raise a timeout exception if the timeout period value has
            elapsed before the operation has completed. If ``None`` is given, the function
            will wait until the function is finished (no timeout exception is raised).
            Defaults to ``None``.

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
        return self.__osl_server.get_project_description(timeout)

    def get_project_location(self, timeout: Union[float, None] = None) -> str:
        """Get path to the optiSLang project file.

        Parameters
        ----------
        timeout : float, None, optional
            Timeout in seconds to perform the query. It must be greater than zero or ``None``.
            The function will raise a timeout exception if the timeout period value has
            elapsed before the operation has completed. If ``None`` is given, the function
            will wait until the function is finished (no timeout exception is raised).
            Defaults to ``None``.

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
        return self.__osl_server.get_project_location(timeout)

    def get_project_name(self, timeout: Union[float, None] = None) -> str:
        """Get name of the optiSLang project.

        Parameters
        ----------
        timeout : float, None, optional
            Timeout in seconds to perform the query. It must be greater than zero or ``None``.
            The function will raise a timeout exception if the timeout period value has
            elapsed before the operation has completed. If ``None`` is given, the function
            will wait until the function is finished (no timeout exception is raised).
            Defaults to ``None``.

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
        return self.__osl_server.get_project_name(timeout)

    def get_project_status(self, timeout: Union[float, None] = None) -> str:
        """Get status of the optiSLang project.

        Parameters
        ----------
        timeout : float, None, optional
            Timeout in seconds to perform the query. It must be greater than zero or ``None``.
            The function will raise a timeout exception if the timeout period value has
            elapsed before the operation has completed. If ``None`` is given, the function
            will wait until the function is finished (no timeout exception is raised).
            Defaults to ``None``.

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
        return self.__osl_server.get_project_status(timeout)

    def get_working_dir(self, timeout: Union[float, None] = None) -> str:
        """Get path to the optiSLang project working directory.

        Parameters
        ----------
        timeout : float, None, optional
            Timeout in seconds to perform the query. It must be greater than zero or ``None``.
            The function will raise a timeout exception if the timeout period value has
            elapsed before the operation has completed. If ``None`` is given, the function
            will wait until the function is finished (no timeout exception is raised).
            Defaults to ``None``.

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
        return self.__osl_server.get_working_dir(timeout)

    def reset(self, timeout: Union[float, None] = None) -> None:
        """Reset complete project.

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
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self.__osl_server.reset(timeout)

    def run_python_commands(
        self,
        script: str,
        args: Union[Sequence[object], None] = None,
        timeout: Union[float, None] = None,
    ) -> Tuple[str, str]:
        """Load a Python script in a project context and execute it.

        Parameters
        ----------
        script : str
            Python commands to be executed on the server.
        args : Sequence[object], None, optional
            Sequence of arguments used in Python script. Defaults to ``None``.
        timeout : float, None, optional
            Timeout in seconds to perform the command. It must be greater than zero or ``None``.
            The function will raise a timeout exception if the timeout period value has
            elapsed before the operation has completed. If ``None`` is given, the function
            will wait until the function is finished (no timeout exception is raised).
            Defaults to ``None``.

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
        return self.__osl_server.run_python_commands(script, args, timeout)

    def run_python_script(
        self,
        script_path: str,
        args: Union[Sequence[object], None] = None,
        timeout: Union[float, None] = None,
    ) -> Tuple[str, str]:
        """Read python script from the file, load it in a project context and execute it.

        Parameters
        ----------
        script_path : str
            Path to the Python script file which content is supposed to be executed on the server.
        args : Sequence[object], None, optional
            Sequence of arguments used in Python script. Defaults to ``None``.
        timeout : float, None, optional
            Timeout in seconds to perform the command. It must be greater than zero or ``None``.
            The function will raise a timeout exception if the timeout period value has
            elapsed before the operation has completed. If ``None`` is given, the function
            will wait until the function is finished (no timeout exception is raised).
            Defaults to ``None``.

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
        return self.__osl_server.run_python_script(script_path, args, timeout)

    def save_copy(self, file_path: str, timeout: Union[float, None] = None) -> None:
        """Save the current project as a copy to a location.

        Parameters
        ----------
        file_path : str
            Path where to save the project copy.
        timeout : float, None, optional
            Timeout in seconds to perform the command. It must be greater than zero or ``None``.
            The function will raise a timeout exception if the timeout period value has
            elapsed before the operation has completed. If ``None`` is given, the function
            will wait until the function is finished (no timeout exception is raised).
            Defaults to ``None``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self.__osl_server.save_copy(file_path, timeout)

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
        self.__osl_server.shutdown()

    def start(self, wait_for_finish: bool = True, timeout: Union[float, None] = None) -> None:
        """Start project execution.

        Parameters
        ----------
        wait_for_finish : bool, optional
            Determines whether this function call should wait on the optiSlang to finish
            the project execution. Defaults to ``True``.
        timeout : float, None, optional
            Timeout in seconds to perform the command. It must be greater than zero or ``None``.
            The function will raise a timeout exception if the timeout period value has
            elapsed before the operation has completed. If ``None`` is given, the function
            will wait until the function is finished (no timeout exception is raised).
            Defaults to ``None``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self.__osl_server.start(wait_for_finish, timeout)

    def stop(self, wait_for_finish: bool = True, timeout: Union[float, None] = None) -> None:
        """Stop project execution.

        Parameters
        ----------
        wait_for_finish : bool, optional
            Determines whether this function call should wait on the optiSlang to finish
            the project execution. Defaults to ``True``.
        timeout : float, None, optional
            Timeout in seconds to perform the command. It must be greater than zero or ``None``.
            The function will raise a timeout exception if the timeout period value has
            elapsed before the operation has completed. If ``None`` is given, the function
            will wait until the function is finished (no timeout exception is raised).
            Defaults to ``None``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self.__osl_server.stop(wait_for_finish, timeout)

    def stop_gently(self, wait_for_finish: bool = True, timeout: Union[float, None] = None) -> None:
        """Stop project execution after the current design is finished.

        Parameters
        ----------
        wait_for_finish : bool, optional
            Determines whether this function call should wait on the optiSlang to finish
            the project execution. Defaults to ``True``.
        timeout : float, None, optional
            Timeout in seconds to perform the command. It must be greater than zero or ``None``.
            The function will raise a timeout exception if the timeout period value has
            elapsed before the operation has completed. If ``None`` is given, the function
            will wait until the function is finished (no timeout exception is raised).
            Defaults to ``None``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self.__osl_server.stop_gently(wait_for_finish, timeout)
