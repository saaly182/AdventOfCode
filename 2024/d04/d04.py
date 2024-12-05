#!/usr/bin/python3 -u

directions = (
    (-1,  0),  # n
    (-1,  1),  # ne
    ( 0,  1),  # e
    ( 1,  1),  # se
    ( 1,  0),  # s
    ( 1, -1),  # sw
    ( 0, -1),  # w
    (-1, -1),  # nw
)


def part1(grid: tuple) -> int:
    xmas_count = 0
    # Just inspect every 'X' and check its eight possible XMAS directions
    r = 0
    rmax = len(grid) - 1
    cmax = len(grid[0]) - 1
    for row in grid:
        c = 0
        for letter in row:
            if letter == 'X':
                for dr, dc in directions:
                    mas = []
                    for i in range(1, 4):
                        _r = r + i * dr
                        _c = c + i * dc
                        if not 0 <= _r <= rmax or not 0 <= _c <= cmax:
                            break
                        mas.append(grid[_r][_c])
                    if mas == ['M', 'A', 'S']:
                        xmas_count += 1
            c += 1
        r += 1
    return xmas_count


def part2(grid: tuple) -> int:
    xmas_count = 0
    # Just inspect every interior 'A' for X-MAS
    r = 1
    for row in grid[1:-1]:
        c = 1
        for letter in row[1:-1]:
            if letter == 'A':
                nw = grid[r - 1][c - 1]
                ne = grid[r - 1][c + 1]
                se = grid[r + 1][c + 1]
                sw = grid[r + 1][c - 1]
                if {nw, ne, se, sw} == {'M', 'S'} and nw != se and ne != sw:
                    xmas_count += 1
            c += 1
        r += 1
    return xmas_count


def slurp(fname: str) -> tuple[str, ...]:
    with open(fname) as file:
        return tuple(line.rstrip() for line in file.readlines())


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
