#!/usr/bin/python3 -u

import itertools


def part1dynprog(buckets, liters):
    # The optimal substructure here is that if you know how many combinations
    # of the previous numbers summed to each value, up to the target value,
    # you just have to consider which values the current number can "reach".
    # The initial sub-problem answer is that there is only one way to sum to 0.
    #
    # I suspected there'd be a DP way to solve this, but I was unlikely to
    # work it out on my own. So credit to the following that I had to
    # scrutinize a lot:
    # https://www.reddit.com/r/adventofcode/comments/3x6cyr/comment/cy1xlvq
    cmbs = [1] + [0] * liters
    for b1 in buckets:
        for b2 in range(liters, b1 - 1, -1):
            cmbs[b2] += cmbs[b2 - b1]
    return cmbs[liters]


def part1brute(buckets, liters):
    combcount = 0
    for i in range(1, len(buckets) + 1):
        for b in itertools.combinations(buckets, i):
            if sum(b) == liters:
                combcount += 1
    return combcount


def part2(buckets, liters):
    # Just gonna stick with brute force for this.
    for i in range(1, len(buckets) + 1):
        count = 0
        for b in itertools.combinations(buckets, i):
            if sum(b) == liters:
                count += 1
        if count:
            return count
    return None


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    main_input = slurp('input/input.txt')

    for inp in (main_input, ):
        buckets = tuple(int(b) for b in inp)
        print("Part 1 (brute force) answer =", part1brute(buckets, 150))
        print("Part 1 (dynamic programming) answer =",
              part1dynprog(buckets, 150))
        print("Part 2 answer =", part2(buckets, 150))
        print()


if __name__ == '__main__':
    main()
