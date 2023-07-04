#!/usr/bin/python3 -u

import functools

GRIDSIZE = 300


def max_subgrid_power_part1(grid: tuple) -> tuple[int, int]:
    msp = float('-inf')  # max subgrid power
    mspxy = (-1, -1)
    for y in range(1, GRIDSIZE - 1):
        for x in range(1, GRIDSIZE - 1):
            sp = (grid[y + 0][x + 0] + grid[y + 0][x + 1] + grid[y + 0][x + 2] +
                  grid[y + 1][x + 0] + grid[y + 1][x + 1] + grid[y + 1][x + 2] +
                  grid[y + 2][x + 0] + grid[y + 2][x + 1] + grid[y + 2][x + 2])
            if sp > msp:
                msp = sp
                mspxy = (x, y)
    return mspxy


def max_subgrid_power_part2(grid: tuple) -> tuple[int, int, int]:
    """Use recursive inner function to eliminate repeating computations."""
    @functools.cache
    def subgrid_power(sx: int, sy: int, ssize: int) -> int:
        """
        Dynamic programming approach. Basic idea:
        X X X Y    Bigger square = X + Y
        X X X Y
        X X X Y
        Y Y Y Y
        """
        # base case
        if ssize == 1:
            return grid[sy][sx]

        # main case
        ssp = subgrid_power(sx, sy, ssize - 1)
        for i in range(ssize - 1):
            ssp += grid[sy + ssize - 1][sx + i]  # bottom row
            ssp += grid[sy + i][sx + ssize - 1]  # rightmost col
        ssp += grid[sy + ssize - 1][sx + ssize - 1]  # bottom-right corner cell
        return ssp

    msp = float('-inf')  # max subgrid power
    answer = (-1, -1, -1)
    for size in range(1, GRIDSIZE + 1):
        for y in range(1, GRIDSIZE - size + 2):
            for x in range(1, GRIDSIZE - size + 2):
                sp = subgrid_power(x, y, size)
                if sp > msp:
                    msp = sp
                    answer = (x, y, size)
    return answer


def cell_power(x: int, y: int, grid_sn: int) -> int:
    """
    Power Rules:
    * Find the fuel cell's rack ID, which is its X coordinate plus 10.
    * Begin with a power level of the rack ID times the Y coordinate.
    * Increase the power level by the value of the grid serial number (your
      puzzle input).
    * Set the power level to itself multiplied by the rack ID.
    * Keep only the hundreds digit of the power level (so 12345 becomes 3;
      numbers with no hundreds digit become 0).
    * Subtract 5 from the power level.
    """
    rack_id = x + 10
    pl = rack_id * y
    pl += grid_sn
    pl *= rack_id
    pl = int(f'{pl:03}'[-3])
    pl -= 5
    return pl


def power_levels(grid_sn: int) -> tuple:
    grid = []
    # note: this creates row 0 and column 0, but the problem is only concerned
    # with rows and columns 1..300. So row 0 and column 0 will just be ignored.
    for y in range(GRIDSIZE + 1):
        row = []
        for x in range(GRIDSIZE + 1):
            row.append(cell_power(x, y, grid_sn))
        grid.append(tuple(row))
    return tuple(grid)


def part1(grid_sn: int) -> tuple[int, int]:
    grid = power_levels(grid_sn)
    return max_subgrid_power_part1(grid)


def part2(grid_sn: int) -> tuple[int, int, int]:
    grid = power_levels(grid_sn)
    return max_subgrid_power_part2(grid)


def slurp(fname: str) -> list[str]:
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    for grid_sn in (18, 42, 9306):
        print(f'{grid_sn=}')
        print("Part 1 answer =", ','.join([str(x) for x in part1(grid_sn)]))
        print("Part 2 answer =", ','.join([str(x) for x in part2(grid_sn)]))
        print()


if __name__ == '__main__':
    main()
