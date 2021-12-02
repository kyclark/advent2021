#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2021-12-02
Purpose: Rock the Casbah
"""

import argparse
import sys
from typing import NamedTuple, TextIO


class Args(NamedTuple):
    """ Command-line arguments """
    data: TextIO


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Rock the Casbah',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-f',
                        '--file',
                        help='Data input file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        default=sys.stdin)

    args = parser.parse_args()

    return Args(args.file)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    horz, depth = 0, 0

    for line in args.data:
        direction, num = line.rstrip().split()
        num = int(num)

        if direction == 'forward':
            horz += num
        elif direction == 'down':
            depth += num
        elif direction == 'up':
            depth -= num

    print(f'horz {horz} * depth {depth} = {horz * depth}')

#
# --------------------------------------------------
if __name__ == '__main__':
    main()
