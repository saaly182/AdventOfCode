#!/usr/bin/python3 -u

from collections import defaultdict, deque
import operator
from typing import Iterator


class BidirectionPipe:
    def __init__(self, pid1: int, pid2: int):
        self.pid1 = pid1
        self.pid2 = pid2
        self.pids = (pid1, pid2)
        self.p1_to_p2 = deque()
        self.p2_to_p1 = deque()
        self.send2_count = 0
        self.stalled = {self.pid1: False, self.pid2: False}

    def send(self, caller_pid: int, msg: int) -> None:
        if caller_pid not in self.pids:
            raise ValueError(f'bad pid: {caller_pid}')
        if caller_pid == self.pid1:
            self.p1_to_p2.append(msg)
        else:
            self.send2_count += 1
            self.p2_to_p1.append(msg)

    def recv(self, caller_pid: int) -> int | None:
        if caller_pid not in self.pids:
            raise ValueError(f'bad pid: {caller_pid}')
        try:
            if caller_pid == self.pid1:
                msg = self.p2_to_p1.popleft()
            else:
                msg = self.p1_to_p2.popleft()
        except IndexError:
            self.stalled[caller_pid] = True
            return None
        else:
            self.stalled[caller_pid] = False
            return msg

    def deadlocked(self) -> bool:
        return (False not in self.stalled.values() and not self.p1_to_p2
                and not self.p2_to_p1)

    def show(self):
        print(f'{self.p1_to_p2} {self.p2_to_p1}')


def decode(mem: tuple) -> tuple:
    inst = mem[0]
    op1 = mem[1]
    op2 = mem[2] if len(mem) == 3 else None
    return inst, op1, op2


def execute_part1(program: tuple) -> int | None:
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
                    return frq
            case 'jgz':
                xval = opval(op1)
                if xval > 0:
                    yval = opval(op2)
                    pc_add = yval
            case _:
                raise ValueError(program[pc])

        pc += pc_add


def execute_part2(program: tuple, pid: int,
                  bipipe: BidirectionPipe) -> Iterator[int]:
    pc = 0
    mathops = {'add': operator.add, 'mul': operator.mul, 'mod': operator.mod}
    register = defaultdict(int)
    register['p'] = pid

    def opval(op):
        """Handle whether it's an int literal or a register name."""
        return op if type(op) == int else register[op]

    while 0 <= pc < len(program):
        inst, op1, op2 = decode(program[pc])
        pc_add = 1

        match inst:
            case 'snd':
                bipipe.send(pid, opval(op1))
            case 'set':
                register[op1] = opval(op2)
            case 'add' | 'mul' | 'mod' as thisop:
                register[op1] = mathops[thisop](register[op1], opval(op2))
            case 'rcv':
                msg = None
                while msg is None:
                    msg = bipipe.recv(pid)
                    if msg is None:
                        yield
                        if bipipe.deadlocked():
                            return
                register[op1] = msg
            case 'jgz':
                xval = opval(op1)
                if xval > 0:
                    yval = opval(op2)
                    pc_add = yval
            case _:
                raise ValueError(program[pc])

        pc += pc_add
    print(f"{pid=}DONE")


def part1(program):
    return execute_part1(program)


def part2(program):
    bipipe = BidirectionPipe(0, 1)
    p0 = execute_part2(program, 0, bipipe)
    p1 = execute_part2(program, 1, bipipe)
    p0running = p1running = True

    while p0running or p1running:
        if p0running:
            try:
                next(p0)
            except StopIteration:
                p0running = False
        if p1running:
            try:
                next(p1)
            except StopIteration:
                p1running = False

    return bipipe.send2_count


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
        print("Part 2 answer =", part2(program))
        print()


if __name__ == '__main__':
    main()
