""" Implementation of the command line interface.

"""
import sys
from argparse import ArgumentParser
from inspect import getargspec

from . import __version__
from .api.read_chart import read_chart, list_charts
from .core import config
from .core import logger

__all__ = "main",


def main(argv=None):
    """ Execute the application CLI.

    Arguments are taken from sys.argv by default.

    """
    argv = argv[1:]
    args = _args(argv)
    logger.start(args.warn)
    logger.debug("starting execution")
    config.load(args.config)
    config.core.logging = args.warn
    command = args.command
    args = vars(args)
    spec = getargspec(command)

    if not spec.keywords:
        # No kwargs, remove unexpected arguments.
        args = {key: args[key] for key in args if key in spec.args}
    try:
        command(**args)
    except RuntimeError as err:
        logger.critical(err)
        return 1
    logger.debug("successful completion")
    return 0
 

def _args(argv=None):
    """ Parse command line arguments.

    """
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", action="append",
            help="config file [etc/config.yml]")
    parser.add_argument("-v", "--version", action="version",
            version="resident {:s}".format(__version__),
            help="print version and exit")
    parser.add_argument("-w", "--warn", default="WARN",
            help="logger warning level [WARN]")
    common = ArgumentParser(add_help=False)  # common subcommand arguments
    common.add_argument("--name", "-n", default="World", help="greeting name")
    subparsers = parser.add_subparsers(title="subcommands")

    _read_chart(subparsers, common)
    _list_charts(subparsers, common)

    args = parser.parse_args(argv)

    if not args.config:
        # Don't specify this as an argument default or else it will always be
        # included in the list.
        args.config = "etc/config.yml"
    return args
 

def _read_chart(subparsers, common):
    """ CLI adaptor for the api.cmd1 command.

    """
    parser = subparsers.add_parser("read_chart", parents=[common])
    parser.set_defaults(command=read_chart)
    parser.add_argument("artist_id", type=str)
    parser.add_argument("chart_id", type=int)
    return

def _list_charts(subparsers, common):
    """ CLI adaptor for the api.cmd1 command.

    """
    parser = subparsers.add_parser("list_charts", parents=[common])
    parser.set_defaults(command=list_charts)
    parser.add_argument("artist_id", type=str)
    return
# Make the module executable.

if __name__ == "__main__":
    try:
        status = main(sys.argv)
    except:
        logger.critical("shutting down due to fatal error")
        raise  # print stack trace
    else:
        raise SystemExit(status)
