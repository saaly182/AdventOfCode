#!/usr/bin/python3
'''
During a cycle, all cubes simultaneously change their state according
to the following rules:

* If a cube is active and exactly 2 or 3 of its neighbors are also
  active, the cube remains active. Otherwise, the cube becomes inactive.
* If a cube is inactive but exactly 3 of its neighbors are active,
  the cube becomes active. Otherwise, the cube remains inactive.
'''

import functools

@functools.lru_cache(maxsize=None)
def neighbors(c):
  x, y, z = c
  n = set()
  noff = (
      (-1, -1, -1),
      (-1, -1, 0),
      (-1, -1, 1),
      (-1, 0, -1),
      (-1, 0, 0),
      (-1, 0, 1),
      (-1, 1, -1),
      (-1, 1, 0),
      (-1, 1, 1),
      (0, -1, -1),
      (0, -1, 0),
      (0, -1, 1),
      (0, 0, -1),
      (0, 0, 1),
      (0, 1, -1),
      (0, 1, 0),
      (0, 1, 1),
      (1, -1, -1),
      (1, -1, 0),
      (1, -1, 1),
      (1, 0, -1),
      (1, 0, 0),
      (1, 0, 1),
      (1, 1, -1),
      (1, 1, 0),
      (1, 1, 1),
  )
  for d in noff:
    n.add((x + d[0], y + d[1], z + d[2]))

  return n


def active_neighbor_count(c):
  global ac
  n = neighbors(c)
  active_neighbors = [x for x in n if x in ac]
  return len(active_neighbors)


cycles = 6

# Just store active cubes in a set of (x,y,z) tuples. Top-left
# of the input is (0,0,0).

# ac = "active cubes"
ac = set()

x = y = z = 0
with open('input.txt', 'r') as f:
  for line in f:
    line = line.rstrip()
    for s in line:
      if s == '#':
        ac.add((x,y,z))
      x += 1
    x = 0
    y -= 1

for cycle in range(cycles):
  ac_next = ac.copy()
  for c in ac:
    anc = active_neighbor_count(c)
    if anc != 2 and anc != 3:
      ac_next.discard(c)
    for n in neighbors(c):
      if n not in ac:
        anc = active_neighbor_count(n)
        if anc == 3:
          ac_next.add(n)
  ac = ac_next

print(len(ac))
