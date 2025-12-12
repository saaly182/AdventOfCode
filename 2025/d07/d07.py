#!/usr/bin/python3 -u

import functools

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


def lol2tot(lst: list) -> tuple:
    """Return a tuple-of-tuples given a list-of-lists."""
    return tuple(tuple(r) for r in lst)


@functools.cache
def travel_manifold(grid: tuple, depth: int) -> int:
    # recursive and memoized; note that all the flipping between lists and
    # tuples is required because functools.cache requires the fnc args to be
    # hashable.

    if depth == len(grid) - 1:
        return 1

    pathcount = 0
    g = [list(r) for r in grid]
    tp = g[depth - 1].index(BEAM)  # tachyon position
    c = g[depth][tp]
    # ugly code; basically move the beam down one level, call the recursion,
    # and then restore the previous state. this is required to get memoized
    # results.
    if c == EMPTY:
        g[depth - 1][tp] = EMPTY
        g[depth][tp] = BEAM
        pathcount += travel_manifold(lol2tot(g), depth + 1)
        g[depth - 1][tp] = BEAM
        g[depth][tp] = EMPTY
    elif c == SPLITTER:
        # left case
        c_left = g[depth][tp - 1]
        g[depth - 1][tp] = EMPTY
        g[depth][tp - 1] = BEAM
        pathcount += travel_manifold(lol2tot(g), depth + 1)
        g[depth - 1][tp] = BEAM
        g[depth][tp - 1] = c_left
        # right case
        c_right = g[depth][tp + 1]
        g[depth - 1][tp] = EMPTY
        g[depth][tp + 1] = BEAM
        pathcount += travel_manifold(lol2tot(g), depth + 1)
        g[depth - 1][tp] = BEAM
        g[depth][tp + 1] = c_right
    else:
        raise ValueError(f'Invalid character {c}')

    return pathcount


def part2(grid: tuple) -> int:
    g = [list(r) for r in grid]
    s = g[0].index('S')
    g[1][s] = BEAM

    return travel_manifold(lol2tot(g), 2)


def parse_input(fname: str) -> tuple[tuple, ...]:
    with open(fname) as file:
        return tuple(tuple(line.rstrip()) for line in file.readlines())


def main():
    sample_input = parse_input('input/sample_input.txt')
    main_input = parse_input('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
