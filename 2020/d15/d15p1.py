#!/usr/bin/python3

seq = [1, 0, 15, 2, 10, 13]

def indexes(L, val):
  idx = []
  for j in range(len(L)):
    if L[j] == val:
      idx.append(j)
  return tuple(idx)

for t in range(len(seq), 2020):
  last = seq[t - 1]
  if last not in seq[:-1]:
    seq.append(0)
  else:
    idx = indexes(seq[:-1], last)
    dist = (t - 1) - idx[-1]
    seq.append(dist)

print(seq[-1])
