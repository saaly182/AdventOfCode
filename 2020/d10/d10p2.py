#!/usr/bin/python3
#
# YAY, first real dynamic programming code
#

import functools

@functools.lru_cache(maxsize=None)
def path_count_to(n):
  "Return the number of distinct paths from 0 to n."
  if n == 0:
    return 1

  pc = 0
  for pred in G[n]:
    pc += path_count_to(pred)
  
  return pc


a = []
with open('input.txt', 'r') as f:
  for line in f:
    a.append(int(line))

a.sort()
a.insert(0, 0)
a.append(max(a) + 3)

# graph of predecessors
G = {}

for x in a:
  G[x] = []
  for i in (1, 2, 3):
    if (x - i) in a:
      G[x].append(x - i)

print(path_count_to(max(a)))
