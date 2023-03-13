#!/usr/bin/python3 -u

def scanner_pos(srange: int, t: int) -> int:
    cycle_time = 2 * srange - 2
    tc = t % cycle_time
    if tc < srange:
        spos = tc
    else:
        spos = cycle_time - tc
    return spos


def severity(firewall: dict[int, int]) -> int:
    maxdepth = max(firewall)
    sev = 0

    for t in range(maxdepth + 1):
        layer = t
        if layer in firewall:
            srange = firewall[layer]
            if scanner_pos(srange, t) == 0:
                sev += layer * srange

    return sev


def part1(firewall: dict[int, int]) -> int:
    return severity(firewall)


def part2():
    return None


def slurp(fname: str) -> list[str]:
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp: list[str]) -> dict[int, int]:
    firewall = {}
    for line in inp:
        d, r = line.split(': ')
        firewall[int(d)] = int(r)
    return firewall


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        firewall = parse(inp)
        print("Part 1 answer =", part1(firewall))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
