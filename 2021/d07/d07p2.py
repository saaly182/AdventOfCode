#!/usr/bin/python3 -u

debug = False

h = []
with open('input.txt') as posfile:
  for line in posfile:
    line = line.rstrip()
    h.extend([int(x) for x in line.split(',')])

x1 = min(h)
x2 = max(h)

fmin = len(h) * sum(range((x2 - x1) + 1))
answer = -999

if debug:
  print(f'h = {h}')
  print(f'x1, x2 = {x1}, {x2}')
  print(f'fmin = {fmin}')
  print(f'answer = {answer}')

for x in range(x1, x2 + 1):
  f = 0
  for p in h:
    f += sum(range(abs(p - x) + 1))
    if debug:
      print(f'x, p, f = {x}, {p}, {f}')
  if f < fmin:
    fmin = f
    answer = fmin
    if debug:
      print(f'new min. fmin, answer = {fmin}, {answer}')

print(answer)
