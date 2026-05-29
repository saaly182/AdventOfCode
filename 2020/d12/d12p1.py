#!/usr/bin/python3

nav = []
with open('input.txt', 'r') as f:
  for line in f:
    line = line.rstrip()
    cmd = line[0]
    amt = int(line[1:])
    nav.append((cmd, amt))

# using classic x,y coordinates
d = {
    'N': ( 0,  1),
    'S': ( 0, -1),
    'E': ( 1,  0),
    'W': (-1,  0),
}

h = {
      0 : 'N',
     90 : 'E',
    180 : 'S',
    270 : 'W',
}

x, y = 0, 0

heading = 90
for instruction in nav:
  cmd, amt = instruction

  if cmd in 'NSEW':
    x += d[cmd][0] * amt
    y += d[cmd][1] * amt

  elif cmd == 'F':
    card = h[heading]
    x += d[card][0] * amt
    y += d[card][1] * amt

  elif cmd == 'L':
    heading = (360 + heading - amt) % 360

  elif cmd == 'R':
    heading = (360 + heading + amt) % 360

print(abs(x) + abs(y))
