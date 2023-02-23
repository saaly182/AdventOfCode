#!/usr/bin/python3 -u

import dataclasses
import itertools


@dataclasses.dataclass
class Device:
    name: str
    size: int
    used: int
    avail: int
    pct: int


def part1(df):
    viable_pairs = []
    for a, b in itertools.combinations(df, 2):
        for d1, d2 in ((a, b), (b, a)):
            if 0 < d1.used <= d2.avail:
                viable_pairs.append((d1, d2))

    return len(viable_pairs)


def part2():
    return None


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
    main_input = slurp('input/input.txt')

    for inp in (main_input,):
        df = parse(inp)
        print("Part 1 answer =", part1(df))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
