#!/usr/bin/python3

brules = {}

def bagrules_dfs(cbag, csearch):
  global brules

  for count, c2 in brules[cbag]:
    if c2 == csearch:
      return True
    if bagrules_dfs(c2, csearch):
      return True

  return False


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

count = 0
for cbag in brules:
  if bagrules_dfs(cbag, 'shiny-gold'):
    count += 1
    print(cbag)

print(count)
