#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2021-12-17
Purpose: Rock the Casbah
"""

import argparse
import sys
from typing import NamedTuple, TextIO


class Args(NamedTuple):
    """ Command-line arguments """
    data: TextIO


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Rock the Casbah',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('data',
                        help='Input data/file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        default=sys.stdin)

    args = parser.parse_args()

    return Args(args.data)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    vals = {'(': 1, '{': 3, '[': 2, '<': 4}
    expected = {'(': ')', '{': '}', '[': ']', '<': '>'}
    totals = []

    for line in map(str.rstrip, args.data):
        total = 0
        if rem := remainder(line):
            fix = ''.join(map(expected.get, rem))
            print(' :: '.join([line, fix]))
            for val in map(vals.get, rem):
                print(f'total "{total}" val "{val}"')
                total *= 5
                total += val
            print(total)
            totals.append(total)

    print(totals)
    totals.sort()
    mid = len(totals) // 2
    print('mid', totals[mid])


# --------------------------------------------------
def remainder(val: str) -> str:
    """ Return unpaired chars, else empty string """

    expected = {')': '(', '}': '{', ']': '[', '>': '<'}
    opened = []
    for char in list(val):
        if char in '({[<':
            opened.append(char)
        elif char in ')}]>':
            if opened and opened[-1] == expected[char]:
                opened.pop(-1)
            else:
                return ''
        else:
            return ''

    return ''.join(reversed(opened))


# --------------------------------------------------
def test_remainder() -> None:
    """ Test remainder """

    assert remainder('(') == '('
    assert remainder('[') == '['
    assert remainder('{') == '{'
    assert remainder('<') == '<'
    assert remainder('(()') == '('
    assert remainder('([]') == '('
    assert remainder('({}') == '('
    assert remainder('(<>') == '('


# --------------------------------------------------
if __name__ == '__main__':
    main()
