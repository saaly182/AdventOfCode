#!/usr/bin/python3 -u

x = 0
d = 0
aim = 0
with open('input.txt', 'r') as cmdfile:
  for line in cmdfile:
    c, n = line.split()
    n = int(n)
    if c == 'down':
      aim += n
    elif c == 'up':
      aim -= n
    elif c == 'forward':
      x += n
      d += (aim * n)
      assert d >= 0
    else:
      raise ValueError(c)

print(x * d)
