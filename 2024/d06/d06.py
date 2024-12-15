#!/usr/bin/python3 -u

import re
import sys
sys.path.append('../../lib')
import dirutils  # noqa


class Grid:
    def __init__(self, lines: tuple):
        self.g = []
        self.guard_r = None  # row
        self.guard_c = None  # col
        self.guard_d = None  # direction
        self.visited = 'X'
        self.turn_right = {'^': '>', '>': 'v', 'v': '<', '<': '^'}

        for row, line in enumerate(lines):
            self.g.append(list(line))
            if mo := re.search(r'[<>^v]', line):
                if self.guard_r or self.guard_c or self.guard_d:
                    raise ValueError('Found more than one guard!')
                self.guard_r = row
                self.guard_c = mo.span()[0]
                self.guard_d = mo.group()

        self.r_max = len(self.g) - 1
        self.c_max = len(self.g[0]) - 1

    def do_patrol(self) -> None:
        while True:
            # mark current position as visited
            self.g[self.guard_r][self.guard_c] = self.visited

            # process the next step of the guard
            dr, dc = dirutils.dirvecs[self.guard_d]
            next_r, next_c = self.guard_r + dr, self.guard_c + dc
            if not (0 <= next_r <= self.r_max and 0 <= next_c <= self.c_max):
                break  # guard has left the area

            if self.g[next_r][next_c] == '#':
                self.guard_d = self.turn_right[self.guard_d]
            else:
                assert self.g[next_r][next_c] in ('.', self.visited)
                self.guard_r = next_r
                self.guard_c = next_c

    def show(self) -> None:
        for row in self.g:
            print(''.join(row))

    def visited_count(self) -> int:
        vc = 0
        for row in self.g:
            for char in row:
                if char == self.visited:
                    vc += 1
        return vc


def part1(grid: Grid) -> int:
    grid.do_patrol()
    return grid.visited_count()


def part2():
    return None


def slurp(fname: str) -> tuple[str, ...]:
    with open(fname) as file:
        return tuple(line.rstrip() for line in file.readlines())


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        grid = Grid(inp)
        print("Part 1 answer =", part1(grid))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
