#!/usr/bin/python3

import math

def fuel_needed(mass):
  this_fuel = max(math.floor((mass / 3.0)) - 2, 0)
  if this_fuel == 0:
    return 0
  else:
    return this_fuel + fuel_needed(this_fuel)

masses = []

with open('input.txt', 'r') as f:
  for line in f:
    line = line.rstrip()
    masses.append(int(line))

answer = sum([fuel_needed(m) for m in masses])
print(answer)
