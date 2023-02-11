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
        if not (mo := re.fullmatch(spec, item)):
            raise ValueError(item)
        encname, sectorid, cksum = mo.groups()
        sectorid = int(sectorid)
        if checksum(encname) == cksum:
            secsum += sectorid
    return secsum


def decrypt(s, n):
    dec = []
    offset = ord('a')
    for ec in s:
        if ec == '-':
            dc = ' '
        else:
            dc = chr(((((ord(ec) - offset) + n) % 26) + offset))
        dec.append(dc)
    return ''.join(dec)


def part2(inp):
    for item in inp:
        if not (mo := re.fullmatch(spec, item)):
            raise ValueError(item)
        encname, sectorid, cksum = mo.groups()
        sectorid = int(sectorid)
        if checksum(encname) == cksum:
            name = decrypt(encname, sectorid)
            if name == 'northpole object storage':
                return sectorid
    return None


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
