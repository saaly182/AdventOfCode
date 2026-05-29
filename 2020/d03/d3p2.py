#!/usr/bin/python3

T = []
with open('input.txt', 'r') as trees:
  for line in trees:
    line = (line.rstrip()) * 1000
    T.append(line)

slopes = (
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2))

tmul = 1

for dx, dy in slopes:
  tcount = 0
  x = 0
  for y in range(0, len(T), dy):
    row = T[y]
    if row[x] == '#':
      tcount += 1
    x += dx 

  tmul *= tcount

print(tmul)
