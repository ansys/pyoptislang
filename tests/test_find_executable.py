import os
from typing import OrderedDict

import pytest

from ansys.optislang.core import utils

pytestmark = pytest.mark.local_osl


def test_get_environ_vars():
    "Test that function returns dictionary of matching environment variables."
    environ_vars = utils._get_environ_vars(pattern="^AWP_ROOT.*")
    assert isinstance(environ_vars, dict)
    # linux doesn't have "AWP_ROOT environment variables"
    if os.name == "nt":
        assert len(environ_vars) > 0
    environ_vars = utils._get_environ_vars(pattern="RANDOM_NONEXISTING_VARIABLE")
    assert isinstance(environ_vars, dict)
    assert len(environ_vars) == 0


def test_get_osl_executable():
    "Test that function returns executable, if exists."
    auto_exe_path = utils.get_osl_exec()
    assert isinstance(auto_exe_path, tuple)
    assert isinstance(auto_exe_path[0], int)
    assert isinstance(auto_exe_path[1], str)
    exe_path = utils.get_osl_exec(osl_version="999")
    assert exe_path is None


def test_find_all_osl_exec():
    "Test that function returns OrderedDict."
    dictionary = utils.find_all_osl_exec()
    version = next(iter(dictionary.keys()))
    assert isinstance(dictionary, OrderedDict)
    assert isinstance(version, int)
    assert isinstance(dictionary[version][0], str)
    assert isinstance(dictionary[version], (str, tuple))
