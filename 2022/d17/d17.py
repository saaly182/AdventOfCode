#!/usr/bin/python3 -u

debug = False

class Chamber():
  # 0=space, 1=falling rock, 2=fixed rock, 3=wall/floor
  def __init__(self, getjet):
    self.getjet = getjet
    self.width = 7
    self.cmap = [[3] * (self.width + 2)]  # start with just the floor
    self.empty_row = [3] + [0] * self.width + [3]
    self.highrock = 0

    self.rock = None
    self.rockrow = None  # index of the rock's lowest row
    self.rockheight = 0

  def show(self, msg=None):
    if not debug:
      return

    print('--')
    if msg:
      print(msg)
    for row in reversed(self.cmap):
      rs = ''.join(['.@#|'[i] for i in row])
      print(rs)
    print('--')

  def rockrange(self):
    return range(self.rockrow, self.rockrow + self.rockheight)

  def addbuffer(self):
    # ensure three, and only three, rows of space above highest rock
    self.cmap[self.highrock + 1:] = []
    for i in range(3):
      self.cmap.append(self.empty_row.copy())

  def addrock(self):
    self.rockrow = len(self.cmap)
    for x in reversed(self.rock):
      row = [3, 0, 0] + list(x) + [0] * (self.width - len(x) - 2) + [3]
      self.cmap.append(row)

  def pushrock(self):
    "Push the rock left or right, if possible."
    jetdir = next(self.getjet)
    self.show(f'pushrock in, pushing {jetdir}')
    assert jetdir in ('<', '>')
    incr = 1
    if jetdir == '<':
      incr = -1
    # check if we can move first, then move if possible; not efficient,
    # so consider refactoring
    can_move = True
    for row in self.rockrange():
      maprow1 = self.cmap[row]
      for i, x in enumerate(maprow1):
        if x == 1 and maprow1[i + incr] not in (0, 1):
          can_move = False
          break
    if can_move:
      for row in self.rockrange():
        maprow1 = self.cmap[row]
        maprow2 = maprow1.copy()
        for i, x in enumerate(maprow1):
          if x == 1:
            maprow2[i] = 0
        for i, x in enumerate(maprow1):
          if x == 1:
            maprow2[i + incr] = 1
        self.cmap[row] = maprow2
    self.show('pushrock out')

  def fallrock(self):
    'Try to move rock down one row. Return True if successful, otherwise False.'
    self.show('falling in')
    # check if we can fall first, then fall if possible; not efficient,
    # so consider refactoring
    for row in self.rockrange():
      maprow1 = self.cmap[row]
      maprow2 = self.cmap[row - 1]  # row below
      for i, x in enumerate(maprow1):
        if x == 1 and maprow2[i] not in (0, 1):
          # cannot fall, return False now
          self.show('falling out')
          return False
    for row in self.rockrange():
      maprow1 = self.cmap[row]
      maprow2 = self.cmap[row - 1]
      for i, x in enumerate(maprow1):
        if x == 1:
          maprow1[i] = 0
          maprow2[i] = 1
    self.rockrow -= 1
    self.show('falling out')
    return True

  def droprock(self, rock):
    self.rock = rock
    self.rockheight = len(rock)

    self.addbuffer()
    self.addrock()
    while True:
      self.pushrock()
      if not self.fallrock():
        break

    # set this rock to fixed
    for row in self.rockrange():
      maprow1 = self.cmap[row]
      for i, x in enumerate(maprow1):
        if x == 1:
          maprow1[i] = 2
    self.show('rock just fixed in place')

    # update highrock
    rocktop = self.rockrow + self.rockheight - 1
    if rocktop > self.highrock:
      self.highrock = rocktop


def part1(jet_pattern):
  getjet = jetgen(jet_pattern)
  getrock = rockgen()
  c = Chamber(getjet)
  for i in range(2022):
    c.droprock(next(getrock))
  return c.highrock


def part2():
  return None


def rockgen():
  rocks = (
      ((1, 1, 1, 1),),

      ((0, 1, 0),
       (1, 1, 1),
       (0, 1, 0)),

      ((0, 0, 1),
       (0, 0, 1),
       (1, 1, 1)),

      ((1, ),
       (1, ),
       (1, ),
       (1, )),

      ((1, 1),
       (1, 1)),
  )
  while True:
    for rock in rocks:
      yield rock


def jetgen(jpattern):
  while True:
    for j in jpattern:
      yield j


def slurp(fname):
  with open(fname) as file:
    return [line.rstrip() for line in file.readlines()]


def main():
  sample_input = slurp('sample_input.txt')
  main_input = slurp('input.txt')

  for inp in (sample_input, main_input):
    assert len(inp) == 1
    jet_pattern = inp[0]
    print("Part 1 answer =", part1(jet_pattern))
    print("Part 2 answer =", part2())
    print()


if __name__ == '__main__':
  main()
