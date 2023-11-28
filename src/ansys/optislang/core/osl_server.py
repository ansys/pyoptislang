"""Contains abstract optiSLang server class."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import NamedTuple, Optional, Union


class OslVersion(NamedTuple):
    """optiSLang version.

    Attributes:
        major: int
            The major version number.
        minor: int
            The minor version number.
        maintenance: Optional[int]
            The maintenance version number. ``None`` if not parsed correctly.
        revision: Optional[int]
            The revision number. ``None`` if not parsed correctly.
    """

    major: int
    minor: int
    maintenance: Optional[int]
    revision: Optional[int]


class OslServer(ABC):
    """Base class for classes which provide access to optiSLang server."""

    @abstractmethod
    def __init__(self):  # pragma: no cover
        """``OslServer`` class is an abstract base class and cannot be instantiated."""
        pass

    @property
    @abstractmethod
    def host(self) -> Optional[str]:  # pragma no cover
        """Get optiSLang server address or domain name.

        Get a string representation of an IPv4/v6 address or domain name
        of the running optiSLang server.

        Returns
        -------
        host: Optional[int]
            The IPv4/v6 address or domain name of the running optiSLang server, if applicable.
            Defaults to ``None``.
        """
        pass

    @property
    @abstractmethod
    def osl_version(
        self,
    ) -> OslVersion:  # pragma: no cover
        """Version of used optiSLang.

        Returns
        -------
        OslVersion
            optiSLang version as typing.NamedTuple containing
            major, minor, maintenance and revision versions.
        """
        pass

    @property
    @abstractmethod
    def osl_version_string(self) -> str:  # pragma: no cover
        """Version of used optiSLang.

        Returns
        -------
        str
            optiSLang version.
        """
        pass

    @property
    @abstractmethod
    def port(self) -> Optional[int]:  # pragma: no cover
        """Get the port the osl server is listening on.

        Returns
        -------
        port: Optional[int]
            The port the osl server is listening on, if applicable.
            Defaults to ``None``.
        """
        pass

    @property
    @abstractmethod
    def timeout(self) -> Union[float, None]:  # pragma: no cover
        """Get current timeout value for execution of commands.

        Returns
        -------
        timeout: Union[float, None]
            Timeout in seconds to perform commands.
        """
        pass

    @abstractmethod
    def dispose(self) -> None:  # pragma: no cover
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
        pass

    @abstractmethod
    def shutdown(self, force: bool = False) -> None:  # pragma: no cover
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
        pass
