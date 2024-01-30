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

import pytest

from ansys.optislang.core import Optislang
from ansys.optislang.core.project_parametric import MixedParameter, ObjectiveCriterion, Response

pytestmark = pytest.mark.local_osl


@pytest.fixture()
def optislang(tmp_example_project, scope="function", autouse=False) -> Optislang:
    """Create Optislang class.

    Returns
    -------
    Optislang:
        Connects to the optiSLang application and provides an API to control it.
    """
    osl = Optislang(project_path=tmp_example_project("calculator_with_params"))
    osl.timeout = 20
    return osl


def test_get_parameters(optislang: Optislang):
    """Test ``get_parameters``."""
    project = optislang.project
    root_system = project.root_system
    parameter_manager = root_system.parameter_manager
    parameters = parameter_manager.get_parameters()
    optislang.dispose()
    assert isinstance(parameters, tuple)
    assert len(parameters) > 0
    for parameter in parameters:
        assert isinstance(parameter, MixedParameter)


def test_get_parameters_names(optislang: Optislang):
    """Test ``get_parameters_names``."""
    project = optislang.project
    root_system = project.root_system
    parameter_manager = root_system.parameter_manager
    parameters_names = parameter_manager.get_parameters_names()
    optislang.dispose()
    assert isinstance(parameters_names, tuple)
    assert len(parameters_names) > 0
    assert set(["a", "b"]) == set(parameters_names)


def test_get_criteria(optislang: Optislang):
    """Test ``get_criteria``."""
    project = optislang.project
    root_system = project.root_system
    criteria_manager = root_system.criteria_manager
    criteria = criteria_manager.get_criteria()
    optislang.dispose()
    assert isinstance(criteria, tuple)
    assert len(criteria) > 0
    assert isinstance(criteria[0], ObjectiveCriterion)


def test_get_criteria_names(optislang: Optislang):
    """Test ``get_criteria_names``."""
    project = optislang.project
    root_system = project.root_system
    criteria_manager = root_system.criteria_manager
    criteria_names = criteria_manager.get_criteria_names()
    optislang.dispose()
    assert isinstance(criteria_names, tuple)
    assert len(criteria_names) > 0
    assert criteria_names[0] == "obj_c"


def test_get_responses(optislang: Optislang):
    """Test ``get_responses``."""
    project = optislang.project
    root_system = project.root_system
    response_manager = root_system.response_manager
    responses = response_manager.get_responses()
    optislang.dispose()
    assert isinstance(responses, tuple)
    assert len(responses) > 0
    for response in responses:
        assert isinstance(response, Response)


def test_get_responses_names(optislang: Optislang):
    """Test ``get_responses_names``."""
    project = optislang.project
    root_system = project.root_system
    response_manager = root_system.response_manager
    responses_names = response_manager.get_responses_names()
    optislang.dispose()
    assert isinstance(responses_names, tuple)
    assert len(responses_names) > 0
    assert set(["c", "d"]) == set(responses_names)
