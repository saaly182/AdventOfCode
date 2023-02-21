#!/usr/bin/python3 -u

import dataclasses


@dataclasses.dataclass
class Elf:
    presents: int
    next_elf: int


def winner(nelves):
    """Return the number of the elf that ends up with everything."""
    # elf is a linked-list ring
    elf = {}
    for i in range(1, nelves):
        elf[i] = Elf(1, i + 1)
    elf[nelves] = Elf(1, 1)

    i = 1
    while True:
        if elf[i].presents == 0:
            i = i % nelves + 1
            continue
        if elf[i].presents == nelves:
            # This elf has all the presents
            return i
        # take all presents from the next elf with presents
        j = elf[i].next_elf
        while elf[j].presents == 0:
            j = elf[j].next_elf
        elf[i].presents += elf[j].presents
        elf[j].presents = 0
        i = i % nelves + 1


def part1(nelves):
    return winner(nelves)


def part2():
    return None


def main():
    sample_input = 5
    main_input = 3_005_290

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
