"""Module for input/output functionality."""
from __future__ import annotations

from enum import Enum
from pathlib import Path
import time
from typing import Union

from ansys.optislang.core.utils import enum_from_str


class File:
    """Provides for operating on files."""

    def __init__(self, path: Union[Path, str]) -> None:
        """Create a ``File`` instance.

        Parameters
        ----------
        path : Union[pathlib.Path, str]
            Path to the file.
        id: str, optional
            File ID.
        comment:  str, optional
            Description of the file.
        """
        self.__path = Path(path)

    def __eq__(self, other: File) -> bool:
        r"""Compare properties of two instances of the ``File`` class.

        Parameters
        ----------
        other: File
            File for comparison.

        Returns
        -------
        bool
            ``True`` if all properties match, ``False`` otherwise.
        """
        if type(self) == type(other):
            checks = {}
            checks["exists"] = self.exists == other.exists
            checks["filename"] = self.filename == other.filename
            checks["last_modified_seconds"] = (
                self.last_modified_seconds == other.last_modified_seconds
            )
            checks["last_modified_str"] = self.last_modified_str == other.last_modified_str
            checks["path"] = self.path == other.path
            checks["size"] = self.size == other.size
            return False not in checks.values()
        else:
            return False

    @property
    def exists(self) -> bool:
        """Check whether file exists.

        Returns
        -------
        bool
            Information, whether file exists.
        """
        return self.path.exists()

    @property
    def filename(self) -> str:
        """Get file name.

        Returns
        -------
        str
            File name
        """
        return self.path.name

    @property
    def last_modified_seconds(self) -> Union[float, None]:
        """Last modified time as a timestamp.

        Returns
        -------
        Union[float, None]
            Last modified time in seconds since the Epoch, `None` if file doesn't exist.
        """
        if self.exists:
            return self.path.stat().st_mtime
        else:
            return None

    @property
    def last_modified_str(self) -> Union[str, None]:
        """Last modified time as a datetime.

        Returns
        -------
        Union[str, None]
            Last modified time as string, `None` if file doesn't exist.
        """
        if self.exists:
            return time.ctime(self.last_modified_seconds)
        else:
            return None

    @property
    def path(self) -> Path:
        """Path to the file.

        Returns
        -------
        Path
            Path the the file
        """
        return self.__path

    @property
    def size(self) -> Union[int, None]:
        """File size in bytes.

        Returns
        -------
        Union[int, None]
            File size in bytes, `None` in file doesn't exist.
        """
        if self.exists:
            return self.path.stat().st_size
        else:
            return None


class RegisteredFile(File):
    """Provides for operating on registered files."""

    def __init__(
        self,
        path: Union[Path, str],
        id: str,
        comment: str,
        tag: str,
        usage: Union[RegisteredFileUsage, str],
    ) -> None:
        """Create a ``RegisteredFile`` instance.

        Parameters
        ----------
        path : Union[pathlib.Path, str]
            Path to the file.
        id: str
            File ID.
        comment:  str
            Description of the file.
        tag: str
            File uid.
        usage: Union[RegisteredFileUsage, str]
            Usage of registered file.
        """
        super().__init__(path=path)
        self.__id = id
        self.__comment = comment
        self.__tag = tag
        if not isinstance(usage, RegisteredFileUsage):
            usage = RegisteredFileUsage.from_str(usage)
        self.__usage = usage

    def __eq__(self, other: File) -> bool:
        r"""Compare properties of two instances of the ``RegisteredFile`` class.

        Parameters
        ----------
        other: RegisteredFile
            File for comparison.

        Returns
        -------
        bool
            ``True`` if all properties match, ``False`` otherwise.
        """
        if type(self) == type(other):
            checks = {}
            checks["exists"] = self.exists == other.exists
            checks["filename"] = self.filename == other.filename
            checks["last_modified_seconds"] = (
                self.last_modified_seconds == other.last_modified_seconds
            )
            checks["last_modified_str"] = self.last_modified_str == other.last_modified_str
            checks["path"] = self.path == other.path
            checks["size"] = self.size == other.size
            checks["comment"] = self.comment == other.comment
            checks["id"] = self.id == other.id
            checks["tag"] = self.tag == other.tag
            checks["usage"] = self.usage == other.usage
            return False not in checks.values()
        else:
            return False

    @property
    def comment(self) -> str:
        """File description.

        Returns
        -------
        str
            File description.
        """
        return self.__comment

    @property
    def id(self) -> str:
        """File id.

        Returns
        -------
        str
            File id.
        """
        return self.__id

    @property
    def tag(self) -> str:
        """File uid.

        Returns
        -------
        str
            File uid.
        """
        return self.__tag

    @property
    def usage(self) -> RegisteredFileUsage:
        """Usage of registered file.

        Returns
        -------
        RegisteredFileUsage
            Usage of registered file.
        """
        return self.__usage


class FileOutputFormat(Enum):
    """Provides options for storing files."""

    JSON = 0
    CSV = 1

    def to_str(self) -> str:
        """Convert file type to suffix.

        Returns
        -------
        str
            File suffix.
        """
        return "." + self.name.lower()


class RegisteredFileUsage(Enum):
    """Provides options for registered files usage."""

    UNDETERMINED = 0
    INTERMEDIATE_RESULT = 1
    INPUT_FILE = 2
    OUTPUT_FILE = 3

    @staticmethod
    def from_str(string: str) -> RegisteredFileUsage:
        """Convert string to an instance of the ``RegisteredFileUsage`` class.

        Parameters
        ----------
        string: str
            String to be converted.

        Returns
        -------
        RegisteredFileUsage
            Instance of the ``RegisteredFileUsage`` class.

        Raises
        ------
        TypeError
            Raised when an invalid type of ``string`` is given.
        ValueError
            Raised when an invalid value of ``string`` is given.
        """
        return enum_from_str(string=string, enum_class=__class__, replace=(" ", "_"))

    def to_str(self) -> str:
        """Convert usage type to string.

        Returns
        -------
        str
            Usage type.
        """
        return self.name[0] + self.name[1:].lower().replace("_", " ")
