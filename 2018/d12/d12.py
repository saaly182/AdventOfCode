#!/usr/bin/python3 -u

from collections import defaultdict
from typing import DefaultDict, Tuple


def next_generation(pots: tuple, zero_cell: int,
                    rules: DefaultDict) -> Tuple[tuple, int]:
    """Return the next generation."""
    boundary = ('.',) * 2
    max_boundary_dots = ('.',) * 5
    prefix = pots[:5]
    suffix = pots[-5:]
    if prefix != max_boundary_dots:
        pots = boundary + pots
        zero_cell += 2
    if suffix != max_boundary_dots:
        pots = pots + boundary

    pots2 = list(boundary)
    for i in range(2, len(pots) - 2):
        pattern = ''.join(pots[i - 2:i + 3])
        pots2.append(rules[pattern])
    pots = tuple(pots2) + boundary

    return pots, zero_cell


def answer(pots: tuple, zero_cell: int, offset=0) -> int:
    a = 0
    for i, p in enumerate(pots):
        if p == '#':
            a += i - zero_cell + offset
    return a


def part1(pots: tuple, rules: DefaultDict) -> int:
    zero_cell = 2
    for generation in range(20):
        pots, zero_cell = next_generation(pots, zero_cell, rules)
    return answer(pots, zero_cell)


def gliding(p1: tuple, p2: tuple) -> bool:
    """Return True when the pots tuples have the same 'shape'."""
    s1 = ''.join(p1)
    s1 = s1[s1.index('#'):s1.rindex('#') + 1]
    s2 = ''.join(p2)
    s2 = s2[s2.index('#'):s2.rindex('#') + 1]
    return s1 == s2


def part2(pots: tuple, rules: DefaultDict) -> int:
    """
    Letting part 1 run for more generations, one can see that these inputs
    create "gliders", like in Conway's game of life. In my input cases, the
    gliders even keep a constant pattern/shape. So we just need to evolve until
    the glider starts, and then figure out where it'll be at the 50e9
    generation.
    """
    zero_cell = 2
    generation = 0
    generation_goal = 50_000_000_000
    while True:
        generation += 1
        pots2, zero_cell2 = next_generation(pots, zero_cell, rules)
        if gliding(pots, pots2):
            break
        else:
            pots, zero_cell = pots2, zero_cell2

    # when we reach here, we have a glider moving to the right
    assert zero_cell == zero_cell2
    velocity = pots2.index('#') - pots.index('#')
    pots = pots2
    offset = (generation_goal - generation) * velocity
    return answer(pots, zero_cell, offset)


def slurp(fname: str) -> list[str]:
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp: list) -> tuple[tuple, DefaultDict]:
    pots = tuple(['.', '.'] + list(inp[0].removeprefix('initial state: ')) +
                 ['.', '.'])

    rules = defaultdict(lambda: '.')
    for line in inp[2:]:
        a, b = line.split(' => ')
        rules[a] = b

    return pots, rules


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        pots, rules = parse(inp)
        print("Part 1 answer =", part1(pots, rules))
        print("Part 2 answer =", part2(pots, rules))
        print()


if __name__ == '__main__':
    main()
