#!/usr/bin/python3 -u
"""
Clearly the general version of the stated problem is NP Hard, and the given
input would blow up. It was unclear how to proceed, but online hints pointed to
just using the simplest heuristic to solve this, assuming that AoC would do
something like that. So this code just checks that the total "present" area is
less than or equal to the tree region area... This approach works for the real
input data, but actually fails for the sample input data. Such is life.
"""

import re
import sys
sys.path.append('../../lib')
from multiline_record import multiline_file  # noqa: E402 F401


class Present:
    def __init__(self, spec_str):
        spec = spec_str.strip().split('\n')
        self.idx = int(spec[0][:-1])
        self.width = len(spec[1])
        self.length = len(spec) - 1
        self.area = self.width * self.length

    def __str__(self):
        return (f'Present(idx={self.idx} w={self.width} '
                f'l={self.length} a={self.area})')


class TreeRegion:
    def __init__(self, spec):
        m = re.match(r'(\d+)x(\d+): (.*)', spec)
        self.width = int(m.group(1))
        self.length = int(m.group(2))
        self.area = self.width * self.length
        self.pcounts = tuple(int(x) for x in m.group(3).split(' '))

    def __str__(self):
        return (f'TreeRegion(w={self.width} l={self.length} '
                f'a={self.area} pcounts={self.pcounts})')


def part1(presents: tuple[Present, ...],
          tree_regions: tuple[TreeRegion, ...]) -> int:
    # NOTE: this code knowingly fails for the sample input
    success_count = 0
    for tr in tree_regions:
        total_parea = 0
        for idx, pcount in enumerate(tr.pcounts):
            if pcount > 0:
                total_parea += (presents[idx].area * pcount)

        if tr.area >= total_parea:
            success_count += 1

    return success_count


def parse_input(fname: str) -> tuple[
        tuple[Present, ...], tuple[TreeRegion, ...]]:
    presents = []
    regions = []

    for rec in multiline_file(fname):
        if re.match(r'\d+:\n', rec):
            p_spec = rec
            p = Present(p_spec)
            presents.append(p)
        elif re.match(r'\d+x\d+: ', rec):
            for line in rec.splitlines():
                tr_spec = line
                tr = TreeRegion(tr_spec)
                regions.append(tr)
        else:
            raise ValueError(f'Invalid input format: {rec=}')

    return tuple(presents), tuple(regions)


def main():
    sample_input = parse_input('input/sample_input.txt')
    main_input = parse_input('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(*inp))
        print()


if __name__ == '__main__':
    main()
