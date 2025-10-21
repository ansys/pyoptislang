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

from __future__ import annotations

from enum import Enum
from pathlib import Path
import sys

import pytest

from ansys.optislang.core.io import (
    AbsolutePath,
    File,
    FileOutputFormat,
    OptislangPath,
    OptislangPathType,
    ProjectRelativePath,
    ProjectWorkingDirRelativePath,
    ReferenceFilesDirRelativePath,
    RegisteredFile,
    RegisteredFilePath,
    RegisteredFileUsage,
    WorkingDirRelativePath,
)

CURRENT_FILE = __file__
NON_EXISTING_FILE = Path().cwd() / "non_existing.py"


ABSOLUTE_FILE_PATH1 = (
    Path(r"C:\Users\User\Optislang\Optimization\textfile.txt")
    if sys.platform == "win32"
    else Path("home/user/Optislang/Optimization/textfile.txt")
)
ABSOLUTE_FILE_PATH2 = (
    Path(r"C:\Users\User\Optislang\OtherFolder\textfile.txt")
    if sys.platform == "win32"
    else Path("home/user/Optislang/OtherFolder/textfile.txt")
)
ABSOLUTE_FILE_PATH3 = (
    Path(r"C:\Users\User\AnotherFolder\OtherFolder\textfile.txt")
    if sys.platform == "win32"
    else Path("home/user/AnotherFolder/OtherFolder/textfile.txt")
)
ABSOLUTE_FILE_PATH4 = Path(r"D:\Another\Drive\textfile.txt")
ABSOLUTE_FILE_PATH5 = (
    Path(r"C:\Users\User\Optislang\Optimization\project.opd\file1.txt")
    if sys.platform == "win32"
    else Path("home/user/Optislang/Optimization/project.opd/file1.txt")
)
ABSOLUTE_FILE_PATH6 = (
    Path(r"C:\Users\User\Optislang\Optimization\project.opd\subfolder\file1.txt")
    if sys.platform == "win32"
    else Path("home/user/Optislang/Optimization/project.opd/subfolder/file1.txt")
)
HEAD = (
    Path(r"C:\Users\User\Optislang\Optimization")
    if sys.platform == "win32"
    else Path("home/user/Optislang/Optimization")
)
TAIL = Path(r"subfolder\file1.txt") if sys.platform == "win32" else Path(r"subfolder/file1.txt")

PROJECT_DIR = (
    Path(r"C:\Users\User\Optislang\Optimization")
    if sys.platform == "win32"
    else Path("home/user/Optislang/Optimization")
)
PROJECT_WORKING_DIR = (
    Path(r"C:\Users\User\Optislang\Optimization\project.opd")
    if sys.platform == "win32"
    else Path("home/user/Optislang/Optimization/project.opd")
)
REFERENCE_FILES_DIR = (
    Path(r"C:\Users\User\Optislang\Optimization\project.opr")
    if sys.platform == "win32"
    else Path("home/user/Optislang/Optimization/project.opr")
)


ABSOLUTE_PATH_DICT = {
    "path": {
        "base_path_mode": {"enum": [], "value": "ABSOLUTE_PATH"},
        "split_path": {
            "head": "",
            "tail": (
                "C:/Users/User/Optislang/Optimization/project.opd/file1.txt"
                if sys.platform == "win32"
                else "home/user/Optislang/Optimization/project.opd/file1.txt"
            ),
        },
    }
}
WDIR_RELATIVE_DICT = {
    "path": {
        "base_path_mode": {"enum": [], "value": "WORKING_DIR_RELATIVE"},
        "split_path": {
            "head": (
                "C:/Users/User/Optislang/Optimization/project.opd"
                if sys.platform == "win32"
                else "home/user/Optislang/Optimization/project.opd"
            ),
            "tail": "file1.txt",
        },
    }
}
P_RELATIVE_DICT = {
    "path": {
        "base_path_mode": {"enum": [], "value": "PROJECT_RELATIVE"},
        "split_path": {"head": "", "tail": "./project.opd/file1.txt"},
    }
}
PWDIR_RELATIVE_DICT = {
    "path": {
        "base_path_mode": {"enum": [], "value": "PROJECT_WORKING_DIR_RELATIVE"},
        "split_path": {
            "head": (
                "C:/Users/User/Optislang/Optimization/project.opd"
                if sys.platform == "win32"
                else "home/user/Optislang/Optimization/project.opd"
            ),
            "tail": "file1.txt",
        },
    }
}
REFFILES_RELATIVE_DICT = {
    "path": {
        "base_path_mode": {"enum": [], "value": "REFERENCE_FILES_DIR_RELATIVE"},
        "split_path": {"head": "", "tail": "../project.opd/file1.txt"},
    }
}
REGFILE_DICT = {"id": {"name": "temp1", "uuid": "b0b7a9f0-a683-478b-a205-69f3d13c2fc4"}}


# region TEST ENUMERATION METHODS:
def enumeration_test_method(enumeration_class: Enum, enumeration_name: str):
    """Test instance creation, method `from_str` and spelling."""
    mixed_name = ""
    for index, char in enumerate(enumeration_name):
        if index % 2 == 1:
            mixed_name += char.lower()
        else:
            mixed_name += char
    try:
        enumeration_from_str = enumeration_class.from_str(string=mixed_name)
    except:
        assert False
    assert isinstance(enumeration_from_str, enumeration_class)
    assert isinstance(enumeration_from_str.name, str)
    assert enumeration_from_str.name == enumeration_name


@pytest.mark.parametrize(
    "file_output_format, name",
    [
        (FileOutputFormat, "CSV"),
        (FileOutputFormat, "JSON"),
    ],
)
def test_file_output_format(file_output_format: FileOutputFormat, name: str):
    """Test `FileOutputFormat`."""
    enumeration_test_method(enumeration_class=file_output_format, enumeration_name=name)


@pytest.mark.parametrize(
    "registered_file_usage, name",
    [
        (RegisteredFileUsage, "INPUT_FILE"),
        (RegisteredFileUsage, "INTERMEDIATE_RESULT"),
        (RegisteredFileUsage, "OUTPUT_FILE"),
        (RegisteredFileUsage, "UNDETERMINED"),
    ],
)
def test_file_output_format(registered_file_usage: RegisteredFileUsage, name: str):
    """Test `RegisteredFileUsage`."""
    enumeration_test_method(enumeration_class=registered_file_usage, enumeration_name=name)


@pytest.mark.parametrize(
    "optislang_path_type, name",
    [
        (OptislangPathType, "ABSOLUTE_PATH"),
        (OptislangPathType, "WORKING_DIR_RELATIVE"),
        (OptislangPathType, "PROJECT_RELATIVE"),
        (OptislangPathType, "PROJECT_WORKING_DIR_RELATIVE"),
        (OptislangPathType, "REFERENCE_FILES_DIR_RELATIVE"),
        (OptislangPathType, "REGISTERED_FILE"),
    ],
)
def test_optislang_path_type(optislang_path_type: OptislangPathType, name: str):
    """Test `OptislangPathType`."""
    enumeration_test_method(enumeration_class=optislang_path_type, enumeration_name=name)


# endregion


# region TEST FILE CLASSES
def test_file():
    """Test ``File`` class."""
    existing_file = File(CURRENT_FILE)
    non_existing_file = File(NON_EXISTING_FILE)

    assert isinstance(existing_file.exists, bool)
    assert isinstance(non_existing_file.exists, bool)
    assert existing_file.exists
    assert not non_existing_file.exists

    assert isinstance(existing_file.filename, str)
    assert existing_file.filename == "test_io.py"
    assert non_existing_file.filename == "non_existing.py"

    assert isinstance(existing_file.last_modified_seconds, float)
    assert non_existing_file.last_modified_seconds == None
    assert isinstance(existing_file.last_modified_str, str)
    assert non_existing_file.last_modified_str == None
    assert isinstance(existing_file.path, Path)
    assert isinstance(non_existing_file.path, Path)
    assert isinstance(existing_file.size, int)
    assert non_existing_file.size == None

    assert existing_file == existing_file
    assert not existing_file == non_existing_file


def test_registered_file():
    """Test ``RegisteredFile`` class."""
    registered_file = RegisteredFile(
        CURRENT_FILE, "python_module", "comment", "xxxx-test-uid", RegisteredFileUsage.UNDETERMINED
    )
    non_existing_registered_file = RegisteredFile(
        "xxx", "python_module", "comment", "xxxx-test-uid", RegisteredFileUsage.UNDETERMINED
    )

    assert isinstance(registered_file.comment, str)
    assert isinstance(registered_file.id, str)
    assert isinstance(registered_file.tag, str)
    assert isinstance(registered_file.usage, RegisteredFileUsage)
    assert isinstance(registered_file.path, Path)
    assert isinstance(registered_file.optislang_path, RegisteredFilePath)
    assert not registered_file == non_existing_registered_file


