#!/usr/bin/python3 -u

import sys
sys.path.append('../../lib')

from collections import defaultdict
from utils import drange


class Cave1:
  # based on 2D array
  # NOTE: I could get rid of this original part1 implementation and make Cave2
  #       work for part1, but I wanted to keep the code for the two different
  #       approaches.
  def __init__(self, rockpaths):
    self.rockpaths = rockpaths
    self.sand_source = (500, 0)
    self.sand_count = 0

    # establish boundaries
    _xs = [u[0] for v in rockpaths for u in v]
    _ys = [u[1] for v in rockpaths for u in v]
    self.minx = min(_xs) - 1
    self.maxx = max(_xs) + 1
    self.miny = 0
    self.maxy = max(_ys) + 1

    # create cave as all open space and the sand source
    self.cave = [['.'] * (self.maxx - self.minx + 1)
                    for _ in range(self.maxy + 1)]
    self._mark_sand_source()

    # add in the rock paths
    for rp in self.rockpaths:
      p1 = rp[0]
      for p2 in rp[1:]:
        x1 = p1[0] - self.minx
        x2 = p2[0] - self.minx
        y1 = p1[1]
        y2 = p2[1]
        assert x1 == x2 or y1 == y2
        if x1 == x2:
          for y in drange(y1, y2):
            self.cave[y][x1] = '#'
        else:
          for x in drange(x1, x2):
            self.cave[y1][x] = '#'
        p1 = p2

  def _mark_sand_source(self):
    self.cave[self.sand_source[1]][self.sand_source[0] - self.minx] = '+'

  def show(self):
    for row in self.cave:
      print(''.join(row))
    print()

  def add_sand(self):
    'Add a grain of sand and return True if it comes to rest, False otherwise.'
    sx = self.sand_source[0] - self.minx
    sy = self.sand_source[1]

    # The added buffer points on the side ensure the sand the sand
    # never falls off the sides. Also assume the input is such that
    # the source point cannot become completely blocked.
    while sy < self.maxy:
      moved = False
      for dx, dy in ((0, 1), (-1, 1), (1, 1)):
        sx2 = sx + dx
        sy2 = sy + dy
        if self.cave[sy2][sx2] == '.':
          self.cave[sy][sx] = '.'
          self.cave[sy2][sx2] = 'o'
          sx = sx2
          sy = sy2
          moved = True
          break
      if not moved:
        # sand came to rest, so stop trying to fall deeper
        break

    # put the '+' back on the sand source
    self._mark_sand_source()

    if not moved:
      self.sand_count += 1
      return True
    return False  # finally fell off the bottom


class Cave2:
  # based on dict of points
  def __init__(self, rockpaths):
    self.rockpaths = rockpaths
    self.sand_source = (500, 0)
    self.sand_count = 0

    # create cave as all open space and the sand source
    self.cave = defaultdict(lambda: '.')
    self._mark_sand_source()

    # add in the rock paths
    for rp in self.rockpaths:
      p1 = rp[0]
      for p2 in rp[1:]:
        x1 = p1[0]
        x2 = p2[0]
        y1 = p1[1]
        y2 = p2[1]
        assert x1 == x2 or y1 == y2
        if x1 == x2:
          for y in drange(y1, y2):
            self.cave[(x1, y)] = '#'
        else:
          for x in drange(x1, x2):
            self.cave[(x, y1)] = '#'
        p1 = p2

    # determine the floor level
    self.floory = max([a[1] for a in self.cave]) + 2

  def _mark_sand_source(self):
    self.cave[self.sand_source] = '+'

  def show(self):
    xs = [a[0] for a in self.cave]
    ys = [a[1] for a in self.cave]
    minx = min(xs)
    maxx = max(xs)
    miny = min(ys)
    maxy = max(ys)
    for y in range(miny, maxy + 1):
      for x in range(minx, maxx + 1):
        print(self.cave[(x, y)], end='')
      print()

  def add_sand(self):
    '''Add a grain of sand and return True if it gets past the source point,
    False otherwise.'''
    sx, sy = self.sand_source

    while True:
      moved = False
      for dx, dy in ((0, 1), (-1, 1), (1, 1)):
        sx2 = sx + dx
        sy2 = sy + dy

        if sy2 == self.floory:  # infinite floor
          self.cave[(sx2, sy2)] = '#'

        if self.cave[(sx2, sy2)] == '.':
          self.cave[(sx, sy)] = '.'
          self.cave[(sx2, sy2)] = 'o'
          sx = sx2
          sy = sy2
          moved = True
          break
      if not moved:
        # sand came to rest, so stop trying to fall deeper
        break

    self.sand_count += 1

    # put the '+' back on the sand source
    self._mark_sand_source()

    if (sx, sy) == self.sand_source:
      self.cave[self.sand_source] = 'o'
      return False  # finally blocked the source
    return True


def part1(rockpaths):
  cave = Cave1(rockpaths)
  while cave.add_sand():
    pass
  return cave.sand_count


def part2(rockpaths):
  cave = Cave2(rockpaths)
  while cave.add_sand():
    pass
  return cave.sand_count


def parse(inp):
  rockpaths = []
  for line in inp:
    rp = []
    for pstr in line.split(' -> '):
      x, y = pstr.split(',')
      rp.append((int(x), int(y)))
    rockpaths.append(tuple(rp))

  return tuple(rockpaths)


def slurp(fname):
  with open(fname) as file:
    return [line.rstrip() for line in file.readlines()]


def main():
  sample_input = slurp('sample_input.txt')
  main_input = slurp('input.txt')

  for inp in (sample_input, main_input):
    rockpaths = parse(inp)
    print("Part 1 answer =", part1(rockpaths))
    print("Part 2 answer =", part2(rockpaths))
    print()


if __name__ == '__main__':
  main()
