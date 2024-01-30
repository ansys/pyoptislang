# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
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

"""Osl logging module."""
from __future__ import annotations

from copy import copy
from datetime import datetime
import logging
from typing import TYPE_CHECKING, Optional
import weakref

if TYPE_CHECKING:
    from ansys.optislang.core import Optislang

## Default configuration
LOG_LEVEL = "DEBUG"
FILE_NAME = "pyOptislang.log"

## Formatting

STDOUT_MSG_FORMAT = "%(levelname)s -  %(module)s - %(name)s -  %(funcName)s - %(message)s"
FILE_MSG_FORMAT = STDOUT_MSG_FORMAT

DEFAULT_STDOUT_HEADER = """
LEVEL - MODULE - CLASS - FUNCTION - MESSAGE
"""
DEFAULT_FILE_HEADER = DEFAULT_STDOUT_HEADER
NEW_SESSION_HEADER = f"""
===============================================================================
       NEW SESSION - {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}
===============================================================================
"""


class OslCustomAdapter(logging.LoggerAdapter):
    """Provides a customized logger with extra inputs."""

    file_handler = None
    std_out_handler = None
    log_level = LOG_LEVEL

    def __init__(
        self,
        logger: logging.Logger,
        extra=None,
    ) -> None:
        """
        Initialize the customized logger with extra inputs.

        Parameters
        ----------
        logger : str, optional
            Level of logging. The default is ``LOG_LEVEL``.
        osl_instance : bool, optional
            Whether to record logs to an output file. The default is ``True``.
        """
        self.logger = logger
        if extra:
            self.extra = weakref.proxy(extra)
        else:
            self.extra = None

        self.file_handler = logger.file_handler
        self.std_out_handler = logger.std_out_handler

    def process(self, msg, kwargs):
        """Modify the message and/or keyword arguments passed to a logging call."""
        kwargs["extra"] = {}
        # These are the extra parameters sent to the log.
        # Here, self.extra is the argument passed to the log records.
        try:
            kwargs["extra"]["instance_name"] = self.extra.name
        except ReferenceError:
            kwargs["extra"]["instance_name"] = "Undefined"
        return msg, kwargs


