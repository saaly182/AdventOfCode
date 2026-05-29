#!/usr/bin/python3

import itertools

window = 25
n = []
with open('input.txt', 'r') as xmas:
  for line in xmas:
    n.append(int(line))

# Find first number than is not equal to the sum of a pair
# of numbers in the previous 25 numbers
for i in range(window, len(n)):
  x1 = n[i]
  prev = n[i - window:i]
  found = False
  for pair in itertools.combinations(prev, 2):
    if sum(pair) == x1:
      found = True
      break
  if not found:
    print(x1)
    break
