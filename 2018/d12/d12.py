#!/usr/bin/python3 -u

from collections import defaultdict
from typing import DefaultDict


def part1(pots: tuple, rules: DefaultDict) -> int:
    boundary = ('.',) * 2
    max_boundary_dots = ('.',) * 5
    zero_cell = 2
    for generation in range(20):
        prefix = pots[:5]
        suffix = pots[-5:]
        if prefix != max_boundary_dots:
            pots = boundary + pots
            zero_cell += 2
        if suffix != max_boundary_dots:
            pots = pots + boundary

        pots2 = list(boundary)
        for i in range(2, len(pots) - 2):
            pattern = ''.join(pots[i - 2:i + 3])
            pots2.append(rules[pattern])
        pots = tuple(pots2) + boundary

    answer = 0
    for i, p in enumerate(pots):
        if p == '#':
            answer += i - zero_cell
    return answer


def part2():
    return None


def slurp(fname: str) -> list[str]:
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp: list) -> tuple[tuple, DefaultDict]:
    pots = tuple(['.', '.'] + list(inp[0].removeprefix('initial state: ')) +
                 ['.', '.'])

    rules = defaultdict(lambda: '.')
    for line in inp[2:]:
        a, b = line.split(' => ')
        rules[a] = b

    return pots, rules


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        pots, rules = parse(inp)
        print("Part 1 answer =", part1(pots, rules))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
