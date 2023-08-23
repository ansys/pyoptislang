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


# endregion
