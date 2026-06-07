#!/usr/bin/python3 -u

import re


class Device:
    def __init__(self) -> None:
        self._regcount = 6
        self.registers = [0] * self._regcount

    def op_addr(self, a: int, b: int, c: int) -> None:
        """(add register)
        stores into register C the result of adding register A and
        register B."""
        self.registers[c] = self.registers[a] + self.registers[b]

    def op_addi(self, a: int, b: int, c: int) -> None:
        """(add immediate) stores into register C the result of adding
        register A and value B."""
        self.registers[c] = self.registers[a] + b

    def op_mulr(self, a: int, b: int, c: int) -> None:
        """(multiply register) stores into register C the result of multiplying
        register A and register B."""
        self.registers[c] = self.registers[a] * self.registers[b]

    def op_muli(self, a: int, b: int, c: int) -> None:
        """(multiply immediate) stores into register C the result of
        multiplying register A and value B."""
        self.registers[c] = self.registers[a] * b

    def op_banr(self, a: int, b: int, c: int) -> None:
        """(bitwise AND register) stores into register C the result of the
        bitwise AND of register A and register B."""
        self.registers[c] = self.registers[a] & self.registers[b]

    def op_bani(self, a: int, b: int, c: int) -> None:
        """(bitwise AND immediate) stores into register C the result of the
        bitwise AND of register A and value B."""
        self.registers[c] = self.registers[a] & b

    def op_borr(self, a: int, b: int, c: int) -> None:
        """(bitwise OR register) stores into register C the result of the
        bitwise OR of register A and register B."""
        self.registers[c] = self.registers[a] | self.registers[b]

    def op_bori(self, a: int, b: int, c: int) -> None:
        """(bitwise OR immediate) stores into register C the result of the
        bitwise OR of register A and value B."""
        self.registers[c] = self.registers[a] | b

    def op_setr(self, a: int, b: int, c: int) -> None:
        """(set register) copies the contents of register A into register C.
        (Input B is ignored.)"""
        self.registers[c] = self.registers[a]

    def op_seti(self, a: int, b: int, c: int) -> None:
        """(set immediate) stores value A into register C.
        (Input B is ignored.)"""
        self.registers[c] = a

    def op_gtir(self, a: int, b: int, c: int) -> None:
        """(greater-than immediate/register) sets register C to 1 if value A
        is greater than register B. Otherwise, register C is set to 0."""
        self.registers[c] = 1 if a > self.registers[b] else 0

    def op_gtri(self, a: int, b: int, c: int) -> None:
        """(greater-than register/immediate) sets register C to 1 if register A
        is greater than value B. Otherwise, register C is set to 0."""
        self.registers[c] = 1 if self.registers[a] > b else 0

    def op_gtrr(self, a: int, b: int, c: int) -> None:
        """(greater-than register/register) sets register C to 1 if register A
        is greater than register B. Otherwise, register C is set to 0."""
        self.registers[c] = 1 if self.registers[a] > self.registers[b] else 0

    def op_eqir(self, a: int, b: int, c: int) -> None:
        """(equal immediate/register) sets register C to 1 if value A is equal
        to register B. Otherwise, register C is set to 0."""
        self.registers[c] = 1 if a == self.registers[b] else 0

    def op_eqri(self, a: int, b: int, c: int) -> None:
        """(equal register/immediate) sets register C to 1 if register A is
        equal to value B. Otherwise, register C is set to 0."""
        self.registers[c] = 1 if self.registers[a] == b else 0

    def op_eqrr(self, a: int, b: int, c: int) -> None:
        """(equal register/register) sets register C to 1 if register A is
        equal to register B. Otherwise, register C is set to 0."""
        self.registers[c] = 1 if self.registers[a] == self.registers[b] else 0


def part1(ipreg: int, program: tuple, init_reg0=0) -> int:
    d = Device()
    ip = 0
    d.registers[0] = init_reg0

    # execute the program
    while 0 <= ip < len(program):
        # first write the current ip into the ip register
        d.registers[ipreg] = ip

        # fetch and execute the next instruction
        op, a, b, c = program[ip]
        fnc = getattr(d, f'op_{op}')
        fnc(a, b, c)

        # write the ip register to the ip
        ip = d.registers[ipreg]

        # increment the ip
        ip += 1

    return d.registers[0]


