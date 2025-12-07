#!/usr/bin/python3 -u

import sys
sys.path.append('../../lib')
import dirutils  # noqa: E402 F401


def part1(grid: tuple) -> int:
    rows = len(grid)
    cols = len(grid[0])

    acc_rolls = 0  # accessible rolls of paper
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != '@':
                continue
            adj_rolls = 0  # adjacent rolls of paper
            for dr, dc in dirutils.neighbors:
                r2 = r + dr
                c2 = c + dc
                if 0 <= r2 < rows and 0 <= c2 < cols:
                    if grid[r2][c2] == '@':
                        adj_rolls += 1
            if adj_rolls < 4:
                acc_rolls += 1

    return acc_rolls


def part2() -> int:
    return -99


def parse_input(fname: str) -> tuple[tuple, ...]:
    grid = []
    with open(fname) as file:
        for line in file:
            grid.append(tuple(line.rstrip()))
        return tuple(grid)


def main():
    sample_input = parse_input('input/sample_input.txt')
    main_input = parse_input('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
