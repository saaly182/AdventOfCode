#!/usr/bin/python3 -u

import sys
sys.path.append('../d10')
import d10


def part1(keystring):
    used_count = 0
    for i in range(128):
        kh = d10.knot_hash(f'{keystring}-{i}')
        bits = bin(int(kh, base=16))
        used_count += bits.count('1')
    return used_count


def part2():
    return None


def main():
    for inp in ('flqrgnkx', 'uugsqrei'):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
