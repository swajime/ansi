#!/usr/bin/env python
#

"""Test the SwaANSI module"""

import unittest
from swajime import SwaANSI


class TestSwaANSI(unittest.TestCase):
    """Test the SwaANSI class."""

    def test_class__init__(self):
        self.assertGreater(len(SwaANSI.colors), 200,
                           'Verify at least 200 colors available.')
        self.assertGreater(len(SwaANSI.styles), 20,
                           'Verify at least 20 styles available.')

    def test_class_wrap(self):
        red_foreground = SwaANSI.wrap('test', 'RED')
        self.assertEqual(red_foreground, '\033[38;5;9mtest\033[0m')
        green_background = SwaANSI.wrap('test', None, 'GREEN')
        self.assertEqual(green_background, '\033[48;5;2mtest\033[0m')

    def test_object_wrap(self):
        red_foreground = SwaANSI('RED')
        self.assertEqual(red_foreground.wrap('test'),
                         '\033[38;5;9mtest\033[0m')
        green_background = SwaANSI(None, "GREEN")
        self.assertEqual(green_background.wrap('test'),
                         '\033[48;5;2mtest\033[0m')

if __name__ == '__main__':
    unittest.main()

# Rename this module to match this regular expression:
#     "(([a-z_][a-z0-9_]*)|([A-Z][a-zA-Z0-9]+))$".
