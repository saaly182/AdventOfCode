#!/usr/bin/python3 -u

import sys
sys.path.append('../../lib')

import dirutils
from collections import defaultdict

CLEAN = '.'
INFECTED = '#'
WEAKENED = 'W'
FLAGGED = 'F'
TURN = {('U', 'R'): 'R', ('U', 'L'): 'L', ('U', 'REV'): 'D',
        ('D', 'R'): 'L', ('D', 'L'): 'R', ('D', 'REV'): 'U',
        ('R', 'R'): 'D', ('R', 'L'): 'U', ('R', 'REV'): 'L',
        ('L', 'R'): 'U', ('L', 'L'): 'D', ('L', 'REV'): 'R'}


def part1(nodemap: defaultdict[str], center: tuple[int, int]) -> int:
    current_node = center
    direction = 'U'
    bursts = 10_000
    infections = 0
    for burst in range(bursts):
        state1 = nodemap[current_node]
        tdir = 'R' if state1 == INFECTED else 'L'
        direction = TURN[(direction, tdir)]
        state2 = INFECTED if state1 == CLEAN else CLEAN
        if state2 == INFECTED:
            infections += 1
        nodemap[current_node] = state2
        next_node = (current_node[0] + dirutils.dirvecs[direction][0],
                     current_node[1] + dirutils.dirvecs[direction][1])
        current_node = next_node

    return infections


def part2(nodemap: defaultdict[str], center: tuple[int, int]) -> int:
    # This violates DRY wrt to part1() above, but for performance I am not
    # going to try to make one function that operates in two separate modes.
    current_node = center
    direction = 'U'
    bursts = 10_000_000
    infections = 0
    for burst in range(bursts):
        state1 = nodemap[current_node]
        if state1 == CLEAN:
            tdir = 'L'
            state2 = WEAKENED
        elif state1 == INFECTED:
            tdir = 'R'
            state2 = FLAGGED
        elif state1 == WEAKENED:
            tdir = None
            state2 = INFECTED
            infections += 1
        elif state1 == FLAGGED:
            tdir = 'REV'
            state2 = CLEAN
        else:
            raise ValueError(f'invalid state ({state1=})')
        if state1 != WEAKENED:
            direction = TURN[(direction, tdir)]

        nodemap[current_node] = state2
        next_node = (current_node[0] + dirutils.dirvecs[direction][0],
                     current_node[1] + dirutils.dirvecs[direction][1])
        current_node = next_node

    return infections


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
        print("Part 1 answer =", part1(nodemap.copy(), center))
        print("Part 2 answer =", part2(nodemap.copy(), center))
        print()


if __name__ == '__main__':
    main()
