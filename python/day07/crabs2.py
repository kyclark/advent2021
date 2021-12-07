#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2021-12-06
Purpose: Rock the Casbah
"""

import argparse
import os
from pprint import pprint
from typing import NamedTuple, TextIO


class Args(NamedTuple):
    """ Command-line arguments """
    state: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Rock the Casbah',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('positions', metavar='STR', help='Starting positions')

    args = parser.parse_args()

    if os.path.isfile(args.positions):
        args.positions = open(args.positions).read().rstrip()

    return Args(args.positions)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    pos = list(sorted(map(int, args.state.split(','))))
    costs = []

    for start in range(pos[0], pos[-1] + 1):
        price = sum([cost(start, x) for x in pos])
        costs.append(price)

    print(sorted(costs)[0])


# --------------------------------------------------
def cost(start: int, end: int) -> int:
    """ Expand N by distance """

    dist = abs(end - start)
    return sum(range(1, dist + 1))


# --------------------------------------------------
def test_cost() -> None:
    """ Test expand """

    assert cost(1, 2) == 1 # 1
    assert cost(1, 3) == 3 # 2
    assert cost(1, 4) == 6 # 3
    assert cost(1, 5) == 10 # 4
    assert cost(1, 6) == 15 # 5

    assert cost(2, 1) == 1 # 1
    assert cost(6, 1) == 15 # 5
    assert cost(16, 5) == 66 # 5


# --------------------------------------------------
if __name__ == '__main__':
    main()
