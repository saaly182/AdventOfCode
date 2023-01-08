#!/usr/bin/python3 -u

import collections


class Grid:
  """A grid of elves.
  """
  # class vars
  neighbor_spots = (
      (-1, 0), (-1, 1), (0, 1), (1, 1),
      (1, 0), (1, -1), (0, -1), (-1, -1))

  adj_spots = {
      'N': ((-1, -1), (-1, 0), (-1, 1)),
      'S': ((1, -1), (1, 0), (1, 1)),
      'W': ((-1, -1), (0, -1), (1, -1)),
      'E': ((-1, 1), (0, 1), (1, 1))}

  d_move = {
      'N': (-1,  0),
      'S': ( 1,  0),
      'W': ( 0, -1),
      'E': ( 0,  1)}

  def __init__(self, inp):
    self.dorder = list('NSWE')
    self.elves = set()
    for r, s in enumerate(inp):
      for c in [x for x, v in enumerate(s) if v == '#']:
        self.elves.add((r, c))

  def bounds(self):
    r = [r for r, c in self.elves]
    c = [c for r, c in self.elves]
    return min(r), min(c), max(r), max(c)

  def show(self):
    print('-' * 50)
    minr, minc, maxr, maxc = self.bounds()
    for r in range(minr, maxr + 1):
      for c in range(minc, maxc + 1):
        if (r, c) in self.elves:
          print('#', end='')
        else:
          print('.', end='')
      print()
    print()

  def cycle_dorder(self):
    self.dorder.append(self.dorder.pop(0))

  def execute_rounds(self, n):
    for i in range(n):

      # build proposals
      proposals = collections.defaultdict(list)
      for elf in self.elves:
        r, c = elf
        if self.no_neighbors(elf):
          proposals[elf].append(elf)  # stay put
        else:
          for d in self.dorder:
            can_move = True
            for spot in Grid.adj_spots[d]:
              if (r + spot[0], c + spot[1]) in self.elves:
                can_move = False
                break
            if can_move:
              desired_spot = (r + Grid.d_move[d][0], c + Grid.d_move[d][1])
              proposals[desired_spot].append(elf)
              break
          if not can_move:  # never found a possible direction
            proposals[elf].append(elf)  # stay put

      # process proposals
      for spot, who in proposals.items():
        if len(who) > 1:
          continue
        if spot != who[0]:
          self.elves.remove(who[0])
          self.elves.add(spot)

      # shift the direction evaluation order
      self.cycle_dorder()

  def no_neighbors(self, elf):
    'Return True if elf has no neighbors.'
    r, c = elf
    for ns in Grid.neighbor_spots:
      if (r + ns[0], c + ns[1]) in self.elves:
        return False
    return True

  def empty_tile_count(self):
    minr, minc, maxr, maxc = self.bounds()
    etc = (maxr - minr + 1) * (maxc - minc + 1) - len(self.elves)
    return etc


def part1(inp):
  g = Grid(inp)
  g.execute_rounds(10)
  return g.empty_tile_count()


def part2():
  return None


def slurp(fname):
  with open(fname) as file:
    return [line.rstrip() for line in file.readlines()]


def main():
  sample_input = slurp('sample_input.txt')
  main_input = slurp('input.txt')

  for inp in (sample_input, main_input):
    print("Part 1 answer =", part1(inp))
    print("Part 2 answer =", part2())
    print()


if __name__ == '__main__':
  main()
