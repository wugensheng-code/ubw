from os import getcwd
from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import ubwError
from .controllers.base import Base
from .ext.ext_loguru import LoguruLogHandler
from loguru import logger
from .ext.ext_build import BuildInterface
from .ext.ext_debug import DebugInterface
from .ext.ext_flash import FlashInterface

class ubw(App):
    """ubw primary application."""

    class Meta:
        label = 'ubw'

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            # 'yaml',
            # 'colorlog',
            'jinja2',
            'ubw.ext.ext_loguru',
            'ubw.ext.ext_build',
            'json'
        ]

        # List of config directories to search config files
        # (appended to the builtin list of directories defined by Cement).
        config_dirs = getcwd()

        # List of config files to parse
        # (appended to the builtin list of config files defined by Cement).
        config_files = [r'ubw.json']
        config_handler = 'json'
        config_file_suffix = '.json'
        # set the log handler
        log_handler = 'loguru'

        # set the output handler
        output_handler = 'jinja2'

        # register handlers
        handlers = [
            Base,
            LoguruLogHandler
        ]

        interfaces = [
            BuildInterface,
            DebugInterface,
            FlashInterface,
        ]


class ubwTest(TestApp,ubw):
    """A sub-class of ubw that is better suited for testing."""

    class Meta:
        label = 'ubw'


@logger.catch
def main():
    with ubw() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except ubwError as e:
            print('ubwError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
