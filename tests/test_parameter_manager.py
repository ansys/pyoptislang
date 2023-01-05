import pytest

from ansys.optislang.core import Optislang, examples
from ansys.optislang.core.project_parametric import MixedParameter

pytestmark = pytest.mark.local_osl
parametric_project = examples.get_files("calculator_with_params")[1][0]


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


def test_get_parameters(optislang: Optislang):
    """Test ``get_parameters_names``."""
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
