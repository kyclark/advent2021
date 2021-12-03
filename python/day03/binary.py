#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2021-12-03
Purpose: Rock the Casbah
"""

import argparse
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
    nums = [list(map(int, list(v.rstrip()))) for v in args.file]
    epsilon, gamma = '', ''

    for i in range(len(nums[0])):
        bits = [n[i] for n in nums]
        ones = len(list(filter(lambda b: b, bits)))
        zeros = len(bits) - ones
        epsilon += '1' if ones > zeros else '0'
        gamma += '0' if ones > zeros else '1'

    epsilon_bin = int(epsilon, base=2)
    gamma_bin = int(gamma, base=2)
    print(f'epsilon {epsilon} ({epsilon_bin}) gamma {gamma} ({gamma_bin}) = '
          f'{epsilon_bin * gamma_bin}')


# --------------------------------------------------
if __name__ == '__main__':
    main()
