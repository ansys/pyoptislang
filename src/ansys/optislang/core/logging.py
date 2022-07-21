"""Logging module."""

from datetime import datetime
import inspect
import logging
import sys
import weakref

## Default configuration
LOG_LEVEL = logging.DEBUG
FILE_NAME = "pyOptislang.log"
DEBUG = logging.DEBUG
INFO = logging.INFO
WARN = logging.WARN
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

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


class OslLogger:
    """Logger class created for each session."""

    file_handler = None
    std_out_handler = None
    log_level = LOG_LEVEL
    instances = {}

    def __init__(
        self,
        loglevel=LOG_LEVEL,
        log_to_file=False,
        logfile_name=FILE_NAME,
        log_to_stdout=True,
    ):
        """Initialize customized logger.

        Parameters
        ----------
        loglevel : str, optional
            Level of logging, by default LOG_LEVEL.
        log_to_file : bool, optional
            Record logs to file, by default ``True``.
        logfile_name: str, optional
            Output file name, by default FILE_NAME
        log_to_stdout : bool, optional
            Log to command line, by default ``False``.
        """
        # Set class/method name from where its called
        logger_name = inspect.stack()[1][3]

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
        loglevel,
    ):
        """Set loglevel of the object and its handlers."""
        self.logger.setLevel(loglevel)
        for handler in self.logger.handlers:
            handler.setLevel(loglevel)
        self.log_level = loglevel

    def add_file_handler(
        self,
        logfile_name=FILE_NAME,
        loglevel=LOG_LEVEL,
    ):
        """Add file handler (output file) to the logger.

        Parameters
        ----------
        logger: logging.Logger
            Logger where file_handle will be created
        logfile_name: str, optional
            Output file name, by default FILE_NAME.
        loglevel : str, optional
            Level of logging, by default LOG_LEVEL.
        Returns
        -------
        logging.logger
            Logger class.
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
        loglevel=LOG_LEVEL,
    ):
        """Add standard output to the terminal.

        Parameters
        ----------
        loglevel : str, optional
            Level of logging, by default LOG_LEVEL.
        Returns
        -------
        logging.logger
            Logger class.
        """
        std_out_handler = logging.StreamHandler()
        std_out_handler.setLevel(loglevel)
        std_out_handler.setFormatter(logging.Formatter(FILE_MSG_FORMAT))
        self.logger.addHandler(std_out_handler)
        self.std_out_handler = std_out_handler
        std_out_handler.stream.write(NEW_SESSION_HEADER)
        std_out_handler.stream.write(DEFAULT_STDOUT_HEADER)

    def create_logger(
        self,
        new_logger_name,
    ):
        """Create a logger for Optislang instance.

        Parameters
        ----------
        new_logger_name : str
            Name of the new logger.
        Returns
        -------
        logging.logger
            Logger class.
        """
        new_logger = logging.getLogger(new_logger_name)
        if self.file_handler:
            new_logger.file_handler = self.file_handler
            new_logger.addHandler(new_logger.file_handler)

        if self.std_out_handler:
            new_logger.std_out_handler = self.std_out_handler
            new_logger.addHandler(new_logger.std_out_handler)

        new_logger.propagate = True
        return new_logger

    def add_child_logger(
        self,
        child_logger_name,
    ):
        """Call create_logger and a child logger is created (more general logger than main).

        Parameters
        ----------
        child_logger_name : str
            Name of the new child logger.
        """
        if type(child_logger_name) is not str:
            raise ValueError("Expected input child_logger_name: str")
        child_logger = self.logger.name + "." + child_logger_name
        self.instances[child_logger] = self.create_logger(child_logger)

    def add_instance_logger(
        self,
        instance_name,
        osl_instance,
    ):
        """Create a logger for Optislang instance.

        Parameters
        ----------
        instance_name : str
            Name of the new instance logger.
        osl_instance: ansys.optislang.core
            Optislang instance object. This should contain the attribute ``name``.
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
            self.create_logger(instance_name), osl_instance
        )

    def __getitem__(self, instance_name):
        """Return logger with instance_name.

        Parameters
        ----------
        instance_name : str
            Name of the instance.
        Returns
        -------
        logging.logger
            Logger class.
        """
        if instance_name in self.instances.keys():
            return self.instances[instance_name]
        else:
            raise KeyError(f"There is no instances with name {instance_name}")

    def add_handling_uncaught_expections(self, logger):
        """Redirect the output of an exception to the logger.

        Parameters
        ----------
        logging.logger
            Logger class.
        """

        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

        sys.excepthook = handle_exception


class OslCustomAdapter(logging.LoggerAdapter):
    """Customized logger with extra inputs."""

    file_handler = None
    std_out_handler = None
    log_level = LOG_LEVEL

    def __init__(
        self,
        logger,
        extra=None,
    ):
        """
        Initialize customized logger with extra inputs.

        Parameters
        ----------
        logger : str, optional
            Level of logging, by default LOG_LEVEL.
        osl_instance : bool, optional
            Record logs to file, by default ``True``.
        """
        self.logger = logger
        if extra:
            self.extra = weakref.proxy(extra)

        self.file_handler = logger.file_handler
        self.std_out_handler = logger.std_out_handler