def test_file_equality():
    file_1 = File(CURRENT_FILE)
    file_2 = File(NON_EXISTING_FILE)

    assert file_1 == file_1
    assert file_1 != file_2

    reg_file_1 = RegisteredFile(
        CURRENT_FILE, "id1", "comment", "uid1", RegisteredFileUsage.UNDETERMINED
    )

    reg_file_2 = RegisteredFile(
        CURRENT_FILE, "id2", "comment", "uid2", RegisteredFileUsage.UNDETERMINED
    )

    assert reg_file_1 == reg_file_1
    assert reg_file_1 != reg_file_2

    assert file_1 != reg_file_1
    assert reg_file_1 != file_1

    reg_file_3 = RegisteredFile(
        NON_EXISTING_FILE, "id3", "comment", "uid3", RegisteredFileUsage.UNDETERMINED
    )

    assert file_1 != reg_file_3
    assert reg_file_3 != file_1


# endregion

# region TEST OPTISLANG PATHS


@pytest.mark.parametrize(
    "path",
    [
        ABSOLUTE_FILE_PATH1,
        str(ABSOLUTE_FILE_PATH1),
    ],
)
def test_absolute_path(path: str | Path):
    """Test ``AbsolutePath`` class."""
    path_instance = AbsolutePath(path)
    assert path_instance.type == OptislangPathType.ABSOLUTE_PATH
    assert isinstance(path_instance.path, Path)

    path_instance.path = path
    assert isinstance(path_instance.path, Path)

    path_dict = path_instance.to_dict()
    assert isinstance(path_dict, dict)
    assert path_dict["path"]
    assert path_dict["path"]["base_path_mode"]["value"] == "ABSOLUTE_PATH"
    assert path_dict["path"]["split_path"]["head"] == ""
    assert path_dict["path"]["split_path"]["tail"] == str(path)


def test_absolute_path_2_to_absolute():
    """Test conversion of `AbsolutePath` to working directory relative."""
    absolute_path = AbsolutePath(ABSOLUTE_FILE_PATH1)
    converted = absolute_path.convert_to_absolute_path()
    assert isinstance(converted, AbsolutePath)
    assert converted.path == ABSOLUTE_FILE_PATH1


@pytest.mark.parametrize(
    "path, tail",
    [
        (ABSOLUTE_FILE_PATH5, Path(r"file1.txt")),
        (ABSOLUTE_FILE_PATH6, Path(r"subfolder/file1.txt")),
    ],
)
def test_absolute_path_2_to_wdir_relative(path, tail):
    """Test conversion of `AbsolutePath` to working directory relative."""
    absolute_path = AbsolutePath(path)
    wdir_relative = absolute_path.convert_to_working_dir_relative(tail)

    assert isinstance(wdir_relative, WorkingDirRelativePath)
    assert wdir_relative.head == PROJECT_WORKING_DIR
    assert wdir_relative.tail == tail
    assert wdir_relative.path == path
    abs_from_wdir = wdir_relative.convert_to_absolute_path()
    assert abs_from_wdir.path == path


@pytest.mark.parametrize(
    "path, expected",
    [
        (ABSOLUTE_FILE_PATH1, Path(r"./textfile.txt")),
        (ABSOLUTE_FILE_PATH2, Path(r"../OtherFolder/textfile.txt")),
        (ABSOLUTE_FILE_PATH3, Path(r"../../AnotherFolder/OtherFolder/textfile.txt")),
        pytest.param(
            ABSOLUTE_FILE_PATH4,
            ABSOLUTE_FILE_PATH4,
            marks=pytest.mark.skipif(
                sys.platform.startswith("linux"), reason="Not supported on Linux"
            ),
        ),
    ],
)
def test_absolute_path_2_to_project_relative(path, expected):
    """Test conversion of `AbsolutePath` to working directory relative."""
    absolute_path = AbsolutePath(path)
    project_relative = absolute_path.convert_to_project_dir_relative(PROJECT_DIR)

    assert isinstance(project_relative, ProjectRelativePath)
    assert project_relative.tail == expected
    assert project_relative.file_path == path
    assert project_relative.project_dir_path == PROJECT_DIR

    abs_from_pdir_rel = project_relative.convert_to_absolute_path()
    assert abs_from_pdir_rel.path == path
    assert isinstance(abs_from_pdir_rel, AbsolutePath)


