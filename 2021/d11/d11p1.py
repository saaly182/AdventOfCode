#!/usr/bin/python3 -u

debug = False

class Octopus:
  def __init__(self, energy, row, col):
    self.energy = energy
    self.row = row
    self.col = col
    self.neighbors = []
    self.in_step = False
    self.flashcount = 0


  def add_neighbors(self, ns):
    'Add the list of new neighbors'
    self.neighbors.extend(ns)


  def incr_energy(self):
    self.energy += 1
    if self.energy == 10:
      self.flash_myself()


  def step_begin(self):
    self.in_step = True
    self.incr_energy()


  def step_end(self):
    self.in_step = False
    if self.energy > 9:
      self.energy = 0


  def flash_myself(self):
    if debug:
      print(f'Octopus at {self.row}, {self.col} flashing!')
    self.flashcount += 1
    for n in self.neighbors:
      n.receive_flash()


  def receive_flash(self):
    if debug:
      print(f'Octopus at {self.row}, {self.col} received flash.')
    self.incr_energy()


def neighbors(row, col, rowlen, collen):
  '''Return a list of r,c tuples of neighoring cells.'''
  # Corners only have three neighbors.
  # Other boundary points only have five neighbors.
  # Interior points have eight neighbors.
  n = [
      ((row - 1), (col + 0)), # N
      ((row - 1), (col + 1)), # NE
      ((row + 0), (col + 1)), # E
      ((row + 1), (col + 1)), # SE
      ((row + 1), (col + 0)), # S
      ((row + 1), (col - 1)), # SW
      ((row + 0), (col - 1)), # W
      ((row - 1), (col - 1)), # NW
  ]

  # Fix N and W boundaries
  n = [x for x in n if x[0] >= 0 and x[1] >= 0]

  # Fix E and S boundaries
  n = [x for x in n if x[0] < rowlen and x[1] < collen]

  return n


def showoctgrid(octopuses):
  for octrow in octopuses:
    for octo in octrow:
      print(octo.energy, end='')
    print()


def takestep(octopuses):
  for octrow in octopuses:
    for octo in octrow:
      octo.step_begin()

  for octrow in octopuses:
    for octo in octrow:
      octo.step_end()


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
  for i in range(100):
    takestep(octopuses)
    if debug:
      showoctgrid(octopuses)

  total_flash = 0
  for octrow in octopuses:
    for octo in octrow:
      total_flash += octo.flashcount
      
  answer = total_flash
  print(answer)


if __name__ == '__main__':
  main()
