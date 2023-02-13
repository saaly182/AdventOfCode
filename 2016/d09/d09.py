#!/usr/bin/python3 -u

import re


def decompress(c, version=1):
    d = []
    idx = 0
    if version not in (1, 2):
        raise ValueError(f'bad version number: {version}')

    while idx < len(c):
        if mo := re.match(r'\((\d+)x(\d+)\)', c[idx:]):
            clen = len(mo.group(0))
            slen = int(mo.group(1))
            repeat = int(mo.group(2))
            idx += clen
            s = c[idx:idx + slen]

            if version == 1:
                ds = list(s)
            else:
                ds = list(decompress(s, version=2))
            for _ in range(repeat):
                d.extend(ds)

            idx += slen
        else:
            d.append(c[idx])
            idx += 1

    return ''.join(d)


def part1(comp_msg):
    return len(decompress(comp_msg))


def part2(comp_msg):
    return len(decompress(comp_msg, version=2))


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
