#!/usr/bin/python3 -u

import itertools


def part1(spreadsheet):
    return sum([max(row) - min(row) for row in spreadsheet])


def part2(spreadsheet):
    sm = 0  # sum
    for row in spreadsheet:
        for a, b in itertools.combinations(row, 2):
            if b > a:
                a, b = b, a
            if a % b == 0:
                sm += a // b
                break  # problem says that there's only one such pair per row
    return sm


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp):
    ss = []
    for line in inp:
        ss.append([int(a) for a in line.split()])
    return ss


def main():
    sample_input1 = slurp('input/sample_input_1.txt')
    sample_input2 = slurp('input/sample_input_2.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input1, sample_input2, main_input):
        spreadsheet = parse(inp)
        print("Part 1 answer =", part1(spreadsheet))
        print("Part 2 answer =", part2(spreadsheet))
        print()


if __name__ == '__main__':
    main()
