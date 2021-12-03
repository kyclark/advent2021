#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2021-12-03
Purpose: Rock the Casbah
"""

import argparse
from pprint import pprint
from typing import List, NamedTuple, TextIO, Optional


class Args(NamedTuple):
    """ Command-line arguments """
    file: TextIO


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Rock the Casbah',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        help='Data input file',
                        metavar='FILE',
                        type=argparse.FileType('rt'))

    args = parser.parse_args()

    return Args(args.file)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    nums = [list(v.rstrip()) for v in args.file]
    oxygen = calc(nums, True)
    oxygen_val = int(oxygen, base=2)
    print(f'oxygen {oxygen} oxygen_val {oxygen_val}')

    co2 = calc(nums, False)
    co2_val = int(co2, base=2)
    print(f'co2 {co2} co2_val {co2_val}')

    print(f'oxygen {oxygen_val} * co2 {co2_val} = {oxygen_val * co2_val}')


# --------------------------------------------------
def calc(vals: List[List[str]], most_wanted: bool) -> Optional[str]:
    """ Calculate """

    copied = vals[:]
    for i in range(len(vals[0])):
        bits = [n[i] for n in copied]
        ones = len(list(filter(lambda b: b == '1', bits)))
        zeros = len(bits) - ones
        most_common, least_common = ('1', '0') if ones >= zeros else ('0', '1')
        cmp = most_common if most_wanted else least_common
        copied = [v for v in copied if v[i] == cmp]

        if len(copied) == 1:
            return ''.join(copied[0])


# --------------------------------------------------
if __name__ == '__main__':
    main()
