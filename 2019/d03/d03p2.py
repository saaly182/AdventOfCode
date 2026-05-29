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


def dist2points(wire, points):
  """
  Return a dict with the points as keys, and the walking distance
  along the wire as values.
  """
  d2p = {}

  w = wire
  dist = 0
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
      pt = tuple(p)
      dist += 1

      if pt in points:
        # only count the first occurrence
        if pt not in d2p:
          d2p[pt] = dist

  return d2p


with open('input.txt') as f:
  line = f.readline().rstrip()
  wire1 = line.split(',')
  line = f.readline().rstrip()
  wire2 = line.split(',')

a = wirepoints(wire1)
b = wirepoints(wire2)
common_points = a.intersection(b)

x = dist2points(wire1, common_points)
y = dist2points(wire2, common_points)

minwalks = max(x.values()) + max(y.values())
for pt in x:
  walks = x[pt] + y[pt]
  if walks < minwalks:
    minwalks = walks

answer = minwalks
print(answer)
