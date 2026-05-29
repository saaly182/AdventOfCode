#!/usr/bin/python3

import string
import sys
sys.path.append('../../lib')

from multiline_record import multiline_file

letters = set(string.ascii_lowercase)
running_sum = 0

for record in multiline_file('input.txt'):
  lines = record.rstrip().split('\n')
  questions = [set(x) for x in lines]
  common_qs = set.intersection(*questions)
  running_sum += len(common_qs)

print(running_sum)
