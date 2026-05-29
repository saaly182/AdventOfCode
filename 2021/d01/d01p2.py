#!/usr/bin/python3 -u

with open('input.txt', 'r') as depthfile:
  firstwindow = True
  incr_count = 0
  line1 = depthfile.readline()
  d1 = int(line1.rstrip())
  line2 = depthfile.readline()
  d2 = int(line2.rstrip())
  for line3 in depthfile:
    d3 = int(line3.rstrip())
    depth = d1 + d2 + d3
    if firstwindow:
      firstwindow = False
    else:
      delta = depth - depth_prev
      if delta > 0:
        incr_count += 1
    depth_prev = depth
    d1 = d2
    d2 = d3

print(incr_count)
