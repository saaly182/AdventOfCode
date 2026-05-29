#!/usr/bin/python3 -u

import itertools
import math


def part1(entries: list[int], n: int) -> int:
    answer = -1
    for x in itertools.combinations(entries, n):
        if sum(x) == 2020:
            answer = math.prod(x)
            break
    return answer


def parse_input(fname: str) -> tuple[str, ...]:
    with open(fname) as file:
        return tuple(int(line.rstrip()) for line in file.readlines())


def main():
    sample_input = parse_input('input/sample_input.txt')
    main_input = parse_input('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp, 2))
        print("Part 2 answer =", part1(inp, 3))
        print()


if __name__ == '__main__':
    main()
