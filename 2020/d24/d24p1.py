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

answer = list(tiles.values()).count('B')
print(answer)
