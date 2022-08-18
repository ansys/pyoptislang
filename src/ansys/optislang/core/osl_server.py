"""Contains abstract optiSLang server class."""

from abc import ABC, abstractmethod
from typing import Sequence, Tuple, Union


class OslServer(ABC):
    """Base class for classes which provide access to optiSLang server."""

    @abstractmethod
    def close(self, timeout: Union[float, None] = None) -> None:
        """Close the current project.

        Parameters
        ----------
        timeout : float, None, optional
            Timeout in seconds to perform the query. It must be greater than zero or ``None``.
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def new(self, timeout: Union[float, None] = None) -> None:
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
        file_path: str,
        force: bool,
        restore: bool,
        reset: bool,
        timeout: Union[float, None] = None,
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
        OslCommunicationError
            Raised when an error occurs while communicating with server.
        OslCommandError
            Raised when the command or query fails.
        TimeoutError
            Raised when the timeout float value expires.
        """
        pass

    @abstractmethod
    def reset(self, timeout: Union[float, None] = None):
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def save(self, timeout: Union[float, None] = None) -> None:
        """Save the changed data and settings of the current project.

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
        pass

    @abstractmethod
    def save_as(
        self,
        file_path: str,
        force: bool,
        restore: bool,
        reset: bool,
        timeout: Union[float, None] = None,
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def start(self, timeout: Union[float, None] = None) -> None:
        """Start project execution.

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
        pass

    @abstractmethod
    def stop(self, timeout: Union[float, None] = None) -> None:
        """Stop project execution.

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
        pass

    @abstractmethod
    def stop_gently(self, timeout: Union[float, None] = None) -> None:
        """Stop project execution after the current design is finished.

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
        pass
