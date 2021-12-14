#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2021-12-13
Purpose: Find path
"""

import argparse
import numpy as np
import re
import sys
from typing import Any, List, NamedTuple, Optional, TextIO, Tuple


class Point(NamedTuple):
    """ A row/col tuple """
    row: int
    col: int


class Args(NamedTuple):
    """ Command-line arguments """
    puzzle: TextIO
    start: Point
    end: Point


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Find path',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-s', '--start', help='Starting point')

    parser.add_argument('-e', '--end', help='Ending point')

    parser.add_argument('-p',
                        '--puzzle',
                        help='Input puzzle file',
                        metavar='FILE',
                        type=argparse.FileType('rt'))

    args = parser.parse_args()

    start = parse_point(args.start)
    if not start:
        parser.error(f'Invalid --start "{args.start}"')

    end = parse_point(args.end)
    if not end:
        parser.error(f'Invalid --end "{args.end}"')

    return Args(puzzle=args.puzzle, start=start, end=end)


# --------------------------------------------------
def parse_point(val: str) -> Optional[Point]:
    """ Parse input as point """

    if matches := re.search('^(\d+),(\d+)$', val):
        return Point(int(matches.group(1)), int(matches.group(2)))


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    data = '; '.join(
        map(lambda line: ' '.join(list(line)),
            args.puzzle.read().splitlines()))

    m = np.matrix(data)
    print(m)

    paths = [[args.start]]
    while True:
        new_paths = []
        for path in paths:
            terminal = path[-1]
            # Do not backtrack
            neighbors = filter(lambda pt: pt not in path,
                               get_neighbors(terminal, m.shape))
            # print('terminal', terminal)
            # print('neighbors', neighbors)
            forward = list(
                map(
                    fst,
                    filter(lambda tup: snd(tup) == 0,
                           map(lambda pt: (pt, m.item(pt)), neighbors))))

            # print('forward', forward)
            if forward:
                for pt in forward:
                    new_path = path + [pt]
                    if pt == args.end:
                        print('Found end!')
                        for row, col in new_path:
                            m[row, col] = 8
                        print(m)
                        sys.exit()
                    else:
                        new_paths.append(new_path)

        if new_paths:
            paths = new_paths
        else:
            print('No solution')
            break


# --------------------------------------------------
def fst(tup: Tuple[Any, Any]) -> Any:
    """ Return first element of tuple """

    return tup[0]


# --------------------------------------------------
def snd(tup: Tuple[Any, Any]) -> Any:
    """ Return second element of tuple """

    return tup[1]


# --------------------------------------------------
def get_neighbors(pt: Point, shape: Tuple[int, int]) -> List[Point]:
    """ Get neighbors """

    row, col = pt
    nrow, ncol = shape

    neighbors = []
    # above
    if row > 0:
        neighbors.append((row - 1, col))

    # below
    if row < nrow - 1:
        neighbors.append((row + 1, col))

    # left
    if col > 0:
        neighbors.append((row, col - 1))

    # right
    if col < ncol - 1:
        neighbors.append((row, col + 1))

    return set(neighbors)


# --------------------------------------------------
if __name__ == '__main__':
    main()
