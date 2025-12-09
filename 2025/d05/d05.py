#!/usr/bin/python3 -u

import re
import sys
sys.path.append('../../lib')
import aocutils  # noqa: E402 F401


def part1(fresh_ranges: tuple, ingredient_ids: tuple) -> int:
    fresh_ones = []
    for i_id in ingredient_ids:
        for a, b in fresh_ranges:
            if a <= i_id <= b:
                fresh_ones.append(i_id)
                break
    return len(fresh_ones)


def part2(fresh_ranges: tuple) -> int:
    # fortunately I had this merge_intervals() fnc in my library
    merged_ranges = aocutils.merge_intervals(fresh_ranges)
    fresh_id_count = 0
    for a, b in merged_ranges:
        fresh_id_count += (b - a + 1)
    return fresh_id_count


def parse_input(fname: str) -> tuple[tuple, tuple]:
    fresh_ranges = []
    ingredient_ids = []
    with open(fname) as file:
        for line in file:
            line = line.rstrip()
            if m := re.fullmatch(r'(\d+)-(\d+)', line):
                fresh_ranges.append((int(m[1]), int(m[2])))
            if m := re.fullmatch(r'(\d+)', line):
                ingredient_ids.append(int(m[1]))
    return tuple(fresh_ranges), tuple(ingredient_ids)


def main():
    sample_input = parse_input('input/sample_input.txt')
    main_input = parse_input('input/input.txt')

    for fresh_ranges, ingredient_ids in (sample_input, main_input):
        print("Part 1 answer =", part1(fresh_ranges, ingredient_ids))
        print("Part 2 answer =", part2(fresh_ranges))
        print()


if __name__ == '__main__':
    main()
