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

"""Module for input/output functionality."""
from __future__ import annotations

from abc import abstractmethod
from enum import Enum
import os
from pathlib import Path
import time
from typing import Optional, Union

from ansys.optislang.core.utils import enum_from_str


# region files
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

    def __eq__(self, other) -> bool:
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
        return (
            type(self) == type(other)
            and self.exists == other.exists
            and self.filename == other.filename
            and self.last_modified_seconds == other.last_modified_seconds
            and self.last_modified_str == other.last_modified_str
            and self.path == other.path
            and self.size == other.size
        )

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
    def last_modified_seconds(self) -> Optional[float]:
        """Last modified time as a timestamp.

        Returns
        -------
        Optional[float]
            Last modified time in seconds since the Epoch, `None` if file doesn't exist.
        """
        if self.exists:
            return self.path.stat().st_mtime
        else:
            return None

    @property
    def last_modified_str(self) -> Optional[str]:
        """Last modified time as a datetime.

        Returns
        -------
        Optional[str]
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
    def size(self) -> Optional[int]:
        """File size in bytes.

        Returns
        -------
        Optional[int]
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

    def __eq__(self, other) -> bool:
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
        return (
            type(self) == type(other)
            and self.comment == other.comment
            and self.id == other.id
            and self.tag == other.tag
            and self.usage == other.usage
            and super().__eq__(other)
        )

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

    @property
    def optislang_path(self) -> RegisteredFilePath:
        """Get optislang path object.

        Returns
        -------
        RegisteredFilePath
            Usage of registered file.
        """
        return RegisteredFilePath(name=self.id, uuid=self.tag, path=self.path)


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

    @classmethod
    def from_str(cls, string: str) -> RegisteredFileUsage:
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
        return enum_from_str(string=string, enum_class=cls, replace=(" ", "_"))

    def to_str(self) -> str:
        """Convert usage type to string.

        Returns
        -------
        str
            Usage type.
        """
        return self.name[0] + self.name[1:].lower().replace("_", " ")


# endregion


# region optislang paths
class OptislangPathType(Enum):
    """Provides optislang path types."""

    ABSOLUTE_PATH = 0
    WORKING_DIR_RELATIVE = 1
    PROJECT_RELATIVE = 2
    PROJECT_WORKING_DIR_RELATIVE = 3
    REFERENCE_FILES_DIR_RELATIVE = 4
    REGISTERED_FILE = 5

    @classmethod
    def from_str(cls, string: str) -> OptislangPathType:
        """Convert a string to an instance of the ``OptislangPathType`` class.

        Parameters
        ----------
        string: str
            String that shall be converted.

        Returns
        -------
        OptislangPathType
            Instance of the ``OptislangPathType`` class.

        Raises
        ------
        TypeError
            Raised when invalid type of ``string`` was given.
        ValueError
            Raised when invalid value of ``string`` was given.
        """
        return enum_from_str(string=string, enum_class=cls)


