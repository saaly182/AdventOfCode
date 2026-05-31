#!/usr/bin/python3 -u

import re
import sys
sys.path.append('../../lib')
import multiline_record  # noqa: E402 F401


class Device:
    def __init__(self) -> None:
        self.regcount = 4
        self.registers = [0] * self.regcount
        self.opnames = tuple(n for n in dir(self) if n.startswith('op_'))
        self.opname2code = {n: None for n in self.opnames}
        self.code2opname = {}

    def set_registers(self, registers: list) -> None:
        assert len(registers) == self.regcount
        self.registers = registers

    def cmp_registers(self, registers: list) -> bool:
        assert len(registers) == self.regcount
        return self.registers == registers

    def op_addr(self, instruction: tuple[int, ...]) -> None:
        """(add register)
        stores into register C the result of adding register A and
        register B."""
        a, b, c = instruction[1:]
        self.registers[c] = self.registers[a] + self.registers[b]

    def op_addi(self, instruction: tuple[int, ...]) -> None:
        """(add immediate) stores into register C the result of adding
        register A and value B."""
        a, b, c = instruction[1:]
        self.registers[c] = self.registers[a] + b

    def op_mulr(self, instruction: tuple[int, ...]) -> None:
        """(multiply register) stores into register C the result of multiplying
        register A and register B."""
        a, b, c = instruction[1:]
        self.registers[c] = self.registers[a] * self.registers[b]

    def op_muli(self, instruction: tuple[int, ...]) -> None:
        """(multiply immediate) stores into register C the result of
        multiplying register A and value B."""
        a, b, c = instruction[1:]
        self.registers[c] = self.registers[a] * b

    def op_banr(self, instruction: tuple[int, ...]) -> None:
        """(bitwise AND register) stores into register C the result of the
        bitwise AND of register A and register B."""
        a, b, c = instruction[1:]
        self.registers[c] = self.registers[a] & self.registers[b]

    def op_bani(self, instruction: tuple[int, ...]) -> None:
        """(bitwise AND immediate) stores into register C the result of the
        bitwise AND of register A and value B."""
        a, b, c = instruction[1:]
        self.registers[c] = self.registers[a] & b

    def op_borr(self, instruction: tuple[int, ...]) -> None:
        """(bitwise OR register) stores into register C the result of the
        bitwise OR of register A and register B."""
        a, b, c = instruction[1:]
        self.registers[c] = self.registers[a] | self.registers[b]

    def op_bori(self, instruction: tuple[int, ...]) -> None:
        """(bitwise OR immediate) stores into register C the result of the
        bitwise OR of register A and value B."""
        a, b, c = instruction[1:]
        self.registers[c] = self.registers[a] | b

    def op_setr(self, instruction: tuple[int, ...]) -> None:
        """(set register) copies the contents of register A into register C.
        (Input B is ignored.)"""
        a, b, c = instruction[1:]
        self.registers[c] = self.registers[a]

    def op_seti(self, instruction: tuple[int, ...]) -> None:
        """(set immediate) stores value A into register C.
        (Input B is ignored.)"""
        a, b, c = instruction[1:]
        self.registers[c] = a

    def op_gtir(self, instruction: tuple[int, ...]) -> None:
        """(greater-than immediate/register) sets register C to 1 if value A
        is greater than register B. Otherwise, register C is set to 0."""
        a, b, c = instruction[1:]
        self.registers[c] = 1 if a > self.registers[b] else 0

    def op_gtri(self, instruction: tuple[int, ...]) -> None:
        """(greater-than register/immediate) sets register C to 1 if register A
        is greater than value B. Otherwise, register C is set to 0."""
        a, b, c = instruction[1:]
        self.registers[c] = 1 if self.registers[a] > b else 0

    def op_gtrr(self, instruction: tuple[int, ...]) -> None:
        """(greater-than register/register) sets register C to 1 if register A
        is greater than register B. Otherwise, register C is set to 0."""
        a, b, c = instruction[1:]
        self.registers[c] = 1 if self.registers[a] > self.registers[b] else 0

    def op_eqir(self, instruction: tuple[int, ...]) -> None:
        """(equal immediate/register) sets register C to 1 if value A is equal
        to register B. Otherwise, register C is set to 0."""
        a, b, c = instruction[1:]
        self.registers[c] = 1 if a == self.registers[b] else 0

    def op_eqri(self, instruction: tuple[int, ...]) -> None:
        """(equal register/immediate) sets register C to 1 if register A is
        equal to value B. Otherwise, register C is set to 0."""
        a, b, c = instruction[1:]
        self.registers[c] = 1 if self.registers[a] == b else 0

    def op_eqrr(self, instruction: tuple[int, ...]) -> None:
        """(equal register/register) sets register C to 1 if register A is
        equal to register B. Otherwise, register C is set to 0."""
        a, b, c = instruction[1:]
        self.registers[c] = 1 if self.registers[a] == self.registers[b] else 0


