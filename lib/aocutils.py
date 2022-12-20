#!/usr/bin/python3
"""
Various utility functions for AoC
"""

import copy
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


if __name__ == "__main__":
    unittest.main()
