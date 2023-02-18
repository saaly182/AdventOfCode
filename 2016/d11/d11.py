#!/usr/bin/python3 -u
"""
The main data structure for this code is a tuple of int pairs. Each pair of
ints tells the floor numbers of the corresponding "generator" and
"microchip". So for example, ((3, 3), (2, 1), (4, 3)) means generator1 and
microchip1 are on floor 3; generator2 is on floor 2 and microchip2 is on
floor1; generator3 is on floor 4 and microchip3 is on floor 3. It's not
important to know or track their element names.
"""

import itertools


def flatten(pos):
    f = []
    for p in pos:
        f.extend(p)
    return f


def pairup(f):
    return tuple(zip(f[::2], f[1::2]))


def next_positions(elev, pos):
    for floor in (elev - 1, elev + 1):
        if floor < 1 or floor > 4:
            continue

        f = flatten(pos)

        # take one item in the elevator
        for i in range(len(f)):
            if f[i] == elev:
                f[i] = floor
                yield floor, pairup(f)
                f[i] = elev

        # take two items in the elevator
        for i, j in itertools.combinations(range(len(f)), 2):
            if f[i] == f[j] == elev:
                f[i] = f[j] = floor
                yield floor, pairup(f)
                f[i] = f[j] = elev


def valid_pos(pos):
    # if a chip is ever left in the same area as another RTG, and it's not
    # connected to its own RTG, the chip will be fried.
    unprotected_chip_floors = set([x[1] for x in pos if x[0] != x[1]])
    generator_floors = set([x[0] for x in pos])
    if generator_floors.intersection(unprotected_chip_floors):
        return False
    return True


def bfs(positions):
    tgt = tuple([(4, 4)] * len(positions))
    steps = 0
    elev = 1  # elevator floor
    q = [(steps, elev, positions)]
    seen = set()

    while q:
        steps, elev, pos = q.pop(0)
        if pos == tgt:
            return steps
        if (elev, pos) in seen:
            continue
        seen.add((elev, pos))
        if not valid_pos(pos):
            continue
        for nelev, npos in next_positions(elev, pos):
            q.append((steps + 1, nelev, npos))


def part1(positions):
    steps = bfs(positions)
    return steps


def part2():
    return None


def main():
    # The first floor contains a hydrogen-compatible microchip and a
    # lithium-compatible microchip.
    # The second floor contains a hydrogen generator.
    # The third floor contains a lithium generator.
    # The fourth floor contains nothing relevant.
    sample_input = ((2, 1), (3, 1))
    # The first floor contains a promethium generator and a
    # promethium-compatible microchip.
    # The second floor contains a cobalt generator, a curium generator, a
    # ruthenium generator, and a plutonium generator.
    # The third floor contains a cobalt-compatible microchip, a
    # curium-compatible microchip, a ruthenium-compatible microchip, and a
    # plutonium-compatible microchip.
    # The fourth floor contains nothing relevant.
    main_input = ((1, 1), (2, 3), (2, 3), (2, 3), (2, 3))

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
