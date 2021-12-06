#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2021-12-06
Purpose: Rock the Casbah
"""

import argparse
import os
from pprint import pprint
from collections import defaultdict
from typing import NamedTuple, TextIO


class Args(NamedTuple):
    """ Command-line arguments """
    state: str
    days: int


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Rock the Casbah',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('state', metavar='STR', help='Starting ages')

    parser.add_argument('-d',
                        '--days',
                        metavar='INT',
                        type=int,
                        default=80,
                        help='Number of days for simulation')

    args = parser.parse_args()

    if os.path.isfile(args.state):
        args.state = open(args.state).read().rstrip()

    return Args(args.state, args.days)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    ages = defaultdict(int)
    for age in map(int, args.state.split(',')):
        ages[age] += 1

    print(ages)

    for day in range(1, args.days + 1):
        print(f'Day {day:04d}')
        new = defaultdict(int)
        for age, num in ages.items():
            if age == 0:
                new[6] += num
                new[8] += num
            else:
                new[age - 1] += num
        ages = new

    print(f'There are {sum(ages.values())} fish')


# --------------------------------------------------
if __name__ == '__main__':
    main()
