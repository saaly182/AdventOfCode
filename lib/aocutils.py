#!/usr/bin/python3
"""
Various utility functions for AoC
"""

import copy
import heapq
import math
import unittest


def drange(a, b):
  """
  Return a range between a and b inclusive regardless
  of which is larger.
  """
  if a <= b:
    dr = range(a, b + 1)
  else:
    dr = range(a, b - 1, -1)
  return dr


def merge_intervals(input_intervals):
  """
  Return a list of the merged set of the input intervals.

  Input: an iterable of [a, b] intervals, where a & b are ints and a <= b
  Based on https://www.geeksforgeeks.org/merging-intervals/
  """
  intervals = copy.deepcopy(input_intervals)  # don't change the input
  for i in intervals:
    assert len(i) == 2 and (i[0] <= i[1])
  intervals.sort()
  stack = []
  stack.append(intervals[0])
  for i in intervals[1:]:
    if stack[-1][0] <= i[0] <= stack[-1][1]:
      stack[-1][1] = max(stack[-1][1], i[1])
    else:
      stack.append(i)
  return stack


def shortest_paths(G, src):
  """
  Return distance and path info from src to all other vertices in the graph.

  Uses the "lazy" Dijkstra algorithm, which basically means the
  min-priority-queue does not have a decrease-key method. This is not space
  efficient, but AoC problems don't tend to have *huge* graphs.

  G structure: dict with vertex key and value of adjacency list with
  (vertex, edge length) elements.

  reference: http://nmamano.com/blog/dijkstra/dijkstra.html
  """
  dist = {}
  prev = {}
  seen = {}
  minq = []
  for v in G:
    dist[v] = math.inf
    seen[v] = False
  dist[src] = 0
  heapq.heappush(minq, (0, src))

  while minq:
    _, u = heapq.heappop(minq)
    if seen[u]:
      continue  # already seen this vertex
    seen[u] = True

    for v, e in G[u]:
      alt = dist[u] + e
      if alt < dist[v]:
        dist[v] = alt
        prev[v] = u
        heapq.heappush(minq, (alt, v))

  return dist, prev


###########################################################################


class TestDrange(unittest.TestCase):
  def test_drange(self):
    x = list(drange(3, 6))
    self.assertEqual(x, [3, 4, 5, 6])
    x = list(drange(7, 2))
    self.assertEqual(x, [7, 6, 5, 4, 3, 2])
    x = list(drange(9, 9))
    self.assertEqual(x, [9])


class TestMergeIntervals(unittest.TestCase):
  def test_merge_intervals(self):
    i1 = [[10, 20], [1, 5], [11, 21], [5, 8], [0, 1]]
    i2 = merge_intervals(i1)
    self.assertEqual(i2, [[0, 8], [10, 21]])
    i1 = [[10, 20], [-1, 5], [6, 6], [90, 99], [91, 98]]
    i2 = merge_intervals(i1)
    self.assertEqual(i2, [[-1, 5], [6, 6], [10, 20], [90, 99]])


class TestShortestPaths(unittest.TestCase):
  def test_shortest_paths(self):
    G = {
        'a': (('b', 1),),
        'b': (('a', 1),),
    }
    dist, prev = shortest_paths(G, 'a')
    self.assertEqual(dist, {'a': 0, 'b': 1})
    self.assertEqual(prev, {'b': 'a'})

    G = {
        'A': [('B', 1), ('C', 5)],
        'B': [('A', 1), ('D', 3)],
        'C': [('A', 5), ('D', 2), ('E', 7)],
        'D': [('C', 2), ('B', 3)],
        'E': [('C', 7), ('F', 8)],
        'F': [('E', 8)],
    }
    dist, prev = shortest_paths(G, 'A')
    self.assertEqual(dist, {'A': 0, 'B': 1, 'C': 5, 'D': 4, 'E': 12, 'F': 20})
    self.assertEqual(prev, {'B': 'A', 'C': 'A', 'D': 'B', 'E': 'C', 'F': 'E'})


if __name__ == "__main__":
    unittest.main()