class OslLogger:
    """Provides the logger class created for each session."""

    file_handler = None
    std_out_handler = None
    log_level = LOG_LEVEL
    instances = {}

    def __init__(
        self,
        loglevel: str = LOG_LEVEL,
        log_to_file: bool = False,
        logfile_name: str = FILE_NAME,
        log_to_stdout: bool = True,
    ) -> None:
        """Initialize the customized logger.

        Parameters
        ----------
        loglevel : str, optional
            Level of logging. The default is ``LOG_LEVEL``.
        log_to_file : bool, optional
            Whether to record logs to an output file. The default is ``False``.
        logfile_name: str, optional
            Name of the output file. The default is ``FILE_NAME``.
        log_to_stdout : bool, optional
            Whether to log to the command line. The default is ``False``.
        """
        # Create logger
        self.logger = logging.getLogger("pyoptislang_global")
        self.set_log_level(loglevel)
        self.logger.propagate = True

        if log_to_file:
            self.add_file_handler(logfile_name=logfile_name, loglevel=loglevel)

        if log_to_stdout:
            self.add_std_out_handler(loglevel=loglevel)

    def set_log_level(
        self,
        loglevel: str,
    ) -> None:
        """Set the log level of the object and its handlers.

        Parameters
        ----------
        loglevel : str
            Level of logging. The default is ``LOG_LEVEL``.
        """
        self.logger.setLevel(loglevel)
        for handler in self.logger.handlers:
            handler.setLevel(loglevel)
        self.log_level = loglevel

    def add_file_handler(
        self,
        logfile_name: str = FILE_NAME,
        loglevel: str = LOG_LEVEL,
    ) -> None:
        """Add a file handler (output file) to the logger.

        Parameters
        ----------
        logger: logging.Logger
            Logger for creating the output file.
        logfile_name: str, optional
            Name of the output file. The default is ``FILE_NAME``.
        loglevel : str, optional
            Level of logging. The default is ``LOG_LEVEL``.
        """
        file_handler = logging.FileHandler(logfile_name)
        file_handler.setFormatter(logging.Formatter(FILE_MSG_FORMAT))
        file_handler.setLevel(loglevel)
        self.logger.addHandler(file_handler)
        self.file_handler = file_handler
        file_handler.stream.write(NEW_SESSION_HEADER)
        file_handler.stream.write(DEFAULT_FILE_HEADER)

    def add_std_out_handler(
        self,
        loglevel: str = LOG_LEVEL,
    ) -> None:
        """Add standard output to the terminal.

        Parameters
        ----------
        loglevel : str, optional
            Level of logging. The default is ``LOG_LEVEL``.
        """
        std_out_handler = logging.StreamHandler()
        std_out_handler.setLevel(loglevel)
        std_out_handler.setFormatter(logging.Formatter(FILE_MSG_FORMAT))
        self.logger.addHandler(std_out_handler)
        self.std_out_handler = std_out_handler
        std_out_handler.stream.write(NEW_SESSION_HEADER)
        std_out_handler.stream.write(DEFAULT_STDOUT_HEADER)

    def create_logger(self, new_logger_name: str, level: Optional[str] = None) -> logging.Logger:
        """Create a logger for the Optislang instance.

        Parameters
        ----------
        new_logger_name : str
            Name of the logger.
        level: Optional[str], optional
            Level of logging. The default is ``None``, in which gase the global log level is set.

        Returns
        -------
        logging.logger
            Logger class.
        """
        new_logger = logging.getLogger(new_logger_name)
        new_logger.std_out_handler = None
        new_logger.file_handler = None

        if level is None:
            level = self.log_level
        level = level.upper()
        new_logger.setLevel(level)

        if self.file_handler:
            new_logger.file_handler = copy(self.file_handler)
            new_logger.addHandler(new_logger.file_handler)
            new_logger.file_handler.setLevel(level)

        if self.std_out_handler:
            new_logger.std_out_handler = copy(self.std_out_handler)
            new_logger.addHandler(new_logger.std_out_handler)
            new_logger.std_out_handler.setLevel(level)

        new_logger.propagate = True
        return new_logger

    def add_child_logger(
        self,
        child_logger_name: str,
    ) -> None:
        """Call the ``create_logger`` method to add a child logger.

        This looger is more general than the main logger.

        Parameters
        ----------
        child_logger_name : str
            Name of the  child logger.
        """
        if type(child_logger_name) is not str:
            raise ValueError("Expected input child_logger_name: str")
        child_logger = self.logger.name + "." + child_logger_name
        self.instances[child_logger] = self.create_logger(child_logger)

    def add_instance_logger(
        self, instance_name: str, osl_instance: Optislang, level: Optional[str] = None
    ) -> OslCustomAdapter:
        """Add a logger for an Optislang instance.

        Parameters
        ----------
        instance_name : str
            Name of the instance logger.
        osl_instance: Optislang
            Optislang instance object. This object should contain the ``name``
            attribute.
        level: Optional[str], optional
            Level of logging. Defaults to ``None``.

        Returns
        -------
        OslCustomAdapter
            Customized logger with extra inputs.
        """
        if type(instance_name) is not str:
            raise ValueError("Expected input instance_name: str")

        # Rename instance if already exists
        counter = 0
        name = instance_name
        while instance_name in logging.root.manager.__dict__.keys():
            counter += 1
            instance_name = name + str(counter)

        self.instances[instance_name] = OslCustomAdapter(
            self.create_logger(instance_name, level), osl_instance
        )

        return self.instances[instance_name]

    def __getitem__(self, instance_name: str) -> logging.Logger:
        """Get a logger by an instance name.

        Parameters
        ----------
        instance_name : str
            Name of the instance.
        Returns
        -------
        self.instances[instance_name]: logging.Logger()
            Logger class.
        """
        if instance_name in self.instances.keys():
            return self.instances[instance_name]
        else:
            raise KeyError(f"There is no instances with name {instance_name}")
