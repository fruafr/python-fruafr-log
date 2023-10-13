#!/usr/bin/env python3
"""
# Copyright 2023 by David Heurtevent.
# SPDX_LICENSE: MIT
# License: MIT License
# Author: David HEURTEVENT <david@heurtevent.org>

Test of fruafr.log.lib.formatter
"""

import unittest
from fruafr.log.lib import formatter
from fruafr.log.lib import common


class TestFormatter(unittest.TestCase):
    """Class TestFormatter"""

    def setUp(self):
        self.formatter = formatter.FormatterClass()

    def test_init(self):
        """Test constructor"""
        self.assertIsInstance(self.formatter, formatter.FormatterClass)
        self.assertIsInstance(self.formatter._fmt, str)

    def test_init_with_format_str(self):
        """Test constructor with format string"""
        self.formatter = formatter.FormatterClass(common.BASIC_FORMAT)
        assert self.formatter._fmt == common.BASIC_FORMAT

    def test_supported(self):
        """Test supported"""
        self.formatter = formatter.FormatterClass()
        k = self.formatter.supported
        assert k == common.LOGGING_OPTIONS.keys()

    def test_fmt(self):
        """Test fmt property"""
        self.formatter = formatter.FormatterClass(common.BASIC_FORMAT)
        assert self.formatter.fmt == common.BASIC_FORMAT

    def test_set_fmt(self):
        """Test fmt setter"""
        self.formatter = formatter.FormatterClass()
        self.formatter.fmt = common.BASIC_FORMAT
        assert self.formatter.fmt == common.BASIC_FORMAT

    def test_create_format_str(self):
        """Test create_format_str"""
        k = ['asctime', 'name', 'levelname', 'message']
        m = '%(asctime)s %(name)s %(levelname)s %(message)s'
        m1 = '%(asctime)s-%(name)s-%(levelname)s-%(message)s'
        m2 = "${asctime}-${name}-${levelname}-${message}"
        m3 = "{asctime}-{name}-{levelname}-{message}"
        # test with space separator
        self.formatter.create_format_str(k, ' ')
        self.assertEqual(self.formatter._fmt, m)
        # test with space hyphen
        self.formatter.create_format_str(k, '-')
        self.assertEqual(self.formatter._fmt, m1)
        # test with space hyphen and dollar sign style
        self.formatter.create_format_str(k, '-', '$')
        self.assertEqual(self.formatter._fmt, m2)
        # test with space hyphen and colon
        self.formatter.create_format_str(k, '-', '{')
        self.assertEqual(self.formatter._fmt, m3)

    def test_default(self):
        """Test default"""
        self.formatter.default()
        assert self.formatter._fmt == common.DEFAULT_FORMAT

    def test_typical(self):
        """Test typical"""
        self.formatter.typical()
        assert self.formatter._fmt == common.TYPICAL_FORMAT

    def test_simple(self):
        """Test simple"""
        self.formatter.simple()
        assert self.formatter._fmt == common.SIMPLE_FORMAT

    def test_basic(self):
        """Test basic"""
        self.formatter.basic()
        assert self.formatter._fmt == common.BASIC_FORMAT

    def test_raw(self):
        """Test raw"""
        self.formatter.raw()
        assert self.formatter._fmt == common.RAW_FORMAT

    def test_custom(self):
        """Test custom"""
        c = '%(asctime)s - %(name)s - %(message)s'
        self.formatter.custom(c)
        assert self.formatter._fmt == c

    def test_str(self):
        """Test __str__"""
        self.formatter.formatstr = common.BASIC_FORMAT
        m = "<class 'fruafr.log.lib.formatter.FormatterClass'>(%(message)s)"
        self.assertEqual(str(self.formatter), m)

    def test_repr(self):
        """Test __repr__"""
        m = "<class 'fruafr.log.lib.formatter.FormatterClass'>({'_style':"
        self.assertIn(m, repr(self.formatter))


def main():
    """Main"""
    unittest.main()


if __name__ == "__main__":
    main()
