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

from pathlib import Path

import pytest

from ansys.optislang.core import Optislang
from ansys.optislang.core.tcp.project import TcpProjectProxy

pytestmark = pytest.mark.local_osl


@pytest.fixture()
def optislang(scope="function", autouse=True) -> Optislang:
    """Create Optislang class.

    Returns
    -------
    Optislang:
        Connects to the optiSLang application and provides an API to control it.
    """
    osl = Optislang(ini_timeout=60)
    osl.timeout = 20
    yield osl
    osl.dispose()


def test_application_properties(optislang: Optislang):
    """Test `root_system`, `uid` and `__str__` method."""
    application = optislang.application
    project = application.project
    assert isinstance(project, TcpProjectProxy)

    major_version, minor_version, maintenance_version, revision = application.version
    assert isinstance(major_version, int)
    assert isinstance(minor_version, int)
    assert isinstance(maintenance_version, int) or maintenance_version == None
    assert isinstance(revision, int) or revision == None

    version_str = application.version_string
    assert isinstance(version_str, str)


def test_new(optislang: Optislang, tmp_path: Path):
    "Test ``new()``."
    application = optislang.application
    application.new()
    assert application.project.get_name() == "Unnamed project"
    application.save_as(file_path=tmp_path / "newProject.opf")


@pytest.mark.parametrize("path_type", [str, Path])
def test_open(optislang: Optislang, path_type, tmp_example_project):
    "Test ``open``."
    application = optislang.application
    project = tmp_example_project("simple_calculator")
    project = path_type(project)

    application.open(file_path=project)
    project_name = application.project.get_name()
    assert project_name == "calculator"


def test_save(optislang: Optislang):
    "Test ``save()`` command."
    application = optislang.application
    project = application.project
    file_path = project.get_location()
    assert file_path.is_file()
    mod_time = file_path.stat().st_mtime
    application.save()
    save_time = file_path.stat().st_mtime
    assert mod_time != save_time


@pytest.mark.parametrize("path_type", [str, Path])
def test_save_as(optislang: Optislang, tmp_path: Path, path_type):
    "Test ``save_as() command.``"
    application = optislang.application
    file_path = tmp_path / "test_save.opf"
    if path_type == str:
        arg_path = str(file_path)
    else:
        arg_path = file_path
    old_wdir = application.project.get_working_dir()
    old_location = application.project.get_location()
    application.save_as(file_path=arg_path)

    new_wdir = application.project.get_working_dir()
    new_location = application.project.get_location()

    assert file_path.is_file()
    assert old_wdir != new_wdir
    assert old_location != new_location


@pytest.mark.parametrize("path_type", [str, Path])
def test_save_copy(optislang: Optislang, tmp_path: Path, path_type):
    "Test ``save_copy()`` command."
    application = optislang.application
    copy_path = tmp_path / "test_save_copy.opf"
    if path_type == str:
        arg_path = str(copy_path)
    else:
        arg_path = copy_path

    old_wdir = application.project.get_working_dir()
    old_location = application.project.get_location()

    application.save_copy(file_path=arg_path)

    new_wdir = application.project.get_working_dir()
    new_location = application.project.get_location()

    assert copy_path.is_file()
    assert old_wdir == new_wdir
    assert old_location == new_location


# def test_close(optislang: Optislang):
#     "Test ``close`` (close opened and create new project)."
#     application = optislang.application
#     optislang.close()
#     optislang.new()
#     optislang.dispose()
