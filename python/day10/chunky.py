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

    val = {')': 3, ']': 57, '}': 1197, '>': 25137}
    nums = []
    for line in map(str.rstrip, args.data):
      if bad := is_corrupt(line):
            n = val.get(bad, 0)
            print(bad, n)
            nums.append(n)

    print(' + '.join(map(str, nums)), '=', sum(nums))


# --------------------------------------------------
def is_corrupt(val: str) -> str:
    """ Return unexpected character if corrupt, else empty string """

    expected = {')': '(', '}': '{', ']': '[', '>': '<'}
    opened = []
    for char in list(val):
        if char in '({[<':
            opened.append(char)
        elif char in ')}]>':
            if opened and opened[-1] == expected[char]:
                opened.pop(-1)
            else:
                return char
        else:
            return char

    return ''


# --------------------------------------------------
def test_is_corrupt() -> None:
    """ Test is_corrupt """

    # assert is_corrupt('(')
    # assert is_corrupt('[')
    # assert is_corrupt('{')
    # assert is_corrupt('<')
    # assert is_corrupt(')')
    # assert is_corrupt(']')
    # assert is_corrupt('}')
    # assert is_corrupt('>')

    assert is_corrupt('()') == ''
    assert is_corrupt('([])') == ''
    assert is_corrupt('([]>') == '>'
    assert is_corrupt('([])') == ''
    assert is_corrupt('{()()()}') == ''
    assert is_corrupt('<([{}])>') == ''
    assert is_corrupt('[<>({}){}[([])<>]]') == ''
    assert is_corrupt('(((((((((())))))))))') == ''

    assert is_corrupt('(]') == ']'
    assert is_corrupt('((])') == ']'
    assert is_corrupt('{()()()>') == '>'
    assert is_corrupt('(((()))}') == '}'
    assert is_corrupt('<([]){()}[{}])') == ')'
    assert is_corrupt('{([(<{}[<>[]}>{[]{[(<()>') == '}'
    assert is_corrupt('[[<[([]))<([[{}[[()]]]') == ')'
    assert is_corrupt('[{[{({}]{}}([{[{{{}}([]') == ']'
    assert is_corrupt('[<(<(<(<{}))><([]([]()') == ')'
    assert is_corrupt('<{([([[(<>()){}]>(<<{{') == '>'



# --------------------------------------------------
if __name__ == '__main__':
    main()
