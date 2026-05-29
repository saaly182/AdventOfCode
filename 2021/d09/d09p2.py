#!/usr/bin/python3 -u

import collections

hmap = []

with open('input.txt') as heightmap:
  for line in heightmap:
    line = line.rstrip()
    hmap.append([int(x) for x in line])

# dict, with low points as keys, and a list of all points that
# "drain" to that low point as values. 9s don't count.
basins = collections.defaultdict(list)

rmax = len(hmap) - 1
cmax = len(hmap[0]) - 1

def descend(row, col):
  'Return the low point this point drains to.'
  new_low = True
  while new_low:
    hn = hs = he = hw = 999
    h = hmap[row][col]
    if row > 0:
      hn = hmap[row - 1][col]
    if row < rmax:
      hs = hmap[row + 1][col]
    if col > 0:
      hw = hmap[row][col - 1]
    if col < cmax:
      he = hmap[row][col + 1]

    new_low = False
    if hn < h:
      new_low = True
      row -= 1
    elif hs < h:
      new_low = True
      row += 1
    elif hw < h:
      new_low = True
      col -= 1
    elif he < h:
      new_low = True
      col += 1

  return (row, col)


for row in range(rmax + 1):
  for col in range(cmax + 1):
    if hmap[row][col] != 9:
      low_point = descend(row, col)
      basins[low_point].append((row, col))

bsizes = [len(basins[x]) for x in basins]
bsizes.sort(reverse=True)
answer = 1
for b in bsizes[:3]:
  answer *= b

print(answer)
