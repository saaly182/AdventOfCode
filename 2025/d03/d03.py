#!/usr/bin/python3 -u

def max_joltage(bank: tuple, n: int) -> int:
    j = []
    pos1 = 0
    pos2 = -n + 1
    for _ in range(n):
        if pos2 == 0: pos2 = None
        x = max(bank[pos1:pos2])
        j.append(x)
        pos1 += (bank[pos1:].index(x) + 1)
        if pos2: pos2 += 1
    mj = int(''.join([str(x) for x in j]))
    return mj


def total_joltage(banks: tuple, n: int) -> int:
    tj = 0
    for bank in banks:
        tj += max_joltage(bank, n)
    return tj


def part1(banks: tuple) -> int:
    return total_joltage(banks, 2)


def part2(banks: tuple) -> int:
    return total_joltage(banks, 12)


def parse_input(fname: str) -> tuple[tuple[int], ...]:
    banks = []
    with open(fname) as file:
        for line in file:
            jolts = tuple(int(x) for x in line.rstrip())
            banks.append(jolts)
    return tuple(banks)


def main():
    sample_input = parse_input('input/sample_input.txt')
    main_input = parse_input('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