def decompile(ipreg: int, program: tuple) -> None:
    # just print a simple decompiled version of program
    # with variable names instead of register numbers
    v = list('abcdef')
    v[ipreg] = 'ip'

    for address, (op, x1, x2, x3) in enumerate(program):
        print(f'{address:3} ({op} {x1:2} {x2:2} {x3:2}): ', end='')
        match op:
            case 'addr':
                print(f'{v[x3]} = {v[x1]} + {v[x2]}')
            case 'addi':
                print(f'{v[x3]} = {v[x1]} + {x2}')
            case 'mulr':
                print(f'{v[x3]} = {v[x1]} * {v[x2]}')
            case 'muli':
                print(f'{v[x3]} = {v[x1]} * {x2}')
            case 'banr':
                print(f'{v[x3]} = {v[x1]} & {v[x2]}')
            case 'bani':
                print(f'{v[x3]} = {v[x1]} & {x2}')
            case 'borr':
                print(f'{v[x3]} = {v[x1]} | {v[x2]}')
            case 'bori':
                print(f'{v[x3]} = {v[x1]} | {x2}')
            case 'setr':
                print(f'{v[x3]} = {v[x1]}')
            case 'seti':
                print(f'{v[x3]} = {x1}')
            case 'gtir':
                print(f'{v[x3]} = 1 if {x1} > {v[x2]} else 0')
            case 'gtri':
                print(f'{v[x3]} = 1 if {v[x1]} > {x2} else 0')
            case 'gtrr':
                print(f'{v[x3]} = 1 if {v[x1]} > {v[x2]} else 0')
            case 'eqir':
                print(f'{v[x3]} = 1 if {x1} == {v[x2]} else 0')
            case 'eqri':
                print(f'{v[x3]} = 1 if {v[x1]} == {x2} else 0')
            case 'eqrr':
                print(f'{v[x3]} = 1 if {v[x1]} == {v[x2]} else 0')
            case _:
                raise ValueError(f'Unknown opcode {op}')


