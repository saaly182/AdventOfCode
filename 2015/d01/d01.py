#!/usr/bin/python3 -u

def part1(inp):
    return inp[0].count('(') - inp[0].count(')')


def part2(inp):
    steps = 0
    floor = 0
    d = {'(': 1, ')': -1}
    for move in inp[0]:
        floor += d[move]
        steps += 1
        if floor == -1:
            break
    return steps


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    main_input = slurp('input/input.txt')

    for inp in (main_input,):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
