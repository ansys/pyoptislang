"""Contains Optislang class which provides python API for optiSLang application."""
from typing import Sequence

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

        if loglevel is None:
            loglevel = LOG.log_level
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
        return self.__osl_server.get_osl_version()

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
        """
        return self.__osl_server.get_project_status()

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
        return self.__osl_server.get_working_dir()

    def reset(self) -> None:
        """Reset complete project.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        """
        self.__osl_server.reset()

    def run_python_script(self, script: str, args: Sequence[object]) -> None:
        """Load a Python script in a project context and execute it.

        Parameters
        ----------
        script : str
            Python script to be executed on the server.
        args : Sequence[object]
            Sequence of script arguments.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        """
        self.__osl_server.run_python_script(script, args)

    def save_copy(self, file_path: str):
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
        self.__osl_server.save_copy(file_path)

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

    def start(self) -> None:
        """Start project execution.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        """
        self.__osl_server.start()

    def stop(self) -> None:
        """Stop project execution.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        """
        self.__osl_server.stop()

    def stop_gently(self) -> None:
        """Stop project execution after the current design is finished.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        """
        self.__osl_server.stop_gently()
