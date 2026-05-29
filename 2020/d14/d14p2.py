#!/usr/bin/python3

import itertools
import re

def make_addrs(addr, mask):
  ads = []
  mask_or = int(mask.replace('X','0'), base=2)
  xlocs = [z.start() for z in re.finditer(r'X', mask)]
  addr = '{:b}'.format(int(addr) | mask_or).zfill(len(mask))
  xcount = mask.count('X')
  for bs in itertools.product('01', repeat=xcount):
    a = list(addr)
    for i in range(len(bs)):
      a[xlocs[i]] = bs[i]
    a = int(''.join(a), base=2)
    ads.append(a)
  return ads


ops = []
with open('input.txt', 'r') as f:
  for line in f:
    line = line.rstrip()
    if line.startswith('mask'):
      ops.append(('m', line.split()[2]))
    elif line.startswith('mem'):
      addr, value = [x for x in re.findall(r'\d+', line)]
      ops.append(('w', addr, value))
    else:
      raise InputError

mem = {}

mask = 0
for inst in ops:
  if inst[0] == 'm':
    mask = inst[1]
  elif inst[0] == 'w':
    addr, value = inst[1], inst[2]

    for a in make_addrs(addr, mask):
      mem[a] = int(value)

print(sum(mem.values()))
