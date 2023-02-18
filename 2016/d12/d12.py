#!/usr/bin/python3 -u

# FYI - this is pretty much the same as https://adventofcode.com/2015/day/23

def decode(mem):
    inst = mem[0]
    op1 = mem[1]
    op2 = mem[2] if len(mem) == 3 else None
    return inst, op1, op2


def execute(program, c=0):
    pc = 0
    register = {'a': 0, 'b': 0, 'c': c, 'd': 0}

    while 0 <= pc < len(program):
        inst, op1, op2 = decode(program[pc])
        pc_add = 1

        if inst == 'cpy':
            if type(op1) == int:
                register[op2] = op1
            else:
                register[op2] = register[op1]

        elif inst == 'inc':
            register[op1] += 1

        elif inst == 'dec':
            register[op1] -= 1

        elif inst == 'jnz':
            if type(op1) == int:
                cmpval = op1
            else:
                cmpval = register[op1]
            if cmpval != 0:
                pc_add = op2

        pc += pc_add

    return register


def part1(program):
    register = execute(program)
    return register['a']


def part2(program):
    register = execute(program, c=1)
    return register['a']


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
        program.append(tuple(toks))
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
