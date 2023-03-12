#!/usr/bin/python3 -u

# Using hex coords described at the excellent documentation at
# https://www.redblobgames.com/grids/hexagons/#coordinates-axial

def walk(steps: tuple[str]) -> tuple[int, int]:
    """Return max dist and final dist from origin after walking the steps."""
    dqdr = {
        'n': (0, -1),
        'ne': (1, -1),
        'se': (1, 0),
        's': (0, 1),
        'sw': (-1, 1),
        'nw': (-1, 0)
    }
    q = r = 0  # the walk starts at the origin
    max_dist = 0

    for step in steps:
        dq, dr = dqdr[step]
        q += dq
        r += dr
        dist_here = dist(q, r)
        if dist_here > max_dist:
            max_dist = dist_here

    final_dist = dist(q, r)
    return max_dist, final_dist


def dist(q: int, r: int) -> int:
    """Return hex distance from the origin.
    https://www.redblobgames.com/grids/hexagons/#distances-axial
    """
    return (abs(q) + abs(q + r) + abs(r)) // 2


def part1(steps: tuple[str]) -> int:
    max_dist, final_dist = walk(steps)
    return final_dist


def part2(steps: tuple[str]) -> int:
    max_dist, final_dist = walk(steps)
    return max_dist


def slurp(fname: str) -> list[str]:
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        steps = tuple(inp[0].split(','))
        print("Part 1 answer =", part1(steps))
        print("Part 2 answer =", part2(steps))
        print()


if __name__ == '__main__':
    main()
