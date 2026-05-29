#!/usr/bin/python3

import copy

def show_map(M):
  print('-------------map-----------------')
  for row in M:
    print(''.join(row))


def update_map(M):
  deltas = (
      (-1, -1),
      (-1,  0),
      (-1,  1),
      ( 0, -1),
      ( 0,  1),
      ( 1, -1),
      ( 1,  0),
      ( 1,  1),
  )

  # hold a non-changing copy of M
  A = copy.deepcopy(M)

  rmax = len(M) - 1
  cmax = len(M[0]) - 1

  for r in range(len(M)):
    for c in range(len(M[0])):

      thistile = A[r][c]

      if thistile != '.':
        sightlines = []
        for d in deltas:
          sightlines.append('.')
          r2, c2 = r + d[0], c + d[1]
          while r2 >= 0 and r2 <= rmax and c2 >= 0 and c2 <= cmax:
            tile = A[r2][c2]
            if tile != '.':
              sightlines[-1] = tile
              break
            r2, c2 = r2 + d[0], c2 + d[1]

      if thistile == 'L' and sightlines.count('#') == 0:
        M[r][c] = '#'
      elif thistile == '#' and sightlines.count('#') > 4:
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
