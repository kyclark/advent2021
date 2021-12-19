#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2021-12-08
Purpose: Rock the Casbah
"""

import argparse
import re
import sys
import numpy as np
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
    data = '; '.join(
        map(lambda line: ' '.join(list(line)),
            args.file.read().splitlines()))

    m = np.matrix(data)
    # print(m)

    lows = []
    for index, val in np.ndenumerate(m):
        neighbors = map(m.item, get_neighbors(index, m.shape))
        if all([val < n for n in neighbors]):
            lows.append(val)

    print(sum(map(lambda n: n + 1, lows)))


# --------------------------------------------------
def get_neighbors(pt, shape):
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
def test_get_neighbors() -> None:
    """ test get_neighbors """

    # top-left corner
    assert get_neighbors((0, 0), (10, 10)) == set([(0, 1), (1, 0)])

    # top-right corner
    assert get_neighbors((0, 10), (10, 10)) == set([(0, 9), (1, 10)])

    # bottom-left corner
    assert get_neighbors((10, 0), (10, 10)) == set([(9, 0), (10, 1)])

    # bottom-right corner
    assert get_neighbors((10, 10), (10, 10)) == set([(9, 10), (10, 9)])

    # middle
    assert get_neighbors((5, 5), (10, 10)) == set([(4, 5), (5, 4), (5, 6),
                                                   (6, 5)])


# --------------------------------------------------
if __name__ == '__main__':
    main()
