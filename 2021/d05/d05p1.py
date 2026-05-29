#!/usr/bin/python3

import collections


pcount = collections.defaultdict(int)

with open('input.txt') as pointsfile:
  for line in pointsfile:
    line = line.rstrip()
    p1, _, p2 = line.split()
    x1, y1 = [int(a) for a in p1.split(',')]
    x2, y2 = [int(a) for a in p2.split(',')]

    # only consider horz or vert lines for this problem
    if x1 == x2:
      x = x1
      for y in range(min(y1, y2), max(y1, y2) + 1):
        pcount[(x, y)] += 1

    if y1 == y2:
      y = y1
      for x in range(min(x1, x2), max(x1, x2) + 1):
        pcount[(x, y)] += 1

answer = len([a for a in pcount if pcount[a] > 1])
print(answer)
