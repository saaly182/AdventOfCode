#!/usr/bin/python3 -u

def part1() -> int:
    return -99


def part2() -> int:
    return -99


def slurp(fname: str) -> tuple[str, ...]:
    with open(fname) as file:
        return tuple(line.rstrip() for line in file.readlines())


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1())
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
