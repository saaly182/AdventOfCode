#!/usr/bin/python3 -u

from collections import defaultdict
import operator


def decode(mem: tuple) -> tuple:
    inst = mem[0]
    op1 = mem[1]
    op2 = mem[2] if len(mem) == 3 else None
    return inst, op1, op2


def execute(program: tuple, first_rcv_mode=False):
    pc = 0
    frq = None
    mathops = {'add': operator.add, 'mul': operator.mul, 'mod': operator.mod}
    register = defaultdict(int)

    def opval(op):
        """Handle whether it's an int literal or a register name."""
        return op if type(op) == int else register[op]

    while 0 <= pc < len(program):
        inst, op1, op2 = decode(program[pc])
        pc_add = 1

        match inst:
            case 'snd':
                frq = opval(op1)
            case 'set':
                register[op1] = opval(op2)
            case 'add' | 'mul' | 'mod' as thisop:
                register[op1] = mathops[thisop](register[op1], opval(op2))
            case 'rcv':
                xval = opval(op1)
                if xval != 0:
                    if first_rcv_mode:
                        return frq
            case 'jgz':
                xval = opval(op1)
                if xval > 0:
                    yval = opval(op2)
                    pc_add = yval
            case _:
                raise ValueError(program[pc])

        pc += pc_add


def part1(program):
    return execute(program, first_rcv_mode=True)


def part2():
    return None


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
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        program = parse(inp)
        print("Part 1 answer =", part1(program))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
