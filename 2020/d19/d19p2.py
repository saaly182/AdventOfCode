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

# As you look over the list of messages, you realize your matching rules
# aren't quite right. To fix them, completely replace rules 8: 42 and 11:
# 42 31 with the following:
# 
# 8: 42 | 42 8
# 11: 42 31 | 42 11 31
rules['8'] = ['(', '42', ')', '+']

# rule 11 requires recursion, so it's not a true regular expression. Some
# libraries do provide "recursive regex" functionality, like PCRE and the
# non-standard python "regex" module. But it looks like people just did a
# practical approach an manually included a number of hardcoded alternations
# of rule 11 to get the proper balancing. I'm doing that here, too.
r11 = []
# range 1..10 is completely arbritrary choice
for i in range(1, 11):
  r11.append('( 42 ) {{{}}} ( 31 ) {{{}}}'.format(i, i))

r11str = '( ' + ' | '.join(r11) + ' )'
rules['11'] = r11str.split()

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
