#!/usr/bin/env python
#

import unittest
from swajime import SwaANSI


class TestSwaANSI(unittest.TestCase):

    def test___init__(self):
        self.assertGreater(len(SwaANSI.colors), 200, 'Verify 256 colors available.')     
        self.assertEqual(len(SwaANSI.styles), 10, 'Verify 10 styles available.')     

    def test_class_display(self):
        redTest = SwaANSI.display("test", "RED")
        self.assertEqual(redTest, "\033[38;5;9mtest\033[0m")

    def test_object_display(self):
        redTest = SwaANSI("RED")
        self.assertEqual(redTest.display('test'), "\033[38;5;9mtest\033[0m")


if __name__ == '__main__':
    unittest.main()
