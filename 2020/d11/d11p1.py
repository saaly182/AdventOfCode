#!/usr/bin/python3

import copy

def show_map(M):
  print('-------------map-----------------')
  for row in M:
    print(''.join(row))


def update_map(M):
  neighbors = (
      (-1, -1),
      (-1,  0),
      (-1,  1),
      ( 0, -1),
      ( 0,  1),
      ( 1, -1),
      ( 1,  0),
      ( 1,  1),
  )

  A = copy.deepcopy(M)

  # add ghost rows and cols to A to make boundary conditions easier
  rlen = len(M[0]) + 2
  for row in A:
    row.insert(0, '.')
    row.append('.')
  A.insert(0, ['.'] * rlen)
  A.append(['.'] * rlen)

  for r in range(len(M)):
    for c in range(len(M[0])):
      if A[r + 1][c + 1] == 'L':
        take = True
        for n in neighbors:
          if A[r + 1 + n[0]][c + 1 + n[1]] == '#':
            take = False
            break
        if take:
          M[r][c] = '#'

      if A[r + 1][c + 1] == '#':
        ncount = 0
        for n in neighbors:
          if A[r + 1 + n[0]][c + 1 + n[1]] == '#':
            ncount += 1
        if ncount > 3:
          M[r][c] = 'L'


def count_filled_seats(M):
  return(sum([x.count('#') for x in M]))


M = []
with open('input.txt', 'r') as f:
  for line in f:
    line = line.rstrip()
    M.append([x for x in line])

while True:
  Msnapshot = copy.deepcopy(M)
  update_map(M)
  if M == Msnapshot:
    break

print(count_filled_seats(M))
