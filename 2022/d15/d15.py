#!/usr/bin/python3 -u

from collections import defaultdict
from datetime import datetime
import re
import sys
sys.path.append('../../lib')
from aocutils import merge_intervals  # noqa: E402


def dist(a, b):
  'Return manhattan dist between a and b.'
  return abs(a[0] - b[0]) + abs(a[1] - b[1])


def neighborhood(a, d, row):
  'Return all points within dist d of point a in row.'
  n = set()
  dy = row - a[1]
  z = d - abs(dy)
  for dx in range(-z, z + 1):
    x = a[0] + dx
    n.add((x, row))
  return n


def show_grid(g):
  print('-' * 50)
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


def get_sboundary(sens, beac):
  "Return the four diamond points for the sensor's boundary"
  d = dist(sens, beac)
  return (
    (sens[0], sens[1] - d),  # north
    (sens[0], sens[1] + d),  # south
    (sens[0] + d, sens[1]),  # east
    (sens[0] - d, sens[1]),  # west
  )


def intersect(p1, p2, row):
  'Return x-intersection of line segment and horizontal line, perhaps None.'
  # This function is not general purpose. It's specialized to this problem
  # with 45-deg line segments and int coordinates.
  x1, y1, x2, y2 = p1[0], p1[1], p2[0], p2[1]
  if row < min(y1, y2) or row > max(y1, y2):
    return None
  x = (row - y1) * (x2 - x1) // (y2 - y1) + x1
  return x


def find_hole(row, sbounds, bmax):
  "Return the x coordinate of a beacon hole if it exists, None otherwise."
  intervals = []
  for sens in sbounds:
    xs = set()
    pn, ps, pe, pw = sbounds[sens]
    for p1, p2 in ((pn, pe), (pe, ps), (ps, pw), (pw, pn)):
      x = intersect(p1, p2, row)
      if x is not None:
        xs.add(x)
    if xs:
      interval = sorted(xs)
      if len(interval) == 1:
        interval.append(interval[0])
      # restrict to the problem's boundary
      interval[0] = max(interval[0], 0)
      interval[1] = min(interval[1], bmax)
      intervals.append(interval)

  m_intervals = merge_intervals(intervals)

  # now check if there is a hole between any intervals, with a number
  # of special cases first
  if m_intervals == [[0, bmax]]:
    return None
  if m_intervals[0][0] == 1:
    return 0
  if m_intervals[-1][1] == (bmax - 1):
    return bmax
  i_prev = m_intervals[0]
  for i_this in m_intervals[1:]:
    if i_this[0] - i_prev[1] == 2:
      x = i_this[0] - 1
      return x

  return None


def part2(beac_near_sens, bmax):
  # Insight from reddit hint: Just track each sensor's boundary diamond.
  sbounds = {}

  for sens in beac_near_sens:
    sbounds[sens] = get_sboundary(sens, beac_near_sens[sens])

  # scan all rows looking for the first instance of a row that has
  # one open beacon hole.
  for row in range(bmax + 1):
    if row % 100_000 == 0:
      print(f'{row=}')
    hole = find_hole(row, sbounds, bmax)
    if hole is not None:
      return hole * 4000000 + row

  assert False  # should not reach this line


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
  print("Part 2 answer =", part2(beac_near_sens, 20))
  print()

  main_input = slurp('input.txt')
  beac_near_sens = parse(main_input)
  print("Main Input")
  t1 = datetime.now()
  print("Part 1 answer =", part1(beac_near_sens, 2000000))
  t2 = datetime.now()
  print(f'Part 1 duration: {t2 - t1}')
  print("Part 2 answer =", part2(beac_near_sens, 4000000))
  t3 = datetime.now()
  print(f'Part 2 duration: {t3 - t2}')
  print()


if __name__ == '__main__':
  main()
