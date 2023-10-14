#!/usr/bin/env python
# pylint: disable=line-too-long
"""
Tiny Syslog Server in Python.

This is a tiny syslog server that is able to receive syslog messages via both UDP and TCP.
It saves the log messages to a file (specified with the -F --file option).
It can display on the console using the --verbose (-v) option.
It requires sudo permission to start the server.
It uses two processes (one for UDP and one for TCP)

Originally inspired by:
- by: https://gist.github.com/marcelom/4218010 (pysyslog.py for UDP)
- by: https://stackoverflow.com/questions/61633410/how-do-i-accept-tcp-and-udp
    (for UDP and TCP threading)
"""
# Copyright 2023 by David Heurtevent.
# SPDX_LICENSE: MIT
# License: MIT License
# Author: David HEURTEVENT <david@heurtevent.org>

import logging
import argparse
import socketserver
import sys
import multiprocessing

from fruafr.log import logtoconsole

# Defaults
DEFAULT_LOG_FILE = '/tmp/fruafr-log-tinysyslogserver.log'
ADDRESS = "0.0.0.0"
PORT = 514
LEVEL = 'info'
MODE = 'a'
ENCODING = 'utf-8'
POLL_INTERVAL = 0.1
SEP = ' '

class Console(logtoconsole.Console):
    """Class Console
    Extends logtoconsole.Console
    """
    def parse_args(self, args) -> argparse.Namespace:
        """Parse the arguments from the command line
        Args:
            args (list): the list of arguments from the command line
        Returns:
            the argparse.Namespace object containing the parsed arguments
        """
        parser = argparse.ArgumentParser(
                        prog = 'Tiny UDP/TCP syslog server\n',
                        description = 'It saves the log messages to a file (specified with the -F --file option). It can display on the console using the --verbose (-v) option.',
                        epilog = 'Requires sudo permission to start the server.')
        # arguments
        parser.add_argument('-a', '--address',
                            dest='address',
                            help=f"IP Address of the server host [Default: {ADDRESS}]",
                            default=ADDRESS)
        parser.add_argument('-p', '--port',
                            dest='port',
                            default=PORT,
                            help=f"syslog port [Defauls is {PORT}")
        parser.add_argument('-F', '--file',
                            dest='file',
                            help=f"log file path. Default is { DEFAULT_LOG_FILE }: ",
                            default=f"{ DEFAULT_LOG_FILE }")
        parser.add_argument('-e', '--encoding',
                            dest='encoding',
                            help=f"Encoding. Default is { ENCODING }",
                            default=f"{ ENCODING }")
        parser.add_argument('-m', '--mode',
                            dest='mode',
                            help=f"File mode (a for append, w to write/overwrite the file). Default is {MODE}",
                            default=f"{MODE}")
        parser.add_argument('-f', '--format',
                            dest='format',
                            help='Python logging format')
        parser.add_argument('-df', '--dateformat',
                            dest='dateformat',
                            help='Datetime format')
        parser.add_argument('-L', '--level',
                            dest='level',
                            choices=['debug', 'info', 'warning', 'error', 'critical'],
                            default=f"{LEVEL}",
                            help=f"The level [debug, info, warning, error, critical]. [Default:{LEVEL}")
        parser.add_argument('-s', '--sep',
                            dest='sep',
                            help=f"Separator [Default: {SEP}]",
                            default=f"{SEP}")
        parser.add_argument('-nou', '--noudp', dest='noudp', action='store_true',
                            default=False,
                            help='syslog port is NOT udp [Defauls is False]')
        parser.add_argument('-t', '--tcp', dest='tcp', action='store_true',
            default=False,
            help='syslog port is tcp [Defauls is false as udp]')
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
        parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
            default=False,
            help='Verbose output')
        # return
        return parser.parse_args(args)

    def _prepare_file_logger(self,
                             filename: str,
                             fmt: str,
                             datefmt: str,
                             mode:str =MODE,
                             encoding:str = ENCODING) -> logging.Logger:
        """Prepares the file logger
        Args:
            filename (str): The filepath to the log file
            fmt (str): the template format
            datefmt (str): the date format
            mode (str): The mode to use for the log file ('a' for append, 'w' for writing) [default: MODE (should be 'a')]
            encoding (str): the encoding [default: ENCODING (should be 'utf-8')]
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

    def process(self, args: argparse.Namespace) -> set:
        """Process the command line arguments
        Args:
            args (argparser.Namespace): Command line arguments
        Returns:
            set: UDPServer, TCPserver
        """
        # determine the format
        fmt = self._prepare_fmt(args)
        # determine the date format
        date_format = self._prepare_date_format(args)
        # create the file logger and obtain it
        self._prepare_file_logger(args.file, fmt, date_format, args.mode, args.encoding)
        if args.verbose:
            # create the logger and obtain it
            self._prepare_console_logger(fmt, date_format)
        # create the server object
        server_tcp = None
        server_udp = None
        # if UDP server
        if not args.noudp:
            server_udp = socketserver.UDPServer((args.address, int(args.port)), SyslogUDPHandler)
        # if TCP server
        if args.tcp:
            server_tcp = socketserver.TCPServer((args.address, int(args.port)), SyslogTCPHandler)
        # return the server
        return (server_udp, server_tcp)

class SyslogUDPHandler(socketserver.BaseRequestHandler):
    """Syslog UDP handler handles UDP requests"""

    def handle(self):
        data = str(bytes.decode(self.request[0].strip()))
        clientip = self.client_address[0]
        message = f"{clientip}-{data}"
        # log the message
        logger = logging.getLogger('')
        logger.info(message)

class SyslogTCPHandler(socketserver.BaseRequestHandler):
    """Syslog TCP handler handles TCP requests"""

    def handle(self):
        data = self.request.recv(1024).strip()
        clientip = self.client_address[0]
        message = f"{clientip}-{data}"
        # log the message
        logger = logging.getLogger('')
        logger.info(message)

def udp_listen(server):
    """Listen to udp traffic"""
    while True:
        server.serve_forever(poll_interval=POLL_INTERVAL)

def tcp_listen(server):
    """Listen to tcp traffic"""
    while True:
        server.serve_forever(poll_interval=POLL_INTERVAL)

def main():
    """Main : CLI logic"""
    # parse arguments
    args = Console().parse_args(sys.argv[1:])
    # process arguments
    servers = Console().process(args)
    # start serving
    try:
        print("SYSLOG server starting...")
        # prepare the UDP and the TCP threads
        if not args.noudp:
            print(f"SYSLOG server starting with : {args.address}:{args.port}/UDP ...", file=sys.stdout)
            t1 = multiprocessing.Process(target=udp_listen, args=(servers[0],))
        if args.tcp:
            print(f"SYSLOG server starting with : {args.address}:{args.port}/TCP ...", file=sys.stdout)
            t2 = multiprocessing.Process(target=tcp_listen, args=(servers[1],))
        # print  messages
        print("Do not forget to open the port in your firewall if necessary (if not running on localhost)")
        print("Waiting for connections...")
        # start the threads
        if not args.noudp:
            t1.start()
        if args.tcp:
            t2.start()
        # join the threads
        if not args.noudp:
            t1.join()
        if args.tcp:
            t2.join()
    except (IOError, SystemExit) as e:
        raise IOError(str(e)) from e
    except KeyboardInterrupt:
        if not args.noudp:
            t1.terminate()
        if args.tcp:
            t2.terminate()
        print (" Crtl+C Pressed.\n SYSLOG server shutting down.")

if __name__ == "__main__":
    main()
