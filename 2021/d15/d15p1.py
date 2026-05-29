#!/usr/bin/python3 -u

class Cave:
  def __init__(self, cavefilename):
    self.risk = {}
    self.g = {}  # graph
    self.rmax = self.cmax = 0
    with open(cavefilename) as cavefile:
      r = 0
      for line in cavefile:
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

  def shortest_path(self, p1, p2):
    # See https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    # keyword: dijkstra
    infinity = 9_999_999_999_999
    unvisited = set(self.g.keys())
    d = {}
    for p in self.g:
      d[p] = infinity
    d[p1] = 0
    current = p1
    while p2 in unvisited:
      for neighbor in self.g[current]:
        if neighbor in unvisited:
          dc = d[current] + self.risk[neighbor]
          if dc < d[neighbor]:
            d[neighbor] = dc
      unvisited.remove(current)
      if unvisited:
        current = min(unvisited, key=d.get)
    return d[p2]


def main():
  cave = Cave('input.txt')
  sp = cave.shortest_path((0, 0), (cave.rmax, cave.cmax))
  print(sp)


if __name__ == '__main__':
  main()
