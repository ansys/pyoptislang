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
from ansys.optislang.core.io import RegisteredFile
from ansys.optislang.core.nodes import RootSystem
from ansys.optislang.core.project_parametric import Design, ParameterManager

pytestmark = pytest.mark.local_osl


@pytest.fixture()
def optislang(scope="function", autouse=True) -> Optislang:
    """Create Optislang class.

    Returns
    -------
    Optislang:
        Connects to the optiSLang application and provides an API to control it.
    """
    osl = Optislang()
    osl.timeout = 20
    yield osl
    osl.dispose()


def test_project_queries(optislang: Optislang, tmp_example_project):
    """Test project queries."""
    project = optislang.project
    assert project is not None

    description = project.get_description()
    assert isinstance(description, str)

    location = project.get_location()
    assert isinstance(location, Path)

    name = project.get_name()
    assert isinstance(name, str)

    status = project.get_status()
    assert isinstance(status, str)

    optislang.open(file_path=tmp_example_project("calculator_with_params"))

    reg_files = project.get_registered_files()
    assert len(reg_files) == 3
    assert isinstance(reg_files[0], RegisteredFile)

    res_files = project.get_result_files()
    assert len(res_files) == 1
    assert isinstance(res_files[0], RegisteredFile)

    project_tree = project._get_project_tree()
    assert isinstance(project_tree, list)


def test_project_properties(optislang: Optislang):
    """Test `root_system`, `uid` and `__str__` method."""
    project = optislang.project
    assert project is not None

    uid = project.uid
    assert isinstance(uid, str)
    root_system = project.root_system
    assert isinstance(root_system, RootSystem)
    parameter_manager = project.parameter_manager
    assert isinstance(parameter_manager, ParameterManager)


def test_get_evaluate_design(optislang: Optislang):
    """Test `get_reference_design` and `evaluate_design`."""
    project = optislang.project
    assert project is not None
    ref_design = project.get_reference_design()
    assert isinstance(ref_design, Design)
    eval_design = project.evaluate_design(design=ref_design)
    assert isinstance(eval_design, Design)
