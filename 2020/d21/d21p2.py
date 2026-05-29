#!/usr/bin/python3

def has_nonempty_elems(D):
  for i in D:
    if len(D[i]) > 0:
      return True
  return False

alookup = {}
aset = set()
iset = set()
icount = {}

with open('input.txt', 'r') as f:
  for line in f:
    line = line.rstrip().replace(')', '').replace(',', '')
    istr, _, astr = line.partition('(contains')
    allergens = astr.split()
    ingredients = istr.split()

    aset.update(allergens)
    iset.update(ingredients)

    for i in ingredients:
      if i in icount:
        icount[i] += 1
      else:
        icount[i] = 1

    for a in allergens:
      if a in alookup:
        alookup[a] = alookup[a].intersection(set(ingredients))
      else:
        alookup[a] = set(ingredients)

# now determine the actual allergy list in the ai (allergy-ingredient) dict
ai = {}
while has_nonempty_elems(alookup):
  for a in alookup:
    if len(alookup[a]) == 1:
      ai[a] = alookup[a].pop()
  for a in ai:
    for b in alookup:
      alookup[b].discard(ai[a])

answer = ','.join([ai[x] for x in sorted(ai.keys())])
print(answer)
