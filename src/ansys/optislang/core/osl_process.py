"""Contains class which starts and controls local opstiSLang server process."""
from enum import Enum
import logging
import os
from pathlib import Path
import subprocess
import tempfile
from threading import Thread
from typing import Any, Callable, Dict, Iterable, List, Mapping, Sequence, Tuple, Union

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
    executable : Union[str, Path]
        Path to the optiSLang executable file.
    project_path : Union[str, Path], optional
        Path to the optiSLang project file.
        - If the project file exists, it is opened.
        - If the project file does not exist, a new project is created on the specified path.
        - If the path is None, a new project is created in the temporary directory.
        Defaults to ``None``.
    batch : bool, optional
        Determines whether to start optiSLang server in batch mode. Defaults to ``True``.
    port_range : Tuple[int, int], optional
        Defines the port range for optiSLang server. Defaults to ``None``.
    password : str, optional
        The server password. Use when communication with the server requires the request
        to contain a password entry. Defaults to ``None``.
    no_save : bool, optional
        Determines whether not to save the specified project after all other actions are completed.
        Defaults to ``False``.
    server_info : Union[str, Path], optional
        Path to the server information file. If an absolute path is not supplied, it is considered
        to be relative to the project working directory. If ``None``, no server information file
        will be written. Defaults to ``None``.
    log_commands : bool, optional
        Determines whether to display server events in the Message log pane. Defaults to ``False``.
    listener : Tuple[str, int], optional
        Host and port of the remote listener (plain TCP/IP based) to be registered by optiSLang
        server. Defaults to ``None``.
    listener_id : str, optional
        Specific unique ID for the TCP listener. Defaults to ``None``.
    notifications : Iterable[ServerNotification], optional
        Notifications to be sent to the listener. Defaults to ``None``.
    shutdown_on_finished: bool, optional
        Shut down when execution is finished. Defaults to ``True``.

    env_vars : Mapping[str, str], optional
        Additional environmental variables (key and value) for the optiSLang server process.
        Defaults to ``None``.
    logger : Any, optional
        Object for logging. If ``None``, standard logging object is used. Defaults to ``None``.
    log_process_stdout : bool, optional
        Determines whether the process STDOUT is supposed to be logged. Defaults to ``True``.
    log_process_stderr : bool, optional
        Determines whether the process STDERR is supposed to be logged. Defaults to ``True``.
    **kwargs : Dict[str, Any], optional
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
        executable: Union[str, Path] = None,
        project_path: Union[str, Path] = None,
        batch: bool = True,
        port_range: Tuple[int, int] = None,
        password: str = None,
        no_save: bool = False,
        server_info: Union[str, Path] = None,
        log_server_events: bool = False,
        listener: Tuple[str, int] = None,
        listener_id: str = None,
        notifications: Iterable[ServerNotification] = None,
        shutdown_on_finished: bool = True,
        env_vars: Mapping[str, str] = None,
        logger=None,
        log_process_stdout: bool = True,
        log_process_stderr: bool = True,
        **kwargs,
    ) -> None:
        """Initialize a new instance of the ``OslServerProcess`` class."""
        if logger is None:
            self._logger = logging.getLogger(__name__)
        else:
            self._logger = logger

        self.__process = None
        self.__handle_process_output_thread = None

        self.__tempdir = None

        if executable is not None:
            if not os.path.isfile(executable):
                raise FileNotFoundError(f"optiSLang executable cannot be found: {executable}")
            self.__executable = Path(executable)
        else:
            osl_exec = utils.get_osl_exec()
            if osl_exec is not None:
                osl_version, osl_exec_path = osl_exec
                self.__executable = osl_exec_path
                self._logger.info(
                    f"optiSLang executable has been found for version {osl_version} "
                    f"on path: {osl_exec_path}"
                )
            else:
                raise RuntimeError("No optiSLang executable could be found.")

        if project_path == None:
            self.__tempdir = tempfile.TemporaryDirectory()
            project_path = Path(self.__tempdir.name) / self.__class__.DEFAULT_PROJECT_FILE

        if isinstance(project_path, str):
            project_path = Path(project_path)

        if not isinstance(project_path, Path):
            raise TypeError(
                f"Invalid type of project_path: {type(project_path)},"
                "Union[str, Path] is supported."
            )

        if not project_path.suffix == ".opf":
            raise ValueError("Invalid optiSLang project file.")

        self.__project_path = project_path

        if isinstance(server_info, str):
            server_info = Path(server_info)
        elif not (isinstance(server_info, Path) or server_info is None):
            raise TypeError(
                f"Invalid type of server_info: {type(server_info)},"
                "Union[str, Path] is supported."
            )
        self.__server_info = server_info

        self.__batch = batch
        self.__port_range = port_range
        self.__password = password
        self.__no_save = no_save
        self.__log_server_events = log_server_events
        self.__listener = listener
        self.__listener_id = listener_id
        self.__notifications = tuple(notifications) if notifications is not None else None
        self.__shutdown_on_finished = shutdown_on_finished
        self.__env_vars = dict(env_vars) if env_vars is not None else None
        self.__log_process_stdout = log_process_stdout
        self.__log_process_stderr = log_process_stderr
        self.__additional_args = kwargs

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
        Path
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
    def server_info(self) -> Union[Path, None]:
        """Path to the server information file.

        Returns
        -------
        Union[Path, None]
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

        The listener (plain TCP/IP based) is registered by optiSLang server.

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
        :class:
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
    def additional_args(self) -> Dict[str, Any]:
        """Additional command line arguments used for optiSLang server process execution.

        Returns
        -------
        Dict[str, Any]
            Dictionary of command line arguments, if defined; ``None`` otherwise.
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
        if self.__process is None:
            return None

        return self.__process.pid

    @property
    def shutdown_on_finished(self) -> str:
        """Whether to shut down when execution is finished.

        Returns
        -------
        str
            Whether to shut down when execution is finished.
        """
        return self.__shutdown_on_finished

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
        args = []
        args.append(str(self.__executable))

        if self.__batch:
            args.append("-b")  # Start batch mode

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
            args.append("--no-run")  # Does not run the specified projects.
            # Forces projects to be processed, even if they are incomplete
            # (can be used for damaged projects).
            args.append("--force")

        # Enables remote surveillance (plain TCP/IP based), the port indication is optional.
        if self.__port_range is not None:
            args.append(f"--enable-tcp-server={self.__port_range[0]}-{self.__port_range[1]}")
        else:
            args.append(f"--enable-tcp-server")

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

        if self.__no_save:
            # Do not save the specified projects after all other actions have been completed.
            args.append("--no-save")

        if self.__log_server_events is not None:
            # Displays server events in the Message log pane.
            args.append("--log-server-events")

        if self.__listener is not None:
            # Registers the remote listener (plain TCP/IP based) for specified host and port.
            args.append(f"--register-tcp-listener={self.__listener[0]}:{self.__listener[1]}")

        if self.__listener_id is not None:
            # Sets a specific unique ID for the TCP listener.
            args.append(f"--tcp-listener-id={self.__listener_id}")

        if self.__notifications is not None:
            # Subscribe to push notifications sent to the listener.
            args.append("--enable-notifications")
            for notification in self.__notifications:
                args.append(notification.name)

        if self.__additional_args is not None:
            for arg_name, arg_value in self.__additional_args.items():
                args.append(f"{arg_name}={arg_value}")

        if self.__shutdown_on_finished:
            args.append("--shutdown-on-finished")
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
