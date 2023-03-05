#!/usr/bin/python3 -u

from collections import defaultdict


def execute(program):
    """Return highest reg value during execution, and final reg values."""
    regmax = float('-inf')
    reg = defaultdict(int)

    for cmd in program:
        r1, op, val1, r2, cmp, val2 = cmd
        if cmp not in ('<', '<=', '>', '>=', '==', '!='):
            raise ValueError(f'syntax error in "{cmd}"')
        xop = eval(f'reg[r2] {cmp} {val2}')
        if xop:
            match op:
                case 'inc':
                    reg[r1] += val1
                case 'dec':
                    reg[r1] -= val1
                case _:
                    raise ValueError(f'syntax error in "{cmd}"')
            if reg[r1] > regmax:
                regmax = reg[r1]

    return regmax, reg


def part1(program):
    _, registers = execute(program)
    return max(registers.values())


def part2(program):
    regmax, _ = execute(program)
    return regmax


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp):
    program = []
    for line in inp:
        a = line.split()
        program.append((a[0], a[1], int(a[2]), a[4], a[5], int(a[6]),))
    return tuple(program)


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        program = parse(inp)
        print("Part 1 answer =", part1(program))
        print("Part 2 answer =", part2(program))
        print()


if __name__ == '__main__':
    main()
