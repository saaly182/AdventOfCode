#!/usr/bin/python3 -u

def execute(jmps, mode=1):
    """Return the number of steps taken by the given jumps."""
    j = list(jmps)
    pc = 0
    steps = 0
    while 0 <= pc < len(j):
        offset = j[pc]
        if mode == 2 and offset > 2:
            j[pc] -= 1
        else:
            j[pc] += 1
        pc += offset
        steps += 1
    return steps


def part1(jmps):
    return execute(jmps, mode=1)


def part2(jmps):
    return execute(jmps, mode=2)


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        jmps = tuple(int(a) for a in inp)
        print("Part 1 answer =", part1(jmps))
        print("Part 2 answer =", part2(jmps))
        print()


if __name__ == '__main__':
    main()
