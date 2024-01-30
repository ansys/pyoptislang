# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
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

"""Contains Optislang class, which provides the Python API for the optiSLang app."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Iterable, Mapping, Optional, Sequence, Tuple, Union

from deprecated.sphinx import deprecated
from importlib_metadata import version

from ansys.optislang.core import LOG
from ansys.optislang.core.tcp.application import TcpApplicationProxy
from ansys.optislang.core.tcp.osl_server import TcpOslServer

if TYPE_CHECKING:
    from ansys.optislang.core.application import Application
    from ansys.optislang.core.logging import OslCustomAdapter
    from ansys.optislang.core.osl_server import OslServer, OslVersion
    from ansys.optislang.core.project import Project


class Optislang:
    """Connects to the optiSLang app and provides an API to control it.

    For remote connection, it is assumed that optiSLang is already running
    on a remote (or local) host as a server. In this case, the host and port
    must be specified. Parameters related to the execution of the new optiSLang
    server are ignored.

    To run optiSLang locally, both the ``host`` and ``port`` parameters must
    be ``None``, which are their defaults. Other parameters can be optionally
    specified.

    Parameters
    ----------
    host : Optional[str], optional
        IPv4/v6 address or domain name on which optiSLang is running as a
        server. The default is ``None``.
    port : Optional[int], optional
        Port on which optiSLang is running as a server. The default is ``None``.
    executable : Optional[Union[str, pathlib.Path]], optional
        Path to the optiSLang executable file to execute on a the local host.
        The default is ``None``. This parameter is ignored when ``host``
        and ``port`` parameters are specified.
    project_path : Optional[Union[str, pathlib.Path]], optional
        Path to the optiSLang project file that a new local optiSLang server
        is to use. The default is ``None``. This parameter is ignored
        when ``host`` and ``port`` parameters are specified. Here is how
        this parameter is used:

        - If the project file exists, it is opened.
        - If the project file does not exist, a project is created in the specified path.
        - If the path is ``None``, a new project is created in the temporary directory.

    batch : bool, optional
        Determines whether to start optiSLang server in batch mode. Defaults to ``True``.

        ..note:: Cannot be used in combination with service mode.

    service: bool, optional
        Determines whether to start optiSLang server in service mode. If ``True``,
        ``batch`` argument is set to ``False``. Defaults to ``False``.

        ..note:: Cannot be used in combination with batch mode.

    port_range : Tuple[int, int], optional
        Defines the port range for optiSLang server. Defaults to ``None``.
    no_run : Optional[bool], optional
        Determines whether not to run the specified project when started in batch mode.
        Defaults to ``None``.

        .. note:: Only supported in batch mode.

    no_save : bool, optional
        Whether to save the specified project after all other actions are completed.
        The default is ``False``. This parameter is ignored when ``host`` and
        ``port`` parameters are specified.

        .. note:: Only supported in batch mode.

    force : bool, optional
        Determines whether to force opening/processing specified project when started in batch mode
        even if issues occur.
        Defaults to ``True``.

        .. note:: Only supported in batch mode.

    reset : bool, optional
        Determines whether to reset specified project after load.
        Defaults to ``False``.

        .. note:: Only supported in batch mode.

    auto_relocate : bool, optional
        Determines whether to automatically relocate missing file paths.
        Defaults to ``False``.

        .. note:: Only supported in batch mode.

    listener_id : Optional[str], optional
        Specific unique ID for the TCP listener. Defaults to ``None``.
    multi_listener : Iterable[Tuple[str, int, Optional[str]]], optional
        Multiple remote listeners (plain TCP/IP based) to be registered at optiSLang server.
        Each listener is a combination of host, port and (optionally) listener ID.
        Defaults to ``None``.
    ini_timeout : float, optional
        Time in seconds to connect to the optiSLang server. The default is ``20``.
    name : Optional[str], optional
        ID of the optiSLang instance. Defaults to ``None``.
    password : Optional[str], optional
        Server password. The default is ``None``. This parameter is used when
        communication with the server requires that the request contain a password.
        Defaults to ``None``.
    loglevel : Optional[str], optional
        Logging level. The options are:

        - ``CRITICAL``: Log errors that are fatal for the app.
        - ``ERROR``: Log errors that are fatal for some operation, but not for the app.
        - ``WARNING``: Log some oddities or potential problems.
        - ``INFO``: Log some useful information that the program works as expected.
        - ``DEBUG``: Log all information for use in debugging.

        Defaults to ``None``.

    shutdown_on_finished: bool, optional
        Whether to shut down when execution is finished and no listeners are registered.
        The default is ``True``. This parameter is ignored when ``host`` and
        ``port`` parameters are specified.

        .. note:: Only supported in batch mode.

    env_vars : Optional[Mapping[str, str]], optional
        Additional environmental variables (key and value) for the optiSLang server process.
        Defaults to ``None``.
    import_project_properties_file : Optional[Union[str, pathlib.Path]], optional
        Optional path to a project properties file to import. Defaults to ``None``.
    export_project_properties_file : Optional[Union[str, pathlib.Path]], optional
        Optional path to a project properties file to export. Defaults to ``None``.

        .. note:: Only supported in batch mode.

    import_placeholders_file : Optional[Union[str, pathlib.Path]], optional
        Optional path to a placeholders file to import. Defaults to ``None``.
    export_placeholders_file : Optional[Union[str, pathlib.Path]], optional
        Optional path to a placeholders file to export. Defaults to ``None``.

        .. note:: Only supported in batch mode.

    output_file : Optional[Union[str, pathlib.Path]], optional
        Optional path to an output file for writing project run results to. Defaults to ``None``.

        .. note:: Only supported in batch mode.

    dump_project_state : Optional[Union[str, pathlib.Path]], optional
        Optional path to a project state dump file to export. If a relative path is provided,
        it is considered to be relative to the project working directory. Defaults to ``None``.

        .. note:: Only supported in batch mode.

    opx_project_definition_file : Optional[Union[str, pathlib.Path]], optional
        Optional path to an OPX project definition file. Defaults to ``None``.

        .. note:: Only supported in batch mode.

    additional_args : Optional[Iterable[str]], optional
        Additional command line arguments used for execution of the optiSLang server process.
        Defaults to ``None``.

    Raises
    ------
    RuntimeError
        Raised when the connection to the optiSLang server cannot be established
        before the specified timeout.

    Examples
    --------
    Start and connect to the local optiSLang server, get the version of optiSLang
    in use, print the version, and shut down the server.

    >>> from ansys.optislang.core import Optislang
    >>> osl = Optislang()
    >>> osl_version = osl.osl_version_string
    >>> print(osl_version)
    >>> osl.dispose()
    """

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        executable: Optional[Union[str, Path]] = None,
        project_path: Optional[Union[str, Path]] = None,
        batch: bool = True,
        service: bool = False,
        port_range: Optional[Tuple[int, int]] = None,
        no_run: Optional[bool] = None,
        no_save: bool = False,
        force: bool = True,
        reset: bool = False,
        auto_relocate: bool = False,
        listener_id: Optional[str] = None,
        multi_listener: Optional[Iterable[Tuple[str, int, Optional[str]]]] = None,
        ini_timeout: Union[int, float] = 20,
        name: Optional[str] = None,
        password: Optional[str] = None,
        loglevel: Optional[str] = None,
        shutdown_on_finished: bool = True,
        env_vars: Optional[Mapping[str, str]] = None,
        import_project_properties_file: Optional[Union[str, Path]] = None,
        export_project_properties_file: Optional[Union[str, Path]] = None,
        import_placeholders_file: Optional[Union[str, Path]] = None,
        export_placeholders_file: Optional[Union[str, Path]] = None,
        output_file: Optional[Union[str, Path]] = None,
        dump_project_state: Optional[Union[str, Path]] = None,
        opx_project_definition_file: Optional[Union[str, Path]] = None,
        additional_args: Optional[Iterable[str]] = None,
    ) -> None:
        """Initialize a new instance of the ``Optislang`` class."""
        self.__host = host
        self.__port = port
        self.__executable = Path(executable) if executable is not None else None
        self.__project_path = Path(project_path) if project_path is not None else None
        self.__batch = batch
        self.__service = service
        self.__port_range = port_range
        self.__no_run = no_run
        self.__no_save = no_save
        self.__force = force
        self.__reset = reset
        self.__auto_relocate = auto_relocate
        self.__ini_timeout = ini_timeout
        self.__name = name
        self.__password = password
        self.__shutdown_on_finished = shutdown_on_finished
        self.__env_vars = env_vars
        self.__listener_id = listener_id
        self.__multi_listener = multi_listener
        self.__import_project_properties_file = import_project_properties_file
        self.__export_project_properties_file = export_project_properties_file
        self.__import_placeholders_file = import_placeholders_file
        self.__export_placeholders_file = export_placeholders_file
        self.__output_file = output_file
        self.__dump_project_state = dump_project_state
        self.__opx_project_definition_file = opx_project_definition_file
        self.__additional_args = additional_args
        self.__logger = LOG.add_instance_logger(self.name, self, loglevel)
        self.__osl_server: OslServer = self.__init_osl_server("tcp")
        self.__application: Application = self.__init_application()

    def __init_osl_server(self, server_type: str) -> OslServer:
        """Initialize optiSLang server.

        Parameters
        ----------
        server_type : str, optional
            Type of the optiSLang server. The default is ``tcp``, in which case
            the plain TCP/IP communication protocol is used.

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
                batch=self.__batch,
                service=self.__service,
                port_range=self.__port_range,
                no_run=self.__no_run,
                force=self.__force,
                reset=self.__reset,
                auto_relocate=self.__auto_relocate,
                env_vars=self.__env_vars,
                import_project_properties_file=self.__import_project_properties_file,
                export_project_properties_file=self.__export_project_properties_file,
                import_placeholders_file=self.__import_placeholders_file,
                export_placeholders_file=self.__export_placeholders_file,
                output_file=self.__output_file,
                dump_project_state=self.__dump_project_state,
                opx_project_definition_file=self.__opx_project_definition_file,
                listener_id=self.__listener_id,
                multi_listener=self.__multi_listener,
                additional_args=self.__additional_args,
            )
        else:
            raise NotImplementedError(
                f"OptiSLang server of type ``{server_type}`` is not supported."
            )

    def __init_application(self) -> Application:
        if isinstance(self.__osl_server, TcpOslServer):
            return TcpApplicationProxy(osl_server=self.__osl_server, logger=self.log)
        else:
            raise NotImplementedError(f"Currently supported only for ``TcpOslServer``.")

    def __str__(self):
        """Return product name, version of optiSLang, and version of PyOptiSLang."""
        return (
            f"Product name: optiSLang\n"
            f"Version: {self.osl_version_string}\n"
            f"PyOptiSLang: {version('ansys.optislang.core')}"
        )

    def __enter__(self):
        """Enter the context."""
        self.log.debug("Enter the context.")
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        """Exit the context.

        Disposes the Optislang instance.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self.log.debug("Exit the context.")
        self.dispose()

    @property
    def application(self) -> Application:
        """Instance of the ``Application`` class.

        Returns
        -------
        Application
            Instance of ``Application`` class for operating with project.
        """
        return self.__application

    @property
    @deprecated(version="0.6.0", reason="Use `Optislang.application.project is not None` instead.")
    def has_active_project(self) -> bool:
        """
        Whether a project is loaded.

        Returns
        -------
        bool
            ``True`` if a project is loaded, ``False`` otherwise.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.application.project is not None

    @property
    def log(self) -> OslCustomAdapter:
        """Instance logger."""
        return self.__logger

    @property
    def name(self) -> str:
        """Unique ID of the optiSLang instance."""
        if not self.__name:
            if self.__host or self.__port:
                self.__name = f"optiSLang_{self.__host}:{self.__port}"
            else:
                self.__name = f"optiSLang_{id(self)}"
        return self.__name

    @property
    def osl_server(self) -> Optional[OslServer]:
        """Get the currently used instance of the OslServer.

        This instance can be used to directly communicate with optiSLang using
        the optiSLang server API.

        Returns
        -------
        Optional[OslServer]
            OptiSLang server object.
        """
        return self.__osl_server

    @property
    def osl_version(self) -> OslVersion:
        """Version of used optiSLang.

        Returns
        -------
        OslVersion
            optiSLang version as typing.NamedTuple containing
            major, minor, maintenance and revision versions.
        """
        return self.__osl_server.osl_version

    @property
    def osl_version_string(self) -> str:
        """Version of used optiSLang.

        Returns
        -------
        str
            optiSLang version.
        """
        return self.__osl_server.osl_version_string

    @property
    def project(self) -> Optional[Project]:
        """Instance of the ``Project`` class.

        Returns
        -------
        Optional[Project]
            Loaded project. If no project is loaded, ``None`` is returned.
        """
        return self.application.project

    @property
    def timeout(self) -> Union[float, None]:
        """Get the timeout value for executing commands.

        Returns
        -------
        timeout: Union[float, None]
            Timeout in seconds to perform commands. This value must be greater
            than zero or ``None``. The default is ``None``. Another function
            raises a timeout exception if the timeout value has elapsed before
            an operation has completed. If the timeout is ``None``, functions
            wait until they're finished, and no timeout exception is raised.
        """
        return self.__osl_server.timeout

    @timeout.setter
    def timeout(self, timeout: Union[float, None] = None) -> None:
        """Set the timeout value for the executing commands.

        Parameters
        ----------
        timeout: Union[float, None]
            Timeout in seconds to perform commands. This value must be greater
            than zero or ``None``. The default is ``None``. Another function
            raises a timeout exception if the timeout value has elapsed before
            an operation has completed. If the timeout is ``None``, functions
            wait until they're finished, and no timeout exception is raised.

        Raises
        ------
        ValueError
            Raised when the timeout value is less than or equal to 0.
        TypeError
            Raised when the timeout is not a Union[float, None].
        """
        self.__osl_server.timeout = timeout

    def dispose(self) -> None:
        """Close all local threads and unregister listeners.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self.__osl_server.dispose()

    @deprecated(version="0.6.0", reason="Use :py:attr:`Optislang.osl_server` instead.")
    def get_osl_server(self) -> Optional[OslServer]:
        """Get the currently used instance of the OslServer.

        This instance can be used to directly communicate with optiSLang using
        the optiSLang server API.

        Returns
        -------
        Optional[OslServer]
            OptiSLang server object.
        """
        return self.osl_server

    @deprecated(version="0.5.0", reason="Use :py:attr:`Optislang.osl_version_string` instead.")
    def get_osl_version_string(self) -> str:
        """Get the optiSLang version in use as a string.

        Returns
        -------
        str
            optiSLang version.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.__osl_server.osl_version_string

    @deprecated(version="0.5.0", reason="Use :py:attr:`Optislang.osl_version` instead.")
    def get_osl_version(self) -> OslVersion:
        """Get the optiSLang version in use as a tuple.

        Returns
        -------
        OslVersion
            optiSLang version as typing.NamedTuple containing
            major, minor, maintenance and revision versions.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        RuntimeError
            Raised when parsing version numbers from string fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.__osl_server.osl_version

    @deprecated(version="0.5.0", reason="Use :py:attr:`Optislang.timeout` instead.")
    def get_timeout(self) -> Union[float, None]:
        """Get the timeout value for executing commands.

        Returns
        -------
        timeout: Union[float, None]
            Timeout in seconds to perform commands. This value must be greater
            than zero or ``None``. The default is ``None``. Another function
            raises a timeout exception if the timeout value has elapsed before
            an operation has completed. If the timeout is ``None``, functions
            wait until they're finished, and no timeout exception is raised.
        """
        return self.osl_server.timeout

    @deprecated(
        version="0.6.0",
        reason=(
            "This functionality was moved to "
            ":py:class:`Project <ansys.optislang.core.project.Project>`."
        ),
    )
    def get_working_dir(self) -> Path:
        """Get the path to the optiSLang project's working directory.

        Returns
        -------
        pathlib.Path
            Path to the optiSLang project's working directory. If no project is loaded
            in optiSLang, ``None`` is returned.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.application.project.get_working_dir()

    @deprecated(
        version="0.6.0",
        reason=(
            "This functionality was moved to "
            ":py:class:`Application <ansys.optislang.core.application.Application>`."
        ),
    )
    def new(self) -> None:
        """Create and open a new project.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self.application.new()

    @deprecated(
        version="0.6.0",
        reason=(
            "This functionality was moved to "
            ":py:class:`Application <ansys.optislang.core.application.Application>`."
        ),
    )
    def open(
        self,
        file_path: Union[str, Path],
        force: bool = True,
        restore: bool = False,
        reset: bool = False,
    ) -> None:
        """Open a project.

        Parameters
        ----------
        file_path : Union[str, pathlib.Path]
            Path to the optiSLang project file to open.
        force : bool, optional
            Whether to force opening of the project even if non-critical errors occur.
            Non-critical errors include:

            - Timestamp of the (auto) save point is newer than the project timestamp.
            - Project (file) is incomplete.

        restore : bool, optional
            Whether to restore the project from the last (auto) save point (if present).
        reset : bool, optional
            Whether to reset the project after loading it.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self.application.open(file_path=file_path, force=force, restore=restore, reset=reset)

    @deprecated(
        version="0.6.0",
        reason=(
            "This functionality was moved to "
            ":py:class:`Project <ansys.optislang.core.project.Project>`."
        ),
    )
    def reset(self) -> None:
        """Reset the project.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self.application.project.reset()

    @deprecated(
        version="0.6.0",
        reason=(
            "This functionality was moved to "
            ":py:class:`Project <ansys.optislang.core.project.Project>`."
        ),
    )
    def run_python_script(
        self,
        script: str,
        args: Union[Sequence[object], None] = None,
    ) -> Tuple[str, str]:
        """Load a Python script in a project context and run it.

        Parameters
        ----------
        script : str
            Python commands to execute on the server.
        args : Sequence[object], None, optional
            Sequence of arguments used in the Python script. The default
            is ``None``.

        Returns
        -------
        Tuple[str, str]
            STDOUT and STDERR from the executed Python script.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.application.project.run_python_script(script, args)

    @deprecated(
        version="0.6.0",
        reason=(
            "This functionality was moved to "
            ":py:class:`Project <ansys.optislang.core.project.Project>`."
        ),
    )
    def run_python_file(
        self,
        file_path: Union[str, Path],
        args: Union[Sequence[object], None] = None,
    ) -> Tuple[str, str]:
        """Read a Python script from a file, load it in a project context, and run it.

        Parameters
        ----------
        file_path : Union[str, pathlib.Path]
            Path to the Python script file with the content to execute on the server.
        args : Sequence[object], None, optional
            Sequence of arguments to use in the Python script. The default is ``None``.

        Returns
        -------
        Tuple[str, str]
            STDOUT and STDERR from the executed Python script.

        Raises
        ------
        FileNotFoundError
            Raised when the specified Python script file does not exist.
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.application.project.run_python_file(file_path, args)

    @deprecated(
        version="0.6.0",
        reason=(
            "This functionality was moved to "
            ":py:class:`Application <ansys.optislang.core.application.Application>`."
        ),
    )
    def save(self) -> None:
        """Save changes to the project data and settings.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.application.save()

    @deprecated(
        version="0.6.0",
        reason=(
            "This functionality was moved to "
            ":py:class:`Application <ansys.optislang.core.application.Application>`."
        ),
    )
    def save_as(
        self,
        file_path: Union[str, Path],
        force: bool = True,
        restore: bool = False,
        reset: bool = False,
    ) -> None:
        """Save and open the project at a new location.

        Parameters
        ----------
        file_path : Union[str, pathlib.Path]
            Path for saving the new project file to.
        force : bool, optional
            Whether to force opening of the project even if non-critical errors occur.
            Non-critical errors include:

            - Timestamp of the (auto) save point is newer than the project timestamp.
            - Project (file) is incomplete.

        restore : bool, optional
            Whether to restore the project from the last (auto) save point (if present).
        reset : bool, optional
            Whether to reset the project after loading it.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        return self.application.save_as(
            file_path=file_path, force=force, restore=restore, reset=reset
        )

    @deprecated(
        version="0.6.0",
        reason=(
            "This functionality was moved to "
            ":py:class:`Application <ansys.optislang.core.application.Application>`."
        ),
    )
    def save_copy(self, file_path: Union[str, Path]) -> None:
        """Save a copy of the project to a specified location..

        Parameters
        ----------
        file_path : Union[str, pathlib.Path]
            Path for saving the copy of the project file to.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self.application.save_copy(file_path)

    @deprecated(version="0.5.0", reason="Use :py:attr:`Optislang.timeout` instead.")
    def set_timeout(self, timeout: Union[float, None] = None) -> None:
        """Set the timeout value for the executing commands.

        Parameters
        ----------
        timeout: Union[float, None]
            Timeout in seconds to perform commands. This value must be greater
            than zero or ``None``. The default is ``None``. Another function
            raises a timeout exception if the timeout value has elapsed before
            an operation has completed. If the timeout is ``None``, functions
            wait until they're finished, and no timeout exception is raised.

        Raises
        ------
        ValueError
            Raised when the timeout value is less than or equal to 0.
        TypeError
            Raised when the timeout is not a Union[float, None].
        """
        self.osl_server.timeout = timeout

    def shutdown(self, force: bool = False) -> None:
        """Shut down the optiSLang server.

        This method stops the server from listening for incoming connections, discards
        pending requests, and shuts down the server. In batch mode, the project runs
        until execution finishes and then optiSLang is shut down.

        Parameters
        ----------
        force : bool, optional
            Whether to forcibly shut down a local optiSLang server. The default is
            ``False``. This parameter has no effect when the connection established
            is to a remote optiSLang server. In all cases, an attempt is made to
            shut down the optiSLang server in the proper way. However, if the
            ``force`` parameter is ``True``, after a while, the process is forcibly
            shut down without an exception being raised.

        Raises
        ------
        OslCommunicationError
            Raised when the ``force`` parameter is ``False`` and an error occurs
            while communicating with the server.
        OslCommandError
            Raised when the ``force`` parameter is ``False`` and the command or query fails.
        TimeoutError
            Raised when the ``force`` parameter is ``False`` and the timeout float value expires.
        """
        self.osl_server.shutdown(force)

    @deprecated(
        version="0.6.0",
        reason=(
            "This functionality was moved to "
            ":py:class:`Project <ansys.optislang.core.project.Project>`."
        ),
    )
    def start(self, wait_for_started: bool = True, wait_for_finished: bool = True) -> None:
        """Start project execution.

        Parameters
        ----------
        wait_for_started : bool, optional
            Whether this function call should wait for optiSLang to start
            the command execution. The default is ``True``, in which case the
            function call does not continue on to the next line of the Python
            script after the command is successfully sent to optiSLang but
            rater waits for execution of the flow inside optiSLang to start.
        wait_for_finished : bool, optional
            Whether this function call should wait for optiSLang to finish
            the command execution. The default is ``True``, in which case the
            function call does not continue on to the next line of the Python
            script after the command is successfully sent to optiSLang but
            rather waits for execution of the flow inside optiSLang to finish.
            This implicitly interprets ``wait_for_started`` as True.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self.application.project.start(
            wait_for_started=wait_for_started, wait_for_finished=wait_for_finished
        )

    @deprecated(
        version="0.6.0",
        reason=(
            "This functionality was moved to "
            ":py:class:`Project <ansys.optislang.core.project.Project>`."
        ),
    )
    def stop(self, wait_for_finished: bool = True) -> None:
        """Stop project execution.

        Parameters
        ----------
        wait_for_finished : bool, optional
            Whether this function call should wait for optiSLang to finish
            the command execution. The default is ``True``, in which case the
            function call does not continue on to the next line of the Python
            script after the command is successfully sent to optiSLang but
            rather waits for execution of the flow inside optiSLang to finish.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with the server.
        OslCommandError
            Raised when a command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        self.application.project.stop(wait_for_finished=wait_for_finished)
