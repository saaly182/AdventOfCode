#!/usr/bin/python3

import itertools

n = []
with open('input.txt', 'r') as xmas:
  for line in xmas:
    n.append(int(line))

# Find a contiguous sequence in n of two or more numbers that sum to
# 104054607.  Report the sum of the min and max numbers in that
# sequence.

w = 2  # width
L = len(n)
X = 104054607

found = False
while w <= L and not found:
  for begin in range(0, L - w + 1):
    seq = n[begin:begin + w]
    if sum(seq) == X:
      found = True
      answer = min(seq) + max(seq)
      print(answer)
      break
  w += 1
