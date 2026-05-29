#!/usr/bin/python3

def logical_xor(a, b):
  return a ^ b

with open('input.txt', 'r') as pwfile:

  validpw = 0

  for line in pwfile:
    pos, c, p = line.split()
    pos1, pos2 = [int(n) for n in pos.split('-')]
    c = c.replace(':', '')

    if logical_xor(p[pos1 - 1] == c, p[pos2 - 1] == c):
      validpw += 1

print(validpw)
