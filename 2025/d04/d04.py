#!/usr/bin/python3 -u

import sys
sys.path.append('../../lib')
import dirutils  # noqa: E402 F401


def accessible_rolls(grid: list | tuple) -> tuple:
    rows = len(grid)
    cols = len(grid[0])

    acc_rolls = []
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
                acc_rolls.append((r, c))
    return tuple(acc_rolls)


def part1(grid: tuple) -> int:
    return len(accessible_rolls(grid))


def part2(grid: tuple) -> int:
    # need a mutable list-based version of grid
    g = [list(x) for x in grid]
    total_removed = 0
    while removable_rolls := accessible_rolls(g):
        total_removed += len(removable_rolls)
        for r, c in removable_rolls:
            g[r][c] = '.'
    return total_removed


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
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
