from cement.core import log
from loguru import logger
from cement.utils.misc import is_true, minimal_logger
import sys

LOG = minimal_logger(__name__)


class LoguruLogHandler(log.LogHandler):
    """
    This class is an implementation of the :ref:`Log <cement.core.log>`
    interface, and sets up the loguru facility using the ` loguru module:
    <https://github.com/Delgan/loguru>`.

    """

    class Meta:

        """Handler Meta-data."""

        #: The string identifier of this handler.
        label = 'loguru'

        #: An identifier associated with the added sink and which
        # should be used to remove() it
        id = None

        #: object in charge of receiving formatted logging messages
        # and propagating them to an appropriate endpoint.
        sink = sys.stdout

        padding = 0

        #: The logging format for the file logger.
        file_format = "{time} | {level: <8} | {name}:{function}:{line}{extra[padding]} | {message}\n{exception}"

        #: The logging format for the consoler logger.
        # console_format = "{level}: {message}"
        console_format = "{level: <8} | {name}:{function}:{line}{extra[padding]} | {message}\n{exception}"

        #: The logging format for both file and console if ``debug==True``.
        # strace_format = "{level}-{file}-{function}-{line}: {message}"
        debug_format = "{time} | {level: <8} | {name}:{function}:{line}{extra[padding]} | {message}\n{exception}"

        #: The default configuration dictionary to populate the ``log``
        #: section.
        config_defaults = dict(
            file=None,
            level='INFO',
            to_console=True,
        )

        #: List of arguments to use for the cli options
        #: (ex: [``-l``, ``--list``]).  If a log-level argument is not wanted,
        #: set to ``None`` (default).
        log_level_argument = None

        #: The help description for the log level argument
        log_level_argument_help = 'logging level'

        #: Current Log Level
        log_level = None

    levels = ['INFO', 'WARNING', 'ERROR', 'DEBUG', 'FATAL']

    def __init__(self, *args, **kw):
        super(LoguruLogHandler, self).__init__(*args, **kw)
        self.app = None

    def _setup(self, app_obj):
        super(LoguruLogHandler, self)._setup(app_obj)

        self.backend = logger

        # hack for application debugging
        if is_true(self.app._meta.debug):
            self.app.config.set(self._meta.config_section, 'level', 'DEBUG')

        level = self.app.config.get(self._meta.config_section, 'level')
        self.set_level(level)

        LOG.debug("Loguru initialized using %s" %
                  self.__class__.__name__)

    def set_level(self, level):
        """
        Set the log level.  Must be one of the log levels configured in
        self.levels which are
        ``['INFO', 'WARNING', 'ERROR', 'DEBUG', 'FATAL']``.

        :param level: The log level to set.

        """
        level = level.upper()
        if level not in self.levels:
            level = 'INFO'
        self.backend.level(level)

        # self.backend.setLevel(level)

        # # console
        # self._setup_console_log()
        #
        # # file
        # self._setup_file_log()

    def get_level(self):
        """Returns the current log level."""
        return self._meta.log_level

    def _get_console_format(self):
        if self._meta.log_level == 'DEBUG':
            format = self._meta.debug_format
        else:
            format = self._meta.console_format

        return format

    def _get_file_format(self):
        if self._meta.log_level == 'DEBUG':
            format = self._meta.debug_format
        else:
            format = self._meta.file_format

        return format

    def _get_file_formatter(self, record):
        length = len(self._meta.file_format.format(**record))
        self._meta.padding = max(self._meta.padding, length)
        record["extra"]["padding"] = " " * (self._meta.padding - length)
        return self._meta.file_format

    def _get_console_formatter(self, record):
        length = len(self._meta.console_format.format(**record))
        self._meta.padding = max(self._meta.padding, length)
        record["extra"]["padding"] = " " * (self._meta.padding - length)
        return self._meta.console_format

    def _setup_console_log(self):
        """Add a console log handler."""
        to_console = self.app.config.get(self._meta.config_section,
                                         'to_console')
        if is_true(to_console):
            self._meta.sink = sys.stdout
            # self._meta.id = logger.add(self._meta.sink, format=format, backtrace=True)
            format = self._get_console_format()
            logger.remove(self._meta.id)
            self._meta.id = logger.add(self._meta.sink, format=format, backtrace=True)
        else:
            LOG.debug("The Log are not set to output to the console")

    def _setup_file_log(self):
        """Add a file log handler."""

        file_path = self.app.config.get(self._meta.config_section, 'file')
        # TODO: Perfecting file logging
        # rotate = self.app.config.get(self._meta.config_section, 'rotate')
        # max_bytes = self.app.config.get(self._meta.config_section,
        #                                 'max_bytes')
        # max_files = self.app.config.get(self._meta.config_section,
        #                                 'max_files')

        # if file_path:
        #     file_path = fs.abspath(file_path)
        #     log_dir = os.path.dirname(file_path)
        #     if not os.path.exists(log_dir):
        #         os.makedirs(log_dir)

        self._meta.sink = file_path
        # self._meta.id = logger.add(self._meta.sink, format=format, backtrace=True)
        format = self._get_file_format()
        logger.remove(self._meta.id)
        self._meta.id = logger.add(self._meta.sink, format=format, backtrace=True)

    def info(self, msg, *args, **kwargs):
        """
        Log to the INFO facility.

        Args:
            msg (str): The message to log.

        Keyword Args:
            namespace (str): A log prefix, generally the module ``__name__``
                that the log is coming from.  Will default to
                ``self._meta.namespace`` if none is passed.

        Other Parameters:
            kwargs: Keyword arguments are passed on to the backend logging
                system.

        """
        self.backend.info(msg, format=self._get_file_formatter)

    def warning(self, msg, *args, **kwargs):
        """
        Log to the WARNING facility.

        Args:
            msg (str): The message to log.

        Keyword Args:
            namespace (str): A log prefix, generally the module ``__name__``
                that the log is coming from.  Will default to
                ``self._meta.namespace`` if none is passed.

        Other Parameters:
            kwargs: Keyword arguments are passed on to the backend logging
                system.

        """

        self.backend.warning(msg, format=self._get_file_formatter)

    def error(self, msg, *args, **kwargs):
        """
        Log to the ERROR facility.

        :Args:
            msg (str): The message to log.

        Keyword Args:
            namespace (str): A log prefix, generally the module ``__name__``
                that the log is coming from.  Will default to
                ``self._meta.namespace`` if none is passed.

        Other Parameters:
            kwargs: Keyword arguments are passed on to the backend logging
                system.

        """

        self.backend.error(msg, format=self._get_file_formatter)

    def fatal(self, msg, *args, **kwargs):
        """
        Log to the FATAL (aka CRITICAL) facility.

        Args:
            msg (str): The message to log.

        Keyword Args:
            namespace (str): A log prefix, generally the module ``__name__``
                that the log is coming from.  Will default to
                ``self._meta.namespace`` if none is passed.

        Other Parameters:
            kwargs: Keyword arguments are passed on to the backend logging
                system.

        """

        self.backend.error(msg, format=self._get_file_formatter)

    def debug(self, msg, *args, **kwargs):
        """
        Log to the DEBUG facility.

        Args:
            msg (str): The message to log.

        Keyword Args:
            namespace (str): A log prefix, generally the module ``__name__``
                that the log is coming from.  Will default to
                ``self._meta.namespace`` if none is passed.

        Other Parameters:
            kwargs: Keyword arguments are passed on to the backend logging
                system.

        """
        self.backend.debug(msg, format=self._get_file_formatter)


def add_logguru_arguments(app):
    if app.log._meta.log_level_argument is not None:
        app.args.add_argument(*app.log._meta.log_level_argument,
                              dest='log_logging_level',
                              help=app.log._meta.log_level_argument_help,
                              choices=[x.lower() for x in app.log.levels])


def handle_logguru_arguments(app):
    if hasattr(app.pargs, 'log_logging_level'):
        if app.pargs.log_logging_level is not None:
            app.log.set_level(app.pargs.log_logging_level)
        if app.pargs.log_logging_level in ['debug', 'DEBUG']:
            app._meta.debug = True


def load(app):
    app.handler.register(LoguruLogHandler)
    app.hook.register('pre_argument_parsing', add_logguru_arguments)
    app.hook.register('post_argument_parsing', handle_logguru_arguments)