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

import logging as deflogging  # Default logging
from pathlib import Path

from ansys.optislang.core import LOG  # Global logger
from ansys.optislang.core import logging

LOG_LEVELS = {"CRITICAL": 50, "ERROR": 40, "WARNING": 30, "INFO": 20, "DEBUG": 10}


def test_initialization():
    """This tests correct initialization
    of class OslLogger"""
    log0 = logging.OslLogger()
    assert log0.logger.level == LOG_LEVELS[logging.LOG_LEVEL]
    assert log0.file_handler == None
    assert isinstance(log0.std_out_handler, type(LOG.std_out_handler))
    log1 = logging.OslLogger(loglevel="ERROR")
    assert log1.logger.level == deflogging.ERROR


def test_create_log_file(tmp_path: Path):
    "This tests creation of logfile with ``logfile_name`` when initialized"
    logfile_path = tmp_path / "testlog.log"
    assert not logfile_path.is_file()
    logging.OslLogger(log_to_file=True, logfile_name=str(logfile_path))
    assert logfile_path.is_file()


def test_set_log_level():
    """This tests setting and changing of log_level"""
    log = logging.OslLogger()
    log.set_log_level(loglevel="CRITICAL")
    assert log.logger.level == deflogging.CRITICAL
    log.set_log_level(loglevel="ERROR")
    assert log.logger.level == deflogging.ERROR
    log.set_log_level(loglevel="WARNING")
    assert log.logger.level == deflogging.WARNING
    log.set_log_level(loglevel="INFO")
    assert log.logger.level == deflogging.INFO
    log.set_log_level(loglevel="DEBUG")
    assert log.logger.level == deflogging.DEBUG


def test_add_file_handler(tmp_path: Path):
    log = logging.OslLogger()
    log.add_file_handler(logfile_name=str(tmp_path / "testlog.log"))
    assert log.file_handler is not None
    assert log.file_handler.level == LOG_LEVELS[logging.LOG_LEVEL]
    log.set_log_level(loglevel="ERROR")
    assert log.file_handler.level == deflogging.ERROR


def test_add_stdout_handler():
    log = logging.OslLogger(log_to_stdout=False)
    assert log.std_out_handler == None
    log.add_std_out_handler(loglevel="INFO")
    assert log.std_out_handler.level == deflogging.INFO


def test_global_logger_exist():
    "This tests if global logger exists"
    assert isinstance(LOG.logger, deflogging.Logger)
    assert LOG.logger.name == "pyoptislang_global"


def test_global_logger_has_handlers():
    "This tests if global logger has handlers"
    assert hasattr(LOG, "file_handler")
    assert hasattr(LOG, "std_out_handler")
    assert LOG.logger.hasHandlers()
    assert LOG.file_handler or LOG.std_out_handler  # at least a handler is not empty


def test_global_logger_stdout(caplog):
    LOG.logger.setLevel("DEBUG")
    LOG.std_out_handler.setLevel("DEBUG")
    for each_log_name, each_log_number in LOG_LEVELS.items():
        msg = f"This is an {each_log_name} message."
        LOG.logger.log(each_log_number, msg)
        # Make sure we are using the right logger, the right level and message.
        assert caplog.record_tuples[-1] == ("pyoptislang_global", each_log_number, msg)


def test_global_logger_log_to_file(tmp_path: Path):
    LOG.logger.setLevel("DEBUG")
    LOG.add_file_handler(logfile_name=str(tmp_path / "testlog.log"), loglevel="DEBUG")
    msg = "Random debug message"
    LOG.logger.debug(msg)
    with open(tmp_path / "testlog.log", "r") as fid:
        text = "".join(fid.readlines())
    assert msg in text
