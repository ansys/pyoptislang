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

"""Contains abstract optiSLang server class."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import NamedTuple, Optional


class OslVersion(NamedTuple):
    """optiSLang version.

    Attributes:
        major: int
            The major version number.
        minor: int
            The minor version number.
        maintenance: int
            The maintenance version number.
        revision: int
            The revision number.
    """

    major: int
    minor: int
    maintenance: int
    revision: int


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
    def timeout(self) -> Optional[float]:  # pragma: no cover
        """Get the timeout value for executing commands.

        Returns
        -------
        timeout: Optional[float]
            Timeout in seconds to perform commands. This value must be greater
            than zero or ``None``. The default is ``None``. Another function
            raises a timeout exception if the timeout value has elapsed before
            an operation has completed. If the timeout is ``None``, functions
            wait until they're finished, and no timeout exception is raised.
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
