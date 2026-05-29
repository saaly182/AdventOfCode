#!/usr/bin/python3 -u

debug = False

class Cave:
  def __init__(self, cavefilename):
    self.risk = {}
    self.g = {}  # graph
    self.rmax = self.cmax = 0

    cavemap = self._gencavemap(cavefilename)

    r = 0
    for line in cavemap:
      line = line.rstrip()
      for c, n in enumerate([int(x) for x in line]):
        self.risk[(r, c)] = n
        # just add all neighbors regardless of ghost points at this stage
        self.g[(r, c)] = [(r - 1, c), (r, c + 1), (r + 1, c), (r, c - 1)]
      self.rmax = r
      r += 1
    self.cmax = c

    # now patch up self.g by removing ghost points
    allp = set(self.g.keys())
    for p, neighbors in self.g.items():
      self.g[p] = tuple(allp.intersection(neighbors))

  def _gencavemap(self, cavefilename):
    cm = []

    # first expand the original input lines to the right
    with open(cavefilename) as cavefile:
      for line in cavefile:
        line = line.rstrip()
        mapline = []
        n1 = [int(x) for x in line]
        mapline.extend(n1)
        for i in range(1, 5):
          n2 = [(x - 1 + i) % 9 + 1 for x in n1]
          mapline.extend(n2)
        cm.append(mapline)

    # now expand the new lines down
    downlines = []
    for i in range(1, 5):
      for mapline in cm:
        downlines.append([(x - 1 + i) % 9 + 1 for x in mapline])
    cm.extend(downlines)

    cmstr = []
    for mapline in cm:
      cmstr.append(''.join([str(x) for x in mapline]))

    return cmstr

  def shortest_path(self, p1, p2):
    # See https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    # keyword: dijkstra
    infinity = 1_999_999_999
    unvisited = set(self.g.keys())
    unvisited_notinf = set()
    d = {}

    for p in self.g:
      d[p] = infinity
    d[p1] = 0
    unvisited_notinf.add(p1)
    current = p1

    while p2 in unvisited:
      if debug:
        uc = len(unvisited)
        if uc % 1000 == 0:
          print('current', current)
          print('unvisited count', uc)

      for neighbor in self.g[current]:
        if neighbor in unvisited:
          dc = d[current] + self.risk[neighbor]
          if dc < d[neighbor]:
            d[neighbor] = dc
            unvisited_notinf.add(neighbor)
      unvisited.remove(current)
      unvisited_notinf.remove(current)
      if unvisited:
        current = min(unvisited_notinf, key=d.get)

    return d[p2]


def main():
  cave = Cave('input.txt')
  sp = cave.shortest_path((0, 0), (cave.rmax, cave.cmax))
  print(sp)


if __name__ == '__main__':
  main()
