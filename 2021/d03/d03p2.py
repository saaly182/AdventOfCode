#!/usr/bin/python3

def diagfilter(L, pos, ftype):
  '''
  Return a new list of bitstrings matching the filter.

  L: list of bitstrings
  pos: position to consider
  ftype: filter type, one of 'most common' or 'least common'
  '''

  if ftype not in ('most common', 'least common'):
    raise ValueError(ftype)

  count0 = 0
  count1 = 0
  for b in L:
    check_bit = b[pos]
    assert check_bit == '0' or check_bit == '1'
    if b[pos] == '0':
      count0 += 1
    else:
      count1 += 1

  # most-common-value, least-common-value
  mcv = lcv = -999
  if count0 > count1:
    mcv = 0
    lcv = 1
  elif count1 > count0:
    mcv = 1
    lcv = 0
  else:
    mcv = 1
    lcv = 0

  mcv = str(mcv)
  lcv = str(lcv)

  if ftype == 'most common':
    out = [b for b in L if b[pos] == mcv]
  else:
    out = [b for b in L if b[pos] == lcv]

  return out


def get_one(L, ftype):
  a = L[:]
  for pos in range(len(L[0])):
    a = diagfilter(a, pos, ftype)
    if len(a) == 1:
      return a[0]
  assert False  # should never get here


all_nums = []

with open('input.txt', 'r') as diagfile:
  for line in diagfile:
    line = line.rstrip()
    all_nums.append(line)

oxy_gen = int(get_one(all_nums, 'most common'), 2)
co2_scrub = int(get_one(all_nums, 'least common'), 2)
answer = oxy_gen * co2_scrub
print(answer)
