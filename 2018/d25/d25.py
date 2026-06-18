#!/usr/bin/python3 -u

import itertools


def md(p1: tuple, p2: tuple) -> int:
    """Return the manhattan distance between two points."""
    return sum([abs(i - j) for i, j in zip(p1, p2, strict=True)])


def part1(points: tuple) -> int:
    """Build the connected components of the given list of points."""
    next_cid = 1000
    p2c = {}  # point-to-component mapping
    for p in points:
        p2c[p] = next_cid
        next_cid += 1

    for a, b in itertools.combinations(points, 2):
        if p2c[a] != p2c[b] and md(a, b) <= 3:
            # merge everything into the lowest component number
            cid1, cid2 = min(p2c[a], p2c[b]), max(p2c[a], p2c[b])
            for p in p2c:
                if p2c[p] == cid2:
                    p2c[p] = cid1

    return len(set(p2c.values()))


def parse_input(fname: str) -> tuple[tuple[int, int, int, int], ...]:
    points = []
    with open(fname) as file:
        for line in file:
            line = line.strip()
            p = tuple(map(int, line.split(',')))
            points.append(p)
    return tuple(points)


def main():
    sample1_input = parse_input('input/sample1_input.txt')
    sample2_input = parse_input('input/sample2_input.txt')
    sample3_input = parse_input('input/sample3_input.txt')
    sample4_input = parse_input('input/sample4_input.txt')
    main_input = parse_input('input/input.txt')

    for inp in (sample1_input, sample2_input, sample3_input, sample4_input,
                main_input):
        print("Part 1 answer =", part1(inp))
        print()


if __name__ == '__main__':
    main()
