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

"""Test different start/stop/stop_gently combinations with Optislang class."""
import pytest

from ansys.optislang.core import Optislang

pytestmark = pytest.mark.local_osl


@pytest.fixture
def optislang() -> Optislang:
    """Create Optislang class.

    Returns
    -------
    Optislang:
        Connects to the optiSLang application and provides an API to control it.
    """
    osl = Optislang(ini_timeout=90)
    yield osl
    osl.dispose()


@pytest.mark.parametrize(
    "input",
    [
        (("start", True, True), ("stop", True)),  # default
        (("start", False, True), ("stop", True)),  # don't wait for started -> also default
        (("start", True, True), ("stop", False)),  # stop: don't wait for finished
        (("start", True, False), ("stop", True)),  # start: don't wait for finished
        (("start", False, False), ("stop", False)),  # all false
        (("start", True, True), ("stop", True), ("stop", True)),
        (("start", True, True), ("stop", True), ("start", True, True)),
        (("stop", True), ("stop", True), ("start", True, True)),
        (("start", True, True), ("start", True, True), ("start", True, True)),
    ],
)
def test_combinations(optislang: Optislang, input):
    "Test combinations."
    for method in input:
        if method[0] == "start":
            optislang.project.start(method[1], method[2])
        if method[0] == "stop":
            optislang.project.stop(method[1])
