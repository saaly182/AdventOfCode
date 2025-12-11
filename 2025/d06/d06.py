#!/usr/bin/python3 -u

import math
import sys
sys.path.append('../../lib')
import aocutils  # noqa: E402 F401


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


def part2(sheet: tuple) -> int:
    total = 0
    nums = []
    for row in sheet:
        if row[-1] not in ' 0123456789':
            op = row[-1]
            nums.append(int(''.join(row[:-1])))
            if op == '+':
                total += sum(nums)
            elif op == '*':
                total += math.prod(nums)
            else:
                raise ValueError(f'Unknown operator {op}')
            nums = []
        else:
            numstr = ''.join(row).strip()
            if numstr:
                nums.append(int(numstr))
    return total


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


def parse_input2(fname: str) -> tuple:
    sheet = []
    with open(fname) as file:
        for line in file:
            line = line.rstrip('\n')
            chrs = [c for c in line]
            sheet.append(chrs)
    sheet_ccw = aocutils.rotate_2darray(sheet, 'ccw')
    return tuple(sheet_ccw)


def main():
    sample_input = parse_input('input/sample_input.txt')
    main_input = parse_input('input/input.txt')
    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))

    sample_input = parse_input2('input/sample_input.txt')
    main_input = parse_input2('input/input.txt')
    for inp in (sample_input, main_input):
        print("Part 2 answer =", part2(inp))


if __name__ == '__main__':
    main()
