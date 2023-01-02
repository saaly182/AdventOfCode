#!/usr/bin/python3
"""
Tests
"""

from aocutils import *
import unittest


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
