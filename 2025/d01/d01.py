#!/usr/bin/python3 -u

from typing import Tuple

DTICKS = 100  # number of ticks on the dial


def part1(rots: tuple) -> int:
    d = 50
    zero_count = 0
    for rotdir, dist in rots:
        if rotdir == 'R':
            d = (d + dist) % DTICKS
        else:
            d = (d - dist + DTICKS) % DTICKS
        if d == 0:
            zero_count += 1
    return zero_count


def part2(rots: tuple) -> int:
    d1 = 50
    zero_landing = 0
    zero_passthru = 0

    for rotdir, dist in rots:
        if rotdir == 'R':
            d2 = (d1 + dist) % DTICKS
            if d1 and d2 and d2 < d1:
                zero_passthru += 1
        else:
            d2 = (d1 - dist + DTICKS) % DTICKS
            if d1 and d2 and d2 > d1:
                zero_passthru += 1

        full_rotations = dist // DTICKS
        zero_passthru += full_rotations

        if d2 == 0:  # if we landed on zero
            zero_landing += 1

        d1 = d2
    return zero_landing + zero_passthru


def slurp(fname: str) -> Tuple[Tuple[str, int], ...]:
    rots = []
    with open(fname) as file:
        for line in file:
            rotdir = line[0]
            assert rotdir in 'LR'
            dist = int(line[1:])
            assert dist != 0
            rots.append((rotdir, dist))

        return tuple(rots)


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
