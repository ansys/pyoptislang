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
    osl.timeout = 20
    return osl


def test_delete(optislang: Optislang):
    """Test `delete` method."""
    project = optislang.project
    root_system = project.root_system
    with pytest.raises(NotImplementedError):
        root_system.delete()
    optislang.dispose()


def test_get_reference_design(optislang: Optislang):
    """Test ``get_refence_design``."""
    project = optislang.project
    root_system = project.root_system
    design = root_system.get_reference_design()
    optislang.dispose()
    assert isinstance(design, Design)
    assert isinstance(design.parameters, tuple)
    assert isinstance(design.parameters[0], DesignVariable)
    assert isinstance(design.responses, tuple)
    assert isinstance(design.responses[0], DesignVariable)


def test_evaluate_design(optislang: Optislang, tmp_path: Path):
    """Test ``evaluate_design``."""
    application = optislang.application
    project = application.project
    application.save_as(file_path=tmp_path / "test_modify_parameter.opf")
    project.reset()
    project = optislang.project
    root_system = project.root_system
    design = Design(parameters=parameters)
    assert design.status == DesignStatus.IDLE
    assert design.id == None
    assert design.feasibility == None
    assert isinstance(design.variables, tuple)
    result = root_system.evaluate_design(design=design)
    optislang.dispose()
    assert isinstance(result, Design)
    assert result.status == DesignStatus.SUCCEEDED
    assert design.status == DesignStatus.IDLE
    assert isinstance(result.responses, tuple)
    assert isinstance(design.responses, tuple)
    assert isinstance(result.responses[0], DesignVariable)
    assert result.responses[0].value == 15
    assert len(design.responses) == 0
    assert isinstance(result.constraints, tuple)
    assert isinstance(design.constraints, tuple)
    assert isinstance(result.limit_states, tuple)
    assert isinstance(design.limit_states, tuple)
    assert isinstance(result.objectives, tuple)
    assert isinstance(design.objectives, tuple)
    assert isinstance(result.variables, tuple)
    assert isinstance(design.variables, tuple)
    assert result.feasibility
    assert design.feasibility == None


def test_design_structure(optislang: Optislang):
    """Test ``get_missing&unused_parameters_names``."""
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
        missing = root_system.get_missing_parameters_names(design)
        undefined = root_system.get_undefined_parameters_names(design)
        assert isinstance(missing, tuple)
        assert isinstance(undefined, tuple)
        assert missing == expected_outputs[index][0]
        assert undefined == expected_outputs[index][1]
    optislang.dispose()
