#!/usr/bin/python3 -u

import re


def part1(inp: list[str]) -> int:
    calsum = 0
    for s in inp:
        m = re.findall(r'[0-9]', s)
        if not m:
            raise ValueError(f'no digits in input: {s}')
        calibration = 10 * int(m[0]) + int(m[-1])
        calsum += calibration
    return calsum


def part2():
    return None


def slurp(fname: str) -> list[str]:
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
