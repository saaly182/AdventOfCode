#!/usr/bin/python3

T = []
with open('input.txt', 'r') as trees:
  for line in trees:
    line = (line.rstrip()) * 100
    T.append(line)

tcount = 0

x = 0

for row in T:
  if row[x] == '#':
    tcount += 1
  x += 3

print(tcount)
