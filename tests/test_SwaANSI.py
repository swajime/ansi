#!/usr/bin/env python
#

import unittest
from swajime import SwaANSI


class TestSwaANSI(unittest.TestCase):

    def test_class__init__(self):
        self.assertGreater(len(SwaANSI.colors), 200, 'Verify at least 200 colors available.')     
        self.assertGreater(len(SwaANSI.styles), 20, 'Verify at least 20 styles available.')     

    def test_class_wrap(self):
        redForeground = SwaANSI.wrap('test', 'RED')
        self.assertEqual(redForeground, '\033[38;5;9mtest\033[0m')
        greenBackground = SwaANSI.wrap('test', None, 'GREEN')
        self.assertEqual(greenBackground, '\033[48;5;2mtest\033[0m')

    def test_object_wrap(self):
        redForeground = SwaANSI('RED')
        self.assertEqual(redForeground.wrap('test'), '\033[38;5;9mtest\033[0m')
        greenBackground = SwaANSI(None, "GREEN")
        self.assertEqual(greenBackground.wrap('test'), '\033[48;5;2mtest\033[0m')

if __name__ == '__main__':
    unittest.main()