class OptislangPath:
    """Provides for operating on optislang paths."""

    @property
    @abstractmethod
    def type(self) -> OptislangPathType:  # pragma: no cover
        """Type of the path."""
        pass

    @abstractmethod
    def __init__(self):  # pragma: no cover
        """``OptislangPath`` class is an abstract base class and cannot be instantiated."""
        pass

    @classmethod
    def from_dict(cls, path: dict) -> OptislangPath:
        """Create an instance of the ``OptislangPath`` class from optiSLang output.

        Parameters
        ----------
        path: dict
            Output from the optiSLang server.

        Returns
        -------
        Parameter
            Instance of the ``Parameter`` class.

        Raises
        ------
        TypeError
            Raised when an unsupported path format or type is provided.
        """
        if "path" in path.keys():
            path = path["path"]
            head = path["split_path"]["head"]
            tail = path["split_path"]["tail"]
            type_ = OptislangPathType.from_str(path["base_path_mode"]["value"])
            if type_ == OptislangPathType.ABSOLUTE_PATH:
                return AbsolutePath(path=Path(tail))
            elif type_ == OptislangPathType.PROJECT_RELATIVE:
                return ProjectRelativePath(tail)
            elif type_ == OptislangPathType.PROJECT_WORKING_DIR_RELATIVE:
                return ProjectWorkingDirRelativePath(head, tail)
            elif type_ == OptislangPathType.REFERENCE_FILES_DIR_RELATIVE:
                return ReferenceFilesDirRelativePath(tail)
            elif type_ == OptislangPathType.WORKING_DIR_RELATIVE:
                return WorkingDirRelativePath(head, tail)
            else:
                raise ValueError(f"Unsupported path type: {type_}")
        elif "id" in path.keys():
            name = path["id"]["name"]
            uuid = path["id"]["uuid"]
            return RegisteredFilePath(name, uuid)
        else:
            raise ValueError(f"Unsupported path format: {path}")

    @abstractmethod
    def to_dict(self) -> dict:  # pragma: no cover
        """Abstract method implemented in derived classes."""
        pass

    @abstractmethod
    def convert_to_absolute_path(self) -> AbsolutePath:  # pragma: no cover
        """Abstract method implemented in derived classes."""
        pass


class AbsolutePath(OptislangPath):
    """Provides for operating on optislang absolute paths."""

    @property
    def type(self) -> OptislangPathType:
        """Type of the path."""
        return self.__type

    @property
    def path(self) -> Path:
        """Path to the referenced file.

        Returns
        -------
        Optional[Path]
            Path to the referenced file
        """
        return self.__path

    @path.setter
    def path(self, path: Union[str, Path]) -> None:
        """Set path to the referenced file.

        Parameters
        ----------
        path : Union[str, Path]
            Path to the referenced file.
        """
        self.__path = Path(path)

    def __init__(self, path: Union[str, Path]) -> None:
        """Create an ``AbsolutePath`` instance.

        Parameters
        ----------
        path : Union[str, Path]
            Path to the referenced file.
        """
        self.path = path
        self.__type = OptislangPathType.ABSOLUTE_PATH

    def convert_to_absolute_path(self) -> AbsolutePath:
        """Convert to `AbsolutePath` object.

        Returns
        -------
        AbsolutePath
            `AbsolutePath` instance.
        """
        return AbsolutePath(self.path)

    def convert_to_working_dir_relative(self, tail: Union[str, Path]) -> WorkingDirRelativePath:
        """Convert to `WorkingDirRelativePath` object.

        Parameters
        ----------
        tail : Union[str,Path]
            Relative part of the path.

        Returns
        -------
        WorkingDirRelativePath
            An instance of `WorkingDirRelativePath`
        """
        base = self.path
        tail = Path(tail)

        base_parts = base.parts
        suffix_parts = tail.parts

        if (
            len(suffix_parts) <= len(base_parts)
            and base_parts[-len(suffix_parts) :] == suffix_parts
        ):
            head = Path(*base_parts[: -len(suffix_parts)])
        else:
            raise ValueError(f"{tail} is not a suffix of {base}")
        return WorkingDirRelativePath(head, tail)

    def convert_to_project_dir_relative(
        self, project_dir_path: Union[str, Path]
    ) -> ProjectRelativePath:
        """Convert to `ProjectDirectoryRelativePath` object.

        Parameters
        ----------
        project_dir_path : Union[str, Path]
            Path to the project directory

        Returns
        -------
        ProjectDirectoryRelativePath
            An instance of `ProjectDirectoryRelativePath`
        """
        return ProjectRelativePath.from_file_and_project_dir_paths(self.path, project_dir_path)

    def convert_to_project_working_dir_relative(
        self, tail: Union[str, Path]
    ) -> ProjectWorkingDirRelativePath:
        """Convert to `ProjectWorkingDirRelativePath` object.

        Parameters
        ----------
        tail : Union[str,Path]
            Relative part of the path.

        Returns
        -------
        WorkingDirRelativePath
            An instance of `WorkingDirRelativePath`
        """
        base = self.path
        tail = Path(tail)

        base_parts = base.parts
        suffix_parts = tail.parts

        if (
            len(suffix_parts) <= len(base_parts)
            and base_parts[-len(suffix_parts) :] == suffix_parts
        ):
            head = Path(*base_parts[: -len(suffix_parts)])
        else:
            raise ValueError(f"{tail} is not a suffix of {base}")

        return ProjectWorkingDirRelativePath(head, tail)

    def convert_to_reference_files_dir_relative(
        self, reference_dir_path: Union[str, Path]
    ) -> ReferenceFilesDirRelativePath:
        """Convert to `ReferenceFilesDirRelativePath` object.

        Parameters
        ----------
        reference_dir_path : Union[str, Path]
            Path to the reference files directory

        Returns
        -------
        ReferenceFilesDirRelativePath
            An instance of `ReferenceFilesDirRelativePath`
        """
        return ReferenceFilesDirRelativePath.from_file_and_reference_dir_paths(
            self.path, reference_dir_path
        )

    def to_dict(self) -> dict:
        """Convert to dictionary.

        Returns
        -------
        dict
            Dictionary representation of path in optislang format.
        """
        return {
            "path": {
                "base_path_mode": {"value": self.type.name},
                "split_path": {"head": "", "tail": str(self.path)},
            }
        }


