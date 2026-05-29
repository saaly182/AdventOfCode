#!/usr/bin/python3

def wirepoints(w):
  wp = set()

  p = [0, 0]
  for i in w:
    direction = i[0]
    steps = int(i[1:])

    if direction == 'L':
      move = (-1, 0)
    elif direction == 'R':
      move = (+1, 0)
    elif direction == 'U':
      move = (0, +1)
    elif direction == 'D':
      move = (0, -1)
    else:
      raise BadInput

    for j in range(steps):
      p[0] += move[0]
      p[1] += move[1]
      wp.add(tuple(p))

  return wp

with open('input.txt') as f:
  line = f.readline().rstrip()
  wire1 = line.split(',')
  line = f.readline().rstrip()
  wire2 = line.split(',')

a = wirepoints(wire1)
b = wirepoints(wire2)
common_points = a.intersection(b)

closest = min([abs(x[0]) + abs(x[1]) for x in common_points])

print(closest)
