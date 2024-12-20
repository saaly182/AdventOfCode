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

    def do_patrol(self) -> bool:
        """Return True if guard exits room, False if guard gets into inf loop"""
        guard_states_seen = set()

        while True:
            # mark current position as visited
            self.g[self.guard_r][self.guard_c] = self.visited
            gstate = (self.guard_r, self.guard_c, self.guard_d)
            if gstate in guard_states_seen:
                return False  # guard is now in an inf loop
            guard_states_seen.add(gstate)

            # process the next step of the guard
            dr, dc = dirutils.dirvecs[self.guard_d]
            next_r, next_c = self.guard_r + dr, self.guard_c + dc
            if not (0 <= next_r <= self.r_max and 0 <= next_c <= self.c_max):
                return True  # guard has left the area

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

    def empty_squares(self) -> tuple:
        """Return coords of squares that do not contain an
        obstacle or the guard"""
        es = []
        for r, row in enumerate(self.g):
            for c, col in enumerate(row):
                if col not in '#<>^v':
                    es.append((r, c))
        return tuple(es)


def part1(grid: Grid) -> int:
    grid.do_patrol()
    return grid.visited_count()


def part2(inp: tuple) -> int:
    # ... not worried about efficiency at this point
    loop_count = 0
    for r, c in Grid(inp).empty_squares():
        g = Grid(inp)
        g.g[r][c] = '#'
        if not g.do_patrol():
            loop_count += 1
    return loop_count


def slurp(fname: str) -> tuple[str, ...]:
    with open(fname) as file:
        return tuple(line.rstrip() for line in file.readlines())


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        grid = Grid(inp)
        print("Part 1 answer =", part1(grid))
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
