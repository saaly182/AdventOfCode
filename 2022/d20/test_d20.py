#!/usr/bin/python3 -u

from d20 import *
import unittest



class TestGroveMessage(unittest.TestCase):
  def test_vals_from_zero(self):
    gm = GroveMessage([1, 2, -3, 3, -2, 0, 4])
    vs = gm.vals_from_zero([1000, 2000, 3000])
    self.assertEqual(vs, [4, -3, 2])

  def test_getmsg1(self):
    gm = GroveMessage([3, 2, 1])
    m = gm.getmsg()
    self.assertEqual(m, [2, 1, 3])

  def test_getmsg2(self):
    gm = GroveMessage([7, -4, 0, -8])
    m = gm.getmsg()
    self.assertEqual(m, [7, -8, 0, -4])


if __name__ == "__main__":
  unittest.main()
