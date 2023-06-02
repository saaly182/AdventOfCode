#!/usr/bin/python3 -u

import sys
sys.path.append('../../lib')

import dirutils
from collections import defaultdict

CLEAN = '.'
INFECTED = '#'


def part1(nodemap: defaultdict[str], center: tuple[int, int]) -> int:
    # Rules:
    # *** If the current node is infected, it turns to its right. Otherwise,
    # it turns to its left. (Turning is done in-place; the current node does
    # not change.)
    # *** If the current node is clean, it becomes infected. Otherwise,
    # it becomes cleaned. (This is done after the node is considered for the
    # purposes of changing direction.)
    # *** The virus carrier moves forward one node in the direction it is
    # facing.

    turn = {('U', 'R'): 'R', ('U', 'L'): 'L',
            ('D', 'R'): 'L', ('D', 'L'): 'R',
            ('R', 'R'): 'D', ('R', 'L'): 'U',
            ('L', 'R'): 'U', ('L', 'L'): 'D'}

    current_node = center
    direction = 'U'
    bursts = 10_000
    infections = 0
    for burst in range(bursts):
        state1 = nodemap[current_node]
        tdir = 'R' if state1 == INFECTED else 'L'
        direction = turn[(direction, tdir)]
        state2 = INFECTED if state1 == CLEAN else CLEAN
        if state2 == INFECTED:
            infections += 1
        nodemap[current_node] = state2
        next_node = (current_node[0] + dirutils.dirvecs[direction][0],
                     current_node[1] + dirutils.dirvecs[direction][1])
        current_node = next_node

    return infections


def part2():
    return None


def slurp(fname: str) -> list[str]:
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp: list) -> tuple[defaultdict[str], tuple[int, int]]:
    assert len(inp) % 2 == 1 and len(inp[0]) % 2 == 1
    nodemap = defaultdict(lambda: '.')
    r = c = -99
    for r, line in enumerate(inp):
        for c, val in enumerate(line):
            assert val == CLEAN or val == INFECTED
            nodemap[(r, c)] = val
    center = (r // 2, c // 2)
    return nodemap, center


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        nodemap, center = parse(inp)
        print("Part 1 answer =", part1(nodemap, center))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
