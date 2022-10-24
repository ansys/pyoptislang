"""Contains abstract optiSLang server class."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Sequence, Tuple, Union


class OslServer(ABC):
    """Base class for classes which provide access to optiSLang server."""

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def open(
        self,
        file_path: Union[str, Path],
        force: bool,
        restore: bool,
        reset: bool,
    ) -> None:
        """Open a new project.

        Parameters
        ----------
        file_path : Union[str, Path]
            Path to the optiSLang project file to open.
        force : bool
            # TODO: description of this parameter is missing in ANSYS help
        restore : bool
            # TODO: description of this parameter is missing in ANSYS help
        reset : bool
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def save_as(
        self,
        file_path: Union[str, Path],
        force: bool,
        restore: bool,
        reset: bool,
    ) -> None:
        """Save and open the current project at a new location.

        Parameters
        ----------
        file_path : Union[str, Path]
            Path where to save the project file.
        force : bool
            # TODO: description of this parameter is missing in ANSYS help
        restore : bool
            # TODO: description of this parameter is missing in ANSYS help
        reset : bool
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def start(self, wait_for_finish: bool = True) -> None:
        """Start project execution.

        Parameters
        ----------
        wait_for_finish : bool, optional
            Determines whether this function call should wait on the optiSlang to finish
            the project execution. Defaults to ``True``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def stop(self, wait_for_finish: bool = True) -> None:
        """Stop project execution.

        Parameters
        ----------
        wait_for_finish : bool, optional
            Determines whether this function call should wait on the optiSlang to finish
            the project execution. Defaults to ``True``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def stop_gently(self, wait_for_finish: bool = True) -> None:
        """Stop project execution after the current design is finished.

        Parameters
        ----------
        wait_for_finish : bool, optional
            Determines whether this function call should wait on the optiSlang to finish
            the project execution. Defaults to ``True``.

        Raises
        ------
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass
