#!/usr/bin/python3 -u

import sys
sys.path.append('../../lib')
import aocutils  # noqa: E402


def merge_adjacent_intervals(ilist):
    """
    Return a list of intervals with adjacent ones merged.
    Input list must be sorted and non-overlapping. Needed because
    aocutils.merge_intervals only merges _overlapping_ intervals, but for this
    problem, we need to concat adjacent intervals too.
    """
    intervals = []
    i1 = ilist[0]
    i2 = None
    for i2 in ilist[1:]:
        if i1[1] + 1 == i2[0]:
            i1[1] = i2[1]
        else:
            intervals.append(i1)
            i1 = i2
    if i1[1] == i2[1]:
        intervals.append(i1)
    else:
        intervals.append(i2)

    return intervals


def part1(denylist):
    max_ip = 2 ** 32 - 1
    intervals = merge_adjacent_intervals(aocutils.merge_intervals(denylist))
    if intervals[0][0] > 0:
        min_unblocked_ip = 0
    else:
        min_unblocked_ip = min(intervals[0][1] + 1, max_ip)
    return min_unblocked_ip


def part2(denylist):
    max_ip = 2 ** 32 - 1
    intervals = merge_adjacent_intervals(aocutils.merge_intervals(denylist))
    ip_count = 0  # number of allowed ips
    for n in range(len(intervals)):
        if n == 0:
            ip_count += intervals[0][0] - 0
        else:
            ip_count += intervals[n][0] - intervals[n - 1][1] - 1
    ip_count += max_ip - intervals[-1][1]

    return ip_count


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp):
    denylist = []
    for line in inp:
        a, b = line.split('-')
        denylist.append([int(a), int(b)])
    return denylist


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        denylist = parse(inp)
        print("Part 1 answer =", part1(denylist))
        print("Part 2 answer =", part2(denylist))
        print()


if __name__ == '__main__':
    main()
