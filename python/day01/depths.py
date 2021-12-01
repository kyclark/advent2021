#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2021-12-01
Purpose: Rock the Casbah
"""

import argparse
from typing import NamedTuple, TextIO


class Args(NamedTuple):
    """ Command-line arguments """
    file: TextIO


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Rock the Casbah',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        help='Input data file',
                        metavar='FILE',
                        type=argparse.FileType('rt'))

    args = parser.parse_args()

    return Args(args.file)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    prev = ''
    num_increased = 0

    for num in map(lambda n: int(n.rstrip()), args.file):
        if prev == '':
            print('(N/A - no previous measurement)')
        else:
            print('{} ({}creased)'.format(num, 'in' if num > prev else 'de'))
            if num > prev:
                num_increased += 1

        prev = num

    print(f'{num_increased} increase')

# --------------------------------------------------
if __name__ == '__main__':
    main()
