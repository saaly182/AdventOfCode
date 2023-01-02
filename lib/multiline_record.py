#!/usr/bin/python3
"""
Libary to process input as blank-line-separated multiline records.
"""

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
