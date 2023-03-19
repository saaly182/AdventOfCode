#!/usr/bin/python3 -u

import collections


def make_cbuf(step_size: int, lastval: int) -> collections.deque[int]:
    # Totally had to get the hint from reddit that deque.rotate() is the key
    # to making this work. See my brute-force attempt in the prev commit to
    # this code.
    cbuf = collections.deque([0])
    for i in range(1, lastval + 1):
        cbuf.rotate(-step_size)
        cbuf.append(i)
    return cbuf


def part1(step_size: int) -> int:
    lastval = 2017
    cbuf = make_cbuf(step_size, lastval)
    idx = (cbuf.index(lastval) + 1) % len(cbuf)
    return cbuf[idx]


def part2(step_size: int) -> int:
    lastval = 50_000_000
    cbuf = make_cbuf(step_size, lastval)
    idx = (cbuf.index(0) + 1) % len(cbuf)
    return cbuf[idx]


def slurp(fname: str) -> list[str]:
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    for inp in (3, 366):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
