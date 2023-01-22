#!/usr/bin/python3 -u

import collections
import itertools
import re


def optdist(distdata, findmax=False):
    cities = list(distdata)
    mindist = None
    maxdist = None

    for path in itertools.permutations(cities):
        dist = 0
        for city1, city2 in zip(path, path[1:]):
            dist += distdata[city1][city2]

        if mindist is None:
            mindist = dist
        else:
            mindist = min(dist, mindist)

        if maxdist is None:
            maxdist = dist
        else:
            maxdist = max(dist, maxdist)

    if findmax:
        return maxdist
    else:
        return mindist


def part1(distdata):
    return optdist(distdata)


def part2(distdata):
    return optdist(distdata, findmax=True)


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp):
    distdata = collections.defaultdict(dict)
    spec = r'(\w+) to (\w+) = (\d+)'
    for item in inp:
        match = re.fullmatch(spec, item)
        city1, city2, dist = match.groups()
        dist = int(dist)
        distdata[city1][city2] = dist
        distdata[city2][city1] = dist
    return distdata


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        distdata = parse(inp)
        print("Part 1 answer =", part1(distdata))
        print("Part 2 answer =", part2(distdata))
        print()


if __name__ == '__main__':
    main()
