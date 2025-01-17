# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
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

import os
from pathlib import Path
from typing import OrderedDict

import pytest

from ansys.optislang.core import utils

pytestmark = pytest.mark.local_osl


def test_get_awp_root_dirs():
    "Test that function returns dictionary of matching environment variables."
    environ_vars = list(utils.iter_awp_roots())
    # Unified installer doesn't set AWP_ROOT by default on Linux
    if os.name != "posix":
        assert len(environ_vars) > 0


def test_get_osl_executable():
    "Test that function returns executable, if exists."
    auto_exe_path = utils.get_osl_exec()
    assert isinstance(auto_exe_path, tuple)
    assert isinstance(auto_exe_path[0], int)
    assert isinstance(auto_exe_path[1], Path)
    exe_path = utils.get_osl_exec(osl_version="999")
    assert exe_path is None


def test_find_all_osl_exec():
    "Test that function returns OrderedDict."
    dictionary = utils.find_all_osl_exec()
    version = next(iter(dictionary.keys()))
    assert isinstance(dictionary, OrderedDict)
    assert isinstance(version, int)
    assert isinstance(dictionary[version][0], Path)
    assert isinstance(dictionary[version], (Path, tuple))
