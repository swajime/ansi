#!/usr/bin/env python
#
# Author: john@swajime.com
#
# Project started: 06/26/2020
#
# Compatible with Python 2 and Python 3
# Runs on Linux or Windows
#
# Please report any issues to john@swajime.com
#

"""ANSI wrapper for text strings

This class allows the user to wrap strings with ansi color escape sequences
without the user having to know how they work.
Examples follow:

Note that not all styles work on all terminals.
Also note that some styles do not mix well with colors.

To see colors available, view SwaANSI.colors
    from swajime import SwaANSI
    print(SwaANSI.colors)
    for color in sorted(SwaANSI.colors): print(SwaANSI.wrap(color, color))

To see styles available, view SwaANSI.styles
    from swajime import SwaANSI
    print(SwaANSI.styles)
    for style in sorted(SwaANSI.styles):
        print(SwaANSI.wrap(style, None, None, style))

The class can be accessed without instances:
    from swajime import SwaANSI
    print(SwaANSI.wrap('This is red text',
        'Red',
        'Yellow',
        'Bold', 'Underline', 'Strikethrough'))

Or you can create different objects with different attributes:
    from swajime import SwaANSI
    greenSuccess = SwaANSI('Green', None, 'Bold')
    yellowWarning = SwaANSI('Yellow', None, 'Underline')
    redError = SwaANSI('Red', None, 'Double Underline')

    print(greenSuccess.wrap('This is a green success'))
    print(yellowWarning.wrap('This is a yellow warning'))
    print(redError.wrap('This is a red error'))

Please report any bugs or issues to john@swajime.com
"""

# from __future__ imports must occur at the beginning of the file
from __future__ import print_function

from platform import system

import json
import os
import requests
import six
import sys

VERSION = "0.1.0"  # 07/22/2020
# color_file_dir is a subdirectory in $HOME
color_file_dir = 'dat'
color_file_name = 'color_data.json'

# My version of windows insists on putting a '<-' character on the screen
# instead of processing the escape characters
# Still have not found a fix.  This fix isn't working.
if 'win' in system().lower():
    from ctypes import windll
    k = windll.kernel32
    k.SetConsoleMode(k.GetStdHandle(-11), 7)
    # os.system("") # This fix doesn't work either


class _classOrInstancemethod(classmethod):
    """Private decorator allowing methods to be class methods or instance
    methods."""

    def __get__(self, instance, type_):
        descr_get = (super(_classOrInstancemethod, self).__get__ if
                     instance is None else self.__func__.__get__)
        return descr_get(instance, type_)


class MetaANSI(type):
    """Meta class used to initialize SwaANSI class before instantiating any
    objects.

    The SwaANSI class does not require object instantiation.
    """

    def __init__(cls, name, bases, d):
        """Sets up SwaANSI.colors and SwaANSI.styles tuples."""

        if 'HOME' not in os.environ:
            if 'HOMEDRIVE' not in os.environ or 'HOMEPATH' not in os.environ:
                raise EnvironmentError(
                    'The color library requires HOME or HOMEDRIVE and ' +
                    'HOMEPATH to be set in your environment.  JSON for ' +
                    'available colors will be stored in {}.'.format(
                       os.path.join('$HOME', color_file_dir, color_file_name)))
            HOME = os.getenv('HOMEDRIVE') + os.getenv('HOMEPATH')
        else:
            HOME = os.getenv('HOME')

        color_dir = os.path.join(HOME, color_file_dir)
        color_path = os.path.join(color_dir, color_file_name)
        if os.path.exists(color_path):
            with open(color_path, 'r') as color_file:
                color_data = json.load(color_file)
        else:
            print('Retrieving color data.  This is only necessary for the ' +
                  'first run.')
            print('WARNING: There seem to be duplicate color names in the ' +
                  'list, and there are clashes between web and X11 colors ' +
                  'in the CSS color scheme. Beware.')
            print('Please see https://jonasjacek.github.io/colors/ for more ' +
                  'information.')
            url = 'https://jonasjacek.github.io/colors/data.json'

            try:
                color_data = json.loads(requests.get(url).text)
            except Exception as e:
                print()
                print(str(e))
                print()
                print('Could not download data.json.  Please download {} to ' +
                      'the {} directory as {}.'.format(
                            url, color_dir, color_file_name))
                exit(1)

            if not os.path.isdir(color_dir):
                os.mkdir(color_dir)
            with open(color_path, 'w') as color_file:
                json.dump(color_data, color_file, indent=4)

        for color in color_data:
            cls._colors[color['name']] = color['colorId']

        # Make colors available as class tuple
        cls.colors = tuple(cls._colors.keys())

        # enable case insensitive lookups
        for color in cls.colors:
            cls._colors[color.lower()] = cls._colors[color]

        proper_style = []
        for style in cls._styles.keys():
            proper_style.append(style.title())

        # Make styles available as class tuple
        cls.styles = tuple(proper_style)

        # enable case insensitive lookups
        for style in cls._styles:
            cls._styles[style.lower()] = cls._styles[style]


