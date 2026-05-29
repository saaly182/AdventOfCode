#!/usr/bin/python3

# TOO SLOW...

a = []
with open('input.txt', 'r') as f:
  for line in f:
    a.append(int(line))

a.insert(0, 0)
a.append(max(a) + 3)
a.sort()

G = {}

for x in a:
  G[x] = []
  for i in (1, 2, 3):
    if (x + i) in a:
      G[x].append(x + i)

p = [0]
pcount = 0
target = max(a)

def find():
  global pcount

  curr = p[-1]

  if curr == target:
    pcount += 1
    if pcount % 1000000 == 0:
      print(pcount)

  children = G[curr]
  for c in children:
    p.append(c)
    find()
    p.pop()

find()

print(pcount)
