#!/usr/bin/python3 -u

import string
import textwrap


def make_graph(hm):
  'Return adjacency graph of hm.'
  G = {}

  for row, col in hm:
    edges = []
    val = hm[(row, col)]
    for adj in (row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1):
      if adj in hm:
        if hm[adj] - val <= 1:  # can't go up more than one unit
          edges.append(adj)
    G[(row, col)] = tuple(edges)

  return G


def shortest_path(hm, start_v, end_v):
  'Return shortest path in the heightmap from start_v to end_v.'
  G = make_graph(hm)

  # now use Dijkstra's algorithm
  # based on https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Pseudocode
  dist = {}
  prev = {}
  queue = set(G)
  for p in G:  # p = point
    dist[p] = float('inf')
  dist[start_v] = 0

  while queue:
    # NOTE: This is a totally brute force min-priority-queue, but it works.
    # I probably won't come back and redo this, because it requires a min-
    # priority-queue with decrease_key functionality for dijkstra.
    min_dist = float('inf')
    for p in queue:
      if dist[p] < min_dist:
        min_dist = dist[p]
        u = p
    if min_dist == float('inf'):
      return None
    if u == end_v:
      break
    queue.remove(u)

    for v in G[u]:
      if v in queue:
        alt = dist[u] + 1
        if alt < dist[v]:
          dist[v] = alt
          prev[v] = u

  # construct the path from start to end, inclusive
  path = []
  u = end_v
  while u != start_v:
    path.append(u)
    u = prev[u]
  path.append(start_v)
  path.reverse()

  return path


def part1(hm, start_v, end_v):
  path = shortest_path(hm, start_v, end_v)
  # path includes start and end, but problem wants the
  # number of steps, so subtract 1 from path length.
  return len(path) - 1


def part2(hm, end_v):
  min_pathlen = float('inf')
  for p in hm:
    if hm[p] == 1:  # 'a'
      path = shortest_path(hm, p, end_v)
      if path:
        pathlen = len(path) - 1
        min_pathlen = min(pathlen, min_pathlen)

  return min_pathlen


def make_heightmap(inp):
  hm = {}
  row = 0
  start_v = end_v = None

  for line in inp:
    col = 0
    for c in line:
      if c in string.ascii_lowercase:
        val = ord(c) - ord('a') + 1
      elif c == 'S':
        val = 1   # 'a'
        start_v = (row, col)
      elif c == 'E':
        val = 26  # 'z'
        end_v = (row, col)
      else:
        raise ValueError
      hm[(row, col)] = val
      col += 1
    row += 1

  return hm, start_v, end_v


def main():
  sample_input = textwrap.dedent('''\
      Sabqponm
      abcryxxl
      accszExk
      acctuvwj
      abdefghi
  ''').rstrip().split('\n')

  main_input = []
  with open('input.txt') as file:
    for line in file:
      line = line.rstrip()
      main_input.append(line)

  for inp in (sample_input, main_input):
    hm, start_v, end_v = make_heightmap(inp)
    print("Part 1 answer =", part1(hm, start_v, end_v))
    print("Part 2 answer =", part2(hm, end_v))


if __name__ == '__main__':
  main()
