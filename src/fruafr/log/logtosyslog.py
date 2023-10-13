#!/usr/bin/env python
# pylint: disable=line-too-long
"""
# Copyright 2023 by David Heurtevent.
# SPDX_LICENSE: MIT
# License: MIT License
# Author: David HEURTEVENT <david@heurtevent.org>

CLI - Save a log message to a log file

No output is written to the console by default (otherwise, use verbose)

"""
import argparse
import logging
from logging import handlers
import sys
import socket

from fruafr.log.lib import common
from fruafr.log import logtoconsole

# Defaults
DEFAULT_LOG_FILE = '/tmp/python-tinysyslogserver.log'
LEVEL = 'info'
SEP = ' - '
OPTSEP = SEP
DEFAULT_SYSLOG_ADDR = '/dev/log'
DEFAULT_SYSLOG_PORT = '514'


class Console(logtoconsole.Console):
    """Class Console
    Parses the command line arguments
    Extends/Replaces logtoconsole.Console
    """
    def parse_args(self, args) -> argparse.Namespace:
        """Parse the arguments from the command line
        Args:
            args (list): the list of arguments from the command line
        Returns:
            the argparse.Namespace object containing the parsed arguments
        """
        parser = argparse.ArgumentParser(
                        prog = 'CLI - Send a log message to a syslog server\n',
                        description = 'Options after --nolevel modify the content of the message before it is logged.',
                        epilog = 'No output is written to the console by default (to override, use -v or --verbose)')
        # arguments
        parser.add_argument('message',
            help='The message to log. Ignored if -MES or --message is specified (please set it to . to avoid error messsages)')
        parser.add_argument('-L', '--level',
                            dest='level',
                            choices=['debug', 'info', 'warning', 'error', 'critical'],
                            default=f"{LEVEL}",
                            help=f"The level [debug, info, warning, error, critical]. [Default: {LEVEL}]")
        parser.add_argument('-a', '--addr', dest='addr',
            help=f"syslog address. can be localhost or a DNS name or an IP address or a string. [Default:{DEFAULT_SYSLOG_ADDR}]",
            default=f"{DEFAULT_SYSLOG_ADDR}")
        parser.add_argument('-p', '--port', dest='port',
            default=f"{DEFAULT_SYSLOG_PORT}",
            help=f"syslog port [Defauls: {DEFAULT_SYSLOG_PORT}]")
        parser.add_argument('-F', '--facility', dest='facility',
            default='user',
            help='syslog facility [Default: user]')
        parser.add_argument('-t', '--tcp', dest='tcp', action='store_true',
            default=False,
            help='syslog port is tcp [Defauls is udp]')
        parser.add_argument('-P', '--program', dest='program',
            default='logtosyslog',
            help='program [Defauls is logtosyslog]')
        parser.add_argument('-s', '--sep',
                            dest='sep',
                            help=f"Separator [Default: {SEP}]",
                            default=f"{SEP}")
        parser.add_argument('-f', '--format', dest='format',
            help='Python logging format')
        parser.add_argument('-df', '--dateformat', dest='dateformat',
            help='Datetime format')
        parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
            default=False,
            help='Verbose output')
        parser.add_argument('-d', '--dryrun', action='store_true', dest='dryrun',
            default=False,
            help='Dry run - Generate log message on console without sending it over syslog. Used for debugging')
        # Additional flags
        parser.add_argument('--noasctime', dest='noasctime', action='store_true',
            default=False,
            help='Removes asctime')
        parser.add_argument('--nolevel', dest='nolevel', action='store_true',
            default=False,
            help='Removes level')
        # Additional arguments that can be passed to append to the message beforehand
        parser.add_argument('-o', '--options',
                            dest='options',
                            help='order of optional fields to template (comma separated string). Values not in this option are ignored even when provided to the cli')
        parser.add_argument('-osep', '--optsep',
                            dest='optsep',
                            help=f"Separator for the additional options [Default: {OPTSEP}]",
                            default=f"{OPTSEP}")
        for option in common.CLI_OPTIONS.items():
            parser.add_argument(
                option[1]['short_option'],
                option[1]['long_option'],
                dest = option[1]['dest'],
                help = option[1]['help'],
                default = option[1]['default']
            )
        # return
        return parser.parse_args(args)

    def _prepare_sys_logger(self,
                             addr: str,
                             facility: int,
                             fmt: str,
                             datefmt: str,
                             socktype: int = socket.SOCK_DGRAM,
                             port: str = DEFAULT_SYSLOG_PORT,
                            ) -> logging.Logger:
        """Prepares the file logger
        Args:
            addr (str): host or address in the /var/log format
            facility (int): facility value found in common.SYSLOG_FACILITIES
            fmt (str): the template format
            datefmt (str): the date format
            socktype (int): socket type [defaults to socket.SOCK_DGRAM]
            port (str): the port [defaults to DEFAULT_SYSLOG_PORT (normally 514)]
        Returns:
            The logger instance
        """
        # get the root logger
        logger = logging.getLogger('')
        # set the level of the root logger
        logger.setLevel(logging.DEBUG)
        # set the formatter
        formatter = logging.Formatter(fmt, datefmt)
        # handle address:
        if addr[0] == '/':
            address = addr
        else:
            address = (addr, int(port))
        # create the syslog handler
        syslogh = handlers.SysLogHandler(address, facility, socktype)
        # set formatter
        syslogh.setFormatter(formatter)
        # set level
        syslogh.setLevel(logging.DEBUG)
        # add handler
        logger.addHandler(syslogh)
        # return logger
        return logger

    def _determine_facility(self, args:argparse.Namespace) -> int:
        """Determine the facility from the given arguments
        Args:
            args (argparse.Namespace): the CLI arguments
        Returns:
            int: the facility integer
        """
        k = common.SYSLOG_FACILITIES.keys()
        if not args.facility in k:
            facilities = ','.join(k)
            print(f"You must specify a facility from the following list: {facilities}", file=sys.stderr)
            sys.exit(1)
        facility = getattr(handlers.SysLogHandler, common.SYSLOG_FACILITIES[str(args.facility)])
        return facility

    def _determine_socktype(self, args:argparse.Namespace) -> int:
        """Determine the type of socket from the given arguments
        Args:
            args (argparse.Namespace): the CLI arguments
        Returns:
            int: the socket integer
        """
        if args.tcp :
            socktype = socket.SOCK_STREAM
        else:
            socktype = socket.SOCK_DGRAM
        return socktype

    def process(self, args: argparse.Namespace):
        """Process the command line arguments
        Args:
            args (argparser.Namespace): Command line arguments
        """
        if args.addr is not None and args.port is None:
            raise ValueError("if you provide a remote or localhost address, --port must be specified")
        # determine the list of command line options to template in the message part
        # of the log record
        if args.options is None:
            options = self._determine_list_options_to_template(args)
        else:
            options = self._validate_list_options_to_template(args.options)
        # prepate the variables
        if options is not None and options != []:
            variables = self._prepare_variables_to_render(args)
            message= self._apply_template(options, variables, args.optsep)
        else:
            message = args.message
        # determine the format
        fmt = self._prepare_fmt(args)
        # determine the date format
        date_format = self._prepare_date_format(args)
        # determine the levelint
        levelint = self._prepare_level(args)
        # create the sys logger and obtain it
        facility = self._determine_facility(args)
        socktype = self._determine_socktype(args)
        # create the syslogger if not dry run
        if not args.dryrun:
            logger = self._prepare_sys_logger(args.addr, facility, fmt, date_format,
                                            socktype, args.port)
        if args.verbose:
            # create the logger and obtain it
            logger = self._prepare_console_logger(fmt, date_format)
        # log the message
        new_message = f"{args.program} {message}"
        logger.log(levelint, new_message)

def main():
    """Main : CLI logic"""
    # parse arguments
    args = Console().parse_args(sys.argv[1:])
    # process arguments
    Console().process(args)


if __name__ == "__main__":
    main()