def part2(ipreg: int, program: tuple) -> int:
    """
    Trying to use the part1 approach blows up, so instead I used the decompile()
    function in this program to print out a more readable version of the
    program. I then had to deduce what it was doing, with some Internet hints.

    === Original decompile() output: ===================================
     0 (addi  2 16  2): ip = ip + 16
     1 (seti  1  2  4): e = 1
     2 (seti  1  8  1): b = 1
     3 (mulr  4  1  5): f = e * b
     4 (eqrr  5  3  5): f = 1 if f == d else 0
     5 (addr  5  2  2): ip = f + ip
     6 (addi  2  1  2): ip = ip + 1
     7 (addr  4  0  0): a = e + a
     8 (addi  1  1  1): b = b + 1
     9 (gtrr  1  3  5): f = 1 if b > d else 0
    10 (addr  2  5  2): ip = ip + f
    11 (seti  2  6  2): ip = 2
    12 (addi  4  1  4): e = e + 1
    13 (gtrr  4  3  5): f = 1 if e > d else 0
    14 (addr  5  2  2): ip = f + ip
    15 (seti  1  2  2): ip = 1
    16 (mulr  2  2  2): ip = ip * ip
    17 (addi  3  2  3): d = d + 2
    18 (mulr  3  3  3): d = d * d
    19 (mulr  2  3  3): d = ip * d
    20 (muli  3 11  3): d = d * 11
    21 (addi  5  2  5): f = f + 2
    22 (mulr  5  2  5): f = f * ip
    23 (addi  5  8  5): f = f + 8
    24 (addr  3  5  3): d = d + f
    25 (addr  2  0  2): ip = ip + a
    26 (seti  0  4  2): ip = 0
    27 (setr  2  5  5): f = ip
    28 (mulr  5  2  5): f = f * ip
    29 (addr  2  5  5): f = ip + f
    30 (mulr  2  5  5): f = ip * f
    31 (muli  5 14  5): f = f * 14
    32 (mulr  5  2  5): f = f * ip
    33 (addr  3  5  3): d = d + f
    34 (seti  0  8  0): a = 0
    35 (seti  0  5  2): ip = 0

    === Hand-manipulated decompilation: ================================
     0 (addi  2 16  2): jmp +16
     1 (seti  1  2  4): e = 1
     2 (seti  1  8  1): b = 1
     3 (mulr  4  1  5): f = e * b
     4 (eqrr  5  3  5): f = 1 if f == d else 0
     5 (addr  5  2  2): jmp +f
     6 (addi  2  1  2): jmp +1
     7 (addr  4  0  0): a = e + a
     8 (addi  1  1  1): b = b + 1
     9 (gtrr  1  3  5): f = 1 if b > d else 0
    10 (addr  2  5  2): jmp +f
    11 (seti  2  6  2): jmp #2
    12 (addi  4  1  4): e = e + 1
    13 (gtrr  4  3  5): f = 1 if e > d else 0
    14 (addr  5  2  2): jmp +f
    15 (seti  1  2  2): jmp #1
    16 (mulr  2  2  2): halt

    jump to the function below and compute 'd'
    then run this inefficient double loop to sum up the divisors of
    'd', storing that sum in register[0], which is 'a'.

    for e in range(1, d + 1):
        for b in range(1, d + 1):
            if b * e == d:
                a += e

    # 'function' below builds up a big number in 'd' then jmps to top
    17 (addi  3  2  3): d = d + 2
    18 (mulr  3  3  3): d = d * d
    19 (mulr  2  3  3): d = ip * d
    20 (muli  3 11  3): d = d * 11
    21 (addi  5  2  5): f = f + 2
    22 (mulr  5  2  5): f = f * ip
    23 (addi  5  8  5): f = f + 8
    24 (addr  3  5  3): d = d + f
    25 (addr  2  0  2): jmp +a (a=1 for part2())
    26 (seti  0  4  2): jmp #0
    27 (setr  2  5  5): f = ip
    28 (mulr  5  2  5): f = f * ip
    29 (addr  2  5  5): f = ip + f
    30 (mulr  2  5  5): f = ip * f
    31 (muli  5 14  5): f = f * 14
    32 (mulr  5  2  5): f = f * ip
    33 (addr  3  5  3): d = d + f
    34 (seti  0  8  0): a = 0
    35 (seti  0  5  2): jmp #0

    d = 2
    d *= d
    d *= 19
    d *= 11
    f = 2
    f *= 22
    f += 8
    d += f
    f = 27
    f *= 28
    f += 29
    f *= 30
    f *= 14
    f *= 32
    d += f
    return

    The lines here result in d = 10551288
    """

    # For my specific input, the correct answer for part 2 is the sum of
    # all the divisors of 10551288
    d = 10551288
    answer = sum([i for i in range(1, d + 1) if d % i == 0])
    return answer


def parse_input(fname: str) -> tuple[int, tuple]:
    ipreg = -1
    program = []

    ipreg_re = re.compile(r'#ip\s+(\d+)')
    program_re = re.compile(r'([a-z]+)\s+(\d+)\s+(\d+)\s+(\d+)')

    with open(fname) as f:
        for line in f:
            line = line.strip()
            if mo := ipreg_re.fullmatch(line):
                ipreg = int(mo.group(1))
            elif mo := program_re.fullmatch(line):
                program.append((mo.group(1),) +
                               tuple(int(x) for x in mo.groups()[1:]))
            else:
                raise ValueError(f'Invalid input: {line}')

    assert 0 <= ipreg <= 5
    return ipreg, tuple(program)


def main():
    sample_input = parse_input('input/sample_input.txt')
    main_input = parse_input('input/input.txt')

    for ipreg, program in (sample_input, main_input):
        print("Part 1 answer =", part1(ipreg, program))
        print("Part 2 answer =", part2(ipreg, program))
        print()


if __name__ == '__main__':
    main()
