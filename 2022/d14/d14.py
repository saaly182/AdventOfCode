#!/usr/bin/python3 -u

import sys
sys.path.append('../../lib')

from utils import drange


class Cave:
  def __init__(self, rockpaths):
    self.rockpaths = rockpaths
    self.sandpoint = (500, 0)

    # establish boundaries
    _xs = [u[0] for v in rockpaths for u in v]
    _ys = [u[1] for v in rockpaths for u in v]
    self.minx = min(_xs) - 1
    self.maxx = max(_xs) + 1
    self.miny = 0
    self.maxy = max(_ys) + 1

    # create cave as all open space and the sand origination point
    self.cave = [['.'] * (self.maxx - self.minx + 1)
                    for _ in range(self.maxy + 1)]
    self.cave[self.sandpoint[1]][self.sandpoint[0] - self.minx] = '+'

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

  def show(self):
    for row in self.cave:
      print(''.join(row))


def part1(rockpaths):
  cave = Cave(rockpaths)
  cave.show()
  return None


def part2(rockpaths):
  return None


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

  main_input = sample_input

  for inp in (sample_input, main_input):
    rockpaths = parse(inp)
    print("Part 1 answer =", part1(rockpaths))
    print("Part 2 answer =", part2(rockpaths))
    print()


if __name__ == '__main__':
  main()
