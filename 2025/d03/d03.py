#!/usr/bin/python3 -u

def part1(banks: tuple) -> int:
    total_jolts = 0
    for bank in banks:
        x1val = max(bank[:-1])
        x1pos = bank.index(x1val)
        x2val = max(bank[x1pos + 1:])
        total_jolts += x1val * 10 + x2val
    return total_jolts


def part2() -> int:
    return -99


def parse_input(fname: str) -> tuple[tuple[int], ...]:
    banks = []
    with open(fname) as file:
        for line in file:
            j = tuple(int(x) for x in line.rstrip())
            banks.append(j)
    return tuple(banks)


def main():
    sample_input = parse_input('input/sample_input.txt')
    main_input = parse_input('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
