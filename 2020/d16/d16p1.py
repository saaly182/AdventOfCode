#!/usr/bin/python3

import re

istate = 'rules'
rules_in = []
tnums = []

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
      m = re.fullmatch(r'.*: (\d+)-(\d+) or (\d+)-(\d+)', line)
      if not m:
        raise InputError
      rules_in.append((int(m.group(1)), int(m.group(2))))
      rules_in.append((int(m.group(3)), int(m.group(4))))

    if istate == 'nearby_tickets':
      tnums.extend([int(x) for x in line.split(',')])
      
rules_opt = []
rules_in.sort()
newrule = rules_in[0]
for r in rules_in[1:]:
  x1, x2 = newrule
  y1, y2 = r

  assert x1 <= x2 and y1 <= y2

  # case 1: this rule is inside the newrule
  if y1 >= x1 and y2 <= x2:
    continue

  # case 2: this rule starts inside newrule and extends it
  elif y1 >= x1 and y1 <= x2 and y2 > x2:
    newrule = (x1, y2)

  # case 3: this rule starts a new range
  elif y1 > x2:
    rules_opt.append(newrule)
    newrule = (y1, y2)

# we always have a pending rule to write
rules_opt.append(newrule)

invalids = []
for n in tnums:
  valid = False
  for r in rules_opt:
    x1, x2 = r
    if n >= x1 and n <= x2:
      valid = True
      break
  if not valid:
    invalids.append(n)

print(sum(invalids))
