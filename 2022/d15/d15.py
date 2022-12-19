#!/usr/bin/python3 -u

from collections import defaultdict
import re


def dist(a, b):
  'Return manhattan dist between a and b.'
  return abs(a[0] - b[0]) + abs(a[1] - b[1])


def neighborhood(a, d, row):
  'Return all points within dist d of point a.'
  n = set()
  dy = row - a[1]
  z = d - abs(dy)
  for dx in range(-z, z + 1):
    x = a[0] + dx
    n.add((x, row))
  return n


def show_grid(g):
  xs = [a[0] for a in g]
  ys = [a[1] for a in g]
  minx = min(xs)
  maxx = max(xs)
  miny = min(ys)
  maxy = max(ys)
  for y in range(miny, maxy + 1):
    for x in range(minx, maxx + 1):
      print(g[(x, y)], end='')
    print()


def no_beacon_count(grid, row):
  count = 0
  for p in grid:
    if p[1] == row and grid[p] == '#':
      count += 1
  return count


def part1(beac_near_sens, row):
  grid = defaultdict(lambda: '.')
  for sens in beac_near_sens:
    grid[sens] = 'S'
    grid[beac_near_sens[sens]] = 'B'
  for sens in beac_near_sens:
    s = sens
    b = beac_near_sens[s]
    d = dist(s, b)
    for n in neighborhood(s, d, row):
      if grid[n] == '.':
        grid[n] = '#'
  return no_beacon_count(grid, row)


def part2(beac_near_sens):
  return None


def parse(inp):
  beac_near_sens = {}
  spec = r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)'
  for line in inp:
    match = re.fullmatch(spec, line)
    assert match
    gr = [int(x) for x in match.groups()]
    beac_near_sens[(gr[0], gr[1])] = (gr[2], gr[3])

  return beac_near_sens


def slurp(fname):
  with open(fname) as file:
    return [line.rstrip() for line in file.readlines()]


def main():
  sample_input = slurp('sample_input.txt')
  beac_near_sens = parse(sample_input)
  print("Sample Input")
  print("Part 1 answer =", part1(beac_near_sens, 10))
  print("Part 2 answer =", part2(beac_near_sens))
  print()

  main_input = slurp('input.txt')
  beac_near_sens = parse(main_input)
  print("Main Input")
  print("Part 1 answer =", part1(beac_near_sens, 2000000))
  print("Part 2 answer =", part2(beac_near_sens))
  print()


if __name__ == '__main__':
  main()
