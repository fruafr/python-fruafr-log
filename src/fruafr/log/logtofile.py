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
import sys

from fruafr.log.lib import common
from fruafr.log import logtoconsole

# Defaults
DEFAULT_LOG_FILE = '/tmp/fruafr-log-logtofile.log'
LEVEL = 'info'
MODE = 'a'
ENCODING = 'utf-8'
SEP = ' - '
OPTSEP = SEP

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
                        prog='CLI - Save a log message to a log file\n',
                        description='Options after --nolevel modify the content of the message before it is logged.',
                        epilog='No output is written to the console by default (to override, use -v or --verbose)')
        # arguments
        parser.add_argument('message',
                            help='The message to log. Ignored if -MES or --message is specified (please set it to . to avoid error messsages)')
        parser.add_argument('-L', '--level',
                            dest='level',
                            choices=['debug', 'info', 'warning', 'error', 'critical'],
                            default=f"{LEVEL}",
                            help=f"The level [debug, info, warning, error, critical]. [Default: {LEVEL}]")
        parser.add_argument('-F', '--file',
                            dest='file',
                            help=f"log file path. [Default: { DEFAULT_LOG_FILE }]",
                            default=f"{ DEFAULT_LOG_FILE }")
        parser.add_argument('-m', '--mode',
                            dest='mode',
                            help=f"File mode (a for append, w to write/overwrite the file). [Default is {MODE}]",
                            default=f"{MODE}")
        parser.add_argument('-e', '--encoding',
                            dest='encoding',
                            help=f"Encoding. [Default: {ENCODING}]",
                            default=f"{ENCODING}")
        parser.add_argument('-s', '--sep',
                            dest='sep',
                            help=f"Separator [Default: {SEP}]",
                            default=f"{SEP}")
        parser.add_argument('-f', '--format',
                            dest='format',
                            help='Python logging format')
        parser.add_argument('-df', '--dateformat',
                            dest='dateformat',
                            help='Datetime format')
        parser.add_argument('-v', '--verbose',
                            action='store_true',
                            dest='verbose',
                            default=False,
                            help='Verbose output')
        # Additional flags
        parser.add_argument('--noasctime',
                            dest='noasctime',
                            action='store_true',
                            default=False,
                            help='Removes asctime')
        parser.add_argument('--nolevel',
                            dest='nolevel',
                            action='store_true',
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

    def _prepare_file_logger(self,
                             filename: str,
                             fmt: str,
                             datefmt: str,
                             mode:str ='a',
                             encoding:str ='utf-8') -> logging.Logger:
        """Prepares the file logger
        Args:
            filename (str): The filepath to the log file
            fmt (str): the template format
            datefmt (str): the date format
            mode (str): The mode to use for the log file ('a' for append, 'w' for writing)\
                  [default: 'a']
            encoding (str): the encoding [default: 'utf-8']
        Returns:
            The logger instance
        """
        # get the root logger
        logger = logging.getLogger('')
        # set the level of the root logger
        logger.setLevel(logging.DEBUG)
        # set the formatter
        formatter = logging.Formatter(fmt, datefmt)
        # add the file handler
        fileh = logging.FileHandler(filename, mode, encoding)
        fileh.setFormatter(formatter)
        fileh.setLevel(logging.DEBUG)
        logger.addHandler(fileh)
        # return the root logger with the console attached to it
        return logger

    def process(self, args: argparse.Namespace):
        """Process the command line arguments
        Args:
            args (argparser.Namespace): Command line arguments
        """
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
        # create the file logger and obtain it
        logger = self._prepare_file_logger(args.file, fmt, date_format, args.mode, args.encoding)
        if args.verbose:
            # create the logger and obtain it
            logger = self._prepare_console_logger(fmt, date_format)
        # log the message
        logger.log(levelint, message)

def main():
    """Main : CLI logic"""
    # parse arguments
    args = Console().parse_args(sys.argv[1:])
    # process arguments
    Console().process(args)


if __name__ == "__main__":
    main()
