#!/usr/bin/env python3
# pylint: disable=line-too-long
# pylint: disable=protected-access
"""
Test of fruafr.log.tinysyslogserver

Must be run with sudo privileges

`sudo python3 ../python-fruafr-log/tests/test_fruafr_log_tinysyslogserver.py`

"""
# Copyright 2023 by David Heurtevent.
# SPDX_LICENSE: MIT
# License: MIT License
# Author: David HEURTEVENT <david@heurtevent.org>

import unittest
import os
import subprocess
import signal

INTERPRETER = "python3"
PATH = os.path.dirname(__file__)
SCRIPT = f"{PATH}/../src/fruafr/log/tinysyslogserver.py"
SYSLOG_SERVER_LOG_FILE='/tmp/fruafr-log-syslog-server-test.txt'

class TestTinySysLogServer(unittest.TestCase):
    """Class TinySysLogServer"""

    def _start(self, add_args: list, sudo: bool = False) -> subprocess.Popen:
        """Append the args to the command line and execute the start and return the subprocess
        Args:
            add_args(list): list of additional arguments and options to append to the command line
            sudo(bool): whether to run the command in sudo mode
        Returns:
            The subprocess.Popen object
        """
        # Append the args to the command line
        if sudo:
            cmd_line_args = ['sudo']
        else:
            cmd_line_args = []
        cmd_line_args.append(INTERPRETER)
        cmd_line_args.append(SCRIPT)
        cmd_line_args += add_args
        #open the subprocess
        p = subprocess.Popen(
            cmd_line_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # return the subprocess.Popen object
        return p

    def _read(self, process: subprocess.Popen):
        """Read a line from stdout from the process
        Args:
            process (subprocess.Popen): the process to read from
        """
        return process.stdout.readline().decode("utf-8").strip()

    def _terminate(self, process: subprocess.Popen):
        """Terminate the process
        Args:
            process (subprocess.Popen): the process to terminate
        """
        try:
            outs, errs = process.communicate(timeout=2)
        except subprocess.TimeoutExpired:
            process.send_signal(signal.SIGINT)
            process.wait(2)
            process.kill()
            process.stdin.close()
            process.stdout.close()
            process.stderr.close()
            outs, errs = process.communicate()
        return outs, errs

    def _remove_test_log_file(self, path: str = SYSLOG_SERVER_LOG_FILE):
        """Remove the output test file
        Args:
            path(str): path to check
        """
        if os.path.exists(path):
            os.remove(path)

    def setUp(self):
        """Remove the log file on set Up"""
        self._remove_test_log_file()

    def tearDown(self):
        """Remove the log file on set Down"""
        self._remove_test_log_file()

    def test_help(self):
        """Test that the CLI help is working"""
        p = self._start(['-h'])
        stdout = p.stdout.readlines()
        stderr = p.stderr.readlines()
        self._terminate(p)
        # no stderr
        self.assertEqual(stderr, [])
        # usage on first line
        self.assertIn(b'usage: Tiny UDP/TCP syslog server', stdout[0])

    def test_start_stop(self):
        """Test that the server can start and stop on localhost, port 5140 (UDP by default)
        Tests -a, -p, -F, -v --address --port --file --verbose
        """
        # SHORT OPTIONS
        p = self._start(['-a', '127.0.0.1', '-p', '5140',
                         '-F', SYSLOG_SERVER_LOG_FILE, '-v'])
        stdout, stderr = self._terminate(p)
        # test file is created
        self.assertTrue(os.path.exists(SYSLOG_SERVER_LOG_FILE))
        # remove it
        self._remove_test_log_file()
        self.assertFalse(os.path.exists(SYSLOG_SERVER_LOG_FILE))
        # no stderr
        self.assertEqual(stderr, b'')
        # started on 127.0.0.1:5140/UDP
        self.assertIn(b'SYSLOG server starting with : 127.0.0.1:5140/UDP', stdout)
        # Waiting for connections
        self.assertIn(b'Waiting for connections...', stdout)
        # LONG OPTIONS
        p = self._start(['--address', '127.0.0.1', '--port', '5140',
                         '--file', SYSLOG_SERVER_LOG_FILE, '--verbose'])
        stdout, stderr = self._terminate(p)
        # test file is created
        self.assertTrue(os.path.exists(SYSLOG_SERVER_LOG_FILE))
        # remove it
        self._remove_test_log_file()
        self.assertFalse(os.path.exists(SYSLOG_SERVER_LOG_FILE))
        # no stderr
        self.assertEqual(stderr, b'')
        # started on 127.0.0.1:5140/UDP
        self.assertIn(b'SYSLOG server starting with : 127.0.0.1:5140/UDP', stdout)
        # Waiting for connections
        self.assertIn(b'Waiting for connections...', stdout)

    def test_start_stop_tcp_udp(self):
        """Test that the server can start and stop on localhost, port 5140/TCP et 5140/UDP
        Tests -a -p -F -v -t --tcp
        """
        # SHORT OPTIONS
        p = self._start(['-a', '127.0.0.1', '-p', '5140',
                         '-F', SYSLOG_SERVER_LOG_FILE, '-t', '-v'])
        stdout, stderr = self._terminate(p)
        # no stderr
        self.assertEqual(stderr, b'')
        # started on 127.0.0.1:5140/UDP
        self.assertIn(b'SYSLOG server starting with : 127.0.0.1:5140/UDP', stdout)
        # started on 127.0.0.1:5140/TCP
        self.assertIn(b'SYSLOG server starting with : 127.0.0.1:5140/TCP', stdout)
        # Waiting for connections
        self.assertIn(b'Waiting for connections...', stdout)
        # LONG OPTIONS
        p = self._start(['-a', '127.0.0.1', '-p', '5140',
                         '-F', SYSLOG_SERVER_LOG_FILE, '--tcp', '-v'])
        stdout, stderr = self._terminate(p)
        # no stderr
        self.assertEqual(stderr, b'')
        # started on 127.0.0.1:5140/UDP
        self.assertIn(b'SYSLOG server starting with : 127.0.0.1:5140/UDP', stdout)
        # started on 127.0.0.1:5140/TCP
        self.assertIn(b'SYSLOG server starting with : 127.0.0.1:5140/TCP', stdout)
        # Waiting for connections
        self.assertIn(b'Waiting for connections...', stdout)

    def test_start_stop_tcp(self):
        """Test that the server can start and stop on localhost, port 5140/TCP only
        Tests -a -p -F -v -t --noudp
        """
        # SHORT OPTIONS
        p = self._start(['-a', '127.0.0.1', '-p', '5140',
                         '-F', SYSLOG_SERVER_LOG_FILE, '-t', '-nou', '-v'])
        stdout, stderr = self._terminate(p)
        # no stderr
        self.assertEqual(stderr, b'')
        # started on 127.0.0.1:5140/UDP
        self.assertNotIn(b'SYSLOG server starting with : 127.0.0.1:5140/UDP', stdout)
        # started on 127.0.0.1:5140/TCP
        self.assertIn(b'SYSLOG server starting with : 127.0.0.1:5140/TCP', stdout)
        # Waiting for connections
        self.assertIn(b'Waiting for connections...', stdout)
        # LONG OPTIONS
        p = self._start(['-a', '127.0.0.1', '-p', '5140',
                         '-F', SYSLOG_SERVER_LOG_FILE, '--tcp', '--noudp', '-v'])
        stdout, stderr = self._terminate(p)
        # no stderr
        self.assertEqual(stderr, b'')
        # started on 127.0.0.1:5140/UDP
        self.assertNotIn(b'SYSLOG server starting with : 127.0.0.1:5140/UDP', stdout)
        # started on 127.0.0.1:5140/TCP
        self.assertIn(b'SYSLOG server starting with : 127.0.0.1:5140/TCP', stdout)
        # Waiting for connections
        self.assertIn(b'Waiting for connections...', stdout)

    def test_start_stop_other_options_accepted(self):
        """Test that the server can start and stop on localhost, port 5140 (UDP by default)
        Tests -a, -p, -F, -v --address --port --file --verbose
        Tests accepts
        --encoding --mode --format --dateformat --level --sep --noasctime --nolevel
        does not test functionality of these options
        """
        # SHORT OPTIONS
        p = self._start(['-a', '127.0.0.1', '-p', '5140', '-F', SYSLOG_SERVER_LOG_FILE, '-v',
                         '-e', 'utf-8', '-m', 'w', '-f', '%(asctime)s %(message)s',
                         '-df', '%H:%m', '-L', 'debug',
                         '-s', ':', '--noasctime', '--nolevel'])
        stdout, stderr = self._terminate(p)
        # test file is created
        self.assertTrue(os.path.exists(SYSLOG_SERVER_LOG_FILE))
        # remove it
        self._remove_test_log_file()
        self.assertFalse(os.path.exists(SYSLOG_SERVER_LOG_FILE))
        # no stderr
        self.assertEqual(stderr, b'')
        # started on 127.0.0.1:5140/UDP
        self.assertIn(b'SYSLOG server starting with : 127.0.0.1:5140/UDP', stdout)
        # Waiting for connections
        self.assertIn(b'Waiting for connections...', stdout)
        # LONG OPTIONS
        p = self._start(['-a', '127.0.0.1', '-p', '5140', '-F', SYSLOG_SERVER_LOG_FILE, '-v',
                         '--encoding', 'utf-8', '--mode', 'w',
                         '--format', '%(asctime)s %(message)s',
                         '--dateformat', '%H:%m', '--level', 'debug',
                         '--sep', ':', '--noasctime', '--nolevel'])
        stdout, stderr = self._terminate(p)
        # test file is created
        self.assertTrue(os.path.exists(SYSLOG_SERVER_LOG_FILE))
        # remove it
        self._remove_test_log_file()
        self.assertFalse(os.path.exists(SYSLOG_SERVER_LOG_FILE))
        # no stderr
        self.assertEqual(stderr, b'')
        # started on 127.0.0.1:5140/UDP
        self.assertIn(b'SYSLOG server starting with : 127.0.0.1:5140/UDP', stdout)
        # Waiting for connections
        self.assertIn(b'Waiting for connections...', stdout)

def main():
    """Main"""
    unittest.main()


if __name__ == "__main__":
    main()
