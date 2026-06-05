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


def part1(ipreg: int, program: tuple) -> int:
    d = Device()
    ip = 0

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


def part2() -> int:
    return -99


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
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
