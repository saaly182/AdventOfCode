#!/usr/bin/python3 -u

import collections
import sys
sys.path.append('../../lib')
import dirutils  # noqa: E402 F401


class Garden:
    def __init__(self, g: tuple):
        self.garden = g
        self.r_max = len(self.garden) - 1
        self.c_max = len(self.garden[0]) - 1

        # parse and store all the regions in the garden
        self.regions = collections.defaultdict(list)
        gset = self.__create_gset()
        while gset:
            r, c, plant = gset.pop()
            self.regions[plant].append([(r, c)])
            self.__fill_region(r, c, plant, gset)

    def __create_gset(self) -> set:
        gset = set()
        for r, row in enumerate(self.garden):
            for c, plant in enumerate(row):
                gset.add((r, c, plant))
        return gset

    def __fill_region(self, r: int, c: int, plant: str, gset: set) -> None:
        for d in 'NSEW':
            dr, dc = dirutils.dirvecs[d]
            r2, c2 = r + dr, c + dc
            if 0 <= r2 <= self.r_max and 0 <= c2 <= self.c_max:
                if (r2, c2, plant) in gset:
                    gset.remove((r2, c2, plant))
                    self.regions[plant][-1].append((r2, c2))
                    self.__fill_region(r2, c2, plant, gset)

    @staticmethod
    def region_area(reg: list) -> int:
        return len(reg)

    @staticmethod
    def region_perimeter(reg: list) -> int:
        adjcount = 0
        regplots = set(reg)
        for r, c in reg:
            for d in 'NSEW':
                dr, dc = dirutils.dirvecs[d]
                if (r + dr, c + dc) in regplots:
                    adjcount += 1
        perimeter = 4 * len(reg) - adjcount
        return perimeter

    def fence_price(self) -> int:
        fp = 0
        for plant in self.regions:
            for reg in self.regions[plant]:
                fp += self.region_area(reg) * self.region_perimeter(reg)
        return fp


def part1(garden: tuple) -> int:
    g = Garden(garden)
    return g.fence_price()


def part2() -> int:
    return -99


def slurp(fname: str) -> tuple[str, ...]:
    with open(fname) as file:
        return tuple(line.rstrip() for line in file.readlines())


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
