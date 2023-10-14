#!/usr/bin/env python3
"""
# Copyright 2023 by David Heurtevent.
# SPDX_LICENSE: MIT
# License: MIT License
# Author: David HEURTEVENT <david@heurtevent.org>

Test of fruafr.log.logtosyslog

Tests the CLI without requiring to launch the syslog server.
Most tests require the verbose and dryrun flags to be set.

The UDP/TCP connection is not tested in this test suite

"""
import unittest
import os
import subprocess

INTERPRETER = 'python3'
PATH = os.path.dirname(__file__)
SCRIPT = f"{PATH}/../src/fruafr/log/logtosyslog.py"

class TestLogToSysLog(unittest.TestCase):
    """Class LogToSysLog tests"""

    def _execute(self, add_args: list, sudo: bool = False) -> object:
        """Append the args to the command line and execute the command and return the result
        Args:
            add_args(list): list of additional arguments and options to append to the command line
            sudo(bool): whether to run the command in sudo mode
        Returns:
            The output object of subprocess.run
        """
        # Append the args to the command line
        if sudo:
            cmd_line_args = ['sudo']
        else:
            cmd_line_args = []
        cmd_line_args.append(INTERPRETER)
        cmd_line_args.append(SCRIPT)
        cmd_line_args += add_args
        # Execute the command and return the result
        p = subprocess.run(cmd_line_args, capture_output=True, text=True, check=False)
        return p

    def test_missing_message(self):
        """Test command line with missing message"""
        p = self._execute([])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn(": error: the following arguments are required: message", stderr)

    def test_help(self):
        """Test command line with help"""
        # test with short option
        p = self._execute(['-h'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stderr)
        self.assertIn('usage: CLI - Send a log message to a syslog server', stdout)
        # test with long option
        p = self._execute(['--help'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stderr)
        self.assertIn('usage: CLI - Send a log message to a syslog server', stdout)

    def test_normal_verbose_dryrun(self):
        """Test command line with message
        Uses verbose mode and dry run mode
        """
        # Test short option
        p = self._execute(['test1', '-v', '-d'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        # INFO must be before test1
        self.assertLess(stderr.index("INFO"),stderr.index("test1"))
        # Test long options
        p = self._execute(['test1', '--verbose', '--dryrun'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        # INFO must be before test1
        self.assertLess(stderr.index("INFO"),stderr.index("test1"))

    def test_address_port(self):
        """Test address and port
        with file : /dev/log
        with host: localhost
        wih ip: 127.0.0.1
        with port set to a custom port (5140)
        Uses verbose mode and dry run mode
        """
        # TEST WITH FILE
        # Test short option
        p = self._execute(['test1','-a', '/dev/test', '-v', '-d'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        # INFO must be before test1
        self.assertLess(stderr.index("INFO"),stderr.index("test1"))
        # Test long options
        p = self._execute(['test1', '--addr', '/dev/test', '--verbose', '--dryrun'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        # INFO must be before test1
        self.assertLess(stderr.index("INFO"),stderr.index("test1"))
        # TEST WITH HOST
        p = self._execute(['test1', '-a', 'localhost', '--verbose', '--dryrun'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        # INFO must be before test1
        self.assertLess(stderr.index("INFO"),stderr.index("test1"))
        # TEST WITH IP ADDRESS
        p = self._execute(['test1', '-a', '127.0.0.1', '--verbose', '--dryrun'])
        stdout = p.stdout
        stderr = p.stderr
        # TEST WITH PORT SET
        p = self._execute(['test1', '-a', '127.0.0.1', '-p', '5140', '--verbose', '--dryrun'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        # INFO must be before test1
        self.assertLess(stderr.index("INFO"),stderr.index("test1"))

    def test_facility(self):
        """Test facility
        """
        # Test short option
        p = self._execute(['test1', '-F', 'auth', '-v', '-d'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        # INFO must be before test1
        self.assertLess(stderr.index("INFO"),stderr.index("test1"))
        # Test long options
        p = self._execute(['test1', '--facility', 'auth', '--verbose', '--dryrun'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        # INFO must be before test1
        self.assertLess(stderr.index("INFO"),stderr.index("test1"))
        # TEST WITH INEXISTING FACILITY (should be impossible)
        p = self._execute(['test1', '-F', 'myfacility', '--verbose', '--dryrun'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("You must specify a facility from the following", stderr)
        self.assertNotIn("INFO", stderr)
        self.assertNotIn(" - ", stderr)
        self.assertNotIn("test1", stderr)

    def test_program(self):
        """Test program
        """
        # Test short option
        p = self._execute(['test1', '-P', 'testprog', '-v', '-d'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        self.assertIn("testprog", stderr)
        # INFO must be before test1
        self.assertLess(stderr.index("INFO"),stderr.index("test1"))
        # Test long options
        p = self._execute(['test1', '--program', 'testprog', '--verbose', '--dryrun'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        self.assertIn("testprog", stderr)
        # INFO must be before test1
        self.assertLess(stderr.index("INFO"),stderr.index("test1"))

    def test_level(self):
        """Test command line with level
        Uses verbose mode and dry run mode
        """
        # test with short option
        p = self._execute(['test1', '-L', 'debug',
                           '-v', '-d'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("DEBUG", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        # test with long option
        p = self._execute(['test1', '--level', 'debug',
                           '--verbose', '--dryrun'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("DEBUG", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        # test with a non-existing level
        p = self._execute(['test1', '--level', 'newlevel',
                           '--verbose', '--dryrun'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        error_msg = ': error: argument -L/--level:'
        self.assertIn(error_msg, stderr)

    def test_separator(self):
        """Test command line with message
        Uses verbose mode and dry run mode
        """
        # test with short option
        p = self._execute(['test1', '-s', ':', '-v', '-d'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("INFO", stderr)
        self.assertNotIn(" - ", stderr)
        self.assertIn("test1", stderr)
        self.assertIn("INFO:logtosyslog test1", stderr)
        # test with long option
        p = self._execute(['test1', '--sep', ':',
                           '--verbose', '--dryrun'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("INFO", stderr)
        self.assertNotIn(" - ", stderr)
        self.assertIn("test1", stderr)
        self.assertIn("INFO:logtosyslog test1", stderr)

    def test_format(self):
        """Test format
        Uses verbose mode and dry run mode
        """
        fmt = "%(message)s"
        # test with short option
        p = self._execute(['test1', '-f', fmt,
                           '-v', '-d'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertNotIn("INFO", stderr)
        self.assertNotIn(" - ", stderr)
        self.assertIn("test1", stderr)
        # test with long option
        p = self._execute(['test1', '--format', fmt,
                           '--verbose', '--dryrun'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertNotIn("INFO", stderr)
        self.assertNotIn(" - ", stderr)
        self.assertIn("test1", stderr)
        # test with format error
        p = self._execute(['test1', '--format', 'newlevel',
                           '--verbose', '--dryrun'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("ValueError", stderr)

    def test_date_format(self):
        """Test date format
        Uses verbose mode and dry run mode
        """
        dfmt = "%H"
        # test with short option
        p = self._execute(['test1', '-df', dfmt, '-v', '-d'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        ## date should be removed
        self.assertEqual(5, stderr.count(" "))
        ## should be an hour
        self.assertLess(int(stderr.split(" ")[0]), 24)
        # test with long option
        p = self._execute(['test1', '--dateformat', dfmt,
                           '--verbose', '--dryrun'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        ## date should be removed
        self.assertEqual(5, stderr.count(" "))
        ## should be an hour
        self.assertLess(int(stderr.split(" ")[0]), 24)

    def test_no_asctime(self):
        """Test no asctime
        Uses verbose mode and dry run mode
        """
        p = self._execute(['test1', '--noasctime',
                           '-v', '-d'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        ## datetime should be removed
        self.assertEqual(3, stderr.count(" "))

    def test_nolevel(self):
        """Test no level
        Uses verbose mode and dry run mode
        """
        p = self._execute(['test1', '--nolevel',
                           '-v', '-d'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertNotIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        ## level should be removed
        self.assertEqual(4, stderr.count(" "))

    def test_options_valid_with_value(self):
        """Test options valid case
         with option value provided
        Uses verbose mode and dry run mode
        """
        ## test with short option
        p = self._execute(['test1', '-o', 'ip', '--ip', '127.0.0.1',
                           '-v', '-d'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        # test with long option
        p = self._execute(['test1', '--options', 'ip', '--ip', '127.0.0.1',
                           '--verbose', '--dryrun'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)

    def test_options_valid_with_message_option(self):
        """Test options valid case
         with message option value provided
        Uses verbose mode and dry run mode
        """
        ## test with short option
        p = self._execute(['test1', '-o', 'message,ip', '--ip', '127.0.0.1',
                           '-v', '-d'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        # message must be before the IP given the message,ip options order
        self.assertLess(stderr.index("test1"),stderr.index("127.0.0.1"))
        # test with long option
        p = self._execute(['test1', '--options', 'message,ip', '--ip', '127.0.0.1',
                           '--verbose', '--dryrun'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        # message must be before the IP given the message,ip options order
        self.assertLess(stderr.index("test1"),stderr.index("127.0.0.1"))

    def test_options_valid_without_value(self):
        """Test options without matching option value provided
           should not be able to apply the template
        Uses verbose mode and dry run mode
        """
        ## test with short option
        p = self._execute(['test1', '-o', 'ip',
                           '-v', '-d'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("Could not apply the template $ip - $message", stderr)
        # test with long option
        p = self._execute(['test1', '--options', 'ip',
                           '--verbose', '--dryrun'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("Could not apply the template $ip - $message", stderr)

    def test_options_invalid_inexisting_option(self):
        """Test options without an inexisting option
        Uses verbose mode and dry run mode
        """
        ## test with short option
        p = self._execute(['test1', '-o', 'newoption',
                           '-v', '-d'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("OPTION no found. ", stderr)
        # test with long option
        p = self._execute(['test1', '--options', 'newoption',
                           '--verbose', '--dryrun'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("OPTION no found. ", stderr)

    def test_optsep(self):
        """Test options with another option separator
        Uses verbose mode and dry run mode
        """
        ## test with short option
        p = self._execute(['test1', '-o', 'message,ip',
                           '--ip', '127.0.0.1', '-osep', ';',
                           '-v', '-d'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        self.assertIn(";", stderr)
        self.assertIn("test1;127.0.0.1", stderr)
        # test with long option
        p = self._execute(['test1', '--options', 'message,ip',
                           '--ip', '127.0.0.1','--optsep', ';',
                           '--verbose', '--dryrun'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        self.assertIn(";", stderr)
        self.assertIn("test1;127.0.0.1", stderr)


def main():
    """Main"""
    unittest.main()


if __name__ == "__main__":
    main()
