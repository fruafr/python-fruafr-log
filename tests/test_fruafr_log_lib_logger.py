#!/usr/bin/env python3
"""
# Copyright 2023 by David Heurtevent.
# SPDX_LICENSE: MIT
# License: MIT License
# Author: David HEURTEVENT <david@heurtevent.org>

Test of fruafr.log.lib.logger
"""

import unittest
import logging
from fruafr.log.lib import logger


class TestLogger(unittest.TestCase):
    """Class TestLogger"""

    def setUp(self):
        self.logger_name = 'test'
        self.logger = logger.LoggerClass(self.logger_name)
        hdlr = logging.Handler()
        self.hdlr_name = 'handler_test'
        hdlr.name = self.hdlr_name
        self.logger.addHandler(hdlr)

    # Tests
    def test_init(self):
        """Test constructor"""
        self.assertEqual(self.logger.name, self.logger_name)
        self.assertEqual(self.logger.level, logging.NOTSET)

    def test_default_formatter(self):
        """Test default_formatter"""
        newformatter = logging.Formatter()
        self.logger.default_formatter = newformatter
        self.assertEqual(self.logger._default_formatter, newformatter)  # pylint: disable=W0212
        self.assertEqual(self.logger.default_formatter, newformatter)

    def test_remove_handler(self):
        """Test removeHander"""
        self.logger.removeHandler(self.hdlr_name)

    def test_get_handler(self):
        """Test getHandler"""
        hdlr = self.logger.get_handler(self.hdlr_name)
        self.assertIsInstance(hdlr, logging.Handler)
        self.assertEqual(hdlr.name, self.hdlr_name)

    def test_set_handler_level(self):
        """Test setHandlerLevel"""
        hdlr = self.logger.get_handler(self.hdlr_name)
        newlevel = logging.CRITICAL
        self.logger.set_handler_level(self.hdlr_name, newlevel)
        self.assertEqual(hdlr.level, newlevel)

    def test_set_handler_name(self):
        """Test setHandlerName"""
        newname = 'handler_newname'
        self.logger.set_handler_name(self.hdlr_name, newname)
        hdlr = self.logger.get_handler(newname)
        self.assertEqual(hdlr.name, newname)

    def test_set_handler_formatter(self):
        """Test setHanderFormatter"""
        newformatter = logging.Formatter()
        self.logger.set_handler_formatter(self.hdlr_name, newformatter)
        hdlr = self.logger.get_handler(self.hdlr_name)
        self.assertEqual(hdlr.formatter, newformatter)


# Main
def main():
    """Main"""
    unittest.main()


if __name__ == "__main__":
    main()
