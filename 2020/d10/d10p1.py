#!/usr/bin/python3

data = []
with open('input.txt', 'r') as f:
  for line in f:
    data.append(int(line))

data.sort()
data.insert(0, 0)
data.append(max(data) + 3)
delta1 = 0
delta3 = 0
for i in range(1, len(data)):
    diff = data[i] - data[i - 1]
    if diff == 1:
      delta1 += 1
    elif diff == 3:
      delta3 += 1

print(delta1 * delta3)
