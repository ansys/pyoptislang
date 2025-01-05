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

import pytest

from ansys.optislang.core.io import File, FileOutputFormat, RegisteredFile, RegisteredFileUsage

CURRENT_FILE = __file__
NON_EXISTING_FILE = Path().cwd() / "non_existing.py"


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
