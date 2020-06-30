#!/usr/bin/env python
#
# Author: John.Simpson@hmhs.com john@swajime.com
# 
# This is just a test script for ansi.py
# Works with Python 2 or Python 3
# Runs on Linux or Windows
#
# Please report any issues to author.
#

# from __future__ imports must occur at the beginning of the file
from __future__ import print_function

VERSION = "0.0.3"
WARNING_COLOR = "YELLOW"
ERROR_COLOR = "RED"

from subprocess import check_output, STDOUT, CalledProcessError
from swajime import SwaANSI as ANSI

import argparse
import sys

# The purpose of this function is to convert bytestrings or strings to strings before printing.
# The check_output function for example returns bytestrings or strings depending on Python version.
def fsdecode(byte_or_str):
    if byte_or_str is None:
        return None
    elif sys.version_info >= (3, 0):
        if isinstance(byte_or_str, str):
            return byte_or_str
        else:
            return byte_or_str.decode(sys.stdout.encoding)
    else:
        if sys.stdout.encoding is None:
            return str(byte_or_str)
        else:
            return str(byte_or_str.encode(sys.stdout.encoding))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Just a test script',
        epilog='Using color to distinguish file types is disabled both by default and with --color=never.  With --color=auto, ls emits color codes only when standard output is connected to a terminal.')
    parser.add_argument('--color', nargs='?', const='always', default='never',
        help="colorize the output; WHEN can be 'never', 'auto', or 'always' (the default); more info below",
        choices=['never', 'always', 'auto'],
        metavar='=WHEN')
    parser.add_argument('--version', action='version', version='%(prog)s ' + VERSION)
    
    args = parser.parse_args()
    ANSI.setWHEN(args.color)
    
    yellowWarning = ANSI(WARNING_COLOR)
    redError = ANSI(ERROR_COLOR, None, 'BLINKING')
    
    output = ''

    try:
        # attempt some shell commands that may error out
        output += ANSI.display('Use --color option to enable color.', 'YELLOW', None, 'UNDERLINE') + '\n'
        output += fsdecode(check_output(['echo', 'java', 'HelloWorld'], stderr=STDOUT))
        output += fsdecode(check_output(['java', 'not found', 'ExcelWriter'], stderr=STDOUT))
        output += fsdecode(check_output(['echo', 'java', 'SimpleExcelReaderExample'], stderr=STDOUT))
        print(output)
    
    except CalledProcessError as e:
        # print any output we did collect
        if output:
            print(output)

        # print any output we can from the failing call in YELLOW
        if e.output:
            print(yellowWarning.display(fsdecode(e.output)))

        # print the error itself in RED
        print(redError.display("CalledProcessError: Command '{}' returned {}.".format(" ".join(e.cmd), e.returncode)))

    except OSError as e:
        # print any output we did collect
        if output:
            print(output)
        
        # print the error itself in RED
        if e.filename:
            print(ANSI.display("OSError: {}: {} in file {}.".format(e.errno, e.strerror, e.filename), ERROR_COLOR))
        else:
            print(ANSI.display("OSError: {}: {}.".format(e.errno, e.strerror), ERROR_COLOR))
