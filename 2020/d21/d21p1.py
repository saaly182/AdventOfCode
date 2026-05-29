#!/usr/bin/python3

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

# create a set of all possible ingredients with allergens
possible_allergy_ingredients = set()
for a in alookup:
  possible_allergy_ingredients.update(alookup[a])

non_allergy_ingredients = iset - possible_allergy_ingredients

answer = sum([icount[x] for x in icount if x in non_allergy_ingredients])

print(answer)
