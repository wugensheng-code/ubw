
from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import ubwError
from .controllers.base import Base
from .ext.ext_loguru import LoguruLogHandler
from loguru import logger


class ubw(App):
    """ubw primary application."""

    class Meta:
        label = 'ubw'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'jinja2',
            'ubw.ext.ext_loguru'
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'loguru'

        # set the output handler
        output_handler = 'jinja2'

        # register handlers
        handlers = [
            Base,
            LoguruLogHandler
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
