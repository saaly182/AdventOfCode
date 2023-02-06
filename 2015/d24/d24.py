#!/usr/bin/python3 -u

# FYI, pypy3 ran in 1/12th the time of python3 for this.

import itertools
import math


def tuple_subtract(a, b):
    """Like set subtraction, but for tuples. Basically multiset subtraction."""
    al = list(a)
    bl = list(b)
    for v in bl:
        if v in al:
            al.remove(v)
    return tuple(al)


# https://en.wikipedia.org/wiki/Partition_problem
# https://www.geeksforgeeks.org/partition-problem-dp-18/
# NOTE: This could use @functools.cache, but it blows up memory for part2.
def can_partition(arr, n, tsum):
    # tsum is the "target sum"
    if tsum == 0:
        return True
    if n == 0:
        return False
    if arr[n - 1] > tsum:
        # if an individual elem is > tsum, no soln can exist
        return False
    return (can_partition(arr, n - 1, tsum) or
            can_partition(arr, n - 1, tsum - arr[n - 1]))


def weight_groups(weights, size, tsum):
    """Generate subgroups of the given size that sum to the target sum."""
    for wg in itertools.combinations(weights, size):
        if sum(wg) == tsum:
            yield wg


def part1(weights):
    wsum = sum(weights)
    if wsum % 3 != 0:
        raise ValueError(f'cannot divide into three equal-weight groups')
    gw = wsum // 3  # group weight

    qe = []  # quantum entanglements
    for g1size in range(1, len(weights) - 1):
        if qe:
            break  # no need to search larger g1's
        for g1 in weight_groups(weights, g1size, gw):
            # Now we're down to the classic Partition Problem with the
            # remaining weights.
            weights_left = tuple_subtract(weights, g1)
            if can_partition(weights_left, len(weights_left), gw):
                qe.append(math.prod(g1))

    return min(qe) if qe else None


def part2(weights):
    # NOTE: I'm intentionally not trying to refactor the code to avoid DRY
    # between part1 and part2. Going for minimized effort on this one for now.
    # TODO: consider refactoring to combine part1 and part2.
    # ref: https://en.wikipedia.org/wiki/Multiway_number_partitioning
    wsum = sum(weights)
    if wsum % 4 != 0:
        raise ValueError(f'cannot divide into four equal-weight groups')
    gw = wsum // 4  # group weight

    qe = []  # quantum entanglements
    for g1size in range(1, len(weights) - 2):
        if qe:
            break  # no need to search larger g1's
        for g1 in weight_groups(weights, g1size, gw):
            weights_left1 = tuple_subtract(weights, g1)
            for g2size in range(1, len(weights_left1) - 1):
                for g2 in weight_groups(weights_left1, g2size, gw):
                    # Now we're down to the classic Partition Problem with the
                    # remaining weights.
                    weights_left2 = tuple_subtract(weights_left1, g2)
                    if can_partition(weights_left2, len(weights_left2), gw):
                        qe.append(math.prod(g1))

    return min(qe) if qe else None


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        weights = tuple(int(x) for x in inp)
        print("Part 1 answer =", part1(weights))
        print("Part 2 answer =", part2(weights))
        print()


if __name__ == '__main__':
    main()
