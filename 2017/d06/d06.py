#!/usr/bin/python3 -u

def find_inf_loop(membanks):
    """Return cycles and loop-size once inf loop is seen."""
    mb = list(membanks)
    mbl = len(mb)
    mbstate = tuple(mb)
    cycles = 0
    seen = {mbstate}
    cycle_seen = {mbstate: 0}

    while True:
        bank = mb.index(max(mb))
        redist = mb[bank]
        mb[bank] = 0
        for i in range(bank + 1, bank + 1 + redist):
            mb[i % mbl] += 1
        cycles += 1
        mbstate = tuple(mb)
        if mbstate in seen:
            return cycles, cycles - cycle_seen[mbstate]
        seen.add(mbstate)
        cycle_seen[mbstate] = cycles


def part1(membanks):
    return find_inf_loop(membanks)[0]


def part2(membanks):
    return find_inf_loop(membanks)[1]


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        membanks = tuple([int(a) for a in inp[0].split()])
        print("Part 1 answer =", part1(membanks))
        print("Part 2 answer =", part2(membanks))
        print()


if __name__ == '__main__':
    main()
