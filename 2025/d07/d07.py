#!/usr/bin/python3 -u

BEAM = '|'
SPLITTER = '^'
EMPTY = '.'


def showgrid(grid) -> None:
    for row in grid:
        print(''.join(row))


def part1(grid: tuple) -> int:
    splitcount = 0

    # create a mutable copy of the input grid
    g = [list(r) for r in grid]

    # assuming there's always one and only one S, and it's in the 1st row
    s = g[0].index('S')
    g[1][s] = BEAM

    for i, row in enumerate(g[2:], 2):
        for j, c in enumerate(row):
            if c == EMPTY and g[i - 1][j] == BEAM:
                g[i][j] = BEAM
            elif c == SPLITTER and g[i - 1][j] == BEAM:
                # assume splitters cannot be in the 1st or last columns, and
                # that splitters cannot be adjacent to each other
                g[i][j - 1] = g[i][j + 1] = BEAM
                splitcount += 1

    return splitcount


def part2() -> int:
    return -99


def parse_input(fname: str) -> tuple[tuple, ...]:
    with open(fname) as file:
        return tuple(tuple(line.rstrip()) for line in file.readlines())


def main():
    sample_input = parse_input('input/sample_input.txt')
    main_input = parse_input('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
