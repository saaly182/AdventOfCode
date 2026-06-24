#!/usr/bin/python3 -u

import heapq
import itertools
import re

# TODO: convert SpaceCube to a pure geometry class and move the bot-searching
# logic to either direct tuples in the heap, or a SearchNode class that ties
# together cubes and bots.


class SpaceCube:
    """A cube with points-per-side equal to a power of two."""
    def __init__(self, p1: tuple[int, int, int], p2: tuple[int, int, int]):
        """Initialize a SpaceCube object given two diagonal points."""
        x1, y1, z1 = p1
        x2, y2, z2 = p2
        self.minx = min(x1, x2)
        self.miny = min(y1, y2)
        self.minz = min(z1, z2)
        self.maxx = max(x1, x2)
        self.maxy = max(y1, y2)
        self.maxz = max(z1, z2)
        self.bots_upper_bound = -1
        self.dist_to_origin = self._min_dist_to_point((0, 0, 0))

        # Check for cubeness and power-of-two sides
        xsize = self.maxx - self.minx + 1
        ysize = self.maxy - self.miny + 1
        zsize = self.maxz - self.minz + 1
        if not (xsize == ysize == zsize):
            raise ValueError(f'Box must be a cube')
        if xsize > 0 and xsize.bit_count() != 1:
            raise ValueError(f'Points per side must be a power of two')

    @property
    def priority(self) -> tuple[int, int]:
        return -self.bots_upper_bound, self.dist_to_origin

    def is_single_point(self):
        return (self.minx == self.maxx and self.miny == self.maxy and
                self.minz == self.maxz)

    def subcubes(self) -> list[SpaceCube]:
        """Split cube into its eight subcubes"""
        hd = (self.maxx - self.minx + 1) // 2  # half distance
        x_ranges = [
            (self.minx, self.minx + hd - 1), (self.minx + hd, self.maxx)]
        y_ranges = [
            (self.miny, self.miny + hd - 1), (self.miny + hd, self.maxy)]
        z_ranges = [
            (self.minz, self.minz + hd - 1), (self.minz + hd, self.maxz)]

        return [
            SpaceCube((x1, y1, z1), (x2, y2, z2))
            for (x1, x2), (y1, y2), (z1, z2) in
            itertools.product(x_ranges, y_ranges, z_ranges)
        ]

    def _min_dist_to_point(self, p: tuple[int, int, int]) -> int:
        x, y, z = p
        dist = 0

        for a, amin, amax in ((x, self.minx, self.maxx),
                              (y, self.miny, self.maxy),
                              (z, self.minz, self.maxz)):
            if a < amin:
                dist += (amin - a)
            elif a > amax:
                dist += (a - amax)

        return dist

    def intersects(self, bot: tuple) -> bool:
        """Return True if the bot and its range allows it to reach the cube."""
        bx, by, bz, brange = bot
        dist = self._min_dist_to_point((bx, by, bz))
        return dist <= brange

    def __lt__(self, other):
        return self.priority < other.priority

    def __str__(self):
        s = (f'{self.__class__.__name__}: '
             f'minx={self.minx} maxx={self.maxx} '
             f'miny={self.miny} maxy={self.maxy} '
             f'minz={self.minz} maxz={self.maxz}, '
             f'enclosed bots upper bound: {self.bots_upper_bound}')
        return s


def md(p1: tuple, p2: tuple) -> int:
    """Return the manhattan distance between two points."""
    return sum(abs(i - j) for i, j in zip(p1, p2, strict=True))


def part1(bots: tuple) -> int:
    strongest_bot = bots[0]
    for bot in bots:
        if bot[3] > strongest_bot[3]:
            strongest_bot = bot
    max_r = strongest_bot[3]

    # assert that there's only *one* strongest bot in the input
    max_r_count = len([b[3] for b in bots if b[3] == max_r])
    assert max_r_count == 1

    in_range = [b for b in bots if md(b[:3], strongest_bot[:3]) <= max_r]

    return len(in_range)


def enclosing_cube(bots: tuple) -> SpaceCube:
    ur = -1  # universe radius
    for bot in bots:
        reach = max([abs(a) + bot[3] for a in bot[:3]])
        if reach > ur:
            ur = reach

    # Now increase the radius to the next higher power of two
    ur = (1 << ur.bit_length())

    return SpaceCube((-ur, -ur, -ur), (ur - 1, ur - 1, ur - 1))


def estimate_nearby_bots(sc: SpaceCube, bots: tuple) -> int:
    """Return the upper bound of bots that can "reach" the cube."""
    return sum(1 for bot in bots if sc.intersects(bot))


def part2(bots: tuple) -> int:
    initial_cube = enclosing_cube(bots)
    initial_cube.bots_upper_bound = estimate_nearby_bots(initial_cube, bots)
    heap = []
    heapq.heappush(heap, initial_cube)

    while True:
        cube = heapq.heappop(heap)
        if cube.is_single_point():
            break

        for sc in cube.subcubes():
            sc.bots_upper_bound = estimate_nearby_bots(sc, bots)
            heapq.heappush(heap, sc)

    # We have found the single point with the most in-range bots
    x, y, z = cube.minx, cube.miny, cube.minz
    print(x, y, z)

    return md((0, 0, 0), (x, y, z))


def parse_input(fname: str) -> tuple[tuple[int, int, int, int], ...]:
    bots = []
    input_re = re.compile(r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)')
    with open(fname) as file:
        for line in file:
            line = line.strip()
            if mo := re.fullmatch(input_re, line):
                bot = tuple(int(x) for x in mo.groups())
                bots.append(bot)
            else:
                raise ValueError(f'Invalid input: {line}')

    return tuple(bots)


def main():
    input_files = (
        'input/sample_input.txt',
        'input/sample_input_2.txt',
        'input/input.txt',
    )
    for inpf in input_files:
        inp = parse_input(inpf)
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