class SwaANSI(six.with_metaclass(MetaANSI, object)):
    """Allows adding color and other attributes to text strings.

    Attributes
    ----------
    colors : tuple(str)
        a list of strings identifying available colors
    styles : tuple(str)
        a list of strings identifying available attributes

    Methods
    -------
    setWHEN('always'|'auto'|'never')
        Enable or disable the wrap of colors and attributes
    setForeground(color=None)
        Set the foreground for class or instance for future wrap
    setBackground(color=None)
        Set the background for class or instance for future wrap
    setStyles(*style_list)
        Set the styles for class or instance for future wrap
    setDefaults(foreground=None, background=None, *style_list)
        Set all colors and attributes for class or instance for future wrap
    wrap(text=None, foreground=None, background=None, *style_list)
        Wrap the text with escape codes for the given (or previously set)
            attributes
    """

    _when = 'always'
    _colors = {}
    _default_foreground = None
    _default_background = None
    _default_styles = []
    _styles = {'default': '0',
               'reset': '0',
               'normal': '0',
               'bold': '1',
               'faint': '2',
               'italic': '3',
               'underline': '4',
               'blinking': '5',
               'slow blink': '5',
               'fast_blinking': '6',
               'rapid blink': '6',
               'reverse': '7',
               'hide': '8',
               'conceal': '8',
               'strikethrough': '9',
               'crossed-out': '9',
               'fraktur': '20',
               'double underline': '21',
               'framed': '51',
               'encircled': '52',
               'overlined': '53',
               'underline color': '58',
               'ideogram underline': '60',
               'ideogram double underline': '61',
               'ideogram overline': '62',
               'ideogram double overline': '63',
               'ideogram stress': '64',
               'superscript': '73',
               'subscript': '74'
               }

    def __init__(self, foreground=None, background=None, *style_list):
        """
        Parameters
        ----------
        foreground : str, optional
            The foreground color to be added for future wraps
        background : str, optional
            The background color to be added for future wraps
        style_list : list(str), optional
            A list of styles to be added for future wraps
        """

        self.setForeground(foreground)
        self.setBackground(background)
        self.setStyles(*style_list)

    # always: enables color
    # never: disables color
    # auto: enables color only if output is a tty or console
    @classmethod
    def setWHEN(cls, when):
        """Enables or disables SwaANSI.

        Parameters
        ----------
        when : str, mandatory
            Preset to 'always'.
            'always': Always add color and attributes.
            'never': Never add color and attributes.
            'auto': Add color and attributes if output is a tty.
        """

        if when.lower() in ('never', 'always', 'auto'):
            cls._when = when.lower()
        else:
            print("Invalid WHEN.  Valid values are 'never', 'always', or " +
                  "'auto'.", file=sys.stderr)
            cls._when = 'never'

    @_classOrInstancemethod
    def setForeground(self_or_cls, color=None):  # NOSONAR
        """Sets the foreground color to be used for a class or an instance.

        If the argument `color` isn't passed in, the foreground is not set by
            default when wrapping.

        Parameters
        ----------
        color : str, optional
            Set the default foreground color for future wrapping.
        """

        if color is None:
            self_or_cls._default_foreground = None
        else:
            if color.lower() not in self_or_cls._colors:
                print('Foreground color {} is not available.'.format(color),
                      file=sys.stderr)
            else:
                self_or_cls._default_foreground = color

    @_classOrInstancemethod
    def setBackground(self_or_cls, color=None):  # NOSONAR
        """Sets the background color to be used for a class or an instance.

        If the argument `color` isn't passed in, the background is not set by
            default when wrapping.

        Parameters
        ----------
        color : str, optional
            Set the default background color for future wrapping.
        """

        if color is None:
            self_or_cls._default_background = None
        else:
            if color.lower() not in self_or_cls._colors:
                print('Background color {} is not available.'.format(color),
                      file=sys.stderr)
            else:
                self_or_cls._default_background = color

    @_classOrInstancemethod
    def setStyles(self_or_cls, *style_list):  # NOSONAR
        """Sets the style list to be used for a class or an instance.

        If no `style_list` arguments are passed in, the attributes are not set
            by default when wrapping.

        Parameters
        ----------
        style_list : list[str], optional
            Set the default style list for future wrapping.
        """

        self_or_cls._default_styles = []
        for style in style_list:
            if style is None:
                pass  # NOSONAR
            elif style.lower() not in self_or_cls._styles:
                print('Style {} is not available.'.format(style),
                      file=sys.stderr)
            elif style is not None:
                self_or_cls._default_styles.append(style)

    @_classOrInstancemethod
    def setDefaults(self_or_cls, foreground=None, background=None,  # NOSONAR
                    *style_list):
        """Sets the foreground, background, and style list to be used for a
            class or an instance.

        All parameters are optional.

        Parameters
        ----------
        foreground : str, optional
            Set the default foreground color for future wrapping.
        background : str, optional
            Set the default background color for future wrapping.
        style_list : list[str], optional
            Set the default style list for future wrapping.
        """

        self_or_cls.setForeground(foreground)
        self_or_cls.setBackground(background)
        self_or_cls.setStyles(*style_list)

    @_classOrInstancemethod
    def wrap(self_or_cls, text=None, foreground=None, background=None,  # NOSONAR
             *style_list):
        """Wraps the text string with ansi escape codes for color and attributes.

        All parameters are optional.

        Parameters:
        text : str, optional
            The text that will be wrapped
        foreground:
            If set, overrides the default foreground color
        background:
            If set, overrides the default background color
        style_list:
            If set, overrides the default style list
        """

        # only add ansi if _when is 'always' or output is a tty
        if text is None or text == '' or self_or_cls._when == 'never' or (
                self_or_cls._when == 'auto' and not sys.stdout.isatty()):
            return text

        if foreground is None:
            foreground = self_or_cls._default_foreground
        if foreground:
            if foreground.lower() not in self_or_cls._colors:
                print('Foreground color {} is not available.'.
                      format(foreground), file=sys.stderr)
                fg_string = ''
            else:
                fg_string = '38;5;{}'.format(self_or_cls._colors[foreground.
                                                                 lower()])
        else:
            fg_string = ''

        if background is None:
            background = self_or_cls._default_background
        if background:
            if background.lower() not in self_or_cls._colors:
                print('Background color {} is not available.'.
                      format(background), file=sys.stderr)
                bg_string = ''
            else:
                bg_string = '48;5;{}'.format(self_or_cls._colors[background.
                                                                 lower()])
        else:
            bg_string = ''

        if len(style_list) == 0:
            style_list = self_or_cls._default_styles
        style_string_list = []
        for style in style_list:
            if style is None:
                pass  # NOSONAR
            elif style.lower() not in self_or_cls._styles:
                print('Style {} is not available.'.
                      format(style), file=sys.stderr)
            elif style is not None:
                style_string_list.append(self_or_cls._styles[style.lower()])
        styles_string = ';'.join(style_string_list)

        if fg_string or bg_string or styles_string:
            return '\033[{}m{}\033[0m'.format(
                ';'.join(filter(len, [fg_string, bg_string, styles_string])),
                text)
        else:
            return text


