from pathlib import Path

import pytest

from ansys.optislang.core import Optislang, examples
from ansys.optislang.core.project_parametric import Design, DesignParameter

pytestmark = pytest.mark.local_osl
parametric_project = examples.get_files("calculator_with_params")[1][0]
parameters_dict = {"a": 5, "b": 10}
parameters = [DesignParameter("a", 5), DesignParameter("b", 10)]


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
    assert isinstance(design.parameters["a"], DesignParameter)


def test_get_refence_design(optislang: Optislang):
    """Test ``get_refence_design``."""
    project = optislang.project
    root_system = project.root_system
    design = root_system.get_reference_design()
    optislang.dispose()
    assert isinstance(design, Design)
    assert isinstance(design.parameters["a"], DesignParameter)


def test_evaluate_design(optislang: Optislang, tmp_path: Path):
    """Test ``evaluate_design``."""
    optislang.save_copy(file_path=tmp_path / "test_modify_parameter.opf")
    optislang.reset()
    project = optislang.project
    root_system = project.root_system
    design = Design(parameters=parameters)
    assert design.status == "IDLE"
    assert design.id == "NOT_ASSIGNED"
    result = root_system.evaluate_design(design)
    optislang.dispose()
    assert isinstance(result, tuple)
    assert isinstance(result[0], dict)
    assert isinstance(result[1], dict)
    assert design.status == "SUCCEEDED"
    assert isinstance(design.responses, dict)
    assert isinstance(design.responses["c"], DesignParameter)
    assert design.responses["c"].reference_value == 15
    assert isinstance(design.criteria, dict)


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
        assert design.status == "IDLE"
        assert design.id == "NOT_ASSIGNED"
    results = root_system.evaluate_multiple_designs(designs)
    assert isinstance(results, tuple)
    optislang.dispose()
    for index, result in enumerate(results):
        assert isinstance(result, tuple)
        assert isinstance(result[0], dict)
        assert isinstance(result[1], dict)
        assert designs[index].status == "SUCCEEDED"
        assert isinstance(designs[index].responses, dict)
        assert isinstance(designs[index].responses["c"], DesignParameter)
        assert designs[index].responses["c"].reference_value == expected_results[index]
        assert isinstance(designs[index].criteria, dict)
        assert len(set(["a", "b"]) - set(designs[index].parameters)) == 0


def test_validate_design(optislang: Optislang):
    """Test ``validate_design``."""
    project = optislang.project
    root_system = project.root_system
    designs = [
        Design(parameters=parameters),
        Design(parameters={"a": 3, "b": 4}),
        Design(parameters={"a": 5, "par1": 6}),
        Design(parameters={"par1": 7, "par2": 8}),
    ]
    expected_outputs = (
        ("Valid design.", True, []),
        ("Valid design.", True, []),
        (
            "Parameters ['b'] not defined in design, values set to reference."
            "Parameters ['par1'] are not defined in project and weren't used.",
            False,
            ["b"],
        ),
        (
            "Parameters ['a', 'b'] not defined in design, values set to reference."
            "Parameters ['par1', 'par2'] are not defined in project and weren't used.",
            False,
            ["a", "b"],
        ),
    )
    for index, design in enumerate(designs):
        output = root_system.validate_design(design)
        assert isinstance(output, tuple)
        assert len(output) == 3
        assert isinstance(output[0], str)
        assert output[0] == expected_outputs[index][0]
        assert isinstance(output[1], bool)
        assert output[1] == expected_outputs[index][1]
        assert isinstance(output[2], list)
        assert output[2] == expected_outputs[index][2]
    optislang.dispose()
