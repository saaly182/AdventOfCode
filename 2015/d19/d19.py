#!/usr/bin/python3 -u

import collections
import re


def atomize(molecule):
    return tuple(re.findall(r'[A-Z][a-z]?', molecule))


def part1(replacements, molecule):
    new_molecules = set()
    atoms = atomize(molecule)
    for i, atom in enumerate(atoms):
        nm = list(atoms)
        for new_atom in replacements[atom]:
            nm[i] = new_atom
            new_molecules.add(''.join(nm))
    return len(new_molecules)


def part2():
    return None


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
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
