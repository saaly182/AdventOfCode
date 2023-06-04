#!/usr/bin/python3 -u

import collections
import sys
sys.path.append('../../lib')
import dirutils  # noqa: E402


def part1(moves):
    pos = (0, 0)
    house2presents = collections.defaultdict(int)
    house2presents[pos] = 1
    for m in moves:
        if m not in dirutils.dirvecs:
            raise ValueError(m)
        dx, dy = dirutils.dirvecs[m]
        pos = pos[0] + dx, pos[1] + dy
        house2presents[pos] += 1
    return len(house2presents)


def part2(moves):
    house2presents = collections.defaultdict(int)
    house2presents[(0, 0)] = 2
    for offset in (0, 1):
        pos = (0, 0)
        for m in moves[offset::2]:
            if m not in dirutils.dirvecs:
                raise ValueError(m)
            dx, dy = dirutils.dirvecs[m]
            pos = pos[0] + dx, pos[1] + dy
            house2presents[pos] += 1
    return len(house2presents)


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    main_input = slurp('input/input.txt')

    for inp in (main_input,):
        moves = inp[0]
        print("Part 1 answer =", part1(moves))
        print("Part 2 answer =", part2(moves))
        print()


if __name__ == '__main__':
    main()
