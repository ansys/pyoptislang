"""Contains errors related to this package."""


class MessageError(Exception):
    """Raised when the message is invalid."""

    pass


class MessageFormatError(MessageError):
    """Raised when the format of the message is invalid."""

    pass


class EmptyMessageError(MessageError):
    """Raised when the message is empty."""

    pass


class ConnectionNotEstablishedError(Exception):
    """Raised when the connection is not established."""

    pass


class OslCommandError(Exception):
    """Raised when the optiSLang command or query fails."""

    pass


class OslCommunicationError(Exception):
    """Raised when error occurs during communication with a server."""
