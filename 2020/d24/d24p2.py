#!/usr/bin/python3

# Using hexgrid "cube coordinates" as detailed at https://www.redblobgames.com/grids/hexagons/#neighbors

def parse_cmds(s):
  c = []
  chars = [x for x in s]
  i = 0
  while i < len(s):
    if chars[i] in ('e', 'w'):
      cmd = chars[i]
    else:
      cmd = ''.join((chars[i], chars[i + 1]))
      i += 1
    c.append(cmd)
    i += 1

  return tuple(c)


def tile_neighbors(coords):
  x, y, z = coords
  return (
      (x + 1, y - 1, z + 0),
      (x + 0, y - 1, z + 1),
      (x - 1, y + 0, z + 1),
      (x - 1, y + 1, z + 0),
      (x + 0, y + 1, z - 1),
      (x + 1, y + 0, z - 1),
  )


cmds = []

with open('input.txt', 'r') as f:
  for line in f:
    line = line.rstrip()
    cmds.append(parse_cmds(line))

tiles = {}

for c in cmds:
  x, y, z = 0, 0, 0
  for move in c:
    if move == 'e':
      x += 1
      y -= 1
    elif move == 'se':
      y -= 1
      z += 1
    elif move == 'sw':
      x -= 1
      z += 1
    elif move == 'w':
      x -= 1
      y += 1
    elif move == 'nw':
      y += 1
      z -= 1
    elif move == 'ne':
      x += 1
      z -= 1
    else:
      raise CommandError

  if (x, y, z) in tiles:
    assert tiles[(x, y, z)] in ('B', 'W')
    if tiles[(x, y, z)] == 'W':
      tiles[(x, y, z)] = 'B'
    else:
      tiles[(x, y, z)] = 'W'
  else:
    tiles[(x, y, z)] = 'B'

# * Any black tile with zero or more than 2 black tiles immediately
#   adjacent to it is flipped to white.
# * Any white tile with exactly 2 black tiles immediately adjacent
#   to it is flipped to black.
for days in range(1, 101):
  # First make sure all W tiles adjacent to any B tile are in the tiles dict
  tiles_to_add = {}
  for t in tiles:
    if tiles[t] == 'B':
      for tn in tile_neighbors(t):
        if tn not in tiles:
          tiles_to_add[tn] = 'W'
  tiles.update(tiles_to_add)

  tiles_next = tiles.copy()
  for t in tiles:
    bcount = 0
    for tn in tile_neighbors(t):
      if tn in tiles and tiles[tn] == 'B':
        bcount += 1
    color = tiles[t]
    if color == 'B':
      if bcount == 0 or bcount > 2:
        tiles_next[t] = 'W'
    else:
      if bcount == 2:
        tiles_next[t] = 'B'

  tiles = tiles_next

answer = list(tiles.values()).count('B')
print(answer)
