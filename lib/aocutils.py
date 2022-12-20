#!/usr/bin/python3
"""
Various utility functions for AoC
"""

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


class TestDrange(unittest.TestCase):
  def test_drange(self):
    x = list(drange(3, 6))
    self.assertEqual(x, [3, 4, 5, 6])
    x = list(drange(7, 2))
    self.assertEqual(x, [7, 6, 5, 4, 3, 2])
    x = list(drange(9, 9))
    self.assertEqual(x, [9])


if __name__ == "__main__":
    unittest.main()
