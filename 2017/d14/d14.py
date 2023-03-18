#!/usr/bin/python3 -u

import sys
sys.path.extend(['../d10', '../../lib'])
import d10
import dirutils
import collections


def make_graph(keystring: str) -> list[list[int]]:
    """Return the list of lists per the problem rules."""
    g = []
    for i in range(128):
        bits = f"{int(d10.knot_hash(f'{keystring}-{i}'), base=16):0128b}"
        g.append([int(b) for b in bits])
    return g


def component_count(graph: list[list[int]]) -> int:
    # g is graph with every 1 changed to -1
    g = [[-x for x in y] for y in graph]
    # the problem involves a square graph; this fnc assumes it
    assert len(g) == len(g[0]) and len(set([len(x) for x in g])) == 1
    rlim = clim = len(g[0])
    component_id = 1
    for r in range(rlim):
        for c in range(clim):
            if g[r][c] == -1:
                q = collections.deque()
                q.append((r, c))
                while q:
                    r1, c1 = q.popleft()
                    g[r1][c1] = component_id
                    for dr, dc in dirutils.unitvecs:
                        r2 = r1 + dr
                        c2 = c1 + dc
                        if 0 <= r2 < rlim and 0 <= c2 < clim:
                            if g[r2][c2] == -1:
                                q.append((r2, c2))
                component_id += 1

    # return the max value in all of g
    return max([x for y in g for x in y])


def part1(keystring: str) -> int:
    used_count = 0
    for i in range(128):
        kh = d10.knot_hash(f'{keystring}-{i}')
        bits = bin(int(kh, base=16))
        used_count += bits.count('1')
    return used_count


def part2(keystring: str) -> int:
    g = make_graph(keystring)
    return component_count(g)


def main():
    for inp in ('flqrgnkx', 'uugsqrei'):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
