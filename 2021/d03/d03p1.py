#!/usr/bin/python3

import collections

bits = collections.defaultdict(list)

with open('input.txt', 'r') as diagfile:
  for line in diagfile:
    line = line.rstrip()
    for place, b in enumerate(line):
      bits[place].append(int(b))

gamma_list = []
epsilon_list = []
for place in sorted(bits):
  count0 = bits[place].count(0)
  count1 = bits[place].count(1)
  assert count0 != count1
  if count0 < count1:
    most_frequent = 1
    least_frequent = 0
  else:
    most_frequent = 0
    least_frequent = 1

  gamma_list.append(most_frequent)
  epsilon_list.append(least_frequent)

gamma = int(''.join([str(x) for x in gamma_list]), 2)
epsilon = int(''.join([str(x) for x in epsilon_list]), 2)
power_consumption = gamma * epsilon

print(power_consumption)