class WorkingDirRelativePath(OptislangPath):
    """Provides for operating on optislang working directory relative paths."""

    @property
    def type(self) -> OptislangPathType:
        """Type of the path."""
        return self.__type

    @property
    def path(self) -> Path:
        """Merged head and tail.

        Returns
        -------
        Optional[Path]
            Merged head and tail
        """
        return self.head / self.tail

    @property
    def head(self) -> Path:
        """Path to the file head.

        Returns
        -------
        Optional[Path]
            Path to the file head
        """
        return self.__head

    @head.setter
    def head(self, path: Union[str, Path]) -> None:
        """Set path to the file head.

        Parameters
        ----------
        path : Union[str, Path]
            Path to the file head.
        """
        self.__head = Path(path)

    @property
    def tail(self) -> Path:
        """Path to the file tail.

        Returns
        -------
        Optional[Path]
            Path to the file tail
        """
        return self.__tail

    @tail.setter
    def tail(self, path: Union[str, Path]) -> None:
        """Set path to the file tail.

        Parameters
        ----------
        path : Union[str, Path]
            Path to the file tail
        """
        self.__tail = Path(path)

    def __init__(self, head: Union[str, Path], tail: Union[str, Path]) -> None:
        """Create an ``WorkingDirRelativePath`` instance.

        Parameters
        ----------
        head : Union[str, Path]
            Initial part of the path to the file.
        tail : Union[str, Path]
            Relative part of the path to the file.
        """
        self.head = head
        self.tail = tail
        self.__type = OptislangPathType.WORKING_DIR_RELATIVE

    def to_dict(self) -> dict:
        """Convert to dictionary.

        Returns
        -------
        dict
            Dictionary representation of path in optislang format.
        """
        return {
            "path": {
                "base_path_mode": {"value": self.type.name},
                "split_path": {"head": str(self.head), "tail": str(self.tail)},
            }
        }

    def convert_to_absolute_path(self) -> AbsolutePath:
        """Convert to AbsolutePath object.

        Returns
        -------
        AbsolutePath
            AbsolutePath instance.
        """
        return AbsolutePath(self.path)


