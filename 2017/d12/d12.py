#!/usr/bin/python3 -u

import itertools


def connected_components(graph: dict) -> set[tuple, ...]:
    """Return all connected components of the graph."""
    ccs = set()

    # create the initial set of components from the graph
    for node in graph:
        this_cc = (node,) + graph[node]
        ccs.add(this_cc)

    # now keep combining components until no more is possible
    # warning: this is slow
    while True:
        did_merge = False
        for c1, c2 in itertools.combinations(ccs, 2):
            c1s = set(c1)
            c2s = set(c2)
            if not c1s.isdisjoint(c2s):
                c1s.update(c2s)
                ccs.remove(c1)
                ccs.remove(c2)
                ccs.add(tuple(c1s))
                did_merge = True
                break  # need to break b/c we've modified ccs
        if not did_merge:
            break  # we're done, no more merging is possible

    return ccs


def part1(ccs: set[tuple, ...]) -> int | None:
    for cc in ccs:
        if 0 in cc:
            return len(cc)
    return None  # will only get here if 0 is not in the input


def part2(ccs: set[tuple, ...]) -> int:
    return len(ccs)


def slurp(fname: str) -> list[str]:
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def make_graph(inp: list[str]) -> dict:
    g = {}
    for line in inp:
        tok = line.split()
        node = int(tok[0])
        adj_neighbors = [int(x.removesuffix(',')) for x in tok[2:]]
        if node in g:
            raise ValueError(f'duplicate adj info found for node {node}')
        g[node] = tuple(adj_neighbors)
    return g


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        graph = make_graph(inp)
        ccs = connected_components(graph)
        print("Part 1 answer =", part1(ccs))
        print("Part 2 answer =", part2(ccs))
        print()


if __name__ == '__main__':
    main()