@pytest.mark.parametrize(
    "path, tail",
    [
        (ABSOLUTE_FILE_PATH5, Path(r"file1.txt")),
        (ABSOLUTE_FILE_PATH6, Path(r"subfolder/file1.txt")),
    ],
)
def test_absolute_path_2_to_project_wdir_relative(path, tail):
    """Test conversion of `AbsolutePath` to project working directory relative."""
    absolute_path = AbsolutePath(path)
    project_wdir_relative = absolute_path.convert_to_project_working_dir_relative(tail)

    assert isinstance(project_wdir_relative, ProjectWorkingDirRelativePath)
    assert project_wdir_relative.head == PROJECT_WORKING_DIR
    assert project_wdir_relative.tail == tail
    assert project_wdir_relative.path == path
    abs_from_wdir = project_wdir_relative.convert_to_absolute_path()
    assert abs_from_wdir.path == path


@pytest.mark.parametrize(
    "path, expected",
    [
        (ABSOLUTE_FILE_PATH1, Path(r"../textfile.txt")),
        (ABSOLUTE_FILE_PATH2, Path(r"../../OtherFolder/textfile.txt")),
        (ABSOLUTE_FILE_PATH3, Path(r"../../..\AnotherFolder/OtherFolder/textfile.txt")),
        pytest.param(
            ABSOLUTE_FILE_PATH4,
            ABSOLUTE_FILE_PATH4,
            marks=pytest.mark.skipif(
                sys.platform.startswith("linux"), reason="Not supported on Linux"
            ),
        ),
    ],
)
def test_absolute_path_2_to_reffiles_relative(path, expected):
    """Test conversion of `AbsolutePath` to working directory relative."""
    absolute_path = AbsolutePath(path)
    project_relative = absolute_path.convert_to_reference_files_dir_relative(REFERENCE_FILES_DIR)

    assert isinstance(project_relative, ReferenceFilesDirRelativePath)
    assert project_relative.tail == expected
    assert project_relative.file_path == path
    assert project_relative.reference_dir_path == REFERENCE_FILES_DIR

    abs_from_pdir_rel = project_relative.convert_to_absolute_path()
    assert abs_from_pdir_rel.path == path
    assert isinstance(abs_from_pdir_rel, AbsolutePath)


@pytest.mark.parametrize(
    "head, tail",
    [(HEAD, TAIL), (str(HEAD), str(TAIL)), (HEAD, str(TAIL)), (str(HEAD), TAIL)],
)
def test_working_dir_relative_path(head: str | Path, tail: str | Path):
    """Test ``WorkingDirRelativePath`` class."""
    path_instance = WorkingDirRelativePath(head, tail)
    assert path_instance.type == OptislangPathType.WORKING_DIR_RELATIVE
    assert isinstance(path_instance.head, Path)
    assert isinstance(path_instance.tail, Path)

    assert path_instance.head == HEAD
    assert path_instance.tail == TAIL

    path_dict = path_instance.to_dict()
    assert isinstance(path_dict, dict)
    assert path_dict["path"]
    assert path_dict["path"]["base_path_mode"]["value"] == "WORKING_DIR_RELATIVE"
    assert path_dict["path"]["split_path"]["head"] == str(head)
    assert path_dict["path"]["split_path"]["tail"] == str(tail)


@pytest.mark.parametrize(
    "head, tail",
    [(HEAD, TAIL), (str(HEAD), str(TAIL)), (HEAD, str(TAIL)), (str(HEAD), TAIL)],
)
def test_project_working_dir_relative_path(head: str | Path, tail: str | Path):
    """Test ``ProjectWorkingDirRelativePath`` class."""
    path_instance = ProjectWorkingDirRelativePath(head, tail)
    assert path_instance.type == OptislangPathType.PROJECT_WORKING_DIR_RELATIVE
    assert isinstance(path_instance.head, Path)
    assert isinstance(path_instance.tail, Path)

    assert path_instance.head == HEAD
    assert path_instance.tail == TAIL

    path_dict = path_instance.to_dict()
    assert isinstance(path_dict, dict)
    assert path_dict["path"]
    assert path_dict["path"]["base_path_mode"]["value"] == "PROJECT_WORKING_DIR_RELATIVE"
    assert path_dict["path"]["split_path"]["head"] == str(head)
    assert path_dict["path"]["split_path"]["tail"] == str(tail)


