#!/usr/bin/python3 -u

def part1() -> int:
    return -99


def part2() -> int:
    return -99


def parse_input(fname: str) -> tuple[str, ...]:
    with open(fname) as file:
        return tuple(line.rstrip() for line in file.readlines())


def main():
    input_files = (
        'input/sample_input.txt',
        'input/input.txt',
    )
    for inpf in input_files:
        inp = parse_input(inpf)
        print("Part 1 answer =", part1())
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
