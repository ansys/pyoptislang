"""Contains Optislang class which provides python API for optiSLang application."""
from pathlib import Path
from typing import Sequence, Tuple, Union

from importlib_metadata import version

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
    executable : Union[str, Path], optional
        Path to the optiSLang executable file which supposed to be executed on localhost.
        It is ignored when the host and port parameters are specified. Defaults to ``None``.
    project_path : Union[str, Path], optional
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
    shutdown_on_finished: bool, optional
        Shut down when execution is finished and there are not any listeners registered.
        It is ignored when the host and port parameters are specified. Defaults to ``True``.

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
    >>> osl_version = osl.get_osl_version_string()
    >>> print(osl_version)
    >>> osl.dispose()
    """

    def __init__(
        self,
        host: str = None,
        port: int = None,
        executable: Union[str, Path] = None,
        project_path: Union[str, Path] = None,
        no_save: bool = False,
        ini_timeout: Union[int, float] = 20,
        name: str = None,
        password: str = None,
        loglevel: str = None,
        shutdown_on_finished: bool = True,
    ) -> None:
        """Initialize a new instance of the ``Optislang`` class."""
        self.__host = host
        self.__port = port
        self.__executable = Path(executable) if executable is not None else None
        self.__project_path = Path(project_path) if project_path is not None else None
        self.__no_save = no_save
        self.__ini_timeout = ini_timeout
        self.__name = name
        self.__password = password
        self.__shutdown_on_finished = shutdown_on_finished
        self.__logger = LOG.add_instance_logger(self.name, self, loglevel)
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
                ini_timeout=self.__ini_timeout,
                password=self.__password,
                logger=self.log,
                shutdown_on_finished=self.__shutdown_on_finished,
            )
        else:
            raise NotImplementedError(f'OptiSLang server of type "{server_type}" is not supported.')

    def __str__(self):
        """Return product name, version of optiSLang and PyOptiSLang version."""
        return (
            f"Product name: optiSLang\n"
            f"Version: {self.get_osl_version_string()}\n"
            f"PyOptiSLang: {version('ansys.optislang.core')}"
        )

    def __enter__(self):
        """Enter the context."""
        self.log.debug("Enter the context.")
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        """Exit the context.

        Disposes instance of Optislang.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self.log.debug("Exit the context.")
        self.dispose()

    @property
    def name(self) -> str:
        """Instance unique identifier."""
        if not self.__name:
            if self.__host or self.__port:
                self.__name = f"optiSLang_{self.__host}:{self.__port}"
            else:
                self.__name = f"optiSLang_{id(self)}"
        return self.__name

    @property
    def log(self):
        """Return instance logger."""
        return self.__logger

    def close(self) -> None:
        """Close the current project.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self.__osl_server.close()

    def dispose(self) -> None:
        """Terminate all local threads and unregister listeners.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self.__osl_server.dispose()

    def get_osl_version_string(self) -> str:
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
        return self.__osl_server.get_osl_version_string()

    def get_osl_version(self) -> Tuple[Union[int, None], ...]:
        """Get version of used optiSLang.

        Returns
        -------
        tuple
            optiSLang version as tuple containing
            major version, minor version, maintenance version and revision.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.__osl_server.get_osl_version()

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
        return self.__osl_server.get_project_description()

    def get_project_location(self) -> Path:
        """Get path to the optiSLang project file.

        Returns
        -------
        Path
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
        return self.__osl_server.get_project_location()

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
        return self.__osl_server.get_project_name()

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
        return self.__osl_server.get_project_status()

    def get_timeout(self) -> Union[float, None]:
        """Get current timeout value for execution of commands.

        Returns
        -------
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
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.__osl_server.get_timeout()

    def get_working_dir(self) -> Path:
        """Get path to the optiSLang project working directory.

        Returns
        -------
        Path
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
        return self.__osl_server.get_working_dir()

    def new(self) -> None:
        """Create a new project.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self.__osl_server.new()

    def open(
        self,
        file_path: Union[str, Path],
        force: bool = True,
        restore: bool = False,
        reset: bool = False,
    ) -> None:
        """Open a new project.

        Parameters
        ----------
        file_path : Union[str, Path]
            Path to the optiSLang project file to open.
        force : bool, optional
            # TODO: description of this parameter is missing in ANSYS help
        restore : bool, optional
            # TODO: description of this parameter is missing in ANSYS help
        reset : bool, optional
            # TODO: description of this parameter is missing in ANSYS help

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self.__osl_server.open(file_path=file_path, force=force, restore=restore, reset=reset)

    def reset(self) -> None:
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
        self.__osl_server.reset()

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
        return self.__osl_server.run_python_script(script, args)

    def run_python_file(
        self,
        file_path: Union[str, Path],
        args: Union[Sequence[object], None] = None,
    ) -> Tuple[str, str]:
        """Read python script from the file, load it in a project context and execute it.

        Parameters
        ----------
        file_path : Union[str, Path]
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
        return self.__osl_server.run_python_file(file_path, args)

    def save(self) -> None:
        """Save the changed data and settings of the current project.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.__osl_server.save()

    def save_as(
        self,
        file_path: Union[str, Path],
        force: bool = True,
        restore: bool = False,
        reset: bool = False,
    ) -> None:
        """Save and open the current project at a new location.

        Parameters
        ----------
        file_path : Union[str, Path]
            Path where to save the project file.
        force : bool, optional
            # TODO: description of this parameter is missing in ANSYS help
        restore : bool, optional
            # TODO: description of this parameter is missing in ANSYS help
        reset : bool, optional
            # TODO: description of this parameter is missing in ANSYS help

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.__osl_server.save_as(
            file_path=file_path, force=force, restore=restore, reset=reset
        )

    def save_copy(self, file_path: Union[str, Path]) -> None:
        """Save the current project as a copy to a location.

        Parameters
        ----------
        file_path : Union[str, Path]
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
        self.__osl_server.save_copy(file_path)

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
        self.__osl_server.set_timeout(timeout)

    def shutdown(self, force: bool = False) -> None:
        """Shutdown the optiSLang server.

        Stop listening for incoming connections, discard pending requests, and shut down
        the server. Batch mode exclusive: Continue project run until execution finished.
        Terminate optiSLang.

        Parameters
        ----------
        force : bool, optional
            Determines whether to force shutdown the local optiSLang server. Has no effect when
            the connection is established to the remote optiSLang server. In all cases, it is tried
            to shutdown the optiSLang server process in a proper way. However, if the force
            parameter is ``True``, after a while, the process is forced to terminate and no
            exception is raised. Defaults to ``False``.

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
        self.__osl_server.shutdown(force)

    def start(self, wait_for_started: bool = True, wait_for_finished: bool = True) -> None:
        """Start project execution.

        Parameters
        ----------
        wait_for_started : bool, optional
            Determines whether this function call should wait for optiSLang to start
            the command execution. I.e. don't continue on next line of python script
            after command was successfully sent to optiSLang but wait for execution of
            flow inside optiSLang to start.
            Defaults to ``True``.
        wait_for_finished : bool, optional
            Determines whether this function call should wait for optiSLang to finish
            the command execution. I.e. don't continue on next line of python script
            after command was successfully sent to optiSLang but wait for execution of
            flow inside optiSLang to finish.
            This implicitly interprets wait_for_started as True.
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
        self.__osl_server.start(wait_for_started, wait_for_finished)

    def stop(self, wait_for_finished: bool = True) -> None:
        """Stop project execution.

        Parameters
        ----------
        wait_for_finished : bool, optional
            Determines whether this function call should wait for optiSLang to finish
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
        self.__osl_server.stop(wait_for_finished)

    # stop_gently method doesn't work properly in optiSLang 2023R1, therefore it was commented out

    # def stop_gently(self, wait_for_finished: bool = True) -> None:
    #     """Stop project execution after the current design is finished.

    #     Parameters
    #     ----------
    #     wait_for_finished : bool, optional
    #         Determines whether this function call should wait for optiSLang to finish
    #         the command execution. I.e. don't continue on next line of python script after command
    #         was successfully sent to optiSLang but wait for execution of command inside optiSLang.
    #         Defaults to ``True``.

    #     Raises
    #     ------
    #     OslCommunicationError
    #         Raised when an error occurs while communicating with server.
    #     OslCommandError
    #         Raised when the command or query fails.
    #     TimeoutError
    #         Raised when the timeout float value expires.
    #     """
    #     self.__osl_server.stop_gently(wait_for_finished)
