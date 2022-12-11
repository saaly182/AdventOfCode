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


def multiline_data(iterable):
  """
  Generator of multiline records that use blank elements as the
  record separator. Return each record as a tuple of strings,
  and treat all blank lines as non-records.
  """
  R = []
  for x in iterable:
    if x.strip() == '':
      if R:
        yield tuple(R)
        R = []
    else:
      R.append(x)
  if R:
    yield tuple(R)


class TestMultilineFile(unittest.TestCase):
  # Note: I'm intentionally just using a simple test input file
  # and not doing things like mocking open().
  def test_mlf(self):
    testdir = pathlib.Path(__file__).parent
    testfile = testdir / 'multiline_record_test_input'
    records = tuple(multiline_file(testfile))
    self.assertEqual(records,
        ('apple\nbanana\ncherry\n',
         'x y z\n1 2 3\n',
         'whitespace on next line\n \n',
         'next one\n',
         'arga arga\n',
         'final line with no following blank line\n'))


class TestMultilineData(unittest.TestCase):
  def test_mld(self):
    testdata = [
        'index 0:',
        'gilligan',
        'skipper',
        '',
        'index 1:'
        'maryann',
        'ginger',
        '',
        'index 2:'
        'professor',
        'mr. howell',
        'mrs howell',
    ]
    records = tuple(multiline_data(testdata))
    self.assertEqual(records,
        (('index 0:', 'gilligan', 'skipper'),
         ('index 1:' 'maryann', 'ginger'),
         ('index 2:' 'professor', 'mr. howell', 'mrs howell')))


if __name__ == "__main__":
    unittest.main()
