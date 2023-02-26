#!/usr/bin/python3 -u


def decode(mem):
    inst = mem[0]
    op1 = mem[1]
    op2 = mem[2] if len(mem) == 3 else None
    return inst, op1, op2


def execute(program, a_init):
    """Return True if produces infinite correct output, otherwise False."""
    pc = 0
    register = {'a': a_init, 'b': 0, 'c': 0, 'd': 0}

    # a bunch of state needed to catch various conditions
    expected_output = 0
    output_count = 0
    states_seen = set()
    detected_inf_loop = False
    cycles = 0
    cycles_max = 100_000_000

    while 0 <= pc < len(program):
        inst, op1, op2 = decode(program[pc])
        pc_add = 1

        # NOTE: The code is not self-modifying, and the only state in the
        # machine is the program counter and the registers. So if we ever see
        # the same pc and register values again, we're in an infinite loop.
        # FYI - we could technically have an inf loop that does not involve
        # repeat register values (e.g., inc d; jnz 1 -1). I'm not worrying
        # about that for this problem.
        state = (f"{pc}:{register['a']}:{register['b']}:"
                 f"{register['c']}:{register['d']}")
        if not detected_inf_loop:
            if state in states_seen:
                detected_inf_loop = True
                states_seen.clear()
            else:
                states_seen.add(state)

        # Crude method to catch non-halting execution that is not producing
        # output.
        if cycles > cycles_max:
            raise RuntimeError(f'Max execution cycles reached: {cycles}')

        match inst:
            case 'cpy':
                register[op2] = op1 if type(op1) == int else register[op1]
            case 'inc':
                register[op1] += 1
            case 'dec':
                register[op1] -= 1
            case 'jnz':
                cmpval = op1 if type(op1) == int else register[op1]
                if cmpval != 0:
                    pc_add = op2 if type(op2) == int else register[op2]
            case 'out':
                actual_output = op1 if type(op1) == int else register[op1]
                if actual_output != expected_output:
                    return False
                else:
                    output_count += 1
                    if detected_inf_loop and output_count > 10:  # arbitrary
                        return True
                    expected_output = (1, 0)[expected_output]
            case _:
                raise ValueError(program[pc])

        cycles += 1
        pc += pc_add

    return False


def part1(program):
    a_init = 0
    while True:
        if execute(program, a_init):
            return a_init
        a_init += 1


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
    main_input = slurp('input/input.txt')

    for inp in (main_input,):
        program = parse(inp)
        print("Part 1 answer =", part1(program))
        print()


if __name__ == '__main__':
    main()