class ProjectRelativePath(OptislangPath):
    """Provides for operating on optislang project relative paths."""

    @property
    def type(self) -> OptislangPathType:
        """Type of the path."""
        return self.__type

    @property
    def file_path(self) -> Optional[Path]:
        """Path to the file.

        Returns
        -------
        Optional[Path]
            Path to the file
        """
        return self.__file_path

    @file_path.setter
    def file_path(self, path: Union[str, Path, None]) -> None:
        """Set path to the file.

        Parameters
        ----------
        path : Union[str, Path, None]
            Path to the file
        """
        self.__file_path = Path(path) if path is not None else None

    @property
    def project_dir_path(self) -> Optional[Path]:
        """Path to the project directory.

        Returns
        -------
        Optional[Path]
            Path to the project directory
        """
        return self.__project_dir_path

    @project_dir_path.setter
    def project_dir_path(self, path: Union[str, Path, None]) -> None:
        """Set path to the project directory.

        Parameters
        ----------
        path : Union[str, Path, None]
            Path to the project directory
        """
        self.__project_dir_path = Path(path) if path is not None else None

    @property
    def tail(self) -> Path:
        """Path to the file tail.

        Returns
        -------
        Path
            Path to the file tail
        """
        return self.__tail

    @tail.setter
    def tail(self, path: Union[str, Path]) -> None:
        """Set path to the file tail.

        Parameters
        ----------
        path : Union[str, Path]
            Path to the file tail
        """
        self.__tail = Path(path)

    def __init__(
        self,
        tail: Union[str, Path],
        file_path: Optional[Union[str, Path]] = None,
        project_dir_path: Optional[Union[str, Path]] = None,
    ) -> None:
        """Create an ``ProjectRelativePath`` instance.

        Parameters
        ----------
        tail : Union[str, Path]
            Relative part of the path to the file.
        project_dir_path : Optional[Union[str, Path]]
            Path to the project directory.
        """
        self.tail = tail
        self.file_path = file_path
        self.project_dir_path = project_dir_path
        self.__type = OptislangPathType.PROJECT_RELATIVE

    def to_dict(self) -> dict:
        """Convert to dictionary.

        Returns
        -------
        dict
            Dictionary representation of path in optislang format.
        """
        return {
            "path": {
                "base_path_mode": {"value": self.type.name},
                "split_path": {"head": "", "tail": str(self.tail)},
            }
        }

    def convert_to_absolute_path(self) -> AbsolutePath:
        """Convert to AbsolutePath object.

        Returns
        -------
        AbsolutePath
            AbsolutePath instance.

        Raises
        ------
        ValueError
            Raised if file path is not specified.
        """
        if not self.file_path:
            raise ValueError(
                "Cannot be converted to `AbsolutePath` object, "
                f"file_path is not defined: {self.file_path}`"
            )
        return AbsolutePath(self.file_path)

    @staticmethod
    def from_file_and_project_dir_paths(
        file_path: Union[str, Path], project_dir: Union[str, Path]
    ) -> ProjectRelativePath:
        """Create an ``ProjectRelativePath`` instance.

        Parameters
        ----------
        file_path : Union[str, Path]
            Path to the referenced file.
        project_dir : Union[str, Path]
            Path to the project directory.

        Returns
        -------
        ProjectRelativePath
            Instance of the project relative path
        """
        file_path = Path(file_path)
        project_dir = Path(project_dir)
        head = ""
        try:
            common_path = Path(os.path.commonpath([file_path, project_dir]))
            relative_count = len(project_dir.parts) - len(common_path.parts)
            relative_symbols = [relative_count * "../"]
            relative_path = file_path.relative_to(common_path)
            composed_relative_path = Path(*relative_symbols[0:]) / relative_path
        except Exception:
            composed_relative_path = file_path
        return ProjectRelativePath(composed_relative_path, file_path, project_dir)


