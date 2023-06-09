#!/usr/bin/python3 -u

from collections import defaultdict
import itertools


def part1(words: list[str]) -> int:
    exactly2 = exactly3 = 0
    for word in words:
        letterfreq = defaultdict(int)
        for c in word:
            letterfreq[c] += 1
        freq_set = set(letterfreq.values())
        if 2 in freq_set:
            exactly2 += 1
        if 3 in freq_set:
            exactly3 += 1

    return exactly2 * exactly3


def part2(words: list[str]) -> str | None:
    for w1, w2 in itertools.combinations(words, 2):
        diffcount = 0
        diffpos = None
        for pos, (c1, c2) in enumerate(zip(w1, w2, strict=True)):
            if c1 != c2:
                diffcount += 1
                diffpos = pos
            if diffcount > 1:
                break
        if diffcount == 1:
            return w1[:diffpos] + w1[diffpos + 1:]
    return None


def slurp(fname: str) -> list[str]:
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    main_input = slurp('input/input.txt')

    for inp in (main_input, ):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
