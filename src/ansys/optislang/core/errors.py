# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""Contains errors related to this package."""


class ResponseError(Exception):
    """Raised when the response is invalid."""

    pass


class ResponseFormatError(ResponseError):
    """Raised when the format of the response is invalid."""

    pass


class EmptyResponseError(ResponseError):
    """Raised when the response is empty."""

    pass


class ConnectionEstablishedError(Exception):
    """Raised when the connection is already established."""

    pass


class ConnectionNotEstablishedError(Exception):
    """Raised when the connection is not established."""

    pass


class OslCommandError(Exception):
    """Raised when the optiSLang command or query fails."""

    pass


class OslCommunicationError(Exception):
    """Raised when error occurs during communication with a server."""

    pass


class OslDisposedError(Exception):
    """Raised when command was sent and Optislang instance was already disposed."""

    pass


class OslServerStartError(Exception):
    """Raised when optiSLang server process fails to start."""

    pass


class OslServerLicensingError(OslServerStartError):
    """Raised when optiSLang server process fails to start due to licensing issues."""

    pass
