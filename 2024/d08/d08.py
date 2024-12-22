#!/usr/bin/python3 -u

import collections
import itertools


def get_antinodes(pos1: tuple, pos2: tuple, harmonics=1) -> set:
    assert harmonics > 0
    antinodes = set()
    r1, c1 = pos1
    r2, c2 = pos2
    dr = r2 - r1
    dc = c2 - c1
    if harmonics > 1:
        # add the antennas themselves as antinodes
        antinodes.update((pos1, pos2))
    for h in range(1, harmonics + 1):
        a1r = r2 + h * dr
        a1c = c2 + h * dc
        a2r = r1 - h * dr
        a2c = c1 - h * dc
        antinodes.update(((a1r, a1c), (a2r, a2c)))
    return antinodes


def part1(height: int, width: int, antennas: dict, harmonics=1) -> int:
    antinodes = set()
    for freq in antennas:
        for pair in itertools.combinations(antennas[freq], 2):
            for anti in get_antinodes(pair[0], pair[1], harmonics):
                if 0 <= anti[0] < height and 0 <= anti[1] < width:
                    antinodes.add(anti)
    return len(antinodes)


def part2(height: int, width: int, antennas: dict) -> int:
    harmonics = max(height, width)
    return part1(height, width, antennas, harmonics)


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
    sample_input_2 = slurp('input/sample_input_2.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, sample_input_2, main_input):
        height, width, antennas = inp
        print("Part 1 answer =", part1(height, width, antennas))
        print("Part 2 answer =", part2(height, width, antennas))
        print()


if __name__ == '__main__':
    main()
