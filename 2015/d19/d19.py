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


def bfs(replacements, molecule):
    """Return the number of steps to go from e to molecule."""
    seen_molecules = {'e'}
    q = [('e', 0)]
    curstep = 0
    while q:
        m, step = q.pop(0)
        if step > curstep:
            print(f'{step=} {len(q)=} {m=}')
            curstep = step
        if m == molecule:
            return step
        for next_m in fabricate(replacements, m):
            if next_m not in seen_molecules:
                seen_molecules.add(next_m)
                q.append((next_m, step + 1))
    assert False  # should never get here


def part2(replacements, molecule):
    return bfs(replacements, molecule)


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