@pytest.mark.parametrize(
    "tail, file_path",
    [(Path(r"./textfile.txt"), ABSOLUTE_FILE_PATH1), (r"./textfile.txt", str(ABSOLUTE_FILE_PATH1))],
)
def test_project_dir_relative_path(tail: str | Path, file_path: str | Path):
    """Test ``ProjectRelativePath`` class."""
    path_instance_full = ProjectRelativePath(tail, file_path, PROJECT_DIR)
    assert path_instance_full.type == OptislangPathType.PROJECT_RELATIVE

    assert isinstance(path_instance_full.project_dir_path, Path)
    assert isinstance(path_instance_full.file_path, Path)
    assert isinstance(path_instance_full.tail, Path)

    assert path_instance_full.file_path == Path(file_path)
    assert path_instance_full.project_dir_path == PROJECT_DIR
    assert path_instance_full.tail == Path(tail)

    path_dict = path_instance_full.to_dict()
    assert isinstance(path_dict, dict)
    assert path_dict["path"]
    assert path_dict["path"]["base_path_mode"]["value"] == "PROJECT_RELATIVE"
    assert path_dict["path"]["split_path"]["head"] == ""
    assert path_dict["path"]["split_path"]["tail"] == str(Path(tail))

    path_instance_base = ProjectRelativePath(tail)
    assert isinstance(path_instance_base.tail, Path)
    assert path_instance_base.tail == Path(tail)

    base_dict = path_instance_base.to_dict()
    assert isinstance(path_dict, dict)
    assert base_dict["path"]
    assert base_dict["path"]["base_path_mode"]["value"] == "PROJECT_RELATIVE"
    assert base_dict["path"]["split_path"]["head"] == ""
    assert base_dict["path"]["split_path"]["tail"] == str(Path(tail))

    class_method_instance = ProjectRelativePath.from_file_and_project_dir_paths(
        file_path, PROJECT_DIR
    )
    assert class_method_instance.type == OptislangPathType.PROJECT_RELATIVE

    assert isinstance(class_method_instance.project_dir_path, Path)
    assert isinstance(class_method_instance.file_path, Path)
    assert isinstance(class_method_instance.tail, Path)

    assert class_method_instance.file_path == Path(file_path)
    assert class_method_instance.project_dir_path == PROJECT_DIR
    assert class_method_instance.tail == Path(tail)

    cls_method_dict = class_method_instance.to_dict()
    assert isinstance(path_dict, dict)
    assert cls_method_dict["path"]
    assert cls_method_dict["path"]["base_path_mode"]["value"] == "PROJECT_RELATIVE"
    assert cls_method_dict["path"]["split_path"]["head"] == ""
    assert cls_method_dict["path"]["split_path"]["tail"] == str(Path(tail))


@pytest.mark.parametrize(
    "tail, file_path",
    [
        (Path(r"../textfile.txt"), ABSOLUTE_FILE_PATH1),
        (r"../textfile.txt", str(ABSOLUTE_FILE_PATH1)),
    ],
)
def test_reference_files_dir_relative_path(tail: str | Path, file_path: str | Path):
    """Test ``ReferenceFilesDirRelativePath`` class."""
    path_instance_full = ReferenceFilesDirRelativePath(tail, file_path, REFERENCE_FILES_DIR)
    assert path_instance_full.type == OptislangPathType.REFERENCE_FILES_DIR_RELATIVE

    assert isinstance(path_instance_full.reference_dir_path, Path)
    assert isinstance(path_instance_full.file_path, Path)
    assert isinstance(path_instance_full.tail, Path)

    assert path_instance_full.file_path == Path(file_path)
    assert path_instance_full.reference_dir_path == REFERENCE_FILES_DIR
    assert path_instance_full.tail == Path(tail)

    path_dict = path_instance_full.to_dict()
    assert isinstance(path_dict, dict)
    assert path_dict["path"]
    assert path_dict["path"]["base_path_mode"]["value"] == "REFERENCE_FILES_DIR_RELATIVE"
    assert path_dict["path"]["split_path"]["head"] == ""
    assert path_dict["path"]["split_path"]["tail"] == str(Path(tail))

    path_instance_base = ReferenceFilesDirRelativePath(tail)
    assert isinstance(path_instance_base.tail, Path)
    assert path_instance_base.tail == Path(tail)

    base_dict = path_instance_base.to_dict()
    assert isinstance(path_dict, dict)
    assert base_dict["path"]
    assert base_dict["path"]["base_path_mode"]["value"] == "REFERENCE_FILES_DIR_RELATIVE"
    assert base_dict["path"]["split_path"]["head"] == ""
    assert base_dict["path"]["split_path"]["tail"] == str(Path(tail))

    class_method_instance = ReferenceFilesDirRelativePath.from_file_and_reference_dir_paths(
        file_path, REFERENCE_FILES_DIR
    )
    assert class_method_instance.type == OptislangPathType.REFERENCE_FILES_DIR_RELATIVE

    assert isinstance(class_method_instance.reference_dir_path, Path)
    assert isinstance(class_method_instance.file_path, Path)
    assert isinstance(class_method_instance.tail, Path)

    assert class_method_instance.file_path == Path(file_path)
    assert class_method_instance.reference_dir_path == REFERENCE_FILES_DIR
    assert class_method_instance.tail == Path(tail)

    cls_method_dict = class_method_instance.to_dict()
    assert isinstance(path_dict, dict)
    assert cls_method_dict["path"]
    assert cls_method_dict["path"]["base_path_mode"]["value"] == "REFERENCE_FILES_DIR_RELATIVE"
    assert cls_method_dict["path"]["split_path"]["head"] == ""
    assert cls_method_dict["path"]["split_path"]["tail"] == str(Path(tail))


