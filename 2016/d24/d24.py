#!/usr/bin/python3 -u

import sys
sys.path.append('../../lib')
import aocutils
import dirutils
import itertools
import re


def loc_graph(fullgraph, location):
    """Return the distance graph of just the named nodes."""
    G = {}

    for loc_id_src, loc_src in location.items():
        d, p = aocutils.shortest_paths(fullgraph, loc_src)
        for loc_id_dst, loc_dst in location.items():
            G[(loc_id_src, loc_id_dst)] = d[loc_dst]

    return G


def TSP(G, return_home=False):
    """Return the minimum traveling-salesperson-problem distance."""
    min_dist = float('inf')
    nodes = set([a for pair in G.keys() for a in pair])
    nodes.remove(0)  # we are constrained to start from node 0
    for path in itertools.permutations(nodes):
        path = (0,) + path
        if return_home:
            path = path + (0,)
        dist = 0
        for pair in itertools.pairwise(path):
            dist += G[pair]
        min_dist = dist if dist < min_dist else min_dist

    return min_dist


def part1(full_graph, location):
    graph = loc_graph(full_graph, location)
    return TSP(graph)


def part2(full_graph, location):
    graph = loc_graph(full_graph, location)
    return TSP(graph, return_home=True)


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp):
    G = {}
    location = {}
    dist = 1

    for r, row in enumerate(inp):
        for c, cell in enumerate(row):
            if cell != '#':
                adj = []
                for uv in dirutils.unitvecs:
                    neighbor = r + uv[0], c + uv[1]
                    if inp[neighbor[0]][neighbor[1]] != '#':
                        adj.append((neighbor, dist))
                G[(r, c)] = tuple(adj)
            if mo := re.fullmatch(r'(\d+)', cell):
                location[int(mo.group(1))] = (r, c)
    return G, location


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        full_graph, location = parse(inp)
        print("Part 1 answer =", part1(full_graph, location))
        print("Part 2 answer =", part2(full_graph, location))
        print()


if __name__ == '__main__':
    main()
