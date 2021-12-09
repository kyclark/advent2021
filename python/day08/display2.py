#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2021-12-08
Purpose: Rock the Casbah
"""

import argparse
import re
import sys
from itertools import chain
from random import shuffle
from functools import reduce
from pprint import pprint
from collections import defaultdict
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
    digits = []

    for line in map(str.rstrip, args.file):
        patterns, output = re.split(r'\s*[|]\s*', line)
        decoded = decode(patterns.split())
        output = list(map(lambda s: ''.join(sorted(s)), output.split()))
        digit = ''.join(map(decoded.get, output))
        # print(digit)
        digits.append(int(digit))

    print(sum(digits))


# --------------------------------------------------
def decode(patterns: List[str]):
    """
     aaaaaa   1* =   c  f   2*  0010010
    b      c  2  = a cde g  5   1011101
    b      c  3  = a cd fg  5   1011011
    b      c  4* =  bcd f   4*  0111010
     dddddd   5  = ab d fg  5   1101011
    e      f  6  = ab defg  6   1101111
    e      f  7* = a c  f   3*  1010010
    e      f  8* = abcdefg  7*  1111111
     gggggg   9  = abcd fg  6   1111011
              0  = abc efg  6   1110111
    """

    patterns = list(reversed(sorted(patterns, key=len)))
    bits = list(patterns[0])
    assert len(bits) == 7
    pos = dict([(y, x) for x, y in enumerate(bits)])

    bits_by_len = defaultdict(list)
    for pat in patterns:
        mask = ['0'] * 7
        for char in pat:
            mask[pos[char]] = '1'
        mask = int(''.join(mask), 2)
        bits_by_len[len(pat)].append((pat, mask))

    one = bits_by_len[2][0][1]
    seven = bits_by_len[3][0][1]
    pos_a = one ^ seven

    pos_f = ''
    for b in bits_by_len[6]:
        mask = one & b[1]
        if count_set_bits(mask) == 1:
            pos_f = mask

    pos_c = one ^ pos_f
    fives = list(map(lambda t: t[1], bits_by_len[5]))
    horz = reduce(lambda a, b: a & b, fives)
    pos_d = horz & bits_by_len[4][0][1]
    four = bits_by_len[4][0][1]
    pos_b = four ^ pos_c ^ pos_d ^ pos_f
    eight = bits_by_len[7][0][1]
    pos_e = eight ^ horz ^ pos_b ^ pos_c ^ pos_f
    pos_g = eight ^ pos_a ^ pos_b ^ pos_c ^ pos_d ^ pos_e ^ pos_f

    res = {}
    for pat, bits in chain.from_iterable(bits_by_len.values()):
        pat = ''.join(sorted(pat))
        if bits ^ pos_c ^ pos_f == 0:
            res[pat] = '1'
        elif bits ^ pos_a ^ pos_c ^ pos_d ^ pos_e ^ pos_g == 0:
            res[pat] = '2'
        elif bits ^ pos_a ^ pos_c ^ pos_d ^ pos_f ^ pos_g == 0:
            res[pat] = '3'
        elif bits ^ pos_b ^ pos_c ^ pos_d ^ pos_f == 0:
            res[pat] = '4'
        elif bits ^ pos_a ^ pos_b ^ pos_d ^ pos_f ^ pos_g == 0:
            res[pat] = '5'
        elif bits ^ pos_a ^ pos_b ^ pos_d ^ pos_e ^ pos_f ^ pos_g == 0:
            res[pat] = '6'
        elif bits ^ pos_a ^ pos_c ^ pos_f == 0:
            res[pat] = '7'
        elif bits ^ pos_a ^ pos_b ^ pos_c ^ pos_d ^ pos_e ^ pos_f ^ pos_g == 0:
            res[pat] = '8'
        elif bits ^ pos_a ^ pos_b ^ pos_c ^ pos_d ^ pos_f ^ pos_g == 0:
            res[pat] = '9'
        elif bits ^ pos_a ^ pos_b ^ pos_c ^ pos_e ^ pos_f ^ pos_g == 0:
            res[pat] = '0'

    return res


# --------------------------------------------------
def test_decode() -> None:
    """ Test decode """

    test1 = {
        'cf': '1',
        'acdeg': '2',
        'acdfg': '3',
        'bcdf': '4',
        'abdfg': '5',
        'abdefg': '6',
        'acf': '7',
        'abcdefg': '8',
        'abcdfg': '9',
        'abcefg': '0',
    }

    input1 = list(test1.keys())
    shuffle(input1)
    assert (decode(input1) == test1)

    test2 = {
        'acedgfb': '8',
        'cdfbe': '5',
        'gcdfa': '2',
        'fbcad': '3',
        'dab': '7',
        'cefabd': '9',
        'cdfgeb': '6',
        'eafb': '4',
        'cagedb': '0',
        'ab': '1',
    }
    input2 = list(test2.keys())
    shuffle(input2)
    assert (decode(input2) == test2)


# --------------------------------------------------
def count_set_bits(n: int) -> int:
    """ Count bits == 1 """

    count = 0
    while (n):
        count += n & 1
        n >>= 1

    return count


# --------------------------------------------------
def test_count_set_bits() -> None:
    """ Test count_set_bits """

    assert count_set_bits(0) == 0
    assert count_set_bits(1) == 1
    assert count_set_bits(2) == 1
    assert count_set_bits(3) == 2


# --------------------------------------------------
if __name__ == '__main__':
    main()
