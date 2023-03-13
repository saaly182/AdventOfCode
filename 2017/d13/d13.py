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


def is_caught(firewall: dict[int, int], delay: int) -> bool:
    """Return True if the firewall would catch this attempt with given delay."""
    maxdepth = max(firewall)
    for t in range(delay, maxdepth + delay + 1):
        layer = t - delay
        if layer in firewall:
            srange = firewall[layer]
            if scanner_pos(srange, t) == 0:
                return True  # caught by this layer
    return False


def part1(firewall: dict[int, int]) -> int:
    return severity(firewall)


def part2(firewall: dict[int, int]) -> int:
    # Just gonna brute-force this
    delay = 0
    while is_caught(firewall, delay):
        delay += 1
    return delay


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
        print("Part 2 answer =", part2(firewall))
        print()


if __name__ == '__main__':
    main()