@pytest.mark.parametrize(
    "path",
    [
        ABSOLUTE_FILE_PATH1,
        str(ABSOLUTE_FILE_PATH1),
    ],
)
def test_registered_file_path(path: str | Path):
    """Test ``RegisteredFilePath`` class."""
    regfile = RegisteredFile(
        path, "python_module", "", "xxxx-test-uid", RegisteredFileUsage.UNDETERMINED
    )
    path_from_file = regfile.optislang_path

    path_instance = RegisteredFilePath("python_module", "xxxx-test-uid", path)
    assert path_instance.type == OptislangPathType.REGISTERED_FILE
    assert isinstance(path_instance.path, Path)
    assert isinstance(path_instance.name, str)
    assert isinstance(path_instance.uuid, str)
    assert path_instance.path == path_from_file.path
    assert path_instance.name == path_from_file.name
    assert path_instance.uuid == path_from_file.uuid

    absolute_path = path_instance.convert_to_absolute_path()
    assert isinstance(absolute_path, AbsolutePath)
    assert absolute_path.path == Path(path)

    path_instance_base = RegisteredFilePath("python_module", "xxxx-test-uid")
    assert isinstance(path_instance_base.name, str)
    assert isinstance(path_instance_base.uuid, str)
    assert path_instance_base.name == path_from_file.name
    assert path_instance_base.uuid == path_from_file.uuid

    path_dict = path_instance.to_dict()
    assert isinstance(path_dict, dict)
    assert path_dict["id"]
    assert path_dict["id"]["name"] == "python_module"
    assert path_dict["id"]["uuid"] == "xxxx-test-uid"


def test_from_dict_methods():
    """Test ``OptislangPath.from_dict()`` method."""
    abs = OptislangPath.from_dict(ABSOLUTE_PATH_DICT)
    assert isinstance(abs, AbsolutePath)
    assert abs.path == ABSOLUTE_FILE_PATH5

    wdir = OptislangPath.from_dict(WDIR_RELATIVE_DICT)
    assert isinstance(wdir, WorkingDirRelativePath)
    assert wdir.path == ABSOLUTE_FILE_PATH5

    prel = OptislangPath.from_dict(P_RELATIVE_DICT)
    assert isinstance(prel, ProjectRelativePath)
    assert prel.tail == Path("./project.opd/file1.txt")

    pwdir = OptislangPath.from_dict(PWDIR_RELATIVE_DICT)
    assert isinstance(pwdir, ProjectWorkingDirRelativePath)
    assert pwdir.path == ABSOLUTE_FILE_PATH5

    reffiles = OptislangPath.from_dict(REFFILES_RELATIVE_DICT)
    assert isinstance(reffiles, ReferenceFilesDirRelativePath)
    assert reffiles.tail == Path("../project.opd/file1.txt")

    regfile = OptislangPath.from_dict(REGFILE_DICT)
    assert isinstance(regfile, RegisteredFilePath)
    assert regfile.name == "temp1"
    assert regfile.uuid == "b0b7a9f0-a683-478b-a205-69f3d13c2fc4"


# endregion
