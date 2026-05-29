#!/usr/bin/python3 -u

hmap = []
risk_sum = 0

with open('input.txt') as heightmap:
  for line in heightmap:
    line = line.rstrip()
    hmap.append([int(x) for x in line])

rmax = len(hmap) - 1
cmax = len(hmap[0]) - 1

for row in range(rmax + 1):
  for col in range(cmax + 1):
    hn = hs = he = hw = 999
    h = hmap[row][col]
    if row > 0:
      hn = hmap[row - 1][col]
    if row < rmax:
      hs = hmap[row + 1][col]
    if col > 0:
      hw = hmap[row][col - 1]
    if col < cmax:
      he = hmap[row][col + 1]

    if h < min(hn, hs, he, hw):
      # found a low point
      risk_level = h + 1
      risk_sum += risk_level

answer = risk_sum
print(answer)