class ProjectWorkingDirRelativePath(OptislangPath):
    """Provides for operating on optislang project working directory relative paths."""

    @property
    def type(self) -> OptislangPathType:
        """Type of the path."""
        return self.__type

    @property
    def path(self) -> Path:
        """Merged head and tail.

        Returns
        -------
        Optional[Path]
            Merged head and tail
        """
        return self.head / self.tail

    @property
    def head(self) -> Path:
        """Path to the file head.

        Returns
        -------
        Optional[Path]
            Path to the file head
        """
        return self.__head

    @head.setter
    def head(self, path: Union[str, Path]) -> None:
        """Set path to the file head.

        Parameters
        ----------
        path : Union[str, Path]
            Path to the file head.
        """
        self.__head = Path(path)

    @property
    def tail(self) -> Path:
        """Path to the file tail.

        Returns
        -------
        Optional[Path]
            Path to the file tail
        """
        return self.__tail

    @tail.setter
    def tail(self, path: Union[str, Path]) -> None:
        """Set path to the file tail.

        Parameters
        ----------
        path : Union[str, Path]
            Path to the file tail
        """
        self.__tail = Path(path)

    def __init__(self, head: Union[str, Path], tail: Union[str, Path]) -> None:
        """Create an ``ProjectWorkingDirRelativePath`` instance.

        Parameters
        ----------
        head : Union[str, Path]
            Initial part of the path to the file.
        tail : Union[str, Path]
            Relative part of the path to the file.
        """
        self.head = head
        self.tail = tail
        self.__type = OptislangPathType.PROJECT_WORKING_DIR_RELATIVE

    def to_dict(self) -> dict:
        """Convert to dictionary.

        Returns
        -------
        dict
            Dictionary representation of path in optislang format.
        """
        return {
            "path": {
                "base_path_mode": {"value": self.type.name},
                "split_path": {"head": str(self.head), "tail": str(self.tail)},
            }
        }

    def convert_to_absolute_path(self) -> AbsolutePath:
        """Convert to AbsolutePath object.

        Returns
        -------
        AbsolutePath
            AbsolutePath instance.
        """
        return AbsolutePath(self.path)


class ReferenceFilesDirRelativePath(OptislangPath):
    """Provides for operating on optislang reference files directory relative paths."""

    @property
    def type(self) -> OptislangPathType:
        """Type of the path."""
        return self.__type

    @property
    def file_path(self) -> Optional[Path]:
        """Path to the file.

        Returns
        -------
        Optional[Path]
            Path to the file
        """
        return self.__file_path

    @file_path.setter
    def file_path(self, path: Union[str, Path, None]) -> None:
        """Set path to the file.

        Parameters
        ----------
        path : Union[str, Path, None]
            Path to the file
        """
        self.__file_path = Path(path) if path else None

    @property
    def reference_dir_path(self) -> Optional[Path]:
        """Path to the reference directory.

        Returns
        -------
        Optional[Path]
            Path to the reference directory
        """
        return self.__reference_dir_path

    @reference_dir_path.setter
    def reference_dir_path(self, path: Union[str, Path, None]) -> None:
        """Set path to the reference directory.

        Parameters
        ----------
        path : Union[str, Path, None]
            Path to the reference directory
        """
        self.__reference_dir_path = Path(path) if path else None

    @property
    def tail(self) -> Path:
        """Path to the file tail.

        Returns
        -------
        Optional[Path]
            Path to the file tail
        """
        return self.__tail

    @tail.setter
    def tail(self, path: Union[str, Path]) -> None:
        """Set path to the file tail.

        Parameters
        ----------
        path : Union[str, Path]
            Path to the file tail
        """
        self.__tail = Path(path)

    def __init__(
        self,
        tail: Union[str, Path],
        file_path: Optional[Union[str, Path]] = None,
        reference_dir_path: Optional[Union[str, Path]] = None,
    ) -> None:
        """Create an ``ProjectRelativePath`` instance.

        Parameters
        ----------
        tail : Union[str, Path]
            Relative part of the path to the file.
        file_path : Optional[Union[str, Path]]
            Path to the referenced file.
        reference_dir_path : Optional[Union[str, Path]]
            Path to the reference directory.
        """
        self.tail = tail
        self.file_path = file_path
        self.reference_dir_path = reference_dir_path
        self.__type = OptislangPathType.REFERENCE_FILES_DIR_RELATIVE

    def to_dict(self) -> dict:
        """Convert to dictionary.

        Returns
        -------
        dict
            Dictionary representation of path in optislang format.
        """
        return {
            "path": {
                "base_path_mode": {"value": self.type.name},
                "split_path": {"head": "", "tail": str(self.tail)},
            }
        }

    def convert_to_absolute_path(self) -> AbsolutePath:
        """Convert to AbsolutePath object.

        Returns
        -------
        AbsolutePath
            AbsolutePath instance.

        Raises
        ------
        ValueError
            Raised if file path is not specified.
        """
        if not self.file_path:
            raise ValueError(
                "Cannot be converted to `AbsolutePath` object, "
                f"file_path is not defined: {self.file_path}`"
            )
        return AbsolutePath(self.file_path)

    @staticmethod
    def from_file_and_reference_dir_paths(
        file_path: Union[str, Path], reference_dir: Union[str, Path]
    ) -> ReferenceFilesDirRelativePath:
        """Create an ``ReferenceFilesDirRelativePath`` instance.

        Parameters
        ----------
        file_path : Union[str, Path]
            Path to the referenced file.
        reference_dir : Union[str, Path]
            Path to the reference directory.

        Returns
        -------
        ReferenceFilesDirRelativePath
            Instance of the reference files directory relative path
        """
        file_path = Path(file_path)
        reference_dir = Path(reference_dir)
        head = ""
        try:
            common_path = Path(os.path.commonpath([file_path, reference_dir]))
            relative_count = len(reference_dir.parts) - len(common_path.parts)
            relative_symbols = [relative_count * "../"]
            relative_path = file_path.relative_to(common_path)
            composed_relative_path = Path(*relative_symbols[0:]) / relative_path
        except Exception:
            composed_relative_path = file_path
        return ReferenceFilesDirRelativePath(composed_relative_path, file_path, reference_dir)


