#!/usr/bin/env python
# pylint: disable=line-too-long
"""
# Copyright 2023 by David Heurtevent.
# SPDX_LICENSE: MIT
# License: MIT License
# Author: David HEURTEVENT <david@heurtevent.org>

CLI - Print a log message in the console

Can use: python3 logtoconsole.py [message] -L [level] &>> /tmp/log.log
 to append it to the log file (/tmp/log.log is an example)
"""
import argparse
import logging
import sys

from fruafr.log.lib import templating
from fruafr.log.lib import common

# Defaults
LEVEL = 'info'
SEP = ' - '
OPTSEP = SEP

class Console(object):
    """Class Console
    Parses the command line arguments
    """

    def parse_args(self, args) -> argparse.Namespace:
        """Parse the arguments from the command line
        Args:
            args (list): the list of arguments from the command line
        Returns:
            the argparse.Namespace object containing the parsed arguments
        """
        parser = argparse.ArgumentParser(
            prog='CLI - Print log message to the console\n',
            description='Options after --nolevel modify the content of the message before it is logged.',
            epilog='Can use: python3 logtoconsole.py [message] -L [level] &>> /tmp/log.log to append it to the log file (/tmp/log.log is an example)')
        # arguments
        parser.add_argument('message',
                            help='The message to log. Ignored if -MES or --message is specified (please set it to . to avoid error messsages)')
        parser.add_argument('-L', '--level',
                            dest='level',
                            choices=['debug', 'info', 'warning', 'error', 'critical'],
                            default=f"{LEVEL}",
                            help=f"The level [debug, info, warning, error, critical]. [Default: {LEVEL}]")
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
                dest=option[1]['dest'],
                help=option[1]['help'],
                default=option[1]['default']
            )
        # return
        return parser.parse_args(args)

    def _prepare_fmt(self, args: argparse.Namespace) -> str:
        """Prepares the format string from the CLI arguments
        Args:
            args(argparse.Namespace): The CLI arguments
        Returns:
            str: The format string
        """
        # format if not provided
        if args.format is None:
            if args.noasctime:
                fmt = []
            else:
                fmt = ['%(asctime)s']
            if not args.nolevel:
                fmt.append('%(levelname)s')
            fmt.append('%(message)s')
            output = args.sep.join(fmt)
        else:
            output = args.format
        #return formatted string
        return output

    def _prepare_date_format(self, args: argparse.Namespace) -> str:
        """Prepares the date format string from the CLI arguments
        Args:
            args(argparse.Namespace): The CLI arguments
        Returns:
            str: The date format string
        """
        # date time format if not provided
        if args.dateformat is None:
            return None
        else:
            return args.dateformat

    def _prepare_level(self, args) -> int:
        """Prepares the date format string from the CLI arguments
        Args:
            args(argparse.Namespace): The CLI arguments
        Returns:
            int: The level integer
        """
        levelint = -1
        accepted_levels = ['debug', 'info', 'warning', 'error', 'critical']
        # reject if not an accepted level
        if args.level not in accepted_levels:
            print(f"LEVEL {args.level} is not recognized", file=sys.stderr)
            sys.exit(1)
        # format the output
        if args.level == 'info':
            levelint = logging.INFO
        elif args.level == 'debug':
            levelint = logging.DEBUG
        elif args.level == 'warning':
            levelint = logging.WARNING
        elif args.level == 'error':
            levelint = logging.ERROR
        else:
            levelint = logging.CRITICAL
        # return
        return levelint

    def _prepare_console_logger(self, fmt: str, datefmt: str) -> logging.Logger:
        """Prepares the console logger
        Args:
            fmt (str): the template format
            datefmt (str): the date format
        Return:
            loggign.Logger: The logger instance
        """
        # get the root logger
        logger = logging.getLogger('')
        # set the level of the root logger
        logger.setLevel(logging.DEBUG)
        # set the formatter
        formatter = logging.Formatter(fmt, datefmt)
        # set up logging to console
        console = logging.StreamHandler()
        # set logging level to lowest
        console.setLevel(logging.DEBUG)
        # set the format
        console.setFormatter(formatter)
        # add the handler to the root logger
        logger.addHandler(console)
        # return the root logger with the console attached to it
        return logger

    def _determine_list_options_to_template(self, args: argparse.Namespace) -> list:
        """Determine the list of options provided to template (in the message section of the log record)
        Args:
            args(argparse.Namespace): The CLI arguments
        Returns:
            list: The list of options provided to template (in the message section of the log record)
        """
        # list additional arguments set
        arguments_set = []
        for option in common.CLI_OPTIONS.keys():
            if hasattr(args, option):
                if getattr(args, option) != 'None' and getattr(args, option) is not None:
                    arguments_set.append(option)
        return arguments_set

    def _validate_list_options_to_template(self, options: str):
        """Validates the list of options to template
        Args:
            options (str): the list of options to validate (should be a string representing a comma\
                 separated list)
        Returns:
            list: if valid, the list if valid, otherwise raises ValueError.
            appends message to the list provided if not included in the list
        """
        # the options list must be a comma separated list
        try:
            orders = options.split(',')
        except AttributeError:
            print("order must be a comma(,) separated list", file=sys.stderr)
            sys.exit(1)
        # the options string must contain valid options
        for order in orders:
            # if not a valid option and message is an exception
            if order not in common.CLI_OPTIONS.keys() and order != 'message':
                k = ', '.join(common.CLI_OPTIONS.keys())
                print(f"OPTION no found. Must contain one or several options from: {k}", file=sys.stderr)
                sys.exit(1)
        # if message not found in order, add
        if 'message' not in orders:
            orders.append('message')
        #if valid, return order
        return orders

    def _prepare_variables_to_render(self, args: argparse.Namespace) -> dict:
        """Prepare variables to be rendered with the template
        Args:
            args(argparse.Namespace): The CLI arguments
        Returns:
            dict: The variables to be rendered
        """
        # elements to template
        elements_to_template = {}
        for elem in common.CLI_OPTIONS.keys():
            if hasattr(args, elem):
                if getattr(args, elem) is not None:
                    elements_to_template[elem] = getattr(args, elem)
        #add message
        elements_to_template['message'] = getattr(args, 'message')
        return elements_to_template

    def _apply_template(self, options: list, variables: dict, separator: str):
        """Apply the template to the options with the given variables
        Args:
            options(list): list of options to template
            variables(dict): dict of variables to apply the template to {option: variable}
            separator(str): string to separate the options with in the template
        Returns:
            str : the result of applying the template.
            Otherwise, raises ValueError
        """
        # prepare the template
        t = templating.Templating.create_template(options, separator)
        # validate the template
        validate = templating.Templating.validate_template(t, options)
        if validate is not None:
            raise ValueError(f"order must contain {validate}")
        # apply the template
        try:
            message = templating.Templating.apply_template(t, variables)
            return message
        except KeyError:
            print (f"Could not apply the template {t} with the variables provided\
                            {variables}", file=sys.stderr)
            sys.exit(1)

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
