#!/usr/bin/python3 -u

from collections import defaultdict
import operator


def decode(mem: tuple) -> tuple:
    inst = mem[0]
    op1 = mem[1]
    op2 = mem[2]
    return inst, op1, op2


def part1(program: tuple) -> int:
    pc = 0
    mathops = {'sub': operator.sub, 'mul': operator.mul}
    register = defaultdict(int)
    mulcount = 0

    def opval(op: int | str) -> int:
        """Handle whether it's an int literal or a register name."""
        return op if type(op) == int else register[op]

    while 0 <= pc < len(program):
        inst, op1, op2 = decode(program[pc])
        pc_add = 1

        match inst:
            case 'set':
                register[op1] = opval(op2)
            case 'sub' | 'mul' as thisop:
                register[op1] = mathops[thisop](register[op1], opval(op2))
                if thisop == 'mul':
                    mulcount += 1
            case 'jnz':
                if opval(op1) != 0:
                    pc_add = opval(op2)
            case _:
                raise ValueError(f'Illegal instruction: {program[pc]}')

        pc += pc_add

    return mulcount


def part2():
    pass


def slurp(fname: str) -> list[str]:
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp):
    program = []
    for line in inp:
        toks = line.split()
        for i in range(1, len(toks)):
            if toks[i].lstrip('-').isdigit():
                toks[i] = int(toks[i])
        program.append(tuple(toks))
    return tuple(program)


def main():
    main_input = slurp('input/input.txt')

    for inp in (main_input,):
        program = parse(inp)
        print("Part 1 answer =", part1(program))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
