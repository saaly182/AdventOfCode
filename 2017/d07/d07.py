#!/usr/bin/python3 -u

from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Program:
    name: str
    weight: int
    children: tuple
    parent: str = '_NOT_SET_YET_'


def set_parents(progs):
    """Properly set all the parent fields in the progs."""
    parent_lookup = {}
    for p in progs.values():
        for c in p.children:
            assert c not in parent_lookup
            parent_lookup[c] = p.name
    for p in progs.values():
        if p.name not in parent_lookup:
            p.parent = '_ROOT_'
        else:
            p.parent = parent_lookup[p.name]


def tower_weight(progs, name):
    """Return the total tower weight rooted at name."""
    # Ideally this would be memoized, but it takes a dict as input
    # which cannot be hashed. This is pretty cheap to compute, so not worrying
    # about it for now.
    p = progs[name]
    tw = p.weight
    for c in p.children:
        tw += tower_weight(progs, c)
    return tw


def part1(progs):
    root = [name for name in progs if progs[name].parent == '_ROOT_']
    if len(root) != 1:
        raise ValueError(f'too many roots: {root}')
    return root[0]


def youngest(progs, nodes):
    for n in nodes:
        found = False
        for c in progs[n].children:
            if c in nodes:
                found = True
                break
        if not found:
            return n
    assert False  # should not get here


def new_weight(progs):
    """Return the new weight of the disc that needs adjustment to balance.
    Determine all the towers that are unbalanced. Since there's only one
    weight change needed, per the problem statement, the unbalanced towers
    will all be in the same parent-child chain. The "youngest" child is the
    one that needs a tower adjustment.
    """
    unbalanced = set()
    tws = {}  # tower weights
    for name, p in progs.items():
        if p.children:
            cwlist = []
            for c in p.children:
                tw = tower_weight(progs, c)
                tws[c] = tw
                cwlist.append(tw)
            if len(set(cwlist)) != 1:
                unbalanced.add(name)

    node = youngest(progs, unbalanced)
    # Now we know that one of node's child towers has a bad weight.
    # (This section is a mess...)
    wcounts = defaultdict(int)
    wtowers = defaultdict(list)
    for c in progs[node].children:
        wcounts[tws[c]] += 1
        wtowers[tws[c]].append(c)
    assert len(wcounts) == 2
    good_weight = bad_weight = -1
    for w, count in wcounts.items():
        if count == 1:
            bad_weight = w
        else:
            good_weight = w

    prog_to_fix = wtowers[bad_weight][0]

    return progs[prog_to_fix].weight + (good_weight - bad_weight)


def part2(progs):
    return new_weight(progs)


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp):
    progs = {}
    for line in inp:
        a = line.split()
        name = a[0]
        weight = int(a[1][1:-1])
        children = ()
        if len(a) > 2:
            children = tuple([c.removesuffix(',') for c in a[3:]])
        progs[name] = (Program(name, weight, children))
    set_parents(progs)
    return progs


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        progs = parse(inp)
        print("Part 1 answer =", part1(progs))
        print("Part 2 answer =", part2(progs))
        print()


if __name__ == '__main__':
    main()
