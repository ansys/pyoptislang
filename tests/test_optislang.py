from contextlib import nullcontext as does_not_raise
import os
from pathlib import Path
import time

import pytest

from ansys.optislang.core import Optislang, errors, examples
from ansys.optislang.core.project_parametric import Design, Parameter, ParameterManager

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
    osl = Optislang()
    osl.set_timeout(20)
    return osl


def test_get_osl_version_string(optislang):
    "Test ``get_osl_version_string``."
    version = optislang.get_osl_version_string()
    assert isinstance(version, str)
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


def test_get_osl_version(optislang):
    """Test ``get_osl_version``."""
    major_version, minor_version, maintenance_version, revision = optislang.get_osl_version()
    assert isinstance(major_version, int)
    assert isinstance(minor_version, int)
    assert isinstance(maintenance_version, int) or maintenance_version == None
    assert isinstance(revision, int) or revision == None
    with does_not_raise() as dnr:
        optislang.dispose()
    assert dnr is None


def test_get_project_description(optislang):
    "Test ``get_project_description``."
    description = optislang.get_project_description()
    assert isinstance(description, str)
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


def test_get_project_location(optislang):
    "Test ``get_project_location``."
    location = optislang.get_project_location()
    assert isinstance(location, Path)
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


def test_get_project_name(optislang):
    "Test ``get_project_name``."
    name = optislang.get_project_name()
    assert isinstance(name, str)
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


def test_get_project_status(optislang):
    "Test ``get_project_status``."
    status = optislang.get_project_status()
    assert isinstance(status, str)
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


def test_get_working_dir(optislang):
    "Test ``get_working_dir``."
    working_dir = optislang.get_working_dir()
    assert isinstance(working_dir, Path)
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


def test_reset(optislang):
    "Test ``reset``."
    with does_not_raise() as dnr:
        optislang.reset()
    assert dnr is None
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


def test_run_python_script(optislang):
    "Test ``run_python_script``."
    run_script = optislang.run_python_script(
        """
a = 5
b = 10
result = a + b
print(result)
"""
    )
    assert isinstance(run_script, tuple)
    assert run_script[0][0:2] == "15"
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


def test_run_python_file(optislang, tmp_path):
    "Test ``run_python_file``."
    cmd = """
a = 5
b = 10
result = a + b
print(result)
"""
    cmd_path = os.path.join(tmp_path, "commands.txt")
    with open(cmd_path, "w") as f:
        f.write(cmd)
    run_file = optislang.run_python_file(file_path=cmd_path)
    assert isinstance(run_file, tuple)
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


def test_save_copy(optislang, tmp_path):
    "Test ``save_copy``."
    with does_not_raise() as dnr:
        copy_path = os.path.join(tmp_path, "test_save_copy.opf")
        optislang.save_copy(file_path=copy_path)
    assert dnr is None
    assert os.path.isfile(copy_path)
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


def test_start(optislang):
    "Test ``start``."
    with does_not_raise() as dnr:
        optislang.start()
    assert dnr is None
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


def test_stop(optislang):
    "Test ``stop``."
    with does_not_raise() as dnr:
        optislang.run_python_script(
            r"""
from py_os_design import *
sens = actors.SensitivityActor("Sensitivity")
add_actor(sens)
python = actors.PythonActor('python_sleep')
sens.add_actor(python)
python.source = 'import time\ntime.sleep(0.1)\noutput_value = input_value*2'
python.add_parameter("input_value", PyOSDesignEntry(5.0))
python.add_response(("output_value", PyOSDesignEntry(10)))
connect(sens, "IODesign", python, "IDesign")
connect(python, "ODesign", sens, "IIDesign")
"""
        )
        optislang.start(wait_for_finished=False)
        optislang.stop()
    assert dnr is None
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


# def test_stop_gently(optislang):
#     "Test ``stop_gently``."
#     with does_not_raise() as dnr:
#         optislang.run_python_script(
#             r"""
# from py_os_design import *
# sens = actors.SensitivityActor("Sensitivity")
# add_actor(sens)
# python = actors.PythonActor('python_sleep')
# sens.add_actor(python)
# python.source = 'import time\ntime.sleep(0.1)\noutput_value = input_value*2'
# python.add_parameter("input_value", PyOSDesignEntry(5.0))
# python.add_response(("output_value", PyOSDesignEntry(10)))
# connect(sens, "IODesign", python, "IDesign")
# connect(python, "ODesign", sens, "IIDesign")
# """
#         )
#         optislang.start(wait_for_finished=False)
#         optislang.stop_gently()
#     assert dnr is None
#     with does_not_raise() as dnr:
#         optislang.dispose()
#         time.sleep(3)
#     assert dnr is None


