#!/usr/bin/python3 -u

import re


def part1(inp: list[str]) -> int:
    calsum = 0
    for s in inp:
        m = re.findall(r'[1-9]', s)
        if not m:
            raise ValueError(f'no digits in input: {s}')
        calibration = 10 * int(m[0]) + int(m[-1])
        calsum += calibration
    return calsum


def part2(inp: list[str]) -> int:
    # Note that digit names can overlap, like "twone" is (2, 1). This means
    # that re.findall() cannot be used, because it only finds non-overlapping
    # matches.
    calsum = 0
    dnames = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6,
              'seven': 7, 'eight': 8, 'nine': 9}
    a = '[1-9]|'
    b = '|'.join(dnames.keys())
    dre_forward = a + b
    dre_reverse = a + b[::-1]

    def as_int(ds: str) -> int:
        return int(ds) if ds in '123456789' else dnames[ds]

    for s in inp:
        ds1 = re.search(dre_forward, s).group()
        ds2 = re.search(dre_reverse, s[::-1]).group()[::-1]
        calibration = 10 * as_int(ds1) + as_int(ds2)
        calsum += calibration
    return calsum


def slurp(fname: str) -> list[str]:
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
