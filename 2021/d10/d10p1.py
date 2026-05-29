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

navlines = []

with open('input.txt') as navfile:
  for line in navfile:
    line = line.rstrip()
    navlines.append(line)

serrs = []
for line in navlines:
  s = syntaxerr(line)
  if s is not None:
    serrs.append(s)

errpoints = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

answer = sum([errpoints[x] for x in serrs])
print(answer)
