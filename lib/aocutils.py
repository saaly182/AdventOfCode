#!/usr/bin/python3
"""
Various utility functions for AoC
"""

import copy
import heapq


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
  intervals = list(copy.deepcopy(input_intervals))  # don't change the input
  for i in intervals:
    assert len(i) == 2 and (i[0] <= i[1])
  intervals.sort()
  stack = [list(intervals[0])]
  for i in intervals[1:]:
    if stack[-1][0] <= i[0] <= stack[-1][1]:
      stack[-1][1] = max(stack[-1][1], i[1])
    else:
      stack.append(list(i))
  return stack


def shortest_paths(G, src):
  """
  Return distance and path info from src to all other vertices in the graph.

  Uses the "lazy" Dijkstra algorithm, which basically means the
  min-priority-queue does not have a decrease-key method. This is not space
  efficient, but AoC problems don't tend to have *huge* graphs.

  G structure: dict with vertex key and value of adjacency list with
  (vertex, edge length) elements.

  reference: https://nilmamano.com/blog/implementing-dijkstra
  """
  dist = {}
  prev = {}
  seen = {}
  minq = []
  for v in G:
    dist[v] = float('inf')
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
