#!/usr/bin/python3 -u

import collections
import re
spec = r'(.*)-(\d+)\[(.*)\]'


def checksum(s):
    """
    The five most common letters in the encrypted name, in order,
    with ties broken by alphabetization
    """
    char2count = collections.defaultdict(int)
    count2char = collections.defaultdict(list)

    for c in s:
        if not c.islower():
            continue
        char2count[c] += 1

    for c, count in char2count.items():
        count2char[count].append(c)

    cksum = []
    for count in sorted(count2char, reverse=True):
        cksum.extend(sorted(count2char[count]))

    return ''.join(cksum[:5])


def part1(inp):
    secsum = 0
    for item in inp:
        match = re.fullmatch(spec, item)
        if not match:
            raise ValueError(item)
        encname, sectorid, cksum = match.groups()
        if checksum(encname) == cksum:
            secsum += int(sectorid)
    return secsum


def part2():
    return None


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
