#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2021-12-04
Purpose: Rock the Casbah
"""

import argparse
import sys
from pprint import pprint
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

    parser.add_argument('-f',
                        '--file',
                        help='Input data file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        default=sys.stdin)

    args = parser.parse_args()

    return Args(args.file)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    nums = args.file.readline().rstrip().split(',')
    boards, buffer = [], []

    for line in map(str.rstrip, args.file):
        if line == '':
            if buffer:
                boards.append(buffer[:])
                buffer = []

        buffer.extend(line.split())

    if buffer:
        boards.append(buffer[:])

    won = set()
    for num in nums:
        for i, board in enumerate(boards):
            if positions := [i for i, n in enumerate(board) if n == num]:
                for pos in positions:
                    boards[i][pos] = 'X'

                if find_winner(board):
                    total = sum([int(n) for n in board if n != 'X'])
                    print(f'Winner {i} = {total} * {num} = {total * int(num)}')
                    won.add(i)

            if len(won) == len(boards):
                sys.exit()


# --------------------------------------------------
def find_winner(board):
    """ Return the winner """

    winning = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14],
               [15, 16, 17, 18, 19], [20, 21, 22, 23, 24], [0, 5, 10, 15, 20],
               [1, 6, 11, 16, 21], [2, 7, 12, 17, 22], [3, 8, 13, 18, 23],
               [4, 9, 14, 19, 24]]

    for combo in winning:
        group = list(map(lambda i: board[i], combo))
        if all([spot == 'X' for spot in group]):
            return True


# --------------------------------------------------
def test_find_winner() -> None:
    """ Test find_winner """

    board1 = [
        '31', '93', '46', '11', '30', '2', '45', '40', '69', '33', '82', '21',
        '37', '99', '86', '57', '16', '34', '94', '85', '60', '49', '28', '14',
        '65'
    ]
    assert not find_winner(board1)

    board2 = [
        'X', 'X', 'X', 'X', 'X', '2', '45', '40', '69', '33', '82', '21', '37',
        '99', '86', '57', '16', '34', '94', '85', '60', '49', '28', '14', '65'
    ]
    assert find_winner(board2)

    board3 = [
        'X', '93', '46', '11', '30', 'X', '45', '40', '69', '33', 'X', '21',
        '37', '99', '86', 'X', '16', '34', '94', '85', 'X', '49', '28', '14',
        '65'
    ]
    assert find_winner(board3)


# --------------------------------------------------
if __name__ == '__main__':
    main()
