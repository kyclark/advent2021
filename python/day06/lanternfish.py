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
    ages = list(map(int, args.state.split(',')))

    print(f'Initial state: {",".join(map(str, ages))}')

    for day in range(1, args.days + 1):
        print(f'Day {day:04d}')
        cur, new = [], []
        for num in ages:
            if num == 0:
                cur.append(6)
                new.append(8)
            else:
                cur.append(num - 1)
        ages = cur + new

        # print('After {} day{}: {}'.format(day, "s" if day > 1 else "",
        #                                   ",".join(map(str, ages))))

    print(f'There are {len(ages)} fish')


# --------------------------------------------------
if __name__ == '__main__':
    main()
