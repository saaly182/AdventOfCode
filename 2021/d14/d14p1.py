#!/usr/bin/python3 -u

debug = False
ifile = 'input.txt'

def lettercounts(s):
  counts = {}

  for c in s:
    if c in counts:
      counts[c] += 1
    else:
      counts[c] = 1

  return counts

def polyinsert(p, patterns):
  q = []
  plen = len(p)
  for i, letter in enumerate(p):
    q.append(letter)
    if i != (plen - 1):
      pair = letter + p[i + 1]
      q.append(patterns[pair])
  return ''.join(q)


def main():
  patterns = {}
  with open(ifile) as polyfile:
    for line in polyfile:
      line = line.rstrip()
      toks = line.split()
      if len(toks) == 1:
        tmpl = toks[0]
      if len(toks) == 3:
        patterns[toks[0]] = toks[2]
  if debug:
    print(f'tmpl = {tmpl}')
    print(f'patterns = {patterns}')

  steps = 10

  p = tmpl
  for i in range(steps):
    p = polyinsert(p, patterns)

  c = lettercounts(p)
  cv = c.values()
  answer = max(cv) - min(cv)
  print(answer)


if __name__ == '__main__':
  main()
