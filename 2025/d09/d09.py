#!/usr/bin/python3 -u

import itertools


def part1(cells: tuple) -> int:
    max_area = 0
    for a, b in itertools.combinations(cells, 2):
        area = (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)
        if area > max_area:
            max_area = area
    return max_area


def part2() -> int:
    return -99


def parse_input(fname: str) -> tuple[tuple]:
    cells = []
    with open(fname) as file:
        for line in file:
            a, b = line.split(',')
            cells.append((int(a), int(b)))
    return tuple(cells)


def main():
    sample_input = parse_input('input/sample_input.txt')
    main_input = parse_input('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
