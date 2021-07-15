from ros2cli.command import add_subparsers
from ros2cli.command import CommandExtension
from ros2cli.verb import get_verb_extensions

class ShowCommand(CommandExtension):
    """The 'hello' command extension."""

    def add_arguments(self, parser, cli_name):
        self._subparser = parser
        verb_extensions = get_verb_extensions('rosshow.verb')
        add_subparsers(
            parser, cli_name, '_verb', verb_extensions, required=False)

    def main(self, *, parser, args):
        if not hasattr(args, '_verb'):
            self._subparser.print_help()
            return 0

        extension = getattr(args, '_verb')

        return extension.main(args=args)
