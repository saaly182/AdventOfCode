#!/usr/bin/python3

p1 = [14, 6, 21, 10, 1, 33, 7, 13, 25, 8, 17, 11, 28, 27, 50, 2, 35, 49, 19, 46, 3, 38, 23, 5, 43]

p2 = [18, 9, 12, 39, 48, 24, 32, 45, 47, 41, 40, 15, 22, 36, 30, 26, 42, 34, 20, 16, 4, 31, 37, 44, 29]

while len(p1) > 0 and len(p2) > 0:
  c1 = p1.pop(0)
  c2 = p2.pop(0)

  assert c1 != c2

  if c1 > c2:
    p1.extend((c1, c2))
  else:
    p2.extend((c2, c1))

if p1:
  winner = p1
else:
  winner = p2

winner.reverse()

answer = 0

for i in range(len(winner)):
  answer += (i + 1) * winner[i]

print(answer)
