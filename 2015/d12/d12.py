#!/usr/bin/python3 -u

import re


def part1(inp):
    s = inp[0]
    all_num_sum = sum([int(x) for x in re.findall(r'-?\d+', s)])
    return all_num_sum


def part2():
    return None


def slurp(fname):
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
