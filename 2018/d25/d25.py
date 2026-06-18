#!/usr/bin/python3 -u

import itertools


def md(p1: tuple, p2: tuple) -> int:
    """Return the manhattan distance between two points."""
    return sum(abs(i - j) for i, j in zip(p1, p2, strict=True))


def part1(points: tuple) -> int:
    """Return the number of connected components in the given points,
    where two points are connected if their Manhattan distance is
    at most 3."""

    next_cid = 1000  # "component id"; starting at 1000 to easily spot cids
    p2c = {}  # point-to-component mapping
    c2p = {}  # component-to-points mapping
    for p in points:
        p2c[p] = next_cid
        c2p[next_cid] = {p}
        next_cid += 1

    for a, b in itertools.combinations(points, 2):
        if p2c[a] != p2c[b] and md(a, b) <= 3:
            # merge everything into the lowest component number
            c1, c2 = min(p2c[a], p2c[b]), max(p2c[a], p2c[b])
            for p in c2p[c2]:
                p2c[p] = c1
            c2p[c1].update(c2p[c2])
            del c2p[c2]

    return len(c2p)


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
