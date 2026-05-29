#!/usr/bin/python3 -u

with open('input.txt', 'r') as depthfile:
  firstline = True
  incr_count = 0
  for line in depthfile:
    depth = int(line.rstrip())
    if firstline:
      firstline = False
    else:
      delta = depth - depth_prev
      if delta > 0:
        incr_count += 1
    depth_prev = depth
print(incr_count)
