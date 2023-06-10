#!/usr/bin/python3 -u

from collections import defaultdict
from typing import DefaultDict, NamedTuple
import re


class Claim(NamedTuple):
    id: int
    c0: int
    r0: int
    width: int
    height: int


def mark_fabric(claims: tuple) -> DefaultDict[tuple, set]:
    fabric = defaultdict(set)
    for claim in claims:
        for r in range(claim.r0, claim.r0 + claim.height):
            for c in range(claim.c0, claim.c0 + claim.width):
                fabric[(r, c)].add(claim.id)
    return fabric


def part1(fabric: DefaultDict[tuple, set]) -> int:
    return sum([1 for cell, claim_ids in fabric.items() if len(claim_ids) > 1])


def part2(fabric: DefaultDict[tuple, set]) -> int:
    # Start by marking all claims as non-overlapping, and then remove the ones
    # determined to actually be overlapping.
    nonoverlap_claims = {cid for cids in fabric.values() for cid in cids}
    for cell, claim_ids in fabric.items():
        if len(claim_ids) > 1:
            nonoverlap_claims.difference_update(claim_ids)
    assert len(nonoverlap_claims) == 1
    answer_claim, = nonoverlap_claims
    return answer_claim


def slurp(fname: str) -> list[str]:
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp: list) -> tuple:
    # example: #27 @ 928,149: 14x25
    claims = []
    pattern = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')
    for line in inp:
        if mo := pattern.fullmatch(line):
            claims.append(Claim(*[int(x) for x in mo.groups()]))
        else:
            raise ValueError(f'bad input: {line}')
    return tuple(claims)


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        claims = parse(inp)
        fabric = mark_fabric(claims)
        print("Part 1 answer =", part1(fabric))
        print("Part 2 answer =", part2(fabric))
        print()


if __name__ == '__main__':
    main()
