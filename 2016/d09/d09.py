#!/usr/bin/python3 -u

import re


def decomplen(c):
    """Return the length of the decompressed version of string c under
    the part2 decompression rules."""
    dlen = 0
    idx = 0

    while idx < len(c):
        if mo := re.match(r'\((\d+)x(\d+)\)', c[idx:]):
            clen = len(mo.group(0))
            slen = int(mo.group(1))
            repeat = int(mo.group(2))
            idx += clen
            dlen += decomplen(c[idx:idx + slen]) * repeat
            idx += slen
        else:
            dlen += 1
            idx += 1

    return dlen


def decompress(c):
    """Return the decompressed string of compressed string c under the
    part 1 decompression rules."""
    d = []
    idx = 0

    while idx < len(c):
        if mo := re.match(r'\((\d+)x(\d+)\)', c[idx:]):
            clen = len(mo.group(0))
            slen = int(mo.group(1))
            repeat = int(mo.group(2))
            idx += clen
            s = c[idx:idx + slen]
            for _ in range(repeat):
                d.extend(list(s))
            idx += slen
        else:
            d.append(c[idx])
            idx += 1

    return ''.join(d)


def part1(comp_msg):
    return len(decompress(comp_msg))


def part2(comp_msg):
    return decomplen(comp_msg)


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp[0]))
        print("Part 2 answer =", part2(inp[0]))
        print()


if __name__ == '__main__':
    main()
