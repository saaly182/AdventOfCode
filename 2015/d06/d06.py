#!/usr/bin/python3 -u

class Grid1:
    def __init__(self, size):
        self.g = [[0 for _ in range(size)] for _ in range(size)]

    def toggle(self, r, c):
        self.g[r][c] = abs(1 - self.g[r][c])

    def turn(self, r, c, onoff):
        self.g[r][c] = onoff

    def cmd(self, c):
        toggle = False
        onoff = 1
        match c.split():
            case ['turn', ('on' | 'off') as mode, rc1, 'through', rc2]:
                if mode == 'off':
                    onoff = 0
            case ['toggle', rc1, 'through', rc2]:
                toggle = True
            case _:
                raise ValueError(c)
        r1, c1 = (int(x) for x in rc1.split(','))
        r2, c2 = (int(x) for x in rc2.split(','))
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                if toggle:
                    self.toggle(r, c)
                else:
                    self.turn(r, c, onoff)

    def metric_value(self):
        metric = 0
        for r in self.g:
            metric += sum([x for x in r if x])
        return metric


class Grid2(Grid1):
    def toggle(self, r, c):
        self.g[r][c] += 2

    def turn(self, r, c, onoff):
        delta = 1
        if onoff == 0:
            delta = -1
        self.g[r][c] = max(0, self.g[r][c] + delta)


def part1(cmds):
    g = Grid1(1000)
    for c in cmds:
        g.cmd(c)
    return g.metric_value()


def part2(cmds):
    g = Grid2(1000)
    for c in cmds:
        g.cmd(c)
    return g.metric_value()


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    main_input = slurp('input/input.txt')

    for inp in (main_input, ):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
