#!/usr/bin/python3 -u

import re


def md(p1: tuple, p2: tuple) -> int:
    """Return the manhattan distance between two points."""
    return sum(abs(i - j) for i, j in zip(p1, p2, strict=True))


def part1(bots: tuple) -> int:
    strongest_bot = bots[0]
    for bot in bots:
        if bot[3] > strongest_bot[3]:
            strongest_bot = bot
    max_r = strongest_bot[3]

    # assert that there's only *one* strongest bot in the input
    max_r_count = len([b[3] for b in bots if b[3] == max_r])
    assert max_r_count == 1

    in_range = [b for b in bots if md(b[:-1], strongest_bot[:-1]) <= max_r]

    return len(in_range)


def part2() -> int:
    return -99


def parse_input(fname: str) -> tuple[tuple[int, int, int, int], ...]:
    bots = []
    input_re = re.compile(r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)')
    with open(fname) as file:
        for line in file:
            line = line.strip()
            if mo := re.fullmatch(input_re, line):
                bot = tuple(int(x) for x in mo.groups())
                bots.append(bot)
            else:
                raise ValueError(f'Invalid input: {line}')

    return tuple(bots)


def main():
    sample_input = parse_input('input/sample_input.txt')
    main_input = parse_input('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
