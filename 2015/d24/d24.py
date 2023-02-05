#!/usr/bin/python3 -u

# ref: https://en.wikipedia.org/wiki/Multiway_number_partitioning

import functools
import itertools
import math


def tupsub(a, b):
    """Return tuple_a - tuple_b."""
    al = list(a)
    bl = list(b)
    for v in bl:
        if v in al:
            al.remove(v)
    return tuple(al)


# https://en.wikipedia.org/wiki/Partition_problem
# https://www.geeksforgeeks.org/partition-problem-dp-18/
# recursive
@functools.cache
def can_partition(arr, n, tsum):
    # tsum is the "target sum"
    if tsum == 0:
        return True
    if n == 0:
        return False
    if arr[n - 1] > tsum:
        # if an individual elem is > tsum, must be False
        return False
    return (can_partition(arr, n - 1, tsum) or
            can_partition(arr, n - 1, tsum - arr[n - 1]))


def part1(weights):
    wsum = sum(weights)
    if wsum % 3 != 0:
        raise ValueError('cannot divide into three groups')
    gw = wsum // 3  # group weight

    qe = []  # quantum entanglements
    for g1size in range(1, len(weights) - 1):
        if qe:
            break  # no need to search larger g1's
        for g1 in itertools.combinations(weights, g1size):
            if sum(g1) != gw:
                continue
            # Now we're down to the classic Partition Problem with the
            # remaining weights.
            weights_left = tupsub(weights, g1)
            wlsum = sum(weights_left)
            if wlsum % 2 != 0:
                continue
            if can_partition(weights_left, len(weights_left), wlsum // 2):
                qe.append(math.prod(g1))

    return min(qe) if qe else None


def part2():
    return None


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        weights = tuple(int(x) for x in inp)
        print("Part 1 answer =", part1(weights))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
