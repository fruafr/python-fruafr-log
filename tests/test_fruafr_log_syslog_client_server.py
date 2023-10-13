#!/usr/bin/env python3
"""
# Copyright 2023 by David Heurtevent.
# SPDX_LICENSE: MIT
# License: MIT License
# Author: David HEURTEVENT <david@heurtevent.org>

Integration tests of fruafr.log syslog server (tinysyslog) and client (logtosyslog)

1) Ensure that the server is up and running. It must run in both tcp and udp modes:

`sudo python3 ../python-fruafr-log/src/fruafr/log/tinysyslogserver.py -a 0.0.0.0 -p 5140 -t -F /tmp/fruafr-log-syslog-server-test.txt -v`

2) Run the test with sudo privileges

`sudo python3 ../python-fruafr-log/tests/test_fruafr_log_syslog_client_server.py`

The script will act as a client and send messages to the server.
The incoming messages will be displayed on the server process console
The server will write incoming messages received to the file.
The script will verify that the messages have been logged in the server log file to validate the test.

4) Shut down the server with `Ctrl+C`

5) Delete the log file
`rm /tmp/fruafr-log-syslog-server-test.txt'`

"""
import unittest
import uuid

import test_fruafr_log_logtosyslog as test_client
import test_fruafr_log_logtofile as logtofile

INTERPRETER = 'python3'
SYSLOG_SERVER_LOG_FILE='/tmp/fruafr-log-syslog-server-test.txt'

HOST = 'localhost'
PORT = '5140'

class TestSysLog(unittest.TestCase):
    """Test that the integration of server and client is working properly"""

    def setUp(self) -> None:
        """Set up the integration"""
        self.ltf = logtofile.TestLogToFile()
        # setup the test suites
        self.tc = test_client.TestLogToSysLog()

    def tearDown(self) -> None:
        """Tear down the integration"""

    def test_tcp(self):
        """Test with TCP client"""
        # prepare a unique test identifier to guarantee uniqueness in logs
        uuid1 = uuid.uuid4()
        rid = f'test1tcp{uuid1}'
        # start the client in TCP mode and send a message
        pclient = self.tc._execute([rid, '-a', HOST, '-p', PORT, '-t', '-v'])
        stdout_client = pclient.stdout
        stderr_client = pclient.stderr
        # check that the message sent is correct
        self.assertEqual('', stdout_client)
        self.assertIn("INFO", stderr_client)
        self.assertIn(" - ", stderr_client)
        self.assertIn(rid, stderr_client)
        self.assertLess(stderr_client.index("INFO"),stderr_client.index(rid))
        # Check that the message is found in the server logs
        self.assertGreater(self.ltf._check_in_file(rid, SYSLOG_SERVER_LOG_FILE), -1)

    def test_udp(self):
        """Test with UDP client"""
        # prepare a unique test identifier to guarantee uniqueness in logs
        uuid1 = uuid.uuid4()
        rid = f'test1tcp{uuid1}'
        # start the client in TCP mode and send a message
        pclient = self.tc._execute([rid, '-a', HOST, '-p', PORT, '-v'])
        stdout_client = pclient.stdout
        stderr_client = pclient.stderr
        # check that the message sent is correct
        self.assertEqual('', stdout_client)
        self.assertIn("INFO", stderr_client)
        self.assertIn(" - ", stderr_client)
        self.assertIn(rid, stderr_client)
        self.assertLess(stderr_client.index("INFO"),stderr_client.index(rid))
        # Check that the message is found in the server logs
        self.assertGreater(self.ltf._check_in_file(rid, SYSLOG_SERVER_LOG_FILE), -1)


def main():
    """Main"""
    unittest.main()


if __name__ == "__main__":
    main()
