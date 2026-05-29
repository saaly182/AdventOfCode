#!/usr/bin/python3

with open('input.txt', 'r') as pwfile:

  validpw = 0

  for line in pwfile:
    r, c, p = line.split()
    r1, r2 = [int(n) for n in r.split('-')]
    c = c.replace(':', '')

    ccount = 0
    for a in p:
      if a == c:
        ccount += 1

    if ccount >= r1 and ccount <= r2:
      validpw += 1

print(validpw)
