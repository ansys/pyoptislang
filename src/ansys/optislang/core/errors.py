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
