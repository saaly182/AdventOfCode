#!/usr/bin/python3 -u
"""
Begin in state A.
Perform a diagnostic checksum after 12629077 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 0.
    - Move one slot to the right.
    - Continue with state C.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state B.

In state C:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state D.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state A.

In state D:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state E.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state F.

In state E:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state D.

In state F:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state E.
"""

from collections import defaultdict


def part1() -> int:
    state = 'A'
    tape = defaultdict(int)
    pos = 0
    rules = {
        ('A', 0): (1,  1, 'B'), ('A', 1): (0, -1, 'B'),
        ('B', 0): (0,  1, 'C'), ('B', 1): (1, -1, 'B'),
        ('C', 0): (1,  1, 'D'), ('C', 1): (0, -1, 'A'),
        ('D', 0): (1, -1, 'E'), ('D', 1): (1, -1, 'F'),
        ('E', 0): (1, -1, 'A'), ('E', 1): (0, -1, 'D'),
        ('F', 0): (1,  1, 'A'), ('F', 1): (1, -1, 'E'),
    }

    for _ in range(12629077):
        assert tape[pos] == 0 or tape[pos] == 1
        assert state in 'ABCDEF'
        cmd = rules[(state, tape[pos])]
        tape[pos] = cmd[0]
        pos += cmd[1]
        state = cmd[2]

    return list(tape.values()).count(1)


def main():
    print("Part 1 answer =", part1())
    print()


if __name__ == '__main__':
    main()
