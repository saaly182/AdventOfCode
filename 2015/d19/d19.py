#!/usr/bin/python3 -u

import collections
import re


def atomize(molecule):
    if molecule == 'e':
        return 'e',
    return tuple(re.findall(r'[A-Z][a-z]?', molecule))


def part1(replacements, molecule):
    return len(list(fabricate(replacements, molecule)))


def fabricate(replacements, m):
    """Yield all the distinct molecules than can be fabricated from m."""
    seen_molecules = set()
    atoms = atomize(m)
    for i, atom in enumerate(atoms):
        nmas = list(atoms)  # new molecule atoms
        for new_atom in replacements[atom]:
            nmas[i] = new_atom
            nm = ''.join(nmas)
            if nm not in seen_molecules:
                seen_molecules.add(nm)
                yield nm


def greedy_reduce(replacements, molecule):
    # I initially tried BFS for this, but suspected it would blow up given
    # the branching factor shown from part 1. Eventually had to read some
    # reddit posts to get hints. Learned that the input is actually crafted
    # to only have one possible "fabrication" from 'e'. Looks like the
    # general problem would require complex enough algorithms that I'm not
    # willing to dig into right now. Some folks mentioned the CYK algorithm.
    # Anyway, I'm just going with a greedy reduction from molecule->e.
    steps = 0
    reductions = {}
    for atom, ms in replacements.items():
        for m in ms:
            assert m not in reductions  # for this input, no overlaps
            reductions[m] = atom
    # now just repeatedly make the largest reduction until we get to 'e'
    target = molecule
    ms = sorted(reductions, key=len, reverse=True)
    while target != 'e':
        for m in ms:
            if target.find(m) != -1:
                target = target.replace(m, reductions[m], 1)
                steps += 1
                break
    return steps


def part2(replacements, molecule):
    return greedy_reduce(replacements, molecule)


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp):
    replacements = collections.defaultdict(list)
    molecule = None
    for line in inp:
        if line.find('=>') != -1:
            a, _, b = line.split()
            replacements[a].append(b)
        elif line.isalnum():
            molecule = line
    assert replacements and molecule
    return replacements, molecule


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        replacements, molecule = parse(inp)
        print("Part 1 answer =", part1(replacements, molecule))
        print("Part 2 answer =", part2(replacements, molecule))
        print()


if __name__ == '__main__':
    main()