def test_dispose(optislang):
    "Test ``dispose``."
    with does_not_raise() as dnr:
        optislang.dispose()
        time.sleep(3)
    assert dnr is None


@pytest.mark.parametrize(
    "uid, expected",
    [
        ("3577cb69-15b9-4ad1-a53c-ac8af8aaea82", dict),
        ("3577cb69-15b9-4ad1-a53c-ac8af8aaea83", errors.OslCommandError),
    ],
)
def test_get_actor_properties(uid, expected):
    optislang = Optislang(project_path=parametric_project)
    if expected == errors.OslCommandError:
        with pytest.raises(expected):
            properties = optislang.get_actor_properties(uid)
    else:
        properties = optislang.get_actor_properties(uid)
        assert isinstance(properties, expected)
    optislang.dispose()


def test_get_nodes_dict():
    "Test ``get_nodes_dict``."
    optislang = Optislang(project_path=parametric_project)
    node_dict = optislang.get_nodes_dict()
    assert isinstance(node_dict, dict)
    assert node_dict[0]["name"] == "Calculator"
    optislang.dispose()


def test_get_parameter_manager():
    "Test ``get_parameter_manager``."
    optislang = Optislang(project_path=parametric_project)
    par_manager = optislang.get_parameter_manager()
    parameters = par_manager.parameters
    assert isinstance(par_manager, ParameterManager)
    assert isinstance(parameters, dict)
    optislang.shutdown()


def test_get_parameters_list():
    "Test ``get_parameters_list``."
    optislang = Optislang(project_path=parametric_project)
    params = optislang.get_parameters_list()
    optislang.dispose()
    assert isinstance(params, list)
    assert len(params) > 0
    assert set(["a", "b"]) == set(params)


def test_create_design():
    "Test ``create_design``."
    optislang = Optislang(project_path=parametric_project)
    inputs = {"a": 5, "b": 10}
    design = optislang.create_design(inputs)
    optislang.dispose()

    assert isinstance(design, Design)
    assert isinstance(design.parameters["a"], Parameter)
    design.set_parameter("a", 10)
    assert design.parameters["a"].reference_value == 10
    design.set_parameters({"b": 20, "c": 30})
    assert design.parameters["c"].reference_value == 30
    direct_design = Design(parameters={"a": 5, "b": 10})
    assert isinstance(direct_design, Design)
    assert isinstance(direct_design.parameters["b"], Parameter)


def test_evaluate_design():
    "Test ``evaluate_design``."
    optislang = Optislang(project_path=parametric_project)
    design = Design(parameters={"a": 5, "b": 10})
    assert design.status == "IDLE"
    assert design.id == "NOT ASSIGNED"
    result = optislang.evaluate_design(design)
    optislang.dispose()
    assert isinstance(result, tuple)
    assert isinstance(result[0], dict)
    assert isinstance(result[1], dict)
    assert design.status == "SUCCEEDED"
    assert isinstance(design.responses, dict)
    assert design.responses["c"].reference_value == 15
    assert isinstance(design.criteria, dict)


def test_evaluate_multiple_designs():
    optislang = Optislang(project_path=parametric_project)
    designs = [
        Design(parameters={"a": 1, "b": 2.0}),
        Design(parameters={"a": 3, "b": 4}),
        Design(parameters={"a": 5, "d": 6}),
        Design(parameters={"e": 7, "f": 8}),
        Design(
            parameters={
                "a": Parameter(name="a", reference_value=9),
                "b": Parameter(name="b", reference_value=10.0),
            }
        ),
    ]
    results = optislang.evaluate_multiple_designs(designs)
    optislang.dispose()

    for result in results:
        assert isinstance(result, tuple)
        assert isinstance(result[0], dict)
        assert isinstance(result[1], dict)
        assert "b" in result[0]
        assert "c" in result[1]


def test_validate_design():
    optislang = Optislang(project_path=parametric_project)
    designs = [
        Design(parameters={"a": 1, "b": 2}),
        Design(parameters={"e": 3, "f": 4}),
        Design(parameters={"a": 5, "g": 6}),
        Design(
            parameters={
                "a": Parameter(name="a", reference_value=9),
                "b": Parameter(name="b", reference_value=10.0),
            }
        ),
    ]
    for design in designs:
        result = optislang.validate_design(design)
        assert isinstance(result[0], str)
        assert isinstance(result[1], bool)
        assert isinstance(result[2], list)

    optislang.dispose()
