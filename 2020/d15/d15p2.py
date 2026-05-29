#!/usr/bin/python3

seq = [1, 0, 15, 2, 10, 13]
t_end = 30000000

last_seen = {}

for i in range(len(seq) - 1):
  last_seen[seq[i]] = i

for t in range(len(seq), t_end):
  x = seq[t - 1]
  if x in last_seen:
    seq.append(t - 1 - last_seen[x])
  else:
    seq.append(0)
  last_seen[x] = t - 1

print(seq[-1])
