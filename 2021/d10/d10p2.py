#!/usr/bin/python3

def syntaxerr(navline):
  'Return illegal char, or None if no syntax errors.'
  lifo = []
  ncmds = {
      ')' : '(',
      ']' : '[',
      '}' : '{',
      '>' : '<',
  }
  all_cmds = list(ncmds.keys()) + list(ncmds.values())

  for c in navline:
    assert c in all_cmds
    if c in ncmds.values():
      lifo.append(c)
    if c in ncmds:
      if len(lifo) == 0:
        return c
      cmatch = lifo.pop()
      if cmatch != ncmds[c]:
        return c

  return None


def complete(navline):
  'Return chars needed to correctly complete the line.'
  lifo = []
  ncmds = {
      '(' : ')',
      '[' : ']',
      '{' : '}',
      '<' : '>',
  }
  for c in navline:
    if c in ncmds:
      lifo.append(c)
    if c in ncmds.values():
      cmatch = lifo.pop()

  return ''.join([ncmds[x] for x in reversed(lifo)])


def getscore(cmpbits):
  svals = {
      ')': 1,
      ']': 2,
      '}': 3,
      '>': 4,
  }
  s = 0
  for c in cmpbits:
    s *= 5
    s += svals[c]
  return s


navlines = []

with open('input.txt') as navfile:
  for line in navfile:
    line = line.rstrip()
    navlines.append(line)

scores = []
for line in navlines:
  s = syntaxerr(line)
  if s is not None:
    continue
  cmpbits = complete(line)
  score = getscore(cmpbits)
  scores.append(score)

scores.sort()
middle_score = scores[len(scores) // 2]
answer = middle_score
print(answer)
