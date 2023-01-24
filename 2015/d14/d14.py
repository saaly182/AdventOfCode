#!/usr/bin/python3 -u

import typing


class Reindeer(typing.NamedTuple):
    name: str
    speed: int
    runtime: int
    resttime: int


def part1(rdata, racetime):
    maxdist = 0
    for r in rdata:
        cycletime = r.runtime + r.resttime
        cycles, timeleft = divmod(racetime, cycletime)
        dist = r.speed * cycles * r.runtime + r.speed * min(r.runtime, timeleft)
        maxdist = max(maxdist, dist)
    return maxdist


def part2():
    return None


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp):
    rdata = []
    for line in inp:
        a = line.split()
        rdata.append(Reindeer(a[0], int(a[3]), int(a[6]), int(a[13])))
    return tuple(rdata)


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        rdata = parse(inp)
        print("Part 1 answer =", part1(rdata, 2503))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
