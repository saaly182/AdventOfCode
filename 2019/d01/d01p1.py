#!/usr/bin/python3

import math

def fuel_needed(mass):
  return math.floor((mass / 3.0)) - 2


masses = []

with open('input.txt', 'r') as f:
  for line in f:
    line = line.rstrip()
    masses.append(int(line))

answer = sum([fuel_needed(m) for m in masses])
print(answer)
