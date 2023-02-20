#!/usr/bin/python3 -u

# Observation: The number of positions of every disc is prime, and they're
# each distinct. So the product of the position counts is the interval at which
# all the discs have their initial starting position. Not sure yet if that's
# useful.

from typing import NamedTuple


class Disc(NamedTuple):
    positions: int
    init_pos: int


def disc_pos(disc, t):
    """Return the position of the disc at time t."""
    return (t + disc.init_pos) % disc.positions


def part1(discs):
    # Gonna brute-force this...
    t = 0
    while True:
        success = True
        for i, d in enumerate(discs):
            if disc_pos(d, t + 1 + i) != 0:
                success = False
                break
        if success:
            return t
        t += 1


def part2():
    return None


def main():
    # sample input
    # Disc #1 has 5 positions; at time=0, it is at position 4.
    # Disc #2 has 2 positions; at time=0, it is at position 1.
    sample_input = ((5, 4), (2, 1))

    # main input
    # Disc #1 has 17 positions; at time=0, it is at position 5.
    # Disc #2 has 19 positions; at time=0, it is at position 8.
    # Disc #3 has  7 positions; at time=0, it is at position 1.
    # Disc #4 has 13 positions; at time=0, it is at position 7.
    # Disc #5 has  5 positions; at time=0, it is at position 1.
    # Disc #6 has  3 positions; at time=0, it is at position 0.
    main_input = ((17, 5), (19, 8), (7, 1), (13, 7), (5, 1), (3, 0))

    for inp in (sample_input, main_input):
        discs = []
        for d in inp:
            discs.append(Disc(*d))
        discs = tuple(discs)
        print("Part 1 answer =", part1(discs))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
