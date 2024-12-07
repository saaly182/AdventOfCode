#!/usr/bin/python3 -u

import collections
import functools
import graphlib
import re


@functools.cache
def classify_pagelists(rules: tuple, pagelists: tuple) -> tuple:
    """
    Return a tuple of 2-tuples where the 2-tuples are:
    (pagelist, broken-rules)
    """
    results = []

    for pages in pagelists:
        pset = set(pages)
        # code assumes no dups in each list of pages
        assert len(pages) == len(pset)

        # create hash of indexes for this particular pagelist
        pidx = dict([(b, a) for a, b in enumerate(pages)])

        prules = []  # rules specific to these pages
        broken_rules = []
        for r in rules:
            if r[0] in pset and r[1] in pset:
                prules.append(r)

        for r in prules:
            if pidx[r[0]] > pidx[r[1]]:
                broken_rules.append(r)

        results.append((pages, tuple(broken_rules)))

    return tuple(results)


def part1(rules: tuple, pagelists: tuple) -> int:
    middles_sum = 0
    for pages, br in classify_pagelists(rules, pagelists):
        if not br:  # if no broken rules
            assert len(pages) % 2 == 1
            middle = pages[len(pages) // 2]  # don't forget: zero-based indexes
            middles_sum += middle
    return middles_sum


def part2(rules: tuple, pagelists: tuple) -> int:
    middles_sum = 0
    for pages, br in classify_pagelists(rules, pagelists):
        if not br:
            # ignore pagelists that are already correctly ordered
            continue

        # topo sort this pagelist using only the applicable rules
        pset = set(pages)
        graph = collections.defaultdict(set)
        for r in rules:
            if r[0] in pset and r[1] in pset:
                graph[r[1]].add(r[0])
        ts = graphlib.TopologicalSorter(graph)
        fixed_pages = tuple(ts.static_order())

        assert len(fixed_pages) % 2 == 1
        middle = fixed_pages[len(fixed_pages) // 2]
        middles_sum += middle
    return middles_sum


def slurp(fname: str) -> tuple[str, ...]:
    with open(fname) as file:
        return tuple(line.rstrip() for line in file.readlines())


def parse_input(lines: tuple[str, ...]) -> tuple:
    rules = []
    pagelists = []
    for line in lines:
        if m := re.fullmatch(r'(\d+)\|(\d+)', line):
            rules.append((int(m.group(1)), int(m.group(2))))
        elif re.fullmatch(r'\d+(,\d+)*', line):
            pagelists.append(tuple(int(x) for x in line.split(',')))
        elif not line:
            pass
        else:
            raise ValueError(f'bad input: {line}')
    return tuple(rules), tuple(pagelists)


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        rules, pagelists = parse_input(inp)
        print("Part 1 answer =", part1(rules, pagelists))
        print("Part 2 answer =", part2(rules, pagelists))
        print()


if __name__ == '__main__':
    main()
