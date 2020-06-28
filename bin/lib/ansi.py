#!/usr/bin/env python
#
# Author: John.Simpson@hmhs.com / john@swajime.com
#
# Project started: 06/26/2020
#
# Compatible with Python 2 and Python 3
# Runs on Linux or Windows
#

# from __future__ imports must occur at the beginning of the file
from __future__ import print_function

VERSION = "0.0.2"
color_file_dir = 'dat'  # in $HOME
color_file_name = 'color_data.json';

from platform import system

import json
import os
import requests
import six
import sys

# My version of windows insists on putting a '<-' character on the screen instead of processing the escape characters
# Still have not found a fix.  This fix isn't working.
if 'win' in system().lower():
    from ctypes import windll
    k = windll.kernel32
    k.SetConsoleMode(k.GetStdHandle(-11), 7)
    # os.system("") # This fix doesn't work either
    
class class_or_instancemethod(classmethod):
    def __get__(self, instance, type_):
        descr_get = super(class_or_instancemethod, self).__get__ if instance is None else self.__func__.__get__
        return descr_get(instance, type_)

# Used to initialize ANSI class without instantiating any objects.
class MetaANSI(type):
    def __init__(cls, name, bases, d):
        if not 'HOME' in os.environ:
            raise EnvironmentError('The color library requires HOME to be set in your environment.  JSON for available colors will be stored in {}.'.format(os.path.join('$HOME', color_file_dir, color_file_name)))
            
        HOME = os.getenv('HOME')
        color_dir = os.path.join(HOME, color_file_dir)
        color_path = os.path.join(color_dir, color_file_name) 
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
                print('Could not download data.json.  Please download {} to the {} directory as {}.'.format(url, color_dir, color_file_name))
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

class ANSI(six.with_metaclass(MetaANSI, object)):
    _when = 'always'
    _colors = {}
    _default_foreground = None
    _default_background = None
    _default_styles = []
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

    @class_or_instancemethod
    def display(self_or_cls, text, foreground=None, background=None, *style_list):
        # only add ansi if _when is 'always' or output is a tty
        if self_or_cls._when == 'never' or (self_or_cls._when == 'auto' and not sys.stdout.isatty()):
            return text

        if foreground is None:
            foreground = self_or_cls._default_foreground
        if foreground:
            if foreground.lower() not in self_or_cls._colors:
                print('Foreground color {} is not available.'.format(foreground), file=sys.stderr)
                fg_string = ''
            else:
                fg_string = '38;5;{}'.format(self_or_cls._colors[foreground.lower()])
        else:
            fg_string = ''
        
        if background is None:
            background = self_or_cls._default_background
        if background:
            if background.lower() not in self_or_cls._colors:
                print('Background color {} is not available.'.format(background), file=sys.stderr)
                bg_string = ''
            else:
                bg_string = '48;5;{}'.format(self_or_cls._colors[background.lower()])
        else:
            bg_string = ''

        if len(style_list) == 0:
            style_list = self_or_cls._default_styles
        style_string_list = []
        for style in style_list:
            if style is None:
                pass
            elif style.lower() not in self_or_cls._styles:
                print('Style {} is not available.'.format(style), file=sys.stderr)
            else:
                style_string_list.append(self_or_cls._styles[style.lower()])
        styles_string = ';'.join(style_string_list)

        if fg_string or bg_string or styles_string:
            return '\033[{}m{}\033[0m'.format(';'.join(filter(len, [fg_string, bg_string, styles_string])), text)
        else:
            return text
        
    # always: enables color
    # never: disables color
    # auto: enables color only if output is a tty or console
    @classmethod
    def setWHEN(cls, when):
        if when in ('never', 'always', 'auto'):
            cls._when = when
        else:
            print("Invalid WHEN.  Valid values are 'never', 'always', or 'auto'.", file=sys.stderr)
            cls._when = 'never'

    @class_or_instancemethod
    def setForeground(self_or_cls, color):
        if color is None:
            self_or_cls._default_foreground = None
        else:
            if color.lower() not in self_or_cls._colors:
                print('Foreground color {} is not available.'.format(color), file=sys.stderr)
            else:
                self_or_cls._default_foreground = color

    @class_or_instancemethod
    def setBackground(self_or_cls, color):
        if color is None:
            self_or_cls._default_background = None
        else:
            if color.lower() not in self_or_cls._colors:
                print('Background color {} is not available.'.format(color), file=sys.stderr)
            else:
                self_or_cls._default_background = color

    @class_or_instancemethod
    def setStyles(self_or_cls, *style_list):
        self_or_cls._default_styles = []
        for style in style_list:
            if style is None:
                pass
            elif style.lower() not in self_or_cls._styles:
                print('Style {} is not available.'.format(style), file=sys.stderr)
            else:
                self_or_cls._default_styles.append(style)

    @class_or_instancemethod
    def setDefaults(self_or_cls, foreground=None, background=None, *style_list):
        self_or_cls.setForeground(foreground)
        self_or_cls.setBackground(background)
        self_or_cls.setStyles(*style_list)

    def __init__(self, foreground=None, background=None, *style_list):
        self.setForeground(foreground)
        self.setBackground(background)
        self.setStyles(*style_list)


if __name__ == "__main__":
    print('Color test.');   
    for color in sorted(ANSI.colors):
        print(ANSI.display('{:>40}'.format('This is a {} foreground!'.format(color)), color, None) + ANSI.display('{:<40}'.format('This is a {} background!'.format(color)), None, color))

    print()

    print('Style test.');
    for style in ANSI.styles:
        print(ANSI.display('This is a {} test!'.format(style), 'WHITE', None, style))
    
    print(ANSI.display('This should be red!', 'Red', None, 'UNDERLINE', 'BLINKING'))
    print(ANSI.display('This should be red!', 'RED'))
    print(ANSI.display('Testing', None, None, None, None, None, None))
    print(ANSI.display('Testing', 'FAKE', 'FAKE', 'FAKE', 'FAKE', 'FAKE', 'FAKE'))
    print(ANSI.display('Testing', 'RED', 'FAKE', 'FAKE', 'FAKE', 'FAKE', 'FAKE'))
    print(ANSI.display('Testing', 'RED', 'YELLOW', 'FAKE', 'FAKE', 'FAKE', 'FAKE'))
    print(ANSI.display('Testing', 'RED', 'YELLOW', 'UNDERLINE', 'FAKE', 'FAKE', 'FAKE'))
    
    ANSI.setBackground('BLUE')
    ANSI.setForeground('CYAN')
    ANSI.setStyles('STRIKETHROUGH', 'Invalid', 'UNDERLINE')

    print(ANSI.display('cyan on blue defaults'))

    ANSI.setDefaults('YELLOW', 'GREEN', 'STRIKETHROUGH', 'UNDERLINE')
    print(ANSI.display('yellow on green defaults'))

    red_error = ANSI('RED', 'WHITE', 'UNDERLINE')
    yellow_warning = ANSI('YELLOW', 'BLACK', 'UNDERLINE')

    print(yellow_warning.display('This is a yellow warning'))
    print(red_error.display('This is a red error'))

    red_error.setDefaults('Magenta', 'Green', 'Blinking')
    print(yellow_warning.display('This is a yellow warning'))
    print(red_error.display('This is a red error'))

    print(yellow_warning.display('This is a yellow warning'))
    print(red_error.display('This is a red error', 'Magenta', 'Green'))
   

    print(ANSI.display('yellow on green defaults'))

    print(yellow_warning.display('This is a yellow warning'))
    print(red_error.display('This is a red error'))

