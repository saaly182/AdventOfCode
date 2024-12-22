#!/usr/bin/python3 -u

import collections
import itertools


def get_antinodes(pos1: tuple, pos2: tuple) -> tuple:
    r1, c1 = pos1
    r2, c2 = pos2
    dr = r2 - r1
    dc = c2 - c1
    a1r = r2 + dr
    a1c = c2 + dc
    a2r = r1 - dr
    a2c = c1 - dc
    return (a1r, a1c), (a2r, a2c)


def part1(height: int, width: int, antennas: dict) -> int:
    antinodes = set()
    for freq in antennas:
        for pair in itertools.combinations(antennas[freq], 2):
            for anti in get_antinodes(*pair):
                if 0 <= anti[0] < height and 0 <= anti[1] < width:
                    antinodes.add(anti)
    return len(antinodes)


def part2():
    return None


def slurp(fname: str) -> tuple:
    antennas = collections.defaultdict(list)
    with open(fname) as file:
        lines = tuple(line.rstrip() for line in file.readlines())
    width = len(lines[0])
    height = len(lines)
    for row, line in enumerate(lines):
        for col, freq in enumerate(line):
            if freq != '.':
                antennas[freq].append((row, col))
    return height, width, antennas


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        height, width, antennas = inp
        print("Part 1 answer =", part1(height, width, antennas))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
