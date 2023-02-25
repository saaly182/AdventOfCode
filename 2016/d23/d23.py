#!/usr/bin/python3 -u

import copy


def decode(mem):
    protected = mem[0]  # bool; true means tgl cannot modify this instruction
    inst = mem[1]
    op1 = mem[2] if len(mem) > 2 else None
    op2 = mem[3] if len(mem) == 4 else None
    return protected, inst, op1, op2


def tgl_inst(program, addr):
    """Modify the program at addr according to the tgl instruction rules."""

    # If an attempt is made to toggle an instruction outside the program,
    # nothing happens.
    if addr >= len(program):
        return

    protected, inst, op1, op2 = decode(program[addr])

    if protected:
        raise RuntimeError('Trying to toggle protected instruction: '
                           f'{program[addr]}')

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

    program[addr][1] = new_inst


def execute(program, a=7):
    pc = 0
    register = {'a': a, 'b': 0, 'c': 0, 'd': 0}

    while 0 <= pc < len(program):
        protected, inst, op1, op2 = decode(program[pc])
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
            case 'nop':
                pass
            case 'mul':
                # Multiple reg-b * reg-d and store in reg-a; set reg-{c,d} = 0.
                # NOTE: Not general purpose; super specific to part 2 of this
                # problem.
                register['a'] = register['b'] * register['d']
                register['c'] = 0
                register['d'] = 0
            case _:
                raise ValueError(program[pc])

        pc += pc_add

    return register


def part1(program):
    register = execute(program)
    return register['a']


def part2(program):
    # Insight:
    # 3 cpy 0 a
    # 4 cpy b c
    # 5 inc a
    # 6 dec c
    # 7 jnz c -2
    # 8 dec d
    # 9 jnz d -5
    # is equivalent to a <- b * d; cpy 0 d; cpy 0 c
    # (as long as tgl doesn't modify the code)

    # Hack to change the specific input I got; not generalized.
    # Replace the expensive multiply loops with one 'mul' instruction and then
    # pad with 'nop' instructions to keep the addresses correct. Lastly,
    # protect these replacement instructions from 'tgl' changes.
    if program[3:10] == [[False, 'cpy', 0, 'a'],
                         [False, 'cpy', 'b', 'c'],
                         [False, 'inc', 'a'],
                         [False, 'dec', 'c'],
                         [False, 'jnz', 'c', -2],
                         [False, 'dec', 'd'],
                         [False, 'jnz', 'd', -5]]:
        program[3:10] = [[True, 'mul'],
                         [True, 'nop'],
                         [True, 'nop'],
                         [True, 'nop'],
                         [True, 'nop'],
                         [True, 'nop'],
                         [True, 'nop']]

    register = execute(program, 12)
    return register['a']


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp):
    program = []
    protected = False  # is this instruction protected from tgl changes
    for line in inp:
        toks = line.split()
        for i in range(1, len(toks)):
            if toks[i].lstrip('-').isdigit():
                toks[i] = int(toks[i])
        toks.insert(0, protected)
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
