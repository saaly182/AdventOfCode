#!/usr/bin/python3

import functools
import operator

def prod(x):
  return functools.reduce(operator.mul, x, 1)

def ostr(S):
  "Return rev(S) if it's sorted before S, or S otherwise."
  Srev = S[::-1]
  if Srev < S:
    return Srev
  return S


def borders(T):
  "Return the four borders of T in canonical representation."
  N = ostr(''.join(T[0]))
  S = ostr(''.join(T[-1]))
  E = ostr(''.join([x[-1] for x in T]))
  W = ostr(''.join([x[0] for x in T]))

  return((N, S, E, W))


tilenum = None
tiles = {}
t2b = {}
b2t = {}

with open('input.txt', 'r') as f:
  for line in f:
    line = line.rstrip()

    if not line:
      continue

    if line.startswith('Tile '):
      tilenum = int(line.split()[1].replace(':', ''))
      tiles[tilenum] = []
    else:
      tiles[tilenum].append(line)

for t in tiles:
  bs = borders(tiles[t])
  t2b[t] = bs
  for b in bs:
    if b not in b2t:
      b2t[b] = [t]
    else:
      b2t[b].append(t)

# Examinging the data, there are only four possible corners,
# so just find those. No need to assemble the image itself.

corners = []
for t in t2b:
  shared_border_count = 0
  for b in t2b[t]:
    if len(b2t[b]) > 1:
      shared_border_count += 1

  if shared_border_count == 2:
    corners.append(t)

print('The corners are:', corners)
print('Their product is:', prod(corners))
