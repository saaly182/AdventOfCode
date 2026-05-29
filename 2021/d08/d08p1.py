#!/usr/bin/python3

# 1->2 segments, 4->4 segments, 7->3 segments, 8->7 segments
keep1478 = []

with open('input.txt') as digitsfile:
  for line in digitsfile:
    line = line.rstrip()
    signals_str, outputs_str = line.split('|')
    outputs = outputs_str.split()
    keep1478.extend([x for x in outputs if len(x) in (2, 4, 3, 7)])

answer = len(keep1478)
print(answer)
