#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2021-12-08
Purpose: Rock the Casbah
"""

import argparse
import re
import sys
from pprint import pprint
from collections import defaultdict
from typing import List, NamedTuple, TextIO


class Args(NamedTuple):
    """ Command-line arguments """
    file: TextIO


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Rock the Casbah',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-f',
                        '--file',
                        help='A readable file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        default=sys.stdin)

    args = parser.parse_args()

    return Args(args.file)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()

    num = 0
    for line in map(str.rstrip, args.file):
        _, output = re.split(r'\s*[|]\s*', line)
        num += len(
            list(filter(lambda n: n in [2, 3, 4, 7], map(len,
                                                         output.split()))))
    print(num)


# --------------------------------------------------
if __name__ == '__main__':
    main()
