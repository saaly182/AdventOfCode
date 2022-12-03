#!/usr/bin/python3
"""
Libary to process input as blank-line-separated multiline records.
"""

import unittest
import pathlib


def multiline_file(filename):
  """
  Generator of multiline records that use blank lines as the
  record separator. Return each record as a string with newlines
  intact, and treat all blank lines as non-records.
  """
  with open(filename, 'r') as f:
    # R is the multiline record
    R = ''
    for line in f:
      if line == '\n':
        if R:
          yield R
          R = ''
      else:
        R += line
    if R:
      yield R


class TestMultilineFile(unittest.TestCase):
  # Note: I'm intentionally just using a simple test input file
  # and not doing things like mocking open().
  def test_mlf(self):
    testdir = pathlib.Path(__file__).parent
    testfile = testdir / 'multiline_record_test_input'
    records = list(multiline_file(testfile))
    self.assertEqual(records,
        ['apple\nbanana\ncherry\n',
         'x y z\n1 2 3\n',
         'whitespace on next line\n \n',
         'next one\n',
         'arga arga\n',
         'final line with no following blank line\n'])


if __name__ == "__main__":
    unittest.main()
