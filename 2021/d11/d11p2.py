#!/usr/bin/python3 -u

from d11p1 import *

debug = False

def all_flashed(octopuses):
  '''Return true if all the octopuses flashed this step.'''
  for octrow in octopuses:
     for octo in octrow:
       if octo.energy != 0:
         return False
  return True

def main():
  energies = []
  octopuses = []
  with open('input.txt') as ofile:
    for line in ofile:
      line = line.rstrip()
      energies.append([int(x) for x in line])

  rowlen = len(energies)
  collen = len(energies[0])

  for row in range(rowlen):
    octrow = []
    for col in range(collen):
      thisoct = Octopus(energies[row][col], row, col)
      octrow.append(thisoct)
    octopuses.append(octrow)

  for row in range(rowlen):
    for col in range(collen):
      octopuses[row][col].add_neighbors([octopuses[r][c] for r, c in neighbors(row, col, rowlen, collen)])

  if debug:
    showoctgrid(octopuses)
  i = 0
  while not all_flashed(octopuses):
    takestep(octopuses)
    i += 1
    if debug:
      showoctgrid(octopuses)

  answer = i
  print(answer)


if __name__ == '__main__':
  main()
