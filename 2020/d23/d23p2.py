#!/usr/bin/python3

def printcups(cups):
  print('-----')
  c = 1
  while True:
    print(c, end='')
    c = cups[c]
    if c == 1: break
  print('\n-----')


input=[int(x) for x in '716892543']
cups_total = 1000000
turns = 10000000
input.extend(range(10, cups_total + 1))

# make circular
input.append(input[0])

cups = {}
for i in range(len(input) - 1):
  cups[input[i]] = input[i + 1]

max_cup = max(input)

cur_cup = input[0]
for i in range(turns):
  # track the next 4
  n1 = cups[cur_cup]
  n2 = cups[n1]
  n3 = cups[n2]
  n4 = cups[n3]

  # slice out the next 3
  cups[cur_cup] = n4

  dest_cup = cur_cup - 1
  while dest_cup in (n1, n2, n3):
    dest_cup -= 1

  if dest_cup < 1:
    dest_cup = max_cup
    while dest_cup in (n1, n2, n3):
      dest_cup -= 1

  # slice in the three cups after the destination cup
  dc_next = cups[dest_cup]
  cups[dest_cup] = n1
  cups[n3] = dc_next

  cur_cup = cups[cur_cup]

n1 = cups[1]
n2 = cups[n1]

answer = n1 * n2

print(answer)
