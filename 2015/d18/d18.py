#!/usr/bin/python3 -u

class Grid:
    def __init__(self, rows, corners_on=False):
        self.g = []
        for r in rows:
            self.g.append(list(r))
        self.rowmax = len(self.g) - 1
        self.colmax = len(self.g[0]) - 1
        self.con = corners_on
        if self.con:
            self._corners_on(self.g)

    def show(self):
        print('-' * 5)
        for row in self.g:
            print(''.join(row))
        print()

    def lights_on(self):
        return sum([r.count('#') for r in self.g])

    def _neighbor_on_count(self, g, r, c):
        noc = 0
        deltas = ((-1, 0), (-1, 1), (0, 1), (1, 1),
                  (1, 0), (1, -1), (0, -1), (-1, -1))
        for d in deltas:
            rn, cn = r + d[0], c + d[1]
            if rn < 0 or rn > self.rowmax or cn < 0 or cn > self.colmax:
                continue
            if g[rn][cn] == '#':
                noc += 1
        return noc

    def _corners_on(self, g):
        g[0][0] = g[0][self.colmax] = '#'
        g[self.rowmax][0] = g[self.rowmax][self.colmax] = '#'

    def animate(self, steps):
        # A light which is on stays on when 2 or 3 neighbors are on,
        # and turns off otherwise. A light which is off turns on if exactly 3
        # neighbors are on, and stays off otherwise.
        for i in range(steps):
            g1 = self.g
            g2 = []
            for r in range(len(g1)):
                row = []
                for c in range(len(g1[0])):
                    noc = self._neighbor_on_count(g1, r, c)
                    if g1[r][c] == '#':
                        if noc == 2 or noc == 3:
                            row.append('#')
                        else:
                            row.append('.')
                    else:
                        if noc == 3:
                            row.append('#')
                        else:
                            row.append('.')
                g2.append(row)
            self.g = g2
            if self.con:
                self._corners_on(self.g)


def part1(inp):
    g = Grid(inp)
    g.animate(100)
    return g.lights_on()


def part2(inp):
    g = Grid(inp, corners_on=True)
    g.animate(100)
    return g.lights_on()


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
