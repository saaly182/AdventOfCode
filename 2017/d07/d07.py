#!/usr/bin/python3 -u

from dataclasses import dataclass, field


@dataclass
class Program:
    name: str
    weight: int
    children: tuple[str]
    parent: str = '_NOT_SET_YET_'


def set_parents(progs):
    """Properly set all the parent fields in the progs."""
    parent_lookup = {}
    for p in progs:
        for c in p.children:
            assert c not in parent_lookup
            parent_lookup[c] = p.name
    for p in progs:
        if p.name not in parent_lookup:
            p.parent = '_ROOT_'
        else:
            p.parent = parent_lookup[p.name]


def part1(progs):
    set_parents(progs)
    root = [p.name for p in progs if p.parent == '_ROOT_']
    if len(root) != 1:
        raise ValueError(f'too many roots: {root}')
    return root[0]


def part2():
    return None


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp):
    progs = []
    for line in inp:
        a = line.split()
        name = a[0]
        weight = int(a[1][1:-1])
        children = ()
        if len(a) > 2:
            children = tuple([c.removesuffix(',') for c in a[3:]])
        progs.append(Program(name, weight, children))
    return tuple(progs)


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        progs = parse(inp)
        print("Part 1 answer =", part1(progs))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
