#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2021-12-05
Purpose: Rock the Casbah
"""

import argparse
import sys
from collections import defaultdict
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
    grid = defaultdict(int)

    for line in map(str.rstrip, args.file):
        # print(f'>>> line {line}')
        start, _, stop = line.split(' ')
        x1, y1 = map(int, start.split(','))
        x2, y2 = map(int, stop.split(','))

        if not (x1 == x2 or y1 == y2):
            continue

        xs = range(x1, x2 - 1, -1) if x1 > x2 else range(x1, x2 + 1)
        ys = range(y1, y2 - 1, -1) if y1 > y2 else range(y1, y2 + 1)

        # print(f'({x1}, {y1}) -> ({x2}, {y2})')
        for x in xs:
            for y in ys:
                # print(f'({x}, {y})')
                grid[(x, y)] += 1

        # show_grid(grid)

    print(len([v for v in grid.values() if v > 1]))


# --------------------------------------------------
def show_grid(grid):
    """ Show grid """

    max_x = max([x for x, y in grid.keys()])
    max_y = max([y for x, y in grid.keys()])

    for y in range(0, max_y + 1):
        for x in range(0, max_x + 1):
            print(grid.get((x, y), '.'), end='')
        print()


# --------------------------------------------------
if __name__ == '__main__':
    main()
