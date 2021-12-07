#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2021-12-06
Purpose: Rock the Casbah
"""

import argparse
import os
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
        cost = sum([abs(start - x) for x in pos])
        print(f'{start} = {cost}')
        costs.append(cost)

    print(sorted(costs)[0])


# --------------------------------------------------
if __name__ == '__main__':
    main()
