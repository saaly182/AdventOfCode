#!/usr/bin/python3 -u

x = 0
d = 0
with open('input.txt', 'r') as cmdfile:
  for line in cmdfile:
    c, n = line.split()
    n = int(n)
    if c == 'down':
      d += n
    elif c == 'up':
      d -= n
      assert d >= 0
    elif c == 'forward':
      x += n
    else:
      raise ValueError(c)

print(x * d)
