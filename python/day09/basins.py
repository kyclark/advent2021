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
import operator
from functools import reduce
from itertools import chain
from typing import Any, List, NamedTuple, Optional, TextIO, Tuple


class Args(NamedTuple):
    """ Command-line arguments """
    file: TextIO


class Point(NamedTuple):
    """ A row/col tuple """
    row: int
    col: int


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
    print(m)

    lows = []
    for index, val in np.ndenumerate(m):
        neighbors = map(m.item, get_neighbors(index, m.shape))
        if all([val < n for n in neighbors]):
            lows.append(index)

    # print(lows)

    basins = []
    for i, low in enumerate(lows, start=1):
        # print('low', low)
        basin = set([low])
        while True:
            # print('basin', basin)
            neighbors = set(
                filter(
                    lambda pt: m.item(pt) != 9 and pt not in basin,
                    chain.from_iterable(
                        map(lambda pt: get_neighbors(pt, m.shape), basin))))
            # print('neighbors', neighbors)
            if neighbors:
                for n in neighbors:
                    basin.add(n)
            else:
                basins.append(len(basin))
                break

    basins = list(reversed(sorted(basins)))
    print('{} = {}'.format(' * '.join(map(str, basins[:3])),
                           reduce(operator.mul, basins[:3], 1)))


# --------------------------------------------------
def get_neighbors(pt: Point, shape: Point) -> List[Point]:
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

    return neighbors


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
def get_diagonals(pt: Point, shape: Point) -> List[Point]:
    """ Get diagonal neighbors """

    row, col = pt
    nrow, ncol = shape
    diagonals = []

    # above
    if row > 0:
        # above left
        if col > 0:
            diagonals.append((row - 1, col - 1))

        # above right
        if col < ncol - 1:
            diagonals.append((row - 1, col + 1))

    # below
    if row < nrow - 1:
        # below left
        if col > 0:
            diagonals.append((row + 1, col - 1))

        # below right
        if col < ncol - 1:
            diagonals.append((row + 1, col + 1))

    return diagonals


# --------------------------------------------------
def test_get_diagonals() -> None:
    """ test get_diagonals """

    # top-left corner
    assert get_diagonals((0, 0), (10, 10)) == [(1, 1)]

    # top-right corner
    assert get_diagonals((0, 10), (10, 10)) == [(1, 9)]

    # bottom-left corner
    assert get_diagonals((10, 0), (10, 10)) == [(9, 1)]

    # bottom-right corner
    assert get_diagonals((10, 10), (10, 10)) == [(9, 9)]

    # middle
    assert get_diagonals((5, 5), (10, 10)) == [(4, 4), (4, 6), (6, 4), (6, 6)]


# --------------------------------------------------
def get_perimeter(bounds: List[Point], shape: Point) -> Tuple[Point, Point]:
    """ Get perimeter """

    diagonals = set(
        chain.from_iterable(map(lambda pt: get_diagonals(pt, shape), bounds)))

    if len(diagonals) == 1:
        diagonals.add(bounds[0])

    rows = [row for row, col in diagonals]
    cols = [col for row, col in diagonals]

    return (Point(min(rows), min(cols)), Point(max(rows), max(cols)))


# --------------------------------------------------
def test_get_perimeter() -> None:
    """ Test get_perimeter """

    bounds = (10, 10)

    assert get_perimeter([(0, 0)], bounds) == (Point(0, 0), Point(1, 1))

    assert get_perimeter([(0, 10)], bounds) == (Point(0, 9), Point(1, 10))

    assert get_perimeter([(10, 0)], bounds) == (Point(9, 0), Point(10, 1))

    assert get_perimeter([(10, 10)], bounds) == (Point(9, 9), Point(10, 10))

    assert get_perimeter([(5, 5)], bounds) == (Point(4, 4), Point(6, 6))

    assert get_perimeter([(5, 5), (6, 6)], bounds) == (Point(4,
                                                             4), Point(7, 7))


# --------------------------------------------------
def fst(tup: Tuple[Any, Any]) -> Any:
    """ Return first element of tuple """

    return tup[0]


# --------------------------------------------------
def snd(tup: Tuple[Any, Any]) -> Any:
    """ Return second element of tuple """

    return tup[1]


# --------------------------------------------------
if __name__ == '__main__':
    main()
