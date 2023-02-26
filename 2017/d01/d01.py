#!/usr/bin/python3 -u

def part1(seqstr):
    seq = [int(a) for a in seqstr] + [int(seqstr[0])]
    return sum([a for idx, a in enumerate(seq[:-1]) if a == seq[idx + 1]])


def part2(seqstr):
    seq = [int(a) for a in seqstr]
    ls = len(seq)
    half_offset = ls // 2
    sm = 0  # sum
    for idx, i in enumerate(seq):
        half_idx = (idx + half_offset) % ls
        if i == seq[half_idx]:
            sm += i
    return sm


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp[0]))
        print("Part 2 answer =", part2(inp[0]))
        print()


if __name__ == '__main__':
    main()
