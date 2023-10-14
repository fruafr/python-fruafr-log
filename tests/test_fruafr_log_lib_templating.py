#!/usr/bin/env python3
# pylint: disable=line-too-long
# pylint: disable=protected-access
"""
Test of fruafr.log.lib.templating
"""
# Copyright 2023 by David Heurtevent.
# SPDX_LICENSE: MIT
# License: MIT License
# Author: David HEURTEVENT <david@heurtevent.org>

import unittest
from fruafr.log.lib import templating


class TestTemplating(unittest.TestCase):
    """Class TestTemplating"""

    def setUp(self):
        pass

    def test_create_template(self):
        """Test create_template"""
        variables = ['var1', 'var2']
        t = templating.Templating.create_template(variables, '-')
        self.assertEqual(t, "$var1-$var2")
        variables = ['var1']
        t = templating.Templating.create_template(variables, '-')
        self.assertEqual(t, "$var1")

    def test_validate_template(self):
        """Test validate_template"""
        variables = ['var1', 'var2']
        t = templating.Templating.create_template(variables, '-')
        # valid case : returns None
        valid = templating.Templating.validate_template(t, variables, )
        self.assertEqual(valid, None)
        # missing var2: returns var2
        valid = templating.Templating.validate_template("$var1", variables)
        self.assertEqual(valid, 'var2')

    def test_apply_template(self):
        """Test apply_template"""
        variables = ['var1', 'var2']
        values = {'var1': 10, 'var2': 11}
        t = templating.Templating.create_template(variables, '-')
        res = templating.Templating.apply_template(t, values)
        self.assertEqual(res, '10-11')


def main():
    """Main"""
    unittest.main()


if __name__ == "__main__":
    main()
