import logging as deflogging  # Default logging
import os

from ansys.optislang.core import LOG  # Global logger
from ansys.optislang.core import logging

LOG_LEVELS = {"CRITICAL": 50, "ERROR": 40, "WARNING": 30, "INFO": 20, "DEBUG": 10}


def test_initialization():
    """This tests correct initialization
    of class OslLogger"""
    log0 = logging.OslLogger()
    assert log0.logger.level == logging.LOG_LEVEL
    assert log0.file_handler == None
    assert isinstance(log0.std_out_handler, type(LOG.std_out_handler))
    log1 = logging.OslLogger(loglevel="ERROR")
    assert log1.logger.level == deflogging.ERROR


def test_create_log_file(tmp_path):
    "This tests creation of logfile with ``logfile_name`` when initialized"
    logfile_path = os.path.join(tmp_path, "testlog.log")
    assert not os.path.isfile(logfile_path)
    log = logging.OslLogger(log_to_file=True, logfile_name=logfile_path)
    assert os.path.isfile(logfile_path)


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


def test_add_file_handler():
    log = logging.OslLogger()
    log.add_file_handler(logfile_name="testlog.log")
    assert log.file_handler != None
    assert log.file_handler.level == logging.LOG_LEVEL
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
    assert LOG.logger.hasHandlers
    assert LOG.file_handler or LOG.std_out_handler  # at least a handler is not empty


def test_global_logger_stdout(caplog):
    LOG.logger.setLevel("DEBUG")
    LOG.std_out_handler.setLevel("DEBUG")
    for each_log_name, each_log_number in LOG_LEVELS.items():
        msg = f"This is an {each_log_name} message."
        LOG.logger.log(each_log_number, msg)
        # Make sure we are using the right logger, the right level and message.
        assert caplog.record_tuples[-1] == ("pyoptislang_global", each_log_number, msg)


def test_global_logger_log_to_file():
    LOG.logger.setLevel("DEBUG")
    LOG.add_file_handler(logfile_name="testlog.log", loglevel="DEBUG")
    msg = "Random debug message"
    LOG.logger.debug(msg)
    with open("testlog.log", "r") as fid:
        text = "".join(fid.readlines())
    assert msg in text
