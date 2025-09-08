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

import logging
import os
import re
import time
from typing import Optional

import psutil
import pytest

from ansys.optislang.core import OslServerProcess

NEW_PROJECT_STR = "New project"
OPENED_PROJECT_STR = "Opened project"

pytestmark = pytest.mark.local_osl


def wait_for_file_creation(file: str, timeout: float = 90) -> None:
    """Wait for file to be created.

    Parameters
    ----------
    file : str
        Path to the file to wait for.
    timeout : float, optional
        Maximum time in seconds to wait for file creation. Defaults to 60.
    """
    start = time.time()
    while not os.path.isfile(file) and time.time() - start < timeout:
        time.sleep(0.1)


def wait_for_log_record(text: str, caplog, timeout: float = 90) -> Optional[logging.LogRecord]:
    """Wait for log record.

    Parameters
    ----------
    text : str
        Text in the log record message to wait for.
    caplog : pytest.LogCaptureFixture
        Builtin fixture which captures log records.
    timeout : int, optional
        Maximum time in seconds to wait for log record. Defaults to 60.

    Returns
    -------
    LogRecord
        Returns the log record it was waiting for. ``None`` if the log record did not occur.
    """
    start_index = 0
    while True:
        for log_record in caplog.records[start_index:]:
            if text in log_record.msg:
                return log_record
            start_index += 1
        if timeout <= 0:
            return None
        time.sleep(0.1)
        timeout -= 1


def check_log_for_errors(caplog, level_limit=logging.ERROR):
    """Check log records for an error.

    Parameters
    ----------
    caplog : pytest.LogCaptureFixture
        Builtin fixture which captures log records.
    level_limit : int, optional
        Log level which is assumed as an error. Defaults to logging.ERROR.
    """
    error_strings = []
    if logging.CRITICAL <= level_limit:
        error_strings.append("critical")
    if logging.ERROR <= level_limit:
        error_strings.append("error")
    if logging.WARNING <= level_limit:
        error_strings.append("warning")

    for log_record in caplog.records:
        assert log_record.levelno < level_limit
        error_msg = log_record.msg.lower()
        assert all(not error_str in error_msg for error_str in error_strings)


def get_port_from_server_info_file(server_info_file: str) -> int:
    """Get port number from server information file.

    Parameters
    ----------
    server_info_file : str
        Path to the server information file.

    Returns
    -------
    int
        Server port.

    Raises
    ------
    FileNotFoundError
        Raised when the server information file is not found.
    """
    if not os.path.isfile(server_info_file):
        raise FileNotFoundError(f"Cannot find server info file: {server_info_file}")

    with open(server_info_file, mode="r") as file:
        for line in file:
            try:
                name, value = line.split("=")
                name = name.strip().lower()
                if name == "server_port":
                    return int(value.strip())
            except:
                pass
    return None


