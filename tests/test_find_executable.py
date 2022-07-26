import os

import pytest

from ansys.optislang.core import utils

pytestmark = pytest.mark.local_osl


def test_get_system_vars():
    "Test that function returns dictionary of matching environment variables."
    sys_vars = utils._get_system_vars(pattern="^AWP_ROOT.*")
    assert type(sys_vars) == type({})
    # linux doesn't have "AWP_ROOT environment variables"
    if os.name == "nt":
        assert bool(sys_vars) == True
    sys_vars = utils._get_system_vars(pattern="RANDOM_NONEXISTING_VARIABLE")
    assert type(sys_vars) == type({})
    assert bool(sys_vars) == False


def test_get_osl_executable():
    "Test that function returns executable, if exists."
    auto_exe_path = utils.get_osl_executable()
    assert type(auto_exe_path) == type("")
    with pytest.raises(FileNotFoundError):
        utils.get_osl_executable(osl_version="999")
    exe_path = utils.get_osl_executable(osl_version="221")
    assert type(exe_path) == type("")
