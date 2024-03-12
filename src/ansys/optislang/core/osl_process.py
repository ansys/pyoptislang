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

"""Contains class which starts and controls local opstiSLang server process."""
from enum import Enum
import logging
import os
from pathlib import Path
import subprocess
import tempfile
from threading import Thread
from typing import Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple, Union

import psutil

from ansys.optislang.core import IRON_PYTHON, encoding, utils

if IRON_PYTHON:
    import System


class ServerNotification(Enum):
    """Push notifications available for subscription from the optiSLang server."""

    SERVER_UP = 0
    SERVER_DOWN = 1
    LOG_INFO = 2
    LOG_WARNING = 3
    LOG_ERROR = 4
    LOG_DEBUG = 5
    EXECUTION_STARTED = 6
    PROCESSING_STARTED = 7
    EXECUTION_FINISHED = 8
    NOTHING_PROCESSED = 9
    CHECK_FAILED = 10
    EXEC_FAILED = 11
    ACTOR_STATE_CHANGED = 12
    ACTOR_ACTIVE_CHANGED = 13
    ACTOR_NAME_CHANGED = 14
    ACTOR_CONTENTS_CHANGED = 15
    ACTOR_DATA_CHANGED = 16
    ALL = 17


class OslServerProcess:
    r"""Starts and controls local optiSLang server process.

    Parameters
    ----------
    executable : Optional[Union[str, pathlib.Path]], optional
        Path to the optiSLang executable file. Defaults to ``None``.
    project_path : Optional[Union[str, pathlib.Path]], optional
        Path to the optiSLang project file.
        - If the project file exists, it is opened.
        - If the project file does not exist, a new project is created on the specified path.
        - If the path is None, a new project is created in the temporary directory.
        Defaults to ``None``.
    batch : bool, optional
        Determines whether to start optiSLang server in batch mode. Defaults to ``True``.

        ..note:: Cannot be used in combination with service mode.

    service: bool, optional
        Determines whether to start optiSLang server in service mode. If ``True``,
        ``batch`` argument is set to ``False``. Defaults to ``False``.

        ..note:: Cannot be used in combination with batch mode.

    port_range : Tuple[int, int], optional
        Defines the port range for optiSLang server. Defaults to ``None``.
    password : Optional[str], optional
        The server password. Use when communication with the server requires the request
        to contain a password entry. Defaults to ``None``.
    no_run : Optional[bool], optional
        Determines whether not to run the specified project when started in batch mode.
        Defaults to ``None``.

        .. note:: Only supported in batch mode.

    no_save : bool, optional
        Determines whether not to save the specified project after all other actions are completed.
        Defaults to ``False``.

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

    enable_tcp_server : bool, optional
        Determines whether to enable optiSLang TCP server.
        Defaults to ``True``.
    server_info : Optional[Union[str, pathlib.Path]], optional
        Path to the server information file. If a relative path is provided, it is considered
        to be relative to the project working directory. If ``None``, no server information file
        will be written. Defaults to ``None``.
    log_commands : bool, optional
        Determines whether to display server events in the Message log pane. Defaults to ``False``.
    listener : Optional[Tuple[str, int]], optional
        Host and port of the remote listener (plain TCP/IP based) to be registered at optiSLang
        server. Defaults to ``None``.
    listener_id : Optional[str], optional
        Specific unique ID for the TCP listener. Defaults to ``None``.
    multi_listener : Iterable[Tuple[str, int, Optional[str]]], optional
        Multiple remote listeners (plain TCP/IP based) to be registered at optiSLang server.
        Each listener is a combination of host, port and (optionally) listener ID.
        Defaults to ``None``.
    notifications : Optional[Iterable[ServerNotification]], optional
        Notifications to be sent to the listener. Defaults to ``None``.
    shutdown_on_finished: bool, optional
        Shut down when execution is finished. Defaults to ``True``.

        .. note:: Only supported in batch mode.

    env_vars : Optional[Mapping[str, str]], optional
        Additional environmental variables (key and value) for the optiSLang server process.
        Defaults to ``None``.
    logger : Any, optional
        Object for logging. If ``None``, standard logging object is used. Defaults to ``None``.
    log_process_stdout : bool, optional
        Determines whether the process STDOUT is supposed to be logged. Defaults to ``True``.
    log_process_stderr : bool, optional
        Determines whether the process STDERR is supposed to be logged. Defaults to ``True``.
    import_project_properties_file : Optional[Union[str, pathlib.Path]], optional
        Optional path to a project properties file to import. Defaults to ``None``.
    export_project_properties_file : Optional[Union[str, pathlib.Path]], optional
        Optional path to a project properties file to export. Defaults to ``None``.

        .. note:: Only supported in batch mode.

    import_placeholders_file : Optional[Union[str, pathlib.Path]], optional
        Optional path to a placeholders file to import. Defaults to ``None``.
    export_placeholders_file : Optional[[str, pathlib.Path]], optional
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
    TypeError
        Raised when the optiSLang executable is None.
    FileNotFoundError
        Raised when the optiSLang executable cannot be found.
    ValueError
        Raised when the path to the optiSLang project file is invalid.

    Examples
    --------
    Start optiSLang server process in batch with specified path to the optiSLang project.
    File paths are defined in Windows operating system.

    >>> from ansys.optislang.core import OslServerProcess
    >>> executable = r"C:\Program Files\ANSYS Inc\v221\optiSLang\optislang.com"
    >>> project_path = r"C:\osl_project\project.opf"
    >>> osl_process = OslServerProcess(executable, project_path)
    >>> osl_process.start()
    """

    DEFAULT_PROJECT_FILE = "project.opf"

    def __init__(
        self,
        executable: Optional[Union[str, Path]] = None,
        project_path: Optional[Union[str, Path]] = None,
        batch: bool = True,
        service: bool = False,
        port_range: Optional[Tuple[int, int]] = None,
        password: Optional[str] = None,
        no_run: Optional[bool] = None,
        no_save: bool = False,
        force: bool = True,
        reset: bool = False,
        auto_relocate: bool = False,
        enable_tcp_server: bool = True,
        server_info: Optional[Union[str, Path]] = None,
        log_server_events: bool = False,
        listener: Optional[Tuple[str, int]] = None,
        listener_id: Optional[str] = None,
        multi_listener: Optional[Iterable[Tuple[str, int, Optional[str]]]] = None,
        notifications: Optional[Iterable[ServerNotification]] = None,
        shutdown_on_finished: bool = True,
        env_vars: Optional[Mapping[str, str]] = None,
        logger=None,
        log_process_stdout: bool = True,
        log_process_stderr: bool = True,
        import_project_properties_file: Optional[Union[str, Path]] = None,
        export_project_properties_file: Optional[Union[str, Path]] = None,
        import_placeholders_file: Optional[Union[str, Path]] = None,
        export_placeholders_file: Optional[Union[str, Path]] = None,
        output_file: Optional[Union[str, Path]] = None,
        dump_project_state: Optional[Union[str, Path]] = None,
        opx_project_definition_file: Optional[Union[str, Path]] = None,
        additional_args: Optional[Iterable[str]] = None,
    ) -> None:
        """Initialize a new instance of the ``OslServerProcess`` class."""
        self.__batch = batch if not service else False
        self.__service = service
        self._logger = logging.getLogger(__name__) if logger is None else logger
        self.__process = None
        self.__handle_process_output_thread = None

        self.__tempdir = None

        if executable is None:
            osl_exec = utils.get_osl_exec()
            if osl_exec is None:
                raise RuntimeError("No optiSLang executable could be found.")

            osl_version, osl_exec_path = osl_exec
            self.__executable = osl_exec_path
            self._logger.info(
                f"optiSLang executable has been found for version {osl_version} "
                f"on path: {osl_exec_path}"
            )
        elif not os.path.isfile(executable):
            raise FileNotFoundError(f"optiSLang executable cannot be found: {executable}")
        else:
            self.__executable = Path(executable)
        if self.__batch:
            if project_path is None:
                self.__tempdir = tempfile.TemporaryDirectory()
                project_path = Path(self.__tempdir.name) / self.__class__.DEFAULT_PROJECT_FILE

        self.__project_path = self.__class__.__validated_path(project_path, "project_path")

        if self.__project_path.suffix != ".opf":
            raise ValueError("Invalid optiSLang project file.")

        self.__server_info = self.__class__.__validated_path(server_info, "server_info")
        self.__import_project_properties_file = self.__class__.__validated_path(
            import_project_properties_file, "import_project_properties_file"
        )
        self.__export_project_properties_file = self.__class__.__validated_path(
            export_project_properties_file, "export_project_properties_file"
        )
        self.__import_placeholders_file = self.__class__.__validated_path(
            import_placeholders_file, "import_placeholders_file"
        )
        self.__export_placeholders_file = self.__class__.__validated_path(
            export_placeholders_file, "export_placeholders_file"
        )
        self.__output_file = self.__class__.__validated_path(output_file, "output_file")
        self.__dump_project_state = self.__class__.__validated_path(
            dump_project_state, "dump_project_state"
        )
        self.__opx_project_definition_file = self.__class__.__validated_path(
            opx_project_definition_file, "opx_project_definition_file"
        )

        self.__port_range = port_range
        self.__password = password
        self.__no_run = no_run
        self.__no_save = no_save
        self.__force = force
        self.__reset = reset
        self.__auto_relocate = auto_relocate
        self.__enable_tcp_server = enable_tcp_server
        self.__log_server_events = log_server_events
        self.__listener = listener
        self.__listener_id = listener_id
        self.__multi_listener = multi_listener
        self.__notifications = tuple(notifications) if notifications is not None else None
        self.__shutdown_on_finished = shutdown_on_finished
        self.__env_vars = dict(env_vars) if env_vars is not None else None
        self.__log_process_stdout = log_process_stdout
        self.__log_process_stderr = log_process_stderr
        self.__additional_args = additional_args

        if "PYOPTISLANG_DISABLE_OPTISLANG_OUTPUT" in os.environ:
            self.__log_process_stdout, self.__log_process_stderr = False, False

    @property
    def executable(self) -> Path:
        """Path to the optiSLang executable file.

        Returns
        -------
        Path
            Path to the optiSLang executable file.
        """
        return self.__executable

    @property
    def project_path(self) -> Path:
        """Path to the optiSLang project file.

        Returns
        -------
        pathlib.Path
            Path to the optiSLang project file.
        """
        return self.__project_path

    @property
    def batch(self) -> bool:
        """Get whether the optiSLang server is supposed to be started in batch mode.

        Returns
        -------
        bool
            ``True`` if the optiSLang server is supposed to be started in batch mode; ``False``
            otherwise.
        """
        return self.__batch

    @property
    def port_range(self) -> Tuple[int, int]:
        """Port range for optiSLang server execution.

        Returns
        -------
        Tuple[int, int]
            Tuple of minimum and maximum port number, if defined; ``None`` otherwise.
        """
        return self.__port_range

    @property
    def password(self) -> str:
        """Server password.

        Returns
        -------
        str
            Server password, if defined; ``None`` otherwise.
        """
        return self.__password

    @property
    def no_run(self) -> bool:
        """Get whether not to run the specified project when started in batch mode .

        Returns
        -------
        bool
            ``True`` if the project is explicitly not supposed to be run;
            ``False`` if the project is explicitly supposed to be run;
            ``None`` otherwise.
        """
        return self.__no_run

    @property
    def no_save(self) -> bool:
        """Get whether not to save the specified project after all other actions are completed.

        Returns
        -------
        bool
            ``True`` if the project is not supposed to be saved after all other actions are
            completed; ``False`` otherwise.
        """
        return self.__no_save

    @property
    def reset(self) -> bool:
        """Get whether to reset specified project after load.

        Returns
        -------
        bool
            ``True`` if project is to be reset after load; ``False`` otherwise.
        """
        return self.__reset

    @property
    def auto_relocate(self) -> bool:
        """Get whether to automatically relocate missing file paths.

        Returns
        -------
        bool
            ``True`` if automatic relocation is enabled; ``False`` otherwise.
        """
        return self.__auto_relocate

    @property
    def enable_tcp_server(self) -> bool:
        """Get whether to enable optiSLang TCP server.

        Returns
        -------
        bool
            ``True`` if optiSLang TCP server is enabled; ``False`` otherwise.
        """
        return self.__enable_tcp_server

    @property
    def server_info(self) -> Union[Path, None]:
        """Path to the server information file.

        Returns
        -------
        Union[pathlib.Path, None]
            Path to the server information file, if defined; ``None`` otherwise.
        """
        return self.__server_info

    @property
    def log_commands(self) -> bool:
        """Get whether to display server events in the Message log pane.

        Returns
        -------
        bool
            ``True`` if server events are supposed to be displayed in the Message log pane;
            ``False`` otherwise.
        """
        return self.__log_server_events

    @property
    def listener(self) -> Tuple[str, int]:
        """Host and port of the remote listener.

        The listener (plain TCP/IP based) is registered at optiSLang server.

        Returns
        -------
        Tuple[str, int]
            Host and port of the listener, if defined; ``None`` otherwise.
        """
        return self.__listener

    @property
    def listener_id(self) -> str:
        """Specific unique ID for the TCP listener.

        Returns
        -------
        str
            Specific unique ID for the TCP listener, if defined; ``None`` otherwise.
        """
        return self.__listener_id

    @property
    def multi_listener(self) -> Iterable[Tuple[str, int, Optional[str]]]:
        """Multi remote listener definitions.

        Aeach listener (plain TCP/IP based) is registered at optiSLang server.

        Returns
        -------
        Iterable[Tuple[str, int, Optional[str]]]
            Multi remote listener combinations, if defined; ``None`` otherwise.
        """
        return self.__multi_listener

    @property
    def notifications(self) -> Tuple[ServerNotification, ...]:
        """Notifications which are sent to the listener.

        Returns
        -------
        Tuple[ServerNotification,...]
            Notifications which are sent to the listener, if defined; ``None`` otherwise.
        """
        return self.__notifications

    @property
    def env_vars(self) -> Dict[str, str]:
        """Additional environmental variables for the optiSLang server process.

        Returns
        -------
        Dict[str, str]
            Dictionary of additional environmental variables, if defined; ``None`` otherwise.
        """
        return self.__env_vars

    @property
    def logger(self):
        """Object used for logging.

        Returns
        -------
        Any
            Logger object.
        """
        return self._logger

    @property
    def log_process_stdout(self) -> bool:
        """Get whether the STDOUT of the optiSLang server process is to be logged.

        Returns
        -------
        bool
            ``True`` if the STDOUT of the optiSLang server process is to be logged; ``False``
            otherwise.
        """
        return self.__log_process_stdout

    @property
    def log_process_stderr(self) -> bool:
        """Get whether the STDERR of the optiSLang server process is to be logged.

        Returns
        -------
        bool
            ``True`` if the STDERR of the optiSLang server process is to be logged; ``False``
            otherwise.
        """
        return self.__log_process_stderr

    @property
    def additional_args(self) -> Tuple[str, ...]:
        """Additional command line arguments used for optiSLang server process execution.

        Returns
        -------
        Tuple[str, ...]
            Additional command line arguments, if defined; ``None`` otherwise.
        """
        return self.__additional_args

    @property
    def pid(self) -> Union[int, None]:
        """Process ID.

        Returns
        -------
        Union[int, None]
            Process ID, if exists; ``None`` otherwise.
        """
        return None if self.__process is None else self.__process.pid

    @property
    def shutdown_on_finished(self) -> str:
        """Whether to shut down when execution is finished.

        Returns
        -------
        str
            Whether to shut down when execution is finished.
        """
        return self.__shutdown_on_finished

    @property
    def import_project_properties_file(self) -> Union[Path, None]:
        """Path to the project properties import file.

        Returns
        -------
        Union[pathlib.Path, None]
            Path to the project properties import file, if defined; ``None`` otherwise.
        """
        return self.__import_project_properties_file

    @property
    def export_project_properties_file(self) -> Union[Path, None]:
        """Path to the project properties export file.

        Returns
        -------
        Union[pathlib.Path, None]
            Path to the project properties export file, if defined; ``None`` otherwise.
        """
        return self.__export_project_properties_file

    @property
    def import_placeholders_file(self) -> Union[Path, None]:
        """Path to the placeholders import file.

        Returns
        -------
        Union[pathlib.Path, None]
            Path to the placeholders import file, if defined; ``None`` otherwise.
        """
        return self.__import_placeholders_file

    @property
    def export_placeholders_file(self) -> Union[Path, None]:
        """Path to the placeholders export file.

        Returns
        -------
        Union[pathlib.Path, None]
            Path to the placeholders export file, if defined; ``None`` otherwise.
        """
        return self.__export_placeholders_file

    @property
    def output_file(self) -> Union[Path, None]:
        """Path to the output file for writing project run results to.

        Returns
        -------
        Union[pathlib.Path, None]
            Path to the output file for writing project run results to, if defined;
            ``None`` otherwise.
        """
        return self.__output_file

    @property
    def dump_project_state(self) -> Union[Path, None]:
        """Path to a project state dump file to export.

        Returns
        -------
        Union[pathlib.Path, None]
            Path to a project state dump file to export, if defined; ``None`` otherwise.
        """
        return self.__dump_project_state

    @property
    def opx_project_definition_file(self) -> Union[Path, None]:
        """Path to the OPX project definition file.

        Returns
        -------
        Union[pathlib.Path, None]
            Path to the OPX project definition file, if defined;
            ``None`` otherwise.
        """
        return self.__opx_project_definition_file

    def __enter__(self):
        """Enter the context."""
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        """Exit the context."""
        self.terminate()

    def _get_process_args(self) -> List[str]:
        """Get the command line arguments for the optiSLang server process execution.

        Returns
        -------
        List[str]
            List of command line arguments.
        """
        args = [str(self.__executable)]

        if self.__batch:
            args.append("-b")  # Start batch mode

        if self.__service:
            args.append("--svc")  # Start service mode

        if self.__project_path:
            if not self.__project_path.is_file():
                # Creates a new project in the provided path.
                if IRON_PYTHON:
                    args.append(f'--new="{str(self.__project_path)}"')
                else:
                    args.append(f"--new={str(self.__project_path)}")
            else:
                # Opens existing project
                if IRON_PYTHON:
                    args.append(f'"{str(self.__project_path)}"')
                else:
                    args.append(str(self.__project_path))

        if self.__batch:
            if self.__opx_project_definition_file:
                if IRON_PYTHON:
                    args.append("--python")
                    args.append(f'"{str(utils.get_osl_opx_import_script(self.__executable))}"')
                    args.append("--script-arg")
                    args.append(f'"{str(self.__opx_project_definition_file)}"')
                else:
                    args.append("--python")
                    args.append(str(utils.get_osl_opx_import_script(self.__executable)))
                    args.append("--script-arg")
                    args.append(str(self.__opx_project_definition_file))
            if self.__no_run is None or self.__no_run:
                # Do not run the specified projects.
                args.append("--no-run")
            if self.__no_save:
                # Do not save the specified projects after all other actions have been completed.
                args.append("--no-save")
            if self.__force:
                # Forces projects to be processed, even if they are incomplete
                # (can be used for damaged projects).
                args.append("--force")
            if self.__shutdown_on_finished:
                args.append("--shutdown-on-finished")
            if self.__reset:
                args.append("--reset")
            if self.__auto_relocate:
                args.append("--autorelocate")
            if self.__export_project_properties_file is not None:
                args.append("--export-project-properties")
                if IRON_PYTHON:
                    args.append(f'"{str(self.__export_project_properties_file)}"')
                else:
                    args.append(str(self.__export_project_properties_file))
            if self.__export_placeholders_file is not None:
                args.append("--export-values")
                if IRON_PYTHON:
                    args.append(f'"{str(self.__export_placeholders_file)}"')
                else:
                    args.append(str(self.__export_placeholders_file))
            if self.__output_file is not None:
                args.append("--output-file")
                if IRON_PYTHON:
                    args.append(f'"{str(self.__output_file)}"')
                else:
                    args.append(str(self.__output_file))
            if self.__dump_project_state is not None:
                if IRON_PYTHON:
                    args.append(f'--dump-project-state="{str(self.__dump_project_state)}"')
                else:
                    args.append(f"--dump-project-state={str(self.__dump_project_state)}")

        # Enables remote surveillance (plain TCP/IP based), the port indication is optional.
        if self.__enable_tcp_server:
            if self.__port_range is not None:
                args.append(f"--enable-tcp-server={self.__port_range[0]}-{self.__port_range[1]}")
            else:
                args.append("--enable-tcp-server")

        if self.__password is not None:
            # Submits the server password. Use when communication with the server requires
            # the request to contain a password entry.
            args.append(f"--server-password={self.__password}")

        if self.__server_info is not None:
            # Writes the server information file using the file path specified. If an absolute path
            # is not supplied, it is considered to be relative to the project working directory.
            if IRON_PYTHON:
                args.append(f'--write-server-info="{str(self.__server_info)}"')
            else:
                args.append(f"--write-server-info={str(self.__server_info)}")

        if self.__log_server_events:
            # Displays server events in the Message log pane.
            args.append("--log-server-events")

        if self.__listener is not None:
            # Registers the remote listener (plain TCP/IP based) for specified host and port.
            args.append(f"--register-tcp-listener={self.__listener[0]}:{self.__listener[1]}")

        if self.__listener_id is not None:
            # Sets a specific unique ID for the TCP listener.
            args.append(f"--tcp-listener-id={self.__listener_id}")

        if self.__multi_listener is not None:
            if len(self.__multi_listener) >= 1:
                args.append("--register-multi-tcp-listeners")
            for listener in self.__multi_listener:
                if len(listener) >= 3 and listener[2] is not None:
                    args.append(f"{listener[0]}:{listener[1]}+{listener[2]}")
                else:
                    args.append(f"{listener[0]}:{listener[1]}")

        if self.__notifications is not None:
            # Subscribe to push notifications sent to the listener.
            args.append("--enable-notifications")
            for notification in self.__notifications:
                args.append(notification.name)

        if self.__import_project_properties_file is not None:
            args.append("--import-project-properties")
            if IRON_PYTHON:
                args.append(f'"{str(self.__import_project_properties_file)}"')
            else:
                args.append(str(self.__import_project_properties_file))

        if self.__import_placeholders_file is not None:
            args.append("--import-values")
            if IRON_PYTHON:
                args.append(f'"{str(self.__import_placeholders_file)}"')
            else:
                args.append(str(self.__import_placeholders_file))

        if self.__additional_args is not None:
            for arg in self.__additional_args:
                args.append(arg)

        return args

    def __remove_server_info_files(self):
        """Remove server information files.

        Remove all .ini files located in the same directory as optiSLang project file.
        """
        if self.__project_path is not None:
            project_dir = os.path.dirname(self.__project_path)
            for file in os.listdir(project_dir):
                if file.endswith(".ini"):
                    info_file = os.path.join(project_dir, file)
                    os.remove(info_file)
                    self._logger.info("The server information file %s has been removed", info_file)

    def start(self, remove_ini_files: bool = True):
        """Start new optiSLang server process.

        Parameters
        ----------
        remove_ini_files : bool, optional
            Determines whether to remove all server information files (.ini) located in the same
            directory as the optiSLang project file. Defaults to ``True``.

        Raises
        ------
        RuntimeError
            Raised when the process is already running.
        """
        if self.is_running():
            raise RuntimeError("Process is running.")

        if remove_ini_files:
            self.__remove_server_info_files()

        args = self._get_process_args()
        env_vars = os.environ.copy()
        if self.__env_vars is not None:
            env_vars.update(self.__env_vars)

        if IRON_PYTHON:
            self.__start_in_iron_python(args, env_vars)
        else:
            self.__start_in_python(args, env_vars)

        if self.__log_process_stdout or self.__log_process_stderr:
            self.__start_process_output_thread()

    def __start_in_iron_python(self, args: Sequence[str], env_vars: Mapping[str, str]):
        """Start new optiSLang server process with IronPython interpreter.

        Parameters
        ----------
        args : Sequence[str]
            Sequence of command line arguments.

        env_vars : Mapping[str, str]
            Environment variables.
        """
        start_info = System.Diagnostics.ProcessStartInfo()

        if env_vars is not None:
            for var_name, var_value in env_vars.items():
                var_value = var_value if var_value is not None else ""  # FIX: This is not necessary
                if not start_info.EnvironmentVariables.ContainsKey(var_name):
                    start_info.EnvironmentVariables.Add(var_name, var_value)

        # TODO: Add comment why this is done
        if start_info.EnvironmentVariables.ContainsKey("LD_LIBRARY_PATH"):
            start_info.EnvironmentVariables.Remove("LD_LIBRARY_PATH")
            self._logger.debug(
                "LD_LIBRARY_PATH environment variable has been removed before "
                "start of the optiSLang process."
            )

        start_info.UseShellExecute = False
        start_info.RedirectStandardError = True
        start_info.RedirectStandardOutput = True
        start_info.CreateNoWindow = True
        start_info.FileName = self.executable
        start_info.Arguments = " ".join(args)

        self.__process = System.Diagnostics.Process()
        self.__process.StartInfo = start_info

        self._logger.debug("Executing process %s", args)
        self.__process.Start()

    def __start_in_python(self, args: Sequence[str], env_vars: Mapping[str, str]):
        """Start new optiSLang server process with Python interpreter.

        Parameters
        ----------
        args : Sequence[str]
            Sequence of command line arguments.

        env_vars : Mapping[str, str]
            Environment variables.
        """
        for i in range(len(args)):
            args[i] = encoding.to_ascii_safe(args[i])

        for var_name in env_vars:
            env_vars[var_name] = encoding.to_ascii_safe(env_vars[var_name])

        # TODO: Add comment why this is done
        if "LD_LIBRARY_PATH" in env_vars:
            env_vars.pop("LD_LIBRARY_PATH")
            self._logger.debug(
                "LD_LIBRARY_PATH environment variable has been removed before "
                "start of the optiSLang process."
            )

        self._logger.debug("Executing process %s", args)
        self.__process = subprocess.Popen(
            args,
            env=env_vars,
            cwd=os.getcwd(),
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            shell=False,
        )
        self._logger.debug("optiSLang server process has started with PID: %d", self.__process.pid)

    def __terminate_osl_child_processes(self):
        """Terminate all child processes of the optiSLang server process."""
        try:
            parent = psutil.Process(self.__process.pid)
        except psutil.NoSuchProcess:
            return

        children = parent.children(recursive=True)
        for process in children:
            try:
                process.terminate()
            except psutil.NoSuchProcess:
                self._logger.debug(
                    f"Cannot terminate child process PID: {process.pid}. "
                    "The process does not exist."
                )

        gone, alive = psutil.wait_procs(children, timeout=3)

        for process in alive:
            self._logger.debug(
                f"optiSLang server child process {process} could not be terminated "
                "and will be killed.",
            )
            process.kill()

    def terminate(self):
        """Terminate optiSLang server process."""
        if self.__process is not None:
            self.__terminate_osl_child_processes()
            self.__process.terminate()

        if (
            self.__handle_process_output_thread is not None
            and self.__handle_process_output_thread.is_alive()
        ):
            self.__handle_process_output_thread.join()
        self.__handle_process_output_thread = None

        if self.__tempdir is not None:
            self.__tempdir.cleanup()
            self.__tempdir = None

    def is_running(self) -> bool:
        """Determine whether the optiSLang server process is running.

        Returns
        -------
        bool
            ``True`` if the optiSLang server process is running; ``False`` otherwise.
        """
        if self.__process is None:
            return False

        return self.__process.poll() is None

    def wait_for_finished(self):
        """Wait for the process to finish."""
        if self.__process is not None and self.is_running():
            self.__process.wait()

    def __start_process_output_thread(self):
        """Start new thread responsible for logging of STDOUT/STDERR of the optiSLang process."""

        def finalize_process(process, **kwargs):
            process.wait(**kwargs)

        self.__handle_process_output_thread = Thread(
            target=self.__class__.__handle_process_output,
            name="PyOptiSLang.ProcessOutputHandlerThread",
            args=(
                self.__process,
                self._logger.debug if self.__log_process_stdout else None,
                self._logger.warning if self.__log_process_stderr else None,
                finalize_process,
                True,
                self._logger,
            ),
            daemon=True,
        )
        self.__handle_process_output_thread.start()

    @staticmethod
    def __handle_process_output(
        process: subprocess.Popen,
        stdout_handler: Callable[[str], None],
        stderr_handler: Callable[[str], None],
        finalizer=None,
        decode_streams: bool = True,
        logger=None,
    ):
        """Handle STDOUT/STDERR of the specified process.

        Registers for notifications to lean that process output is ready to read, and dispatches
        lines to the respective line handlers. This function returns once the finalizer returns.

        [the code was taken from gitpython]

        Parameters
        ----------
        process : subprocess.Popen
            Process which STDOUT or STDERR is supposed to be handled.

        stdout_handler : Callable[[str], None], None
            Handler for STDOUT.

        stderr_handler : Callable[[str], None], None
            Handler for STDERR. It is supposed to be a function with one argument of str.

        finalizer : Callable[[subprocess.Popen,...], Any], optional
            Function which finalizes output process handling. Defaults to ``None``.

        decode_streams : bool, optional
            Determines whether to safely decode STDOUT/STDERR streams before pushing their
            contents to handlers. Should be set to ``False`` if 'universal_newline == True'
            (then streams are in text-mode) or if decoding must happen later. Defaults to ``True``.

        logger : Any, optional
            Object for logging. Defaults to ``None``.

        Returns
        -------
        Any
            Result of finalizer.
        """
        logger.debug("Start to handling optiSLang server process output.")

        # Use 2 "pupm" threads and wait for both to finish.
        if IRON_PYTHON:

            def stream_reader(cmdline, name, stream, is_decode, handler):
                try:
                    while True:
                        if stream.EndOfStream:
                            break
                        line = stream.ReadLine()
                        if handler:
                            try:
                                if is_decode:
                                    line = encoding.force_text(line)
                                handler("optiSLang " + name + ": " + line)
                            except:
                                handler("optiSLang " + name + ": " + line)
                except Exception as ex:
                    if logger is not None:
                        logger.debug(
                            "Pumping {0} of cmd({1}) failed due to: {2}".format(name, cmdline, ex)
                        )
                finally:
                    stream.Close()

        else:

            def stream_reader(cmdline, name, stream, is_decode, handler):
                try:
                    for line in stream:
                        if handler:
                            try:
                                if is_decode:
                                    line = encoding.force_text(line)
                                handler("optiSLang " + name + ": " + line)
                            except:
                                handler("optiSLang " + name + ": " + line)
                except Exception as ex:
                    if logger is not None:
                        logger.debug(
                            "Pumping {0} of cmd({1}) failed due to: {2}".format(name, cmdline, ex)
                        )
                finally:
                    stream.close()

        cmdline = getattr(process, "args", "")  # PY3+ only
        if not isinstance(cmdline, (tuple, list)):
            cmdline = cmdline.split()

        pumps = []
        if process.stdout and stdout_handler is not None:
            pumps.append(("Stdout", process.stdout, stdout_handler))
        if process.stderr and stderr_handler is not None:
            pumps.append(("Stderr", process.stderr, stderr_handler))

        threads = []

        for name, stream, handler in pumps:
            thread = Thread(
                target=stream_reader,
                name="PyOptiSLang." + name + "HandlerThread",
                args=(cmdline, name, stream, decode_streams, handler),
            )
            thread.daemon = True
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        if finalizer:
            return finalizer(process)

    @staticmethod
    def __validated_path(
        path: Union[str, Path],
        path_arg_name: str,
    ):
        """Validate a path.

        Parameters
        ----------
        path : Union[str, pathlib.Path]
            The path to validate.
        path_arg_name : str
            Path argument name/description.

        Returns
        -------
        pathlib.Path
            Validated path.
        """
        if isinstance(path, str):
            path = Path(path)
        elif not isinstance(path, Path) and path is not None:
            raise TypeError(
                f"Invalid type of {path_arg_name}: {type(path)},"
                "Union[str, pathlib.Path] is supported."
            )

        return path
