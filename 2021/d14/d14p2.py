#!/usr/bin/python3 -u

debug = False

import collections

ifile = 'input.txt'

def update_paircounts(paircounts, patterns):
  newpc = collections.defaultdict(int)
  for pair in paircounts:
    insletter = patterns[pair]
    count = paircounts[pair]
    lpair = pair[0] + insletter
    rpair = insletter + pair[1]
    newpc[lpair] += count
    newpc[rpair] += count
  return newpc

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

  steps = 40

  p = tmpl
  paircounts = collections.defaultdict(int)
  for i in range(len(p) - 1):
    pair = p[i] + p[i + 1]
    paircounts[pair] += 1

  for i in range(steps):
    paircounts = update_paircounts(paircounts, patterns)

  lettercounts = collections.defaultdict(int)
  for pair, count in paircounts.items():
    lettercounts[pair[0]] += count

  # last letter in the template needs one more count
  lettercounts[tmpl[-1]] += 1

  lcvals = lettercounts.values()
  answer = max(lcvals) - min(lcvals)
  print(answer)


if __name__ == '__main__':
  main()
