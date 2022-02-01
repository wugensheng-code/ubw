from os import getcwd
from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version
from cement import shell

VERSION_BANNER = """
The meta tool for RT-Thread %s
%s
""" % (get_version(), get_version_banner())


class Base(Controller):
    class Meta:
        label = 'base'

        # text displayed at the top of --help output
        description = 'The meta tool for RT-Thread'

        # text displayed at the bottom of --help output
        # epilog = 'Usage: ubw command1 --foo bar'

        # controller level arguments. ex: 'ubw --version'
        arguments = [
            ### add a version banner
            ( [ '-v', '--version' ],
              { 'action'  : 'version',
                'version' : VERSION_BANNER } ),
        ]


    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()


    # @ex(
    #     help='example sub command1',

    #     # sub-command level arguments. ex: 'ubw command1 --foo bar'
    #     arguments=[
    #         ### add a sample foo option under subcommand namespace
    #         ( [ '-f', '--foo' ],
    #           { 'help' : 'notorious foo option',
    #             'action'  : 'store',
    #             'dest' : 'foo' } ),
    #     ],
    # )
    # def command1(self):
    #     """Example sub-command."""

    #     data = {
    #         'foo' : 'bar'
    #     }

    #     ### do something with arguments
    #     if self.app.pargs.foo is not None:
    #         data['foo'] = self.app.pargs.foo

    #     self.app.render(data, 'command1.jinja2')


    @ex(
        help='Initialize the rt-thread workspace',

        # sub-command level arguments. ex: 'ubw command1 --foo bar'
        arguments=[
            ### add a sample foo option under subcommand namespace
            ( [ '-p', '--path' ],
              { 'help' : 'rt-thread workspace path',
                'action'  : 'store',
                'dest' : 'workspace_dir' } ),
            (['-u', '--url'],
             {'help': 'The mirror URL',
              'action': 'store',
              'dest': 'url'}),
        ],
    )

    def init(self):
        """Initialize the rt-thread workspace"""

        data = {
            'workspace_dir': getcwd(),
            'url': 'https://github.com/wugensheng-code/rt-thread'
        }

        ### do something with arguments
        if self.app.pargs.workspace_dir is not None:
            data['workspace_dir'] = self.app.pargs.workspace_dir

        if self.app.pargs.url is not None:
            data['url'] = self.app.pargs.url

        self.app.render(data, 'command1.jinja2')

        shell.cmd('git clone\u0020'+str(data['url'])+'\u0020'+str(data['workspace_dir']), False)




