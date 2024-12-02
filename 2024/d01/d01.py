#!/usr/bin/python3 -u

import collections


def part1(t1: tuple, t2: tuple) -> int:
    answer = sum([abs(x[0] - x[1]) for x in
                  zip(sorted(t1), sorted(t2), strict=True)])
    return answer


def part2(left: tuple, right: tuple) -> int:
    right_counts = collections.defaultdict(int)
    similarity_score = 0

    for n in right:
        right_counts[n] += 1
    for n in left:
        if n in right_counts:
            similarity_score += n * right_counts[n]

    return similarity_score


def slurp(fname: str) -> tuple:
    list1 = []
    list2 = []
    with open(fname) as file:
        for line in file.readlines():
            n1, n2 = line.rstrip().split()
            list1.append(int(n1))
            list2.append(int(n2))
    return tuple(list1), tuple(list2)


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp[0], inp[1]))
        print("Part 2 answer =", part2(inp[0], inp[1]))
        print()


if __name__ == '__main__':
    main()
