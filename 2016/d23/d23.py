#!/usr/bin/python3 -u

import copy


def decode(mem):
    inst = mem[0]
    op1 = mem[1]
    op2 = mem[2] if len(mem) == 3 else None
    return inst, op1, op2


def tgl_inst(program, addr):
    """Modify the program at addr according to the tgl instruction rules."""

    # If an attempt is made to toggle an instruction outside the program,
    # nothing happens.
    if addr >= len(program):
        return

    inst, op1, op2 = decode(program[addr])

    match inst:
        # For one-argument instructions, inc becomes dec, and all other
        # one-argument instructions become inc.
        case 'dec' | 'tgl':
            new_inst = 'inc'
        case 'inc':
            new_inst = 'dec'
        # For two-argument instructions, jnz becomes cpy, and all other
        # two-instructions become jnz.
        case 'cpy':
            new_inst = 'jnz'
        case 'jnz':
            new_inst = 'cpy'
        case _:
            raise ValueError(program[addr])

    program[addr][0] = new_inst


def execute(program):
    pc = 0
    register = {'a': 7, 'b': 0, 'c': 0, 'd': 0}

    while 0 <= pc < len(program):
        inst, op1, op2 = decode(program[pc])
        pc_add = 1

        match inst:
            case 'cpy':
                # If toggling produces an invalid instruction (like cpy 1 2)
                # and an attempt is later made to execute that instruction,
                # skip it instead.
                if op2 in 'abcd':
                    register[op2] = op1 if type(op1) == int else register[op1]
            case 'inc':
                register[op1] += 1
            case 'dec':
                register[op1] -= 1
            case 'jnz':
                cmpval = op1 if type(op1) == int else register[op1]
                if cmpval != 0:
                    pc_add = op2 if type(op2) == int else register[op2]
            case 'tgl':
                offset = op1 if type(op1) == int else register[op1]
                tgl_inst(program, pc + offset)
            case _:
                raise ValueError(program[pc])

        pc += pc_add

    return register


def part1(program):
    register = execute(program)
    return register['a']


def part2(program):
    return None


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp):
    program = []
    for line in inp:
        toks = line.split()
        for i in range(1, len(toks)):
            if toks[i].lstrip('-').isdigit():
                toks[i] = int(toks[i])
        program.append(toks)
    return program


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        program = parse(inp)
        # program is self-modifying, so always make a deep copy
        print("Part 1 answer =", part1(copy.deepcopy(program)))
        print("Part 2 answer =", part2(copy.deepcopy(program)))
        print()


if __name__ == '__main__':
    main()