class RegisteredFilePath(OptislangPath):
    """Provides for operating on optislang registered files paths."""

    @property
    def type(self) -> OptislangPathType:
        """Type of the path."""
        return self.__type

    @property
    def name(self) -> str:
        """Registered file name.

        Returns
        -------
        str
            Registered file name.
        """
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        """Set registered file name.

        Parameters
        ----------
        name: str
            Registered file name.
        """
        self.__name = name

    @property
    def uuid(self) -> str:
        """Registered file uid.

        Returns
        -------
        str
            Registered file uid.
        """
        return self.__uuid

    @uuid.setter
    def uuid(self, uuid: str) -> None:
        """Set registered file uuid.

        Parameters
        ----------
        uuid : str
            Registered file uuid.
        """
        self.__uuid = uuid

    @property
    def path(self) -> Optional[Path]:
        """Path to the registered file.

        Returns
        -------
        Optional[Path]
            Path to the registered file, if defined
        """
        return self.__path

    @path.setter
    def path(self, path: Union[str, Path, None]) -> None:
        """Set path to the registered file.

        Parameters
        ----------
        path : Union[str, Path, None]
            Path to the registered file.
        """
        self.__path = Path(path) if path else None

    def __init__(self, name: str, uuid: str, path: Optional[Union[str, Path]] = None) -> None:
        """Create a ``RegisteredFilePath`` instance.

        Parameters
        ----------
        name : str
            Registered file name.
        uuid : str
            Registered file uuid.
        path: Optional[Union[str, Path]], optional
            Absolute path to the registered file.
        """
        self.name = name
        self.uuid = uuid
        self.path = path
        self.__type = OptislangPathType.REGISTERED_FILE

    def convert_to_absolute_path(self) -> AbsolutePath:
        """Convert to AbsolutePath object.

        Returns
        -------
        AbsolutePath
            AbsolutePath instance.

        Raises
        ------
        ValueError
            Raised if registered file path is not specified.
        """
        if not self.path:
            raise ValueError(
                f"Cannot be converted to `AbsolutePath` object, path is not defined: {self.path}`"
            )
        return AbsolutePath(self.path)

    def to_dict(self) -> dict:
        """Convert to dictionary.

        Returns
        -------
        dict
            Dictionary representation of path in optislang format.
        """
        return {"id": {"name": self.name, "uuid": self.uuid}}


# endregion
