#!/usr/bin/env python
#

from __future__ import print_function
from subprocess import check_output, STDOUT, CalledProcessError
from ansi import ANSI

import argparse
import os
import sys

def fsdecode(byte_or_str):
    if sys.version_info >= (3, 0):
        if isinstance(byte_or_str, str):
            return byte_or_str
        else:
            return byte_or_str.decode(sys.stdout.encoding)
    else:
        #return str(byte_or_str, sys.stdout.encoding)
        return str(byte_or_str.encode(sys.stdout.encoding))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Just a test script',
        epilog='Using color to distinguish file types is disabled both by default and with --color=never.  With --color=auto, ls emits color codes only when standard output is connected to a terminal.')
    parser.add_argument('--color', nargs='?', const='always', default='never',
        help="colorize the output; WHEN can be 'never', 'auto', or 'always' (the default); more info below",
        choices=['never', 'always', 'auto'],
        metavar='=WHEN')
    parser.add_argument('--version', action='version', version='%(prog)s 0.0.1')
    
    args = parser.parse_args()
    ANSI.setWHEN(args.color)

    output = ''

    try:
        output += fsdecode(check_output(['java', 'HelloWorld'], stderr=STDOUT))
        output += fsdecode(check_output(['java', 'a_ExcelWriter'], stderr=STDOUT))
        output += fsdecode(check_output(['java', 'SimpleExcelReaderExample'], stderr=STDOUT))
        print(output)
    
    except CalledProcessError as e:
        if output:
            print(output)

        if e.output:
            print(ANSI.setANSI(fsdecode(e.output), 'Yellow', 'Black'))

        print(ANSI.setANSI("CalledProcessError: Command '{}' returned {}.".format(" ".join(e.cmd), e.returncode), 'Red', 'Black'))

    except OSError as e:
        if output:
            print(output)
        
        if e.filename:
            print(ANSI.setANSI("OSError: {}: {} in file {}.".format(e.errno, e.strerror, e.filename), 'Red', 'Black'))
        else:
            print(ANSI.setANSI("OSError: {}: {}.".format(e.errno, e.strerror), 'Red', 'Black'))
