#!/usr/bin/python3 -u

import dataclasses


@dataclasses.dataclass
class Elf:
    presents: int
    next_elf: int
    prev_elf: int


def elf_ring(nelves):
    # Doubly-linked ring
    elf = {}
    for i in range(2, nelves):
        elf[i] = Elf(1, i + 1, i - 1)
    elf[1] = Elf(1, 2, nelves)
    elf[nelves] = Elf(1, 1, nelves - 1)
    return elf


def elf_unlink(elf, i):
    n = elf[i].next_elf
    p = elf[i].prev_elf
    elf[n].prev_elf = p
    elf[p].next_elf = n
    del elf[i]


def elf_across(elist, i):
    """Return the elf num & idx of the elf across the circle from i."""
    i_loc = elist.index(i)
    j_loc = (i_loc + len(elist) // 2) % len(elist)
    return elist[j_loc], j_loc


def winner_part1(nelves):
    """Return the number of the elf that ends up with everything."""
    elf = elf_ring(nelves)

    i = 1
    while True:
        if elf[i].presents == nelves:
            # This elf has all the presents
            return i
        # take all presents from the next elf
        j = elf[i].next_elf
        elf[i].presents += elf[j].presents
        elf_unlink(elf, j)
        i = elf[i].next_elf


def winner_part2(nelves):
    # This is slow... Took 30 minutes using pypy3 on my machine.
    # Didn't find a faster way to handle the "across the circle"
    # aspect of part 2.
    elf = elf_ring(nelves)
    elist = sorted(elf)

    i = 1
    while True:
        if elf[i].presents == nelves:
            # This elf has all the presents
            return i
        # take from the elf across the circle
        j, j_idx = elf_across(elist, i)
        elf[i].presents += elf[j].presents
        del elist[j_idx]
        elf_unlink(elf, j)
        if len(elist) % 10_000 == 0:
          print(f'{len(elist)=}')
        i = elf[i].next_elf


def part1(nelves):
    return winner_part1(nelves)


def part2(nelves):
    return winner_part2(nelves)


def main():
    sample_input = 5
    main_input = 3_005_290

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
