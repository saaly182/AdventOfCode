#!/usr/bin/python3 -u

def part1():
    return None


def part2():
    return None


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    sample_input = slurp('sample_input.txt')
    main_input = slurp('input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1())
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
