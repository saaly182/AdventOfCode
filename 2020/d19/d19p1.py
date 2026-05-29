#!/usr/bin/python3

import re

rules = {}
msgs = []

with open('input.txt', 'r') as f:
  for line in f:
    line = line.rstrip()

    if not line:
      continue

    if line.find(':') == -1:
      msgs.append(line)
    else:
      rnum, _, rule = line.partition(':')
      rule = rule.split()
      if rule[0] == '"a"':
        rule[0] = 'a'
      if rule[0] == '"b"':
        rule[0] = 'b'
      if rule.count('|') == 1:
        rule.insert(0, '(')
        rule.append(')')
      rules[rnum] = rule

bigrule = rules['0']
still_working = True
while still_working:
  still_working = False
  newrule = []
  for x in bigrule:
    if x.isdigit():
      newrule.extend(rules[x])
      still_working = True
    else:
      newrule.append(x)

  bigrule = newrule

bigre = re.compile('^' + ''.join(bigrule) + '$')
valid_msgs = [x for x in msgs if bigre.match(x)]
print(len(valid_msgs))
