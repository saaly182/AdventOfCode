#!/usr/bin/python3 -u

import heapq
import itertools
import re


class SpaceCube:
    """A cube in space with points-per-side equal to a power of two."""
    def __init__(self, p1: tuple[int, int, int],
                 p2: tuple[int, int, int]) -> None:
        """Initialize a SpaceCube object given two diagonal points."""
        x1, y1, z1 = p1
        x2, y2, z2 = p2
        self.minx = min(x1, x2)
        self.miny = min(y1, y2)
        self.minz = min(z1, z2)
        self.maxx = max(x1, x2)
        self.maxy = max(y1, y2)
        self.maxz = max(z1, z2)

        # Check for cubeness and power-of-two # of sides
        xsize = self.maxx - self.minx + 1
        ysize = self.maxy - self.miny + 1
        zsize = self.maxz - self.minz + 1
        if not (xsize == ysize == zsize):
            raise ValueError('Box must be a cube')
        if xsize > 0 and xsize.bit_count() != 1:
            raise ValueError('Points per side must be a power of two')

    def is_single_point(self) -> bool:
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

    def min_dist_to_point(self, p: tuple[int, int, int]) -> int:
        """Return the minimum distance from the cube to the point."""
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

    def intersects(self, bot: tuple[int, int, int, int]) -> bool:
        """Return True if the bot and its range allows it to reach the cube."""
        bx, by, bz, brange = bot
        dist = self.min_dist_to_point((bx, by, bz))
        return dist <= brange


class SearchNode:
    """The interactions between a space cube and a set of bots.

    Used as the elements of a min-heap.
    """
    def __init__(self, cube: SpaceCube,
                 bots: tuple[tuple[int, int, int, int], ...]) -> None:
        self.cube = cube
        self.bots_upper_bound = sum(
            1 for bot in bots if self.cube.intersects(bot))
        self.dist_to_origin = self.cube.min_dist_to_point((0, 0, 0))
        self.priority = (-self.bots_upper_bound, self.dist_to_origin)

    def __lt__(self, other: SearchNode) -> bool:
        return self.priority < other.priority


def md(p1: tuple[int, ...], p2: tuple[int, ...]) -> int:
    """Return the manhattan distance between two points."""
    return sum(abs(i - j) for i, j in zip(p1, p2, strict=True))


def part1(bots: tuple[tuple[int, int, int, int], ...]) -> int:
    strongest_bot = max(bots, key=lambda b: b[3])
    max_r = strongest_bot[3]

    # assert that there's only *one* strongest bot in the input
    assert sum(1 for b in bots if b[3] == max_r) == 1

    in_range = [b for b in bots if md(b[:3], strongest_bot[:3]) <= max_r]

    return len(in_range)


def enclosing_cube(bots: tuple[tuple[int, int, int, int], ...]) -> SpaceCube:
    ur = -1  # universe radius
    for bot in bots:
        reach = max([abs(a) + bot[3] for a in bot[:3]])
        if reach > ur:
            ur = reach

    # Now increase the radius to the next higher power of two
    ur = (1 << ur.bit_length())

    return SpaceCube((-ur, -ur, -ur), (ur - 1, ur - 1, ur - 1))


def part2(bots: tuple[tuple[int, int, int, int], ...]) -> int:
    initial_cube = enclosing_cube(bots)
    initial_searchnode = SearchNode(initial_cube, bots)
    heap = []
    heapq.heappush(heap, initial_searchnode)

    while True:
        searchnode = heapq.heappop(heap)
        if searchnode.cube.is_single_point():
            break

        for subcube in searchnode.cube.subcubes():
            sub_searchnode = SearchNode(subcube, bots)
            heapq.heappush(heap, sub_searchnode)

    # We have found the single point with the most in-range bots
    x, y, z = searchnode.cube.minx, searchnode.cube.miny, searchnode.cube.minz

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
