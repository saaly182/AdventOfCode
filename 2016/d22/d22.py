#!/usr/bin/python3 -u

import dataclasses
import itertools
import re


@dataclasses.dataclass
class Device:
    name: str
    size: int
    used: int
    avail: int
    pct: int
    x: int = dataclasses.field(init=False)
    y: int = dataclasses.field(init=False)

    def __post_init__(self):
        mo = re.fullmatch(r'/dev/grid/node-x(\d+)-y(\d+)', self.name)
        self.x = int(mo.group(1))
        self.y = int(mo.group(2))


def show_nodes(df):
    """Visualize the nodes."""
    nodes = {}
    for device in df:
        nodes[(device.x, device.y)] = device
    maxx = max([x for x, _ in nodes])
    maxy = max([y for _, y in nodes])

    for y in range(maxy + 1):
        for x in range(maxx + 1):
            device = nodes[(x, y)]
            if y == 0 and x == maxx:
                ch = 'G'
            elif device.used == 0:
                ch = '_'
            elif device.used > 400:
                ch = '#'
            else:
                ch = '.'
            print(ch, end='')
        print()


def part1(df):
    viable_pairs = []
    for a, b in itertools.combinations(df, 2):
        for d1, d2 in ((a, b), (b, a)):
            if 0 < d1.used <= d2.avail:
                viable_pairs.append((d1, d2))
    return len(viable_pairs)


def part2(df):
    # Trying to do a BFS or DFS seems infeasible for this. Finally, scanning
    # reddit, it turns out that the input data is highly specialized in that
    # there's one empty node, and no other pair of nodes can accommodate data
    # moves. That is, the only moves possible involve the currently empty node.
    # There are also a number of very large nodes that simply cannot move.
    # So I'm just printing out the grid graphically and solving by hand. My
    # input looks like this:
    #
    # .............................G
    # ..............................
    # ..............................
    # ..............................
    # ..............................
    # ..............................
    # ..............................
    # ..............................
    # ..............................
    # ..............................
    # ..............................
    # ..............................
    # ..............................
    # ..............................
    # ........######################
    # ..............................
    # ..............................
    # ..............................
    # ..............................
    # ..............................
    # ..............................
    # ..............................
    # ..........._..................
    # ..............................
    # ..............................
    # ..............................
    # ..............................
    # ..............................
    # ..............................
    # ..............................
    # ..............................
    # ..............................
    #
    # Manually determined the minimum moves: 188
    #

    show_nodes(df)


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp):
    df = []
    for line in inp[2:]:
        dev, size, used, avail, percent = line.split()
        size = int(size[:-1])
        used = int(used[:-1])
        avail = int(avail[:-1])
        percent = int(percent[:-1])
        assert size == used + avail
        df.append(Device(dev, size, used, avail, percent))
    return tuple(df)


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        df = parse(inp)
        print("Part 1 answer =", part1(df))
        print("Part 2 answer =", part2(df))
        print()


if __name__ == '__main__':
    main()
