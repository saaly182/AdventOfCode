#!/usr/bin/python3 -u

import collections
import itertools
import re


def part1(happiness_matrix):
    hmax = 0
    head = list(happiness_matrix)[0]
    for tail in itertools.permutations(list(happiness_matrix)[1:]):
        seating = [head] + list(tail) + [head]  # head tacked on end for ring
        happiness = 0
        for p1, p2 in zip(seating, seating[1:]):
            happiness += happiness_matrix[p1][p2] + happiness_matrix[p2][p1]
        hmax = max(hmax, happiness)
    return hmax


def part2(happiness_matrix):
    # Add me to matrix.
    # Use list() here to get a static list of keys, b/c changing the dict
    # in the loop.
    for p in list(happiness_matrix):
        happiness_matrix[p]['me'] = 0
        happiness_matrix['me'][p] = 0
    return part1(happiness_matrix)


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp):
    spec = (r'(\w+) would (gain|lose) (\d+) happiness units by sitting '
            r'next to (\w+).')
    hm = collections.defaultdict(dict)
    for line in inp:
        match = re.fullmatch(spec, line)
        assert match
        person1, mvt, hval, person2 = match.groups()
        hval = int(hval)
        if mvt == 'lose':
            hval = -hval
        hm[person1][person2] = hval
    return hm


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        happiness_matrix = parse(inp)
        print("Part 1 answer =", part1(happiness_matrix))
        print("Part 2 answer =", part2(happiness_matrix))
        print()


if __name__ == '__main__':
    main()
