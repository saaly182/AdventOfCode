#!/usr/bin/python3 -u

import sys
sys.path.append('../../lib')
import dirutils  # noqa: E402


def block_range(a, b):
    """Return a range from the block-past-a to b."""
    if a <= b:
        br = range(a + 1, b + 1)
    else:
        br = range(a - 1, b - 1, -1)
    return br


def walk(moves, revisit_mode=False):
    nd = {'NR': 'E', 'NL': 'W', 'SR': 'W', 'SL': 'E',
          'ER': 'S', 'EL': 'N', 'WR': 'N', 'WL': 'S'}
    seen = {}

    x1, y1, d = 0, 0, 'N'
    seen[(x1, y1)] = 1
    been_here = False
    for move in moves:
        if revisit_mode and been_here:
            break

        d = nd[d + move[0]]
        x2 = x1 + dirutils.dirvecs[d][0] * move[1]
        y2 = y1 + dirutils.dirvecs[d][1] * move[1]

        if revisit_mode:
            for x in block_range(x1, x2):
                if (x, y1) in seen:
                    been_here = True
                    x2 = x
                    break
                else:
                    seen[(x, y1)] = 1
            for y in block_range(y1, y2):
                if (x1, y) in seen:
                    been_here = True
                    y2 = y
                    break
                else:
                    seen[(x1, y)] = 1

        x1, y1 = x2, y2

    return abs(x1) + abs(y1)


def part1(moves):
    return walk(moves)


def part2(moves):
    return walk(moves, revisit_mode=True)


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    main_input = slurp('input/input.txt')

    for inp in (main_input,):
        moves = tuple((m[0], int(m[1:])) for m in inp[0].split(', '))
        print("Part 1 answer =", part1(moves))
        print("Part 2 answer =", part2(moves))
        print()


if __name__ == '__main__':
    main()
