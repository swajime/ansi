#!/usr/bin/env python
#

"""Test the SwaANSI module"""

import os
import shutil
import sys
import time
import unittest

# reload is needed for one of the tests
if sys.version_info[0] == 3:
    if sys.version_info[1] < 4:
        from imp import reload
    else:
        from importlib import reload


class TestSwaANSI(unittest.TestCase):
    """Test the SwaANSI class."""

    def test_class__init__no_dat(self):
        home = os.environ['HOME']

        if os.path.exists(os.path.join(home, 'dat')):
            os.rename(os.path.join(home, 'dat'), os.path.join(home, 'dat-bak'))

        found_before = os.path.exists(os.path.join(home, 'dat'))

        if 'swajime' in sys.modules:
            del sys.modules['swajime.SwaANSI']

        import swajime
        reload(swajime)
        from swajime import SwaANSI

        found_after = os.path.exists(os.path.join(home, 'dat',
                                                  'color_data.json'))

        if os.path.exists(os.path.join(home, 'dat-bak')):
            if os.path.exists(os.path.join(home, 'dat')):
                shutil.rmtree(os.path.join(home, 'dat'))
            os.rename(os.path.join(home, 'dat-bak'), os.path.join(home, 'dat'))

        # fix for some random race condition
        while not os.path.exists(os.path.join(home, 'dat', 'color_data.json')):
            time.sleep(1)

        assert not found_before
        assert found_after

        green_background = SwaANSI.wrap('test', None, 'GREEN')
        self.assertEqual(green_background, '\033[48;5;2mtest\033[0m')

    def test_class__init__(self):
        if 'swajime' in sys.modules:
            del sys.modules['swajime.SwaANSI']
        import swajime
        reload(swajime)
        from swajime import SwaANSI

        self.assertGreater(len(SwaANSI.colors), 200,
                           'Verify at least 200 colors available.')
        self.assertGreater(len(SwaANSI.styles), 20,
                           'Verify at least 20 styles available.')

    def test_class_wrap(self):
        if 'swajime' in sys.modules:
            del sys.modules['swajime.SwaANSI']
        import swajime
        reload(swajime)
        from swajime import SwaANSI

        SwaANSI.setWHEN('ALWAYS')
        SwaANSI.setDefaults('INVALID', 'INVALID', 'INVALID')
        self.assertEqual(SwaANSI.wrap('test', None, None, None),
                         'test')

        SwaANSI.setWHEN('ALWAYS')
        SwaANSI.setDefaults(None, None, 'UNDERLINE')
        self.assertEqual(SwaANSI.wrap('test', None, None),
                         '\033[4mtest\033[0m')

        SwaANSI.setWHEN('ALWAYS')
        SwaANSI.setDefaults(None, None, None)
        self.assertEqual(SwaANSI.wrap('test', None, None, None),
                         'test')

        SwaANSI.setWHEN('INVALID')
        red_foreground = SwaANSI.wrap('test', 'RED', None, None)
        self.assertEqual(red_foreground, 'test')
        green_background = SwaANSI.wrap('test', None, 'GREEN', None)
        self.assertEqual(green_background, 'test')

        SwaANSI.setWHEN('ALWAYS')
        inv_ansi = SwaANSI.wrap('test', 'INVALID', 'INVALID', 'INVALID')
        self.assertEqual(inv_ansi, 'test')

        SwaANSI.setWHEN('ALWAYS')
        red_foreground = SwaANSI.wrap('test', 'RED', None, None)
        self.assertEqual(red_foreground, '\033[38;5;9mtest\033[0m')
        green_background = SwaANSI.wrap('test', None, 'GREEN', None)
        self.assertEqual(green_background, '\033[48;5;2mtest\033[0m')

        SwaANSI.setWHEN('NEVER')
        red_foreground = SwaANSI.wrap('test', 'RED', None, None)
        self.assertEqual(red_foreground, 'test')
        green_background = SwaANSI.wrap('test', None, 'GREEN', None)
        self.assertEqual(green_background, 'test')

    def test_object_wrap(self):
        if 'swajime' in sys.modules:
            del sys.modules['swajime.SwaANSI']
        import swajime
        reload(swajime)
        from swajime import SwaANSI

        SwaANSI.setWHEN('ALWAYS')
        invalid_ansi = SwaANSI('INVALID', 'INVALID', 'INVALID')
        self.assertEqual(invalid_ansi.wrap('test'),
                         'test')

        SwaANSI.setWHEN('INVALID')
        red_foreground = SwaANSI('RED', None, None)
        self.assertEqual(red_foreground.wrap('test'),
                         'test')
        green_background = SwaANSI(None, "GREEN", None)
        self.assertEqual(green_background.wrap('test'),
                         'test')

        SwaANSI.setWHEN('ALWAYS')
        underlined = SwaANSI(None, None, 'UNDERLINE')
        self.assertEqual(underlined.wrap('test'),
                         '\033[4mtest\033[0m')

        SwaANSI.setWHEN('ALWAYS')
        red_foreground = SwaANSI('RED', None, None)
        self.assertEqual(red_foreground.wrap('test'),
                         '\033[38;5;9mtest\033[0m')
        green_background = SwaANSI(None, "GREEN", None)
        self.assertEqual(green_background.wrap('test'),
                         '\033[48;5;2mtest\033[0m')

        SwaANSI.setWHEN('NEVER')
        red_foreground = SwaANSI('RED', None, None)
        self.assertEqual(red_foreground.wrap('test'),
                         'test')
        green_background = SwaANSI(None, "GREEN", None)
        self.assertEqual(green_background.wrap('test'),
                         'test')

        SwaANSI.setWHEN('ALWAYS')
        green_background = SwaANSI(None, "GREEN", None)
        self.assertEqual(green_background.wrap(None),
                         None)
        self.assertEqual(green_background.wrap(''),
                         '')


if __name__ == '__main__':
    unittest.main()
