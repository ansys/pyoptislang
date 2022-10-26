"""Contains Optislang class which provides python API for optiSLang application."""
from typing import TYPE_CHECKING, Dict, Iterable, List, Sequence, Tuple, Union

from importlib_metadata import version

from ansys.optislang.core import LOG
from ansys.optislang.core.tcp_osl_server import TcpOslServer

if TYPE_CHECKING:
    from ansys.optislang.core.osl_server import OslServer
    from ansys.optislang.core.project_parametric import Design, ParameterManager


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
        ini_timeout: Union[int, float] = 20,
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
        self.__ini_timeout = ini_timeout
        self.__name = name
        self.__password = password

        self._logger = LOG.add_instance_logger(self.name, self, loglevel)
        self.__osl_server: OslServer = self.__init_osl_server("tcp")

    def __init_osl_server(self, server_type: str) -> "OslServer":
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
                logger=self._logger,
            )
        else:
            raise NotImplementedError(f'OptiSLang server of type "{server_type}" is not supported.')

    def __str__(self):
        """Return product name, version of optiSLang and PyOptiSLang version."""
        return (
            "----------------------------------------------------------------------\n"
            f"Product name: optiSLang\n"
            f"Version: {self.get_osl_version()}\n"
            f"PyOptiSLang: {version('ansys.optislang.core')}\n"
            f"Project name: {self.get_project_name()}\n"
            "----------------------------------------------------------------------"
        )

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
        return self.__osl_server.get_working_dir()

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
        return self.__osl_server.run_python_file(file_path, args)

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
        self.__osl_server.shutdown(force)

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
        self.__osl_server.start(wait_for_finish)

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
        self.__osl_server.stop(wait_for_finish)

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
        self.__osl_server.stop_gently(wait_for_finish)

    # new functionality
    def get_nodes_dict(self) -> Dict:
        """Return dictionary of nodes in root level."""
        return self.__osl_server.get_nodes_dict()

    def get_parameter_manager(self) -> "ParameterManager":
        """Return instance of class ``ParameterManager``."""
        return self.__osl_server.get_parameter_manager()

    def get_parameters_list(self) -> List:
        """Return list of defined parameters.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        # TODO: create test
        return self.__osl_server.get_parameters_list()

    def create_design(self, inputs: Dict = None) -> "Design":
        """Return a new instance of ``Design`` class.

        Parameters
        ----------
        inputs: Dict, opt
            Dictionary of parameters and it's values {'parname': value, ...}.

        Returns
        -------
        Design
            Instance of ``Design`` class.
        """
        # TODO: create test
        return self.__osl_server.create_design(inputs)

    def evaluate_design(self, design: "Design") -> Tuple:
        """Evaluate requested design.

        Parameters
        ----------
        design: Design
            Instance of ``Design`` class with defined parameters.

        Returns
        -------
        Tuple[Dict, Dict]
            0: Design parameters.
            1: Responses.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        # TODO: create test
        return self.__osl_server.evaluate_design(design)

    def evaluate_multiple_designs(self, designs: Iterable["Design"]) -> Dict:
        """Evaluate multiple designs.

        Parameters
        ----------
        designs: Iterable[Design]
            Iterable of ``Design`` class instances with defined parameters.

        Returns
        -------
        multiple_design_output: List[Tuple[Dict, Dict]]
            Tuple[Dict, Dict]:
                0: Design parameters.
                1: Responses.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        # TODO: create test
        return self.__osl_server.evaluate_multiple_designs(designs)

    def validate_design(self, design: "Design") -> Tuple[str, bool, List]:
        """Compare parameters defined in design and project.

        Parameters
        ----------
        design: Design
            Instance of ``Design`` class with defined parameters.

        Returns
        -------
        Tuple[str, bool, List]
            0: str, Message describing differences.
            1: bool, True if there are not any missing or redundant parameters.
            2: List, Missing parameters.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        # TODO: create test
        return self.__osl_server.validate_design(design)
