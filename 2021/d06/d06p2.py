#!/usr/bin/python3 -u
#
# Have to switch to dynamic programming for p2.
#

debug = True

import functools

@functools.lru_cache(maxsize=None)
def fishcounts(ifish, n):
  """
  Return a list of size 9 with the number of fish in each state
  (0..8) after n days. Memoized with lru_cache.

  Args:
    ifish: int 0..8; initial state of the first fish
    n: number of days to let grow
  """

  # base case
  if n == 0:
    fc = [0] * 9
    fc[ifish] = 1
    return fc

  # generic case
  # "a" means "after"
  # "b" means "before"
  fc_b = fishcounts(ifish, n - 1)
  fc_a = fc_b[1:] + [0]
  fc_a[6] += fc_b[0]
  fc_a[8] = fc_b[0]
  return fc_a

istates = []

with open('input.txt') as fishfile:
  for line in fishfile:
    line = line.rstrip()
    istates.extend([int(x) for x in line.split(',')])

total = 0
days = 256
for fish in istates:
  total += sum(fishcounts(fish, days))

answer = total
print(answer)
