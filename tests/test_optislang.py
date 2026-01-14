# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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

from logging import Logger

import pytest

from ansys.optislang.core import Optislang
from ansys.optislang.core.application import Application
from ansys.optislang.core.osl_server import OslServer
from ansys.optislang.core.project import Project

pytestmark = pytest.mark.local_osl


@pytest.fixture()
def optislang(scope="function", autouse=False) -> Optislang:
    """Create Optislang class.

    Returns
    -------
    Optislang:
        Connects to the optiSLang application and provides an API to control it.
    """
    osl = Optislang(ini_timeout=90)
    osl.timeout = 60
    yield osl
    osl.dispose()


def test_dispose():
    "Test ``dispose``."
    osl = Optislang(ini_timeout=90)
    osl.dispose()


def test_optislang_properties(optislang: Optislang):
    """Test ``Optislang`` properties."""
    print(optislang)

    application = optislang.application
    assert isinstance(application, Application)

    logger = optislang.log
    assert isinstance(logger, Logger)

    name = optislang.name
    assert isinstance(name, str)

    osl_server = optislang.osl_server
    assert isinstance(osl_server, OslServer)

    version = optislang.osl_version_string
    assert isinstance(version, str)

    major_version, minor_version, maintenance_version, revision = optislang.osl_version
    assert isinstance(major_version, int)
    assert isinstance(minor_version, int)
    assert isinstance(maintenance_version, int)
    assert isinstance(revision, int)

    project = optislang.project
    assert isinstance(project, Project)

    assert optislang.timeout == 60
    assert isinstance(optislang.timeout, (int, float))
    optislang.timeout = 30
    assert optislang.timeout == 30
    with pytest.raises(ValueError):
        optislang.timeout = "20"


def test_shutdown():
    "Test ``shutdown``."
    osl = Optislang(shutdown_on_finished=False, ini_timeout=90)
    osl.shutdown()
