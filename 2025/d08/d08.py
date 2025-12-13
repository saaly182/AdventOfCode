#!/usr/bin/python3 -u

import collections
import itertools
import math


class Graph:
    def __init__(self, points: tuple[tuple[int, int, int]]) -> None:
        self.vertices = set(points)
        self.edges = set()
        self.dist2pairs = self._compute_dists()

    def _compute_dists(self) -> collections.defaultdict:
        d2 = collections.defaultdict(list)
        for a, b in itertools.combinations(self.vertices, 2):
            d_squared = ((a[0] - b[0]) ** 2 +
                         (a[1] - b[1]) ** 2 +
                         (a[2] - b[2]) ** 2)
            d2[d_squared].append((a, b))
        return d2

    def add_edge(self, v1: tuple[int, int, int],
                 v2: tuple[int, int, int]) -> None:
        if v1 not in self.vertices:
            raise ValueError(f'{v1} not in graph')
        if v2 not in self.vertices:
            raise ValueError(f'{v2} not in graph')
        self.edges.add((v1, v2))

    def connected_components(self) -> tuple:
        # Possible improvement: keeps ccs updated as each edge is added
        # instead of recomputing for each call
        ccs = collections.defaultdict(set)

        for v in self.vertices:
            ccs[v].add(v)

        # brute force
        for v1, v2 in self.edges:
            for v in ccs:
                if v1 in ccs[v]:
                    ccs[v].update(ccs[v2])
                if v2 in ccs[v]:
                    ccs[v].update(ccs[v1])

        return tuple(set([tuple(sorted(cc)) for cc in ccs.values()]))


def part1(points: tuple) -> int:
    g = Graph(points)
    conn_count = 0
    done = False
    for d2 in sorted(g.dist2pairs):
        for a, b in g.dist2pairs[d2]:
            g.add_edge(a, b)
            conn_count += 1
            if conn_count == 1000:
                done = True
                break
        if done:
            break

    circuit_lengths = sorted([len(c) for c in g.connected_components()])

    return math.prod(circuit_lengths[-3:])


def part2() -> int:
    return -99


def parse_input(fname: str) -> tuple[tuple, ...]:
    with open(fname) as file:
        points = tuple(tuple(map(int, line.rstrip().split(','))) for
                       line in file)
    return points


def main():
    sample_input = parse_input('input/sample_input.txt')
    main_input = parse_input('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
