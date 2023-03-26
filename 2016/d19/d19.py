#!/usr/bin/python3 -u

import collections


def part1(nelves):
    """Return the number of the elf that ends up with everything.

    Use the analytical solution described in detail at
    https://www.youtube.com/watch?v=uCsD3ZGzMgE
    Video title = "The Josephus Problem - Numberphile"
    """
    p2 = 1  # powers of two
    while p2 <= nelves:
        p2 *= 2
    p2 //= 2
    b = nelves - p2
    return 2 * b + 1


def part2(nelves):
    """Return the number of the elf that ends up with everything.

    My attempt at this was brute force with a doubly-linked list
    and took 30m to run. Eventually returned to this problem and
    researched other people's approaches. Settled on the scheme
    described at
    https://www.reddit.com/r/adventofcode/comments/5j4lp1/comment/dbdnz4l
    This keeps the circle as two balanced deques so that it's always cheap and
    easy to handle the position "across" the circle.

      1
    5   2
     4 3

    In the example above, right starts as [1,2] and left as [3,4,5].
    """
    right = collections.deque(range(1, nelves // 2 + 1))
    left = collections.deque(range(nelves // 2 + 1, nelves + 1))

    while right:
        # head of right eliminates head of left
        left.popleft()
        # keep sides balanced
        if len(left) == len(right):
            right.append(left.popleft())
        # head of right now goes to tail of left
        left.append(right.popleft())

    return left[0]


def main():
    sample_input = 5
    main_input = 3_005_290

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
