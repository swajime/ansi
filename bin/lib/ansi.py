#!/usr/bin/env python
#
# Author: John.Simpson@hmhs.com / john@swajime.com
#
# Version: 0.0.1 06/26/2020
#
# Compatible with Python 2 and Python 3
#

from __future__ import print_function
from platform import system

import json
import os
import requests
import six
import sys

# My version of windows insists on putting '<-' on the screen instead of processing the escape characters
# Still have not found a fix.  This fix isn't working.
if 'win' in system().lower():
    from ctypes import windll
    k = windll.kernel32
    k.SetConsoleMode(k.GetStdHandle(-11), 7)
    # os.system("") # This fix doesn't work either
    
# Used to initialize class without instantiating any objects.
class MetaANSI(type):
    def __init__(cls, name, bases, d):
        if not 'HOME' in os.environ:
            raise EnvironmentError('The color library requires HOME to be set in your environment.')
            
        HOME = os.getenv('HOME')
        color_dir = os.path.join(HOME, 'dat')
        color_path = os.path.join(color_dir, 'color_data.json') 
        if os.path.exists(color_path):
            with open(color_path, 'r') as color_file:
                color_data = json.load(color_file)
        else:
            print('Retrieving color data.  This is only necessary for the first run.')
            print('WARNING: There seem to be duplicate color names in the list, and there are clashes between web and X11 colors in the CSS color scheme. Beware.')
            print('Please see https://jonasjacek.github.io/colors/ for more information.')
            url = 'https://jonasjacek.github.io/colors/data.json'
            
            try:
                color_data = json.loads(requests.get(url).text)
            except Exception as e:
                print()
                print(str(e))
                print()
                print('Could not download data.json.  Please download {} to the {} directory.'.format(url, color_dir))
                exit(1)
                
            if not os.path.isdir(color_dir):
                os.mkdir(color_dir)
            with open(color_path, 'w') as color_file:
                json.dump(color_data, color_file, indent=4)

        for color in color_data:
            cls._colors[color['name']] = color['colorId']
        
        # Make colors and styles available as class attributes
        cls.colors = tuple(cls._colors.keys())
        cls.styles = tuple(cls._styles.keys())
        
        # enable case insensitive lookups
        for color in cls.colors:
            cls._colors[color.lower()] = cls._colors[color]

class ANSI(six.with_metaclass(MetaANSI, object)): # <-- v2 & v3
    _when = 'always'
    _colors = {}
    _background = 'Black'
    _styles = {'default':'0',
              'bold':'1',
              'faint':'2',
              'italic':'3', 
              'underline':'4',
              'blinking':'5',
              'fast_blinking':'6',
              'reverse':'7',
              'hide':'8',
              'strikethrough':'9'}

    @classmethod
    def colorId(cls, color):
        return cls.id[color]

    @classmethod
    def setANSI(cls, text, foreground, background=None, *args):
        if cls._when == 'never' or (cls._when == 'auto' and not sys.stdout.isatty()):
            return text

        if background is None:
            background = cls._background

        f = cls._colors[foreground.lower()]
        b = cls._colors[background.lower()]

        s = ''
        for style in args:
            s += ';' + cls._styles[style.lower()]

        return ('\033[38;5;{};48;5;{}{}m' + text + '\033[0m').format(f, b, s)

    @classmethod
    def setWHEN(cls, when):
        if when in ('never', 'always', 'auto'):
            cls._when = when
        else:
            print("Valid values are 'never', 'always', or 'auto'.")
            raise ValueError

    @classmethod
    def setBackground(cls, color):
        cls._background = color

if __name__ == "__main__":
    ANSI.setBackground('WHITE')
    
    for color in sorted(ANSI.colors):
        print(ANSI.setANSI('{:>40}'.format('This is a {} foreground!'.format(color)), color, None) + ANSI.setANSI('{:<40}'.format('This is a {} background!'.format(color)), 'White', color))

    print()

    ANSI.setBackground('BLACK')
    for style in ANSI.styles:
        print(ANSI.setANSI('This is a {} test!'.format(style), 'WHITE', None, style))
    
    print(ANSI.setANSI('This should be red!', 'Red', None, 'UNDERLINE', 'BLINKING'))
    print(ANSI.setANSI('This should be red!', 'RED'))
