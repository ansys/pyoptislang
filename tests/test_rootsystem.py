from pathlib import Path

import pytest

from ansys.optislang.core import Optislang, examples
from ansys.optislang.core.project_parametric import Design, DesignStatus, DesignVariable

pytestmark = pytest.mark.local_osl
parametric_project = examples.get_files("calculator_with_params")[1][0]
parameters_dict = {"a": 5, "b": 10}
parameters = [DesignVariable("a", 5), DesignVariable("b", 10)]


@pytest.fixture()
def optislang(scope="function", autouse=False) -> Optislang:
    """Create Optislang class.

    Returns
    -------
    Optislang:
        Connects to the optiSLang application and provides an API to control it.
    """
    osl = Optislang(project_path=parametric_project)
    osl.set_timeout(20)
    return osl


@pytest.mark.parametrize("parameters", [parameters_dict, parameters])
def test_create_design(optislang: Optislang, tmp_path: Path, parameters):
    """Test ``create_design``."""
    project = optislang.project
    root_system = project.root_system
    design = root_system.create_design(parameters=parameters)
    optislang.dispose()
    assert isinstance(design, Design)
    assert isinstance(design.parameters, tuple)
    assert isinstance(design.parameters[0], DesignVariable)


def test_get_refence_design(optislang: Optislang):
    """Test ``get_refence_design``."""
    project = optislang.project
    root_system = project.root_system
    design = root_system.get_reference_design()
    optislang.dispose()
    assert isinstance(design, Design)
    assert isinstance(design.parameters, tuple)
    assert isinstance(design.parameters[0], DesignVariable)


def test_evaluate_design(optislang: Optislang, tmp_path: Path):
    """Test ``evaluate_design``."""
    optislang.save_copy(file_path=tmp_path / "test_modify_parameter.opf")
    optislang.reset()
    project = optislang.project
    root_system = project.root_system
    design = Design(parameters=parameters)
    assert design.status == DesignStatus.IDLE
    assert design.id == None
    assert design.feasibility == None
    assert isinstance(design.variables, tuple)
    result = root_system.evaluate_design(design)
    optislang.dispose()
    assert isinstance(result, Design)
    assert result.status == DesignStatus.SUCCEEDED
    assert design.status == DesignStatus.SUCCEEDED
    assert isinstance(result.responses, tuple)
    assert isinstance(design.responses, tuple)
    assert isinstance(result.responses[0], DesignVariable)
    assert isinstance(design.responses[0], DesignVariable)
    assert result.responses[0].value == 15
    assert design.responses[0].value == 15
    assert isinstance(result.constraints, tuple)
    assert isinstance(design.constraints, tuple)
    assert isinstance(result.limit_states, tuple)
    assert isinstance(design.limit_states, tuple)
    assert isinstance(result.objectives, tuple)
    assert isinstance(design.objectives, tuple)
    assert isinstance(result.variables, tuple)
    assert isinstance(design.variables, tuple)
    assert result.feasibility
    assert design.feasibility


def test_evaluate_multiple_designs(optislang: Optislang, tmp_path: Path):
    """Test ``evaluate_multiple_designs``."""
    optislang.save_copy(file_path=tmp_path / "test_modify_parameter.opf")
    optislang.reset()
    project = optislang.project
    root_system = project.root_system
    designs = [
        Design(parameters=parameters),
        Design(parameters={"a": 3, "b": 4}),
        Design(parameters={"a": 5, "par1": 6}),
        Design(parameters={"par1": 7, "par2": 8}),
    ]
    expected_results = (15, 7, 5, 1)
    for design in designs:
        assert design.status == DesignStatus.IDLE
        assert design.id == None
        assert design.feasibility == None
    results = root_system.evaluate_multiple_designs(designs)
    assert isinstance(results, tuple)
    optislang.dispose()
    for index, result in enumerate(results):
        assert isinstance(result, Design)
        assert result.status == DesignStatus.SUCCEEDED
        assert result.feasibility
        assert isinstance(result.responses, tuple)
        assert isinstance(result.responses[0], DesignVariable)
        assert result.responses[0].value == expected_results[index]
        assert isinstance(result.constraints, tuple)
        assert isinstance(result.limit_states, tuple)
        assert isinstance(result.objectives, tuple)
        assert isinstance(result.variables, tuple)
        assert len(set(["a", "b"]) - set(result.parameter_names)) == 0


def test_check_design_structure(optislang: Optislang):
    """Test ``check_design_structure``."""
    project = optislang.project
    root_system = project.root_system
    designs = [
        Design(parameters=parameters),
        Design(parameters={"a": 3, "b": 4}),
        Design(parameters={"a": 5, "par1": 6}),
        Design(parameters={"par1": 7, "par2": 8}),
    ]
    expected_outputs = (
        (tuple([]), tuple([])),
        (tuple([]), tuple([])),
        (tuple(["b"]), tuple(["par1"])),
        (tuple(["a", "b"]), tuple(["par1", "par2"])),
    )
    for index, design in enumerate(designs):
        output = root_system.check_design_structure(design)
        assert isinstance(output, tuple)
        assert len(output) == 2
        assert isinstance(output[0], tuple)
        assert isinstance(output[1], tuple)
        assert output[0] == expected_outputs[index][0]
        assert output[1] == expected_outputs[index][1]
    optislang.dispose()
