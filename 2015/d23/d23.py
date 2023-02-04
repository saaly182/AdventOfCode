#!/usr/bin/python3 -u

def decode(mem):
    inst = mem[0]
    op1 = mem[1]
    if len(mem) == 3:
        op2 = mem[2]
    else:
        op2 = None
    return inst, op1, op2


def part1(program, ra=0, rb=0):
    pc = 0
    pc_max = len(program) - 1
    r = {'a': ra, 'b': rb}

    while 0 <= pc <= pc_max:
        inst, op1, op2 = decode(program[pc])
        match inst:
            case 'hlf':
                r[op1] //= 2
                pc += 1
            case 'tpl':
                r[op1] *= 3
                pc += 1
            case 'inc':
                r[op1] += 1
                pc += 1
            case 'jmp':
                pc += op1
            case 'jie':
                if r[op1] % 2 == 0:
                    pc += op2
                else:
                    pc += 1
            case 'jio':
                if r[op1] == 1:
                    pc += op2
                else:
                    pc += 1

    return r['b']


def part2(program, ra=0, rb=0):
    return part1(program, ra, rb)


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp):
    prog = []
    for line in inp:
        toks = line.replace(',', '').split()
        match toks[0]:
            case 'jmp':
                prog.append((toks[0], int(toks[1]),))
            case ('jie' | 'jio'):
                prog.append((toks[0], toks[1], int(toks[2]),))
            case _:
                prog.append(tuple(toks))
    return tuple(prog)


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        program = parse(inp)
        print("Part 1 answer =", part1(program))
        print("Part 2 answer =", part2(program, ra=1))
        print()


if __name__ == '__main__':
    main()
