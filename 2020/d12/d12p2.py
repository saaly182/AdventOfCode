#!/usr/bin/python3
'''
Action N means to move the waypoint north by the given value.
Action S means to move the waypoint south by the given value.
Action E means to move the waypoint east by the given value.
Action W means to move the waypoint west by the given value.
Action L means to rotate the waypoint around the ship left (counter-clockwise) the given number of degrees.
Action R means to rotate the waypoint around the ship right (clockwise) the given number of degrees.
Action F means to move forward to the waypoint a number of times equal to the given value.
'''

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

# Now have to track both the waypoint x,y and the ship x,y
way_x, way_y = 10, 1
shp_x, shp_y = 0, 0

for instruction in nav:
  cmd, amt = instruction

  if cmd in 'NSEW':
    way_x += d[cmd][0] * amt
    way_y += d[cmd][1] * amt

  elif cmd == 'F':
    vx, vy = (way_x - shp_x), (way_y - shp_y)
    shp_x += vx * amt
    shp_y += vy * amt
    way_x = shp_x + vx
    way_y = shp_y + vy

  elif cmd == 'L' or cmd == 'R':
    if cmd == 'L':
      amt = (360 - amt) % 360
    dx = way_x - shp_x
    dy = way_y - shp_y

    if amt == 90:
      way_x = shp_x + dy
      way_y = shp_y - dx
    elif amt == 180:
      way_x = shp_x - dx
      way_y = shp_y - dy
    elif amt == 270:
      way_x = shp_x - dy
      way_y = shp_y + dx
    else:
      raise BadAngle

  else:
    raise BadNav

print(abs(shp_x) + abs(shp_y))