if __name__ == "__main__":
    print('Color test.')
    for color in sorted(SwaANSI.colors):
        print(SwaANSI.wrap('{:>40}'.
                           format('This is a {} foreground!'.format(color)),
                           color, None) +
              SwaANSI.wrap('{:<40}'.
                           format('This is a {} background!'.format(color)),
                           None, color))

    print()

    print('Style test.')
    for style in SwaANSI.styles:
        print(SwaANSI.wrap('This is a {} test!'.format(style),
                           'WHITE', None, style))

    print(SwaANSI.wrap('This should be red!', 'Red',
                       None, 'UNDERLINE', 'BLINKING'))
    print(SwaANSI.wrap('This should be red!', 'RED'))
    print(SwaANSI.wrap('Testing', None, None, None, None, None, None))
    print(SwaANSI.wrap('Testing', 'FAKE', 'FAKE', 'FAKE', 'FAKE', 'FAKE'))
    print(SwaANSI.wrap('Testing', 'RED', 'FAKE', 'FAKE', 'FAKE', 'FAKE'))
    print(SwaANSI.wrap('Testing', 'RED', 'YELLOW', 'FAKE', 'FAKE', 'FAKE'))
    print(SwaANSI.wrap('Testing', 'RED', 'YELLOW', 'UNDERLINE', 'FAKE'))

    SwaANSI.setBackground('BLUE')
    SwaANSI.setForeground('CYAN')
    SwaANSI.setStyles('STRIKETHROUGH', 'Invalid', 'UNDERLINE')

    print(SwaANSI.wrap('cyan on blue defaults'))

    SwaANSI.setDefaults('YELLOW', 'GREEN', 'STRIKETHROUGH', 'UNDERLINE')
    print(SwaANSI.wrap('yellow on green defaults'))

    red_error = SwaANSI('RED', 'WHITE', 'UNDERLINE')
    yellow_warning = SwaANSI('YELLOW', 'BLACK', 'UNDERLINE')

    print(yellow_warning.wrap('This is a yellow warning'))
    print(red_error.wrap('This is a red error'))

    red_error.setDefaults('Magenta', 'Green', 'Blinking')
    print(yellow_warning.wrap('This is a yellow warning'))
    print(red_error.wrap('This is a red error'))

    print(yellow_warning.wrap('This is a yellow warning'))
    print(red_error.wrap('This is a red error', 'Magenta', 'Green'))

    print(SwaANSI.wrap('yellow on green defaults'))

    print(yellow_warning.wrap('This is a yellow warning'))
    print(red_error.wrap('This is a red error'))

    print(SwaANSI.wrap('Testing Complete',
                       foreground='Cyan', background='Blue'))

    plainANSI = SwaANSI()
    plainANSI.setForeground()
    plainANSI.setBackground()
    plainANSI.setStyles()
    plainANSI.setDefaults()
    print(plainANSI.wrap())
    print(plainANSI.wrap("Hello World!"))
