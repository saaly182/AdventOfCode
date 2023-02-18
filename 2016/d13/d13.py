#!/usr/bin/python3 -u

from collections import defaultdict
import math
import heapq

import sys
sys.path.append('../../lib')
from dirutils import unitvecs


class CubeMaze:
    def __init__(self, favnum):
        self.favnum = favnum
        self.maze = {}
        self._wall = '#'
        self._open = '.'
        self._oob = '0'

    def location_type(self, x, y):
        """
        You can determine whether a given x,y coordinate will be a wall or an
        open space using a simple system:
        * If x or y is negative, the point is out of bounds.
        * Find x*x + 3*x + 2*x*y + y + y*y.
        * Add the office designer's favorite number (your puzzle input).
        * Find the binary representation of that sum; count the number of bits
          that are 1.
            * If the number of bits that are 1 is even, it's an open space.
            * If the number of bits that are 1 is odd, it's a wall.
        """
        if x < 0 or y < 0:
            return self._oob
        bstr = bin(x * x + 3 * x + 2 * x * y + y + y * y + self.favnum)[2:]
        count_ones = bstr.count('1')
        is_even = count_ones % 2 == 0
        return self._open if is_even else self._wall

    def neighbors(self, x, y):
        """Return open spaces adjacent to (x, y) and their distance."""
        dst = 1
        n = []
        for uv in unitvecs:
            nx, ny = x + uv[0], y + uv[1]
            spot = (nx, ny)
            if spot not in self.maze:
                ltype = self.location_type(nx, ny)
                self.maze[spot] = ltype
            if self.maze[spot] == self._open:
                n.append((spot, dst))
        return tuple(n)

    def shortest_path(self, src, dst):
        """Return distance from src to dst using dijkstra."""
        # See more details in ../../lib/aocutils.py. Obviously this needs a
        # specialized dijkstra to account for the infinite computed graph.
        dist = defaultdict(lambda: math.inf)
        seen = defaultdict(bool)
        minq = []
        dist[src] = 0
        heapq.heappush(minq, (0, src))

        while minq:
            _, u = heapq.heappop(minq)
            if u == dst:
                break
            if seen[u]:
                continue  # already seen this vertex
            seen[u] = True

            for v, e in self.neighbors(u[0], u[1]):
                alt = dist[u] + e
                if alt < dist[v]:
                    dist[v] = alt
                    heapq.heappush(minq, (alt, v))

        return dist[dst]


def part1(favnum, dst):
    cm = CubeMaze(favnum)
    return cm.shortest_path((1, 1), dst)


def part2():
    return None


def main():

    for inp in ((10, (7, 4)), (1358, (31, 39))):
        print("Part 1 answer =", part1(*inp))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
