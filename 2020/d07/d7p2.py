#!/usr/bin/python3

brules = {}

with open('input.txt', 'r') as bagrules:
  for line in bagrules:
    line = line.rstrip()
    line = line.replace('bags', '')
    line = line.replace('bag', '')
    line = line.replace('.', '')
    line = line.replace(' contain', ':')
    c1, sep, blist1 = line.partition(':')
    c1 = c1.strip()
    c1 = c1.replace(' ', '-')
    blist1 = [x.strip() for x in blist1.split(',')]

    brules[c1] = []

    for b in blist1:
      if b == 'no other':
        continue
      count, sep, c2 = b.partition(' ')
      count = int(count)
      c2 = c2.replace(' ', '-')
      brules[c1].append((count, c2))

bagcount = -1  # don't want to count the original shiny-gold bag
Q = []
Q.append('shiny-gold')

while Q:
  c = Q.pop(0)
  bagcount += 1
  for count, c2 in brules[c]:
    for i in range(count):
      Q.append(c2)

print(bagcount)
