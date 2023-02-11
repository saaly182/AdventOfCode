#!/usr/bin/python3 -u

import collections


def part1(inp):
    # This approach may not be the most efficient
    cols = len(inp[0])
    charcounts = [collections.defaultdict(int) for _ in range(cols)]
    for msg in inp:
        if len(msg) != cols:
            raise ValueError(f"incorrect msg length: {msg}")
        for col, char in enumerate(msg):
            charcounts[col][char] += 1

    realmsg = []
    for col in range(cols):
        maxfreq = max(charcounts[col].values())
        char = [c for c in charcounts[col] if charcounts[col][c] == maxfreq]
        if len(char) != 1:
            raise ValueError(f"multiple chars have max freq {char}")
        realmsg.append(char[0])

    return ''.join(realmsg)


def part2():
    return None


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