def part1(samples: tuple) -> int:
    found3plus = 0
    d = Device()

    for before, instruction, after in samples:
        op_success = 0
        for op in d.opnames:
            fnc = getattr(d, op)
            d.set_registers(list(before))
            fnc(instruction)
            if d.cmp_registers(list(after)):
                op_success += 1

        if op_success >= 3:
            found3plus += 1

    return found3plus


def part2(samples: tuple, test_program: tuple) -> int:
    d = Device()

    # This is the rare case where we don't have a given sample input for part 2,
    # so just return a dummy value if we detect this is the sample input.
    if len(samples) < 15:
        return -99

    # Determine the mappings of op names to op codes. This assumes the input
    # data truly leads to a unique mapping.
    while None in d.opname2code.values():
        for before, instruction, after in samples:
            success_ops = []
            for op in d.opnames:
                fnc = getattr(d, op)
                d.set_registers(list(before))
                fnc(instruction)
                if d.cmp_registers(list(after)):
                    if d.opname2code[op] is None:
                        success_ops.append(op)

            if len(success_ops) == 1:
                found_op = success_ops[0]
                d.opname2code[found_op] = instruction[0]
                d.code2opname[instruction[0]] = found_op

    # Run the given program
    d.set_registers([0, 0, 0, 0])
    for instruction in test_program:
        opname = d.code2opname[instruction[0]]
        fnc = getattr(d, opname)
        fnc(instruction)
    reg0 = d.registers[0]

    return reg0


def parse_input(fname: str) -> tuple[tuple, tuple]:
    samples = []
    test_program = []

    sample_re = re.compile(r'Before:\s+\[(\d+), (\d+), (\d+), (\d+)]\n'
                           r'(\d+) (\d+) (\d+) (\d+)\n'
                           r'After:\s+\[(\d+), (\d+), (\d+), (\d+)]\n')

    test_program_re = re.compile(r'(\d+ \d+ \d+ \d+\n)+')

    for record in multiline_record.multiline_file(fname):
        if mo := sample_re.fullmatch(record):
            nums = [int(x) for x in mo.groups()]
            before = tuple(nums[:4])
            instruction = tuple(nums[4:8])
            after = tuple(nums[8:])
            samples.append((before, instruction, after))
        elif test_program_re.fullmatch(record):
            for program_line in record.strip().split('\n'):
                test_program.append(tuple(int(x) for x in program_line.split()))
        else:
            raise ValueError(f'Invalid input: {record}')

    return tuple(samples), tuple(test_program)


def main():
    sample_input = parse_input('input/sample_input.txt')
    main_input = parse_input('input/input.txt')

    for samples, test_program in (sample_input, main_input):
        print("Part 1 answer =", part1(samples))
        print("Part 2 answer =", part2(samples, test_program))
        print()


if __name__ == '__main__':
    main()
