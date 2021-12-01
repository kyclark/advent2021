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
    window: int


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

    parser.add_argument('-w',
                        '--window',
                        help='Window size',
                        metavar='INT',
                        type=int,
                        default=3)

    args = parser.parse_args()

    return Args(args.file, args.window)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    window = []
    num_increased = 0

    for num in map(lambda n: int(n.rstrip()), args.file):
        if len(window) < args.window:
            window.append(num)
            continue

        prev = sum(window)
        window.pop(0)
        window.append(num)
        this = sum(window)

        print('{} ({}creased)'.format(num, 'in' if this > prev else 'de'))
        if this > prev:
            num_increased += 1

    print(f'{num_increased} increase')


# --------------------------------------------------
if __name__ == '__main__':
    main()
