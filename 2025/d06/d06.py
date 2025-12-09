#!/usr/bin/python3 -u

import math


def part1(sheet: tuple) -> int:
    total = 0
    for col in range(len(sheet[0])):
        op = sheet[-1][col]
        nums = [r[col] for r in sheet[:-1]]
        if op == '+':
            total += sum(nums)
        elif op == '*':
            total += math.prod(nums)
        else:
            raise ValueError(f'Unknown operator {op}')
    return total


def part2() -> int:
    return -99


def parse_input(fname: str) -> tuple:
    sheet = []
    with open(fname) as file:
        for line in file:
            line = line.rstrip()
            cells = line.split()
            if cells[0][0] in '0123456789':
                cells = [int(x) for x in cells]
            sheet.append(tuple(cells))
    assert len(set([len(r) for r in sheet])) == 1
    return tuple(sheet)


def main():
    sample_input = parse_input('input/sample_input.txt')
    main_input = parse_input('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
