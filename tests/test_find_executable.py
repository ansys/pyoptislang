import os

import pytest

from ansys.optislang.core import utils

pytestmark = pytest.mark.local_osl


def test_get_environ_vars():
    "Test that function returns dictionary of matching environment variables."
    environ_vars = utils._get_environ_vars(pattern="^AWP_ROOT.*")
    assert type(environ_vars) == dict
    # linux doesn't have "AWP_ROOT environment variables"
    if os.name == "nt":
        assert len(environ_vars) > 0
    environ_vars = utils._get_environ_vars(pattern="RANDOM_NONEXISTING_VARIABLE")
    assert type(environ_vars) == dict
    assert len(environ_vars) == 0


def test_get_osl_executable():
    "Test that function returns executable, if exists."
    auto_exe_path = utils.get_osl_exec()
    assert type(auto_exe_path) == tuple
    assert type(auto_exe_path[0]) == int
    assert type(auto_exe_path[1]) == str
    exe_path = utils.get_osl_exec(osl_version="999")
    assert exe_path == None
