#!/usr/bin/env python3
# pylint: disable=line-too-long
# pylint: disable=protected-access
"""
Test of fruafr.log.logtofile
"""
# Copyright 2023 by David Heurtevent.
# SPDX_LICENSE: MIT
# License: MIT License
# Author: David HEURTEVENT <david@heurtevent.org>

import unittest
import os
import subprocess

INTERPRETER = 'python3'
PATH = os.path.dirname(__file__)
SCRIPT = f"{PATH}/../src/fruafr/log/logtofile.py"
TEST_LOG_FILE = "/tmp/fruafr-log-logtofile-test.txt"

class TestLogToFile(unittest.TestCase):
    """Class LogToFile tests"""

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

    def _check_test_log_file_exists(self, path: str = TEST_LOG_FILE) -> bool:
        """Check that the output file exists
        Args:
            path(str): path to check
        Returns:
            bool: True if the output file exists
        """
        return (os.path.exists(path) and os.path.isfile(path))

    def _remove_test_log_file(self, path: str = TEST_LOG_FILE):
        """Remove the output test file
        Args:
            path(str): path to check
        """
        if os.path.exists(path):
            os.remove(path)

    def _read_test_log_file(self, path: str = TEST_LOG_FILE) -> list:
        """Read the test log file and return its content
        Args:
            path(str): path to check
        Returns:
            list of lines
        """
        with open(path, 'r', encoding='utf-8') as f:
            return f.readlines()

    def _check_in_file(self, line_to_check: str, path: str = TEST_LOG_FILE) -> int:
        """Check if the given line is in the given file
        Args:
            line_to_check(str): line content to find in the file
            path(str): path to check
        Returns:
            int : line number last found, -1 otherwise
        """
        found = -1
        n = 1
        lines = self._read_test_log_file(path)
        for line in lines:
            if line_to_check in line:
                found = n
            n+=1
        return found

    def setUp(self):
        """Remove the log file on set Up"""
        self._remove_test_log_file()

    def tearDown(self):
        """Remove the log file on set Down"""
        self._remove_test_log_file()

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
        self.assertIn("usage: CLI - Save a log message to a log file", stdout)
        # test with long option
        p = self._execute(['--help'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stderr)
        self.assertIn("usage: CLI - Save a log message to a log file", stdout)

    def test_normal_with_message_file(self):
        """Test command line with message and file"""
        # Test short option
        p = self._execute(['test1', '-F', TEST_LOG_FILE])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        # should not display anything without verbose option
        self.assertEqual('', stderr)
        # check file is created
        self.assertTrue(self._check_test_log_file_exists())
        self.assertGreater(self._check_in_file("INFO"), -1)
        self.assertGreater(self._check_in_file(" - "), -1)
        self.assertGreater(self._check_in_file("test1"), -1)
        self._remove_test_log_file()
        # Test long options
        p = self._execute(['test1', '--file', TEST_LOG_FILE])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        # should not display anything without verbose option
        self.assertEqual('', stderr)
        # check file is created
        self.assertTrue(self._check_test_log_file_exists())
        self.assertGreater(self._check_in_file("INFO"), -1)
        self.assertGreater(self._check_in_file(" - "), -1)
        self.assertGreater(self._check_in_file("test1"), -1)
        self._remove_test_log_file()

    def test_normal_verbose(self):
        """Test command line with message and file in verbose mode"""
        # Test short option
        p = self._execute(['test1', '-F', TEST_LOG_FILE, '-v'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        # should display with verbose option
        self.assertNotEqual('', stderr)
        self.assertIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        # check file is created
        self.assertTrue(self._check_test_log_file_exists())
        self.assertGreater(self._check_in_file("INFO"), -1)
        self.assertGreater(self._check_in_file(" - "), -1)
        self.assertGreater(self._check_in_file("test1"), -1)
        self._remove_test_log_file()
        # Test long options
        p = self._execute(['test1', '--file', TEST_LOG_FILE, '--verbose'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        # should display with verbose option
        self.assertNotEqual('', stderr)
        self.assertIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        # check file is created
        self.assertTrue(self._check_test_log_file_exists())
        self.assertGreater(self._check_in_file("INFO"), -1)
        self.assertGreater(self._check_in_file(" - "), -1)
        self.assertGreater(self._check_in_file("test1"), -1)
        self._remove_test_log_file()

    def test_level(self):
        """Test command line with level"""
        # test with short option
        p = self._execute(['test1', '-F', TEST_LOG_FILE, '-L', 'debug'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertTrue(self._check_test_log_file_exists())
        self.assertGreater(self._check_in_file("DEBUG"), -1)
        self.assertGreater(self._check_in_file(" - "), -1)
        self.assertGreater(self._check_in_file("test1"), -1)
        self._remove_test_log_file()
        # test with long option
        p = self._execute(['test1', '-F', TEST_LOG_FILE, '--level', 'debug'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertTrue(self._check_test_log_file_exists())
        self.assertGreater(self._check_in_file("DEBUG"), -1)
        self.assertGreater(self._check_in_file(" - "), -1)
        self.assertGreater(self._check_in_file("test1"), -1)
        self._remove_test_log_file()
        # test with a non-existing level
        p = self._execute(['test1', '-F', TEST_LOG_FILE, '--level', 'newlevel'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        error_msg = ': error: argument -L/--level:'
        self.assertIn(error_msg, stderr)
        self.assertFalse(self._check_test_log_file_exists())
        self._remove_test_log_file()

    def test_separator(self):
        """Test command line with message
        Test performed on console output (verbose option on) but checks output log file exists first
        """
        # test with short option
        p = self._execute(['test1', '-F', TEST_LOG_FILE, '-s', ':', '-v'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        # check that the output file exists and remove it
        self.assertTrue(self._check_test_log_file_exists())
        self._remove_test_log_file()
        # perform tests on stderr
        self.assertIn("INFO", stderr)
        self.assertNotIn(" - ", stderr)
        self.assertIn("test1", stderr)
        self.assertIn("INFO:test1", stderr)
        # test with long option
        p = self._execute(['test1', '-F', TEST_LOG_FILE, '--sep', ':', '-v'])
        stdout = p.stdout
        stderr = p.stderr
        # check that the output file exists and remove it
        self.assertTrue(self._check_test_log_file_exists())
        self._remove_test_log_file()
        # perform tests on stderr
        self.assertEqual('', stdout)
        self.assertIn("INFO", stderr)
        self.assertNotIn(" - ", stderr)
        self.assertIn("test1", stderr)
        self.assertIn("INFO:test1", stderr)

    def test_format(self):
        """Test format
        Test performed on console output (verbose option on) but checks output log file exists first
        """
        fmt = "%(message)s"
        # test with short option
        p = self._execute(['test1', '-F', TEST_LOG_FILE, '-f', fmt, '-v'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        # check that the output file exists and remove it
        self.assertTrue(self._check_test_log_file_exists())
        self._remove_test_log_file()
        # perform tests on stderr
        self.assertNotIn("INFO", stderr)
        self.assertNotIn(" - ", stderr)
        self.assertIn("test1", stderr)
        # test with long option
        p = self._execute(['test1', '-F', TEST_LOG_FILE, '--format', fmt, '-v'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        # check that the output file exists and remove it
        self.assertTrue(self._check_test_log_file_exists())
        self._remove_test_log_file()
        # perform tests on stderr
        self.assertNotIn("INFO", stderr)
        self.assertNotIn(" - ", stderr)
        self.assertIn("test1", stderr)
        # test with format error
        p = self._execute(['test1', '-F', TEST_LOG_FILE, '--format', 'newlevel', '-v'])
        # check that the output file doesn't exist (due to the error)
        self.assertFalse(self._check_test_log_file_exists())
        # perform tests on stderr
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("ValueError", stderr)

    def test_date_format(self):
        """Test date format
        Test performed on console output (verbose option on) but checks output log file exists first
        """
        dfmt = "%H"
        # test with short option
        p = self._execute(['test1', '-F', TEST_LOG_FILE, '-df', dfmt, '-v'])
        stdout = p.stdout
        # check that the output file exists and remove it
        self.assertTrue(self._check_test_log_file_exists())
        self._remove_test_log_file()
        # perform tests on stderr
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        ## date should be removed
        self.assertEqual(4, stderr.count(" "))
        ## should be an hour
        self.assertLess(int(stderr.split(" ")[0]), 24)
        # test with long option
        p = self._execute(['test1', '-F', TEST_LOG_FILE, '--dateformat', dfmt, '-v'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        # check that the output file exists and remove it
        self.assertTrue(self._check_test_log_file_exists())
        self._remove_test_log_file()
        # perform tests on stderr
        self.assertIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        ## date should be removed
        self.assertEqual(4, stderr.count(" "))
        ## should be an hour
        self.assertLess(int(stderr.split(" ")[0]), 24)

    def test_no_asctime(self):
        """Test no asctime
        Test performed on console output (verbose option on) but checks output log file exists first
        """
        p = self._execute(['test1', '-F', TEST_LOG_FILE, '--noasctime', '-v'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        # check that the output file exists and remove it
        self.assertTrue(self._check_test_log_file_exists())
        self._remove_test_log_file()
        # perform tests on stderr
        self.assertIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        ## datetime should be removed
        self.assertEqual(2, stderr.count(" "))

    def test_nolevel(self):
        """Test no level
        Test performed on console output (verbose option on) but checks output log file exists first
        """
        p = self._execute(['test1', '-F', TEST_LOG_FILE, '--nolevel', '-v'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        # check that the output file exists and remove it
        self.assertTrue(self._check_test_log_file_exists())
        self._remove_test_log_file()
        # perform tests on stderr
        self.assertNotIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        ## level should be removed
        self.assertEqual(3, stderr.count(" "))

    def test_options_valid_with_value(self):
        """Test options valid case
         with option value provided
        Test performed on console output (verbose option on) but checks output log file exists first
        """
        ## test with short option
        p = self._execute(['test1', '-F', TEST_LOG_FILE, '-o', 'ip', '--ip', '127.0.0.1', '-v'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        # check that the output file exists and remove it
        self.assertTrue(self._check_test_log_file_exists())
        self._remove_test_log_file()
        # perform tests on stderr
        self.assertIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        # test with long option
        p = self._execute(['test1', '-F', TEST_LOG_FILE, '--options', 'ip',\
                            '--ip', '127.0.0.1', '-v'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        # check that the output file exists and remove it
        self.assertTrue(self._check_test_log_file_exists())
        self._remove_test_log_file()
        # perform tests on stderr
        self.assertIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)

    def test_options_valid_with_message_option(self):
        """Test options valid case
         with message option value provided
        Test performed on console output (verbose option on) but checks output log file exists first
        """
        ## test with short option
        p = self._execute(['test1', '-F', TEST_LOG_FILE, '-o', 'message,ip',\
                            '--ip', '127.0.0.1', '-v'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        # check that the output file exists and remove it
        self.assertTrue(self._check_test_log_file_exists())
        self._remove_test_log_file()
        # perform tests on stderr
        self.assertIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        # message must be before the IP given the message,ip options order
        self.assertLess(stderr.index("test1"),stderr.index("127.0.0.1"))
        # test with long option
        p = self._execute(['test1', '-F', TEST_LOG_FILE, '--options', 'message,ip',\
                            '--ip', '127.0.0.1', '-v'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        # check that the output file exists and remove it
        self.assertTrue(self._check_test_log_file_exists())
        self._remove_test_log_file()
        # perform tests on stderr
        self.assertIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        # message must be before the IP given the message,ip options order
        self.assertLess(stderr.index("test1"),stderr.index("127.0.0.1"))

    def test_options_valid_without_value(self):
        """Test options without matching option value provided
           should not be able to apply the template
        Test performed on console output (verbose option on) but checks output log file exists first
        """
        ## test with short option
        p = self._execute(['test1', '-F', TEST_LOG_FILE, '-o', 'ip', '-v'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        # check that the output file doesn't exist (due to the error)
        self.assertFalse(self._check_test_log_file_exists())
        # perform tests on stderr
        self.assertIn("Could not apply the template $ip - $message", stderr)
        # test with long option
        p = self._execute(['test1', '-F', TEST_LOG_FILE,'--options', 'ip', '-v'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("Could not apply the template $ip - $message", stderr)

    def test_options_invalid_inexisting_option(self):
        """Test options without an inexisting option
        Test performed on console output (verbose option on) but checks output log file exists first
        """
        ## test with short option
        p = self._execute(['test1', '-F', TEST_LOG_FILE, '-o', 'newoption', '-v'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        # check that the output file doesn't exist (due to the error)
        self.assertFalse(self._check_test_log_file_exists())
        # perform tests on stderr
        self.assertIn("OPTION no found. ", stderr)
        # test with long option
        p = self._execute(['test1', '-F', TEST_LOG_FILE, '--options', 'newoption', '-v'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        self.assertIn("OPTION no found. ", stderr)

    def test_optsep(self):
        """Test options with another option separator
        Test performed on console output (verbose option on) but checks output log file exists first
        """
        ## test with short option
        p = self._execute(['test1', '-F', TEST_LOG_FILE, '-o', 'message,ip', '--ip',\
                            '127.0.0.1', '-osep', ';', '-v'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        # check that the output file exists and remove it
        self.assertTrue(self._check_test_log_file_exists())
        self._remove_test_log_file()
        # perform tests on stderr
        self.assertIn("INFO", stderr)
        self.assertIn(" - ", stderr)
        self.assertIn("test1", stderr)
        self.assertIn(";", stderr)
        self.assertIn("test1;127.0.0.1", stderr)
        # test with long option
        p = self._execute(['test1', '-F', TEST_LOG_FILE, '--options', 'message,ip', '--ip',\
                            '127.0.0.1','--optsep', ';', '-v'])
        stdout = p.stdout
        stderr = p.stderr
        self.assertEqual('', stdout)
        # check that the output file exists and remove it
        self.assertTrue(self._check_test_log_file_exists())
        self._remove_test_log_file()
        # perform tests on stderr
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
