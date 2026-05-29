#!/usr/bin/python3

import re

istate = 'rules'
rules = {}
tickets = []
my_ticket = None

# store the input
with open('input.txt', 'r') as f:
  for line in f:
    line = line.rstrip()
    if not line:
      continue
    if line == 'your ticket:':
      istate = 'your_ticket'
      continue
    if line == 'nearby tickets:':
      istate = 'nearby_tickets'
      continue

    if istate == 'rules':
      # ex: "departure station: 41-578 or 594-962"
      m = re.fullmatch(r'(.*): (\d+)-(\d+) or (\d+)-(\d+)', line)
      if not m:
        raise InputError
      rules[m.group(1)] = (
          (int(m.group(2)), int(m.group(3))),
          (int(m.group(4)), int(m.group(5)))
      )

    if istate == 'your_ticket':
     my_ticket = tuple([int(x) for x in line.split(',')])

    if istate == 'nearby_tickets':
     tickets.append(tuple([int(x) for x in line.split(',')]))
      
# weed out the invalid tickets
valid_tickets = [my_ticket]
all_rules = [x[0] for x in rules.values()] + [x[1] for x in rules.values()]

for t in tickets:
  valid_tick = True
  for n in t:
    valid_num = False
    for r in all_rules:
      x1, x2 = r
      if n >= x1 and n <= x2:
        valid_num = True
        break
    if not valid_num:
      valid_tick = False
  if valid_tick:
    valid_tickets.append(t)

# figure out the possible fields
fcount = len(rules)
possible_fields = [set(rules.keys()) for dummy in range(fcount)]
for t in valid_tickets:
  for i in range(fcount):
    n = t[i]
    for r in possible_fields[i].copy(): # use .copy() b/c we cannot change the thing being iterated
      x1, x2 = rules[r][0]
      x3, x4 = rules[r][1]
      complies = (n >= x1 and n <= x2) or (n >= x3 and n <= x4)
      if not complies:
        possible_fields[i].remove(r)

# trim down possible fields by elimination
while sum([len(x) for x in possible_fields]) != fcount:
  fixed = set()
  for p in possible_fields:
    if len(p) == 1:
      fixed.add(max(p)) # using max() to get the one elem in the set
  for p in possible_fields:
    if len(p) > 1:
      p.difference_update(fixed)

# now we have the unique order of field names
field_order = [max(p) for p in possible_fields]

soln = 1
for i in range(fcount):
  if field_order[i].startswith('departure'):
    soln *= my_ticket[i]

print(soln)
