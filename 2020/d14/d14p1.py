#!/usr/bin/python3

import re

ops = []
with open('input.txt', 'r') as f:
  for line in f:
    line = line.rstrip()
    if line.startswith('mask'):
      ops.append(('m', line.split()[2]))
    elif line.startswith('mem'):
      addr, value = [int(x) for x in re.findall(r'\d+', line)]
      ops.append(('w', addr, value))
    else:
      raise InputError

mem = {}

# used to keep 1s
mask_or = 0
# used to keep 0s
mask_and = int('1'*36, base=2)

for inst in ops:
  if inst[0] == 'm':
    mask = inst[1]
    mask_or = int(mask.replace('X','0'), base=2)
    mask_and = int(mask.replace('X','1'), base=2)
  elif inst[0] == 'w':
    addr, value = inst[1], inst[2]
    value |= mask_or
    value &= mask_and
    mem[addr] = value

print(sum(mem.values()))
