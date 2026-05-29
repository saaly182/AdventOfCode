#!/usr/bin/python3

import string
import sys
sys.path.append('../../lib')

from multiline_record import multiline_file

letters = set(string.ascii_lowercase)
running_sum = 0

for record in multiline_file('input.txt'):
  qcounts = {}
  for c in record:
    if c in letters:
      if c not in qcounts:
        qcounts[c] = 1

  running_sum += sum(qcounts.values())

print(running_sum)
