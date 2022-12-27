#!/usr/bin/python3 -u

debug = False


class Chamber():
  # 0=space, 1=falling rock, 2=fixed rock, 3=wall/floor
  def __init__(self, getjet, getrock, lookback=None):
    self.getjet = getjet
    self.getrock = getrock
    self.width = 7
    self.cmap = [[3] * (self.width + 2)]  # start with just the floor
    self.empty_row = [3] + [0] * self.width + [3]
    self.highrock = 0

    # part 2 cycle bits
    self.lookback = lookback
    self.rocktype = None
    self.jetidx = None
    self.seen = {}
    self.cycle_found = False
    self.rockcount = 0

    # rock bits
    self.rock = None
    self.rockrow = None  # index of the rock's lowest row
    self.rockheight = None

  def show(self, msg=None, always_show=False):
    if not debug and not always_show:
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
    self.rockcount += 1

  def pushrock(self):
    "Push the rock left or right, if possible."
    jetinfo = next(self.getjet)
    jetdir = jetinfo[0]
    self.jetidx = jetinfo[1]
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

  def detect_cycles(self):
    'Update class state once a cycle is found.'
    if self.cycle_found:
      return

    if len(self.cmap) < self.lookback:
      return

    k = (
        self.rocktype,
        self.jetidx,
        tuple(tuple(row) for row in self.cmap[-self.lookback:])
    )
    if k not in self.seen:
      self.seen[k] = (self.highrock, self.rockcount)
    else:
      self.cycle_found = True
      highrock2 = self.highrock
      rockcount2 = self.rockcount
      highrock1, rockcount1 = self.seen[k]
      # per-cycle increments
      hradd = highrock2 - highrock1
      rcadd = rockcount2 - rockcount1
      # now use cycles to increase height and rocks dropped
      rocksleft = self.num - self.rockcount
      cycles_needed = rocksleft // rcadd
      self.highrock_cycles = hradd * cycles_needed
      self.rockcount_cycles = rcadd * cycles_needed
      # account for rocks dropped in the cycles
      self.rockcount += self.rockcount_cycles

  def droprocks(self, num):
    self.num = num
    while self.rockcount < self.num:
      self.droprock(next(self.getrock))

    # ugly hack: patch up highrock after dropping all the rocks if
    # we used a cycle.
    if self.cycle_found:
      self.highrock += self.highrock_cycles

  def droprock(self, rockinfo):
    self.rock = rockinfo[0]
    self.rocktype = rockinfo[1]
    self.rockheight = len(self.rock)

    # setup the next rock to fall
    self.addbuffer()
    self.addrock()

    # watch for cycles
    if self.lookback and not self.cycle_found:
      self.detect_cycles()

    # now let this rock move and fall
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
    self.show('rock just fixed in place', always_show=False)

    # update highrock
    rocktop = self.rockrow + self.rockheight - 1
    if rocktop > self.highrock:
      self.highrock = rocktop

# end class Chamber


def part1(jet_pattern):
  c = Chamber(jetgen(jet_pattern), rockgen())
  c.droprocks(2022)
  return c.highrock


def part2(jet_pattern):
  c = Chamber(jetgen(jet_pattern), rockgen(), 100)  # use a lookback
  trillion = 1_000_000_000_000
  c.droprocks(trillion)
  assert c.highrock == 1514285714288 or c.highrock == 1560932944615
  return c.highrock


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
    for i, rock in enumerate(rocks):
      yield rock, i


def jetgen(jpattern):
  while True:
    for i, j in enumerate(jpattern):
      yield j, i


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
    print("Part 2 answer =", part2(jet_pattern))
    print()


if __name__ == '__main__':
  main()
