#!/usr/bin/python3 -u

import sys
sys.path.append('../../lib')
import dirutils  # noqa: E402 F401

# See:
# https://projecteuler.net/problem=58
# https://en.wikipedia.org/wiki/Ulam_spiral
# The lower-right diagonal is the odd squares.
# 17  16  15  14  13
# 18   5   4   3  12
# 19   6   1   2  11
# 20   7   8   9  10
# 21  22  23  24  25


def odd_squares():
    i = 1
    while True:
        yield i, i * i
        i += 2


def ulam_coords(n):
    """Return the x, y coords of n on the Ulam spiral."""
    if n < 1:
        raise ValueError(f'value must be > 0; {n=}')

    if n == 1:
        return 0, 0

    odd = oddsq = None
    for odd, oddsq in odd_squares():
        if oddsq >= n:
            break

    # n is on oddsq's square ring
    sqlen = odd
    bound = (odd - 1) // 2

    se_corner = oddsq
    sw_corner = se_corner - sqlen + 1
    nw_corner = sw_corner - sqlen + 1
    ne_corner = nw_corner - sqlen + 1
    last_pt = ne_corner - sqlen + 2

    if n in range(sw_corner, se_corner + 1):
        x = -bound + n - sw_corner
        y = -bound
    elif n in range(nw_corner, sw_corner):
        x = -bound
        y = bound - n + nw_corner
    elif n in range(ne_corner, nw_corner):
        x = bound - n + ne_corner
        y = bound
    elif n in range(last_pt, ne_corner):
        x = bound
        y = -bound + 1 + n - last_pt
    else:
        print(f'n should have been in ranges above: {n}')
        assert False  # should never get here

    return x, y


def part1(n):
    x, y = ulam_coords(n)
    return abs(x) + abs(y)


def part2(limit):
    cells = {(0, 0): 1}
    n = 2
    while True:
        x, y = ulam_coords(n)
        sm = 0
        for dx, dy in dirutils.neighbors:
            nx, ny = x + dx, y + dy
            if (nx, ny) in cells:
                sm += cells[(nx, ny)]
        cells[(x, y)] = sm
        if sm > limit:
            return sm
        n += 1


def main():
    for inp in (12, 277678):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
