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
        # perimeter is directly related to the # of adjacent sides
        adjcount = 0
        regplots = set(reg)
        for r, c in reg:
            for d in 'NSEW':
                dr, dc = dirutils.dirvecs[d]
                if (r + dr, c + dc) in regplots:
                    adjcount += 1
        perimeter = 4 * len(reg) - adjcount
        return perimeter

    @staticmethod
    def count_corners(nw: bool, ne: bool, se: bool, sw: bool) -> int:
        plot_count = sum((nw, ne, se, sw))
        match plot_count:
            case 0:
                raise ValueError(f'cannot be all False')
            case 1:
                return 1
            case 2:
                if (nw and se) or (ne and sw):
                    return 2
                else:
                    return 0
            case 3:
                return 1
            case 4:
                return 0

    @staticmethod
    def region_sidecount(reg: list) -> int:
        # The number of sides is equal to the number of corners
        # TODO: DRY refactor this
        cornercount = 0
        regplots = set(reg)
        seen_corners = set()  # point-corner assoc. with its NW square
        for r, c in reg:
            # this plot is a square; evaluate each of its four corners
            # and also track corners that have already been evaluated
            # northwest
            nw_square = (r - 1, c - 1)
            if nw_square not in seen_corners:
                seen_corners.add(nw_square)
                nw = nw_square in regplots
                ne = (r - 1, c) in regplots
                se = (r, c) in regplots
                sw = (r, c - 1) in regplots
                cornercount += Garden.count_corners(nw, ne, se, sw)
            # northeast
            nw_square = (r - 1, c)
            if nw_square not in seen_corners:
                seen_corners.add(nw_square)
                nw = nw_square in regplots
                ne = (r - 1, c + 1) in regplots
                se = (r, c + 1) in regplots
                sw = (r, c) in regplots
                cornercount += Garden.count_corners(nw, ne, se, sw)
            # southeast
            nw_square = (r, c)
            if nw_square not in seen_corners:
                seen_corners.add(nw_square)
                nw = nw_square in regplots
                ne = (r, c + 1) in regplots
                se = (r + 1, c + 1) in regplots
                sw = (r + 1, c) in regplots
                cornercount += Garden.count_corners(nw, ne, se, sw)
            # southwest
            nw_square = (r, c - 1)
            if nw_square not in seen_corners:
                seen_corners.add(nw_square)
                nw = nw_square in regplots
                ne = (r, c) in regplots
                se = (r + 1, c) in regplots
                sw = (r + 1, c - 1) in regplots
                cornercount += Garden.count_corners(nw, ne, se, sw)
        return cornercount

    def fence_price_by_perimeter(self) -> int:
        fp = 0
        for plant in self.regions:
            for reg in self.regions[plant]:
                fp += self.region_area(reg) * self.region_perimeter(reg)
        return fp

    def fence_price_by_sidecount(self) -> int:
        fp = 0
        for plant in self.regions:
            for reg in self.regions[plant]:
                fp += self.region_area(reg) * self.region_sidecount(reg)
        return fp


def part1(garden: tuple) -> int:
    g = Garden(garden)
    return g.fence_price_by_perimeter()


def part2(garden: tuple) -> int:
    g = Garden(garden)
    return g.fence_price_by_sidecount()


def slurp(fname: str) -> tuple[str, ...]:
    with open(fname) as file:
        return tuple(line.rstrip() for line in file.readlines())


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
