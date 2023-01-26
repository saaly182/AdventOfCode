#!/usr/bin/python3 -u

import collections
import typing


class Reindeer(typing.NamedTuple):
    name: str
    speed: int
    runtime: int
    resttime: int
    cycletime: int


def part1(rdata, racetime):
    maxdist = 0
    for r in rdata:
        cycles, timeleft = divmod(racetime, r.cycletime)
        dist = r.speed * cycles * r.runtime + r.speed * min(r.runtime, timeleft)
        maxdist = max(maxdist, dist)
    return maxdist


def part2(rdata, racetime):
    dist = collections.defaultdict(int)
    points = collections.defaultdict(int)

    for t in range(0, racetime):
        for r in rdata:
            tc = t % r.cycletime
            if tc < r.runtime:
                dist[r.name] += r.speed * 1

        maxdist = max(dist.values())
        for r in rdata:
            if dist[r.name] == maxdist:
                points[r.name] += 1

    return max(points.values())


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp):
    rdata = []
    for line in inp:
        a = line.split()
        name = a[0]
        speed = int(a[3])
        runtime = int(a[6])
        resttime = int(a[13])
        cycletime = runtime + resttime
        rdata.append(Reindeer(name, speed, runtime, resttime, cycletime))
    return tuple(rdata)


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        rdata = parse(inp)
        print("Part 1 answer =", part1(rdata, 2503))
        print("Part 2 answer =", part2(rdata, 2503))
        print()


if __name__ == '__main__':
    main()
