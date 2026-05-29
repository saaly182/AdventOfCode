#!/usr/bin/python3 -u

debug = False
ifile = 'input.txt'

class Grid:
  def __init__(self, points):
    xmax = max([a[0] for a in points])
    ymax = max([a[1] for a in points])
    self.g = [[0 for a in range(xmax + 1)] for b in range(ymax + 1)]
    for col, row in points:
      self.g[row][col] = 1

  def show(self):
    print('vvvvvvvvvvvvvvvv')
    for r in self.g:
      r2 = []
      for a in r:
        if a == 0:
          r2.append('.')
        else:
          r2.append('#')
      print(''.join(r2))
    print('^^^^^^^^^^^^^^^^')

  def dotcount(self):
    count = 0
    for row in self.g:
      count += row.count(1)
    return count

  # CAUTION: foldx() still assumes that the fold line is exactly
  # in the middle position. It turns out the input for this problem
  # follows that, so I'm not bothering making this code more generic.
  def foldx(self, col):
    for n, row in enumerate(self.g):
      lside = row[:col]
      rside = row[(col + 1):]
      assert len(lside) == len(rside)
      self.g[n] = [i or j for i, j in zip(lside, reversed(rside))]

  # This foldy() function works even if the fold line is not at the midpoint.
  def foldy(self, row):
    toprows = self.g[:row]
    bottomrows = self.g[(row + 1):]
    if len(bottomrows) > len(toprows):
      raise ValueError(row)

    ridx = row - 1
    for t, b in zip(reversed(toprows), bottomrows):
      toprows[ridx] = [i or j for i, j in zip(t, b)]
      ridx -= 1
    self.g = toprows


def main():
  points = []
  folds = []
  with open(ifile) as graphfile:
    for line in graphfile:
      line = line.rstrip()
      toks = line.split()
      if not toks:
        continue
      if toks[0] == 'fold':
        axis, loc = toks[2].split('=')
        folds.append((axis, int(loc)))
      else:
        x, y = (int(z) for z in toks[0].split(','))
        points.append((x, y))

  g = Grid(points)

  if debug:
    print(f'points = {points}')
    print(f'folds = {folds}')
    g.show()

  # only want to do the first fold cmd for part 1
  for axis, loc in folds:
    if debug:
      print(f'axis, loc = {axis}, {loc}')
    if axis == 'x':
      g.foldx(loc)
    elif axis == 'y':
      g.foldy(loc)
    else:
      raise ValueError(axis)
    if debug:
      g.show()

  g.show()


if __name__ == '__main__':
  main()