def get_logger() -> logging.Logger:
    """Get logger.

    Returns
    -------
    logging.Logger
        Logger instance.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    return logger


@pytest.mark.xfail
def test_start_wo_project_file(executable, caplog):
    """Test start of the optiSLang process without project file specified.

    Parameters
    ----------
    executable : str
        Path to the optiSLang executable.
    caplog : pytest.LogCaptureFixture
        Builtin fixture which captures log records.
    """
    with OslServerProcess(executable, None, logger=get_logger()) as osl_process:
        assert not osl_process.is_running()
        assert osl_process.pid is None
        osl_process.start()
        assert osl_process.is_running()
        assert psutil.pid_exists(osl_process.pid)

        log_record = wait_for_log_record(NEW_PROJECT_STR, caplog)
        assert log_record is not None
        assert NEW_PROJECT_STR in log_record.msg
        check_log_for_errors(caplog)


@pytest.mark.xfail
def test_start_with_project_file(executable, project_file, caplog):
    """Test start of the optiSLang process with path to the project file specified.

    Parameters
    ----------
    executable : str
        Path to the optiSLang executable.
    project_file : str
        Path to the project file.
    caplog : pytest.LogCaptureFixture
        Builtin fixture which captures log records.
    """
    with OslServerProcess(executable, project_file, logger=get_logger()) as osl_process:
        assert not osl_process.is_running()
        assert osl_process.pid is None
        osl_process.start()
        assert osl_process.is_running()
        assert psutil.pid_exists(osl_process.pid)

        log_record = wait_for_log_record(NEW_PROJECT_STR, caplog)
        assert log_record is not None
        assert NEW_PROJECT_STR in log_record.msg
        check_log_for_errors(caplog)


def test_init_with_invalid_project_file(executable, tmp_path):
    """Test initialization of the `OslServerProcess` class with invalid project file.

    Parameters
    ----------
    executable : str
        Path to the optiSLang executable.
    tmp_path : pathlib.Path
        Builtin fixture to temporary directory unique to the test invocation.
    """
    project_file = os.path.join(tmp_path, "test.txt")
    assert not os.path.isfile(project_file)
    with pytest.raises(ValueError):
        osl_process = OslServerProcess(executable, project_file)


@pytest.mark.xfail
def test_open_project_file(executable, project_file, caplog):
    """Test open of optiSLang project file.

    Parameters
    ----------
    executable : str
        Path to the optiSLang executable.
    project_file : str
        Path to the project file.
    caplog : pytest.LogCaptureFixture
        Builtin fixture which captures log records.
    """
    # Create project file
    assert not os.path.isfile(project_file)
    with OslServerProcess(executable, project_file) as osl_process:
        osl_process.start()
        wait_for_file_creation(project_file)

    # Open project file
    assert os.path.isfile(project_file)
    with OslServerProcess(executable, project_file, logger=get_logger()) as osl_process:
        osl_process.start()

        log_record = wait_for_log_record(OPENED_PROJECT_STR, caplog)
        assert log_record is not None
        assert OPENED_PROJECT_STR in log_record.msg
        check_log_for_errors(caplog)


def test_tmp_project_file_exists(executable):
    """Test existence of the temporary project file.

    Parameters
    ----------
    executable : str
        Path to the optiSLang executable.
    """
    with OslServerProcess(executable, None) as osl_process:
        osl_process.start()
        wait_for_file_creation(osl_process.project_path)
        assert os.path.isfile(osl_process.project_path)
        osl_process.terminate()
        assert not os.path.isfile(osl_process.project_path)


def test_new_project_file_exists(executable, project_file):
    """Test existence of the new project file.

    Parameters
    ----------
    executable : str
        Path to the optiSLang executable.
    project_file : str
        Path to the project file.
    """
    assert not os.path.isfile(project_file)
    with OslServerProcess(executable, project_file) as osl_process:
        osl_process.start()
        wait_for_file_creation(project_file)
        assert os.path.isfile(project_file)
        osl_process.terminate()
        assert os.path.isfile(project_file)


def test_write_server_info(executable, project_file, server_info_file):
    """Test creation of the server information file.

    Parameters
    ----------
    executable : str
        Path to the optiSLang executable.
    project_file : str
        Path to the project file.
    server_info_file : str
        Path to the server information file.
    """
    assert not os.path.isfile(server_info_file)
    with OslServerProcess(
        executable, project_file, server_info=server_info_file, enable_tcp_server=True
    ) as osl_process:
        osl_process.start()
        wait_for_file_creation(server_info_file)
        assert os.path.isfile(server_info_file)


# TODO: Implement ``test_wo_no_save`` function (project must be modified)
# TODO: Implement ``test_no_save`` function (project must be modified)


def test_port_range(executable, project_file, server_info_file):
    """Test that the optiSLang server port is in the specified range.

    Parameters
    ----------
    executable : str
        Path to the optiSLang executable.
    project_file : str
        Path to the project file.
    server_info_file : str
        Path to the server information file.
    """
    assert not os.path.isfile(server_info_file)
    port_range = (49690, 49790)
    with OslServerProcess(
        executable,
        project_file,
        enable_tcp_server=True,
        server_info=server_info_file,
        port_range=port_range,
    ) as osl_process:
        osl_process.start()
        wait_for_file_creation(server_info_file)
        assert os.path.isfile(server_info_file)
        port = get_port_from_server_info_file(server_info_file)
        assert port_range[0] <= port and port <= port_range[1]


def test_process_out_override(executable, project_file, caplog):
    """Ensure working override to disable process output."""

    varname = "PYOPTISLANG_DISABLE_OPTISLANG_OUTPUT"

    if varname in os.environ:
        pytest.skip()

    os.environ["PYOPTISLANG_DISABLE_OPTISLANG_OUTPUT"] = "FOO"

    with OslServerProcess(
        executable,
        project_file,
        logger=get_logger(),
        log_process_stdout=True,
        log_process_stderr=True,
    ) as osl_process:
        osl_process.start()
        wait_for_file_creation(project_file)

        def does_not_contain(text):
            return re.search(text, caplog.text, re.IGNORECASE) is None

        assert does_not_contain("starting optiSLang")
        assert does_not_contain("optiSLang Stdout")
        assert does_not_contain("optiSLang Stderr")
