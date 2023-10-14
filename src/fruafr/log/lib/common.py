"""
Contains common utils for the CLI
"""
# Copyright 2023 by David Heurtevent.
# SPDX_LICENSE: MIT
# License: MIT License
# Author: David HEURTEVENT <david@heurtevent.org>
import os
import yaml

# CONSTANTS
DEFAULT_FORMAT = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
TYPICAL_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
SIMPLE_FORMAT = '%(asctime)s - %(message)s'
BASIC_FORMAT = '%(levelname)s:%(name)s:%(message)s'
RAW_FORMAT = '%(message)s'

SYSLOG_FACILITIES = {
    'auth': 'LOG_AUTH',
    'authpriv': 'LOG_AUTHPRIV',
    'cron': 'LOG_CRON',
    'daemon': 'LOG_DAEMON',
    'ftp': 'LOG_FTP',
    'kern': 'LOG_KERN',
    'lpr': 'LOG_LPR',
    'mail': 'LOG_MAIL',
    'news': 'LOG_NEWS',
    'syslog': 'LOG_SYSLOG',
    'user': 'LOG_USER',
    'uucp': 'LOG_UUCP',
    'local0': 'LOG_LOCAL0',
    'local1': 'LOG_LOCAL1',
    'local2': 'LOG_LOCAL2',
    'local3': 'LOG_LOCAL3',
    'local4': 'LOG_LOCAL4',
    'local5': 'LOG_LOCAL5',
    'local6': 'LOG_LOCAL6',
    'local7': 'LOG_LOCAL7',
}

# Load the yaml configuration of logging supported options
path = os.path.dirname(__file__)
LOGGING_OPTIONS_FILE = f"{path}/logging_options.yaml"
LOGGING_OPTIONS = None
try:
    with open(LOGGING_OPTIONS_FILE, 'r', encoding='utf-8') as file:
        LOGGING_OPTIONS = yaml.safe_load(file)
except IOError as e:
    print(e)
    print(f"Could not open the logging options file {LOGGING_OPTIONS_FILE }")

# Load the yaml configuration of CLI options
CLI_OPTIONS_FILE = f"{path}/cli_options.yaml"
CLI_OPTIONS = None
try:
    with open(CLI_OPTIONS_FILE, 'r', encoding='utf-8') as file:
        CLI_OPTIONS = yaml.safe_load(file)
except IOError as e:
    print(e)
    print(f"Could not open the CLI options file {CLI_OPTIONS_FILE }")
