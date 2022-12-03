#!/usr/bin/python3
"""
Libary to process input as blank-line-separated multiline records.
"""

def multiline_file(filename):
  """
  Generator of multiline records that use one blank line as the
  record separator. Return each record as a string with newlines
  intact.
  """
  with open(filename, 'r') as f:
    R = ''
    for line in f:
      if line == '\n':
        yield R
        R = ''
      else:
        R += line
    if R:
      yield R


def main():
  for record in multiline_file('multiline_record_test_input'):
    print(repr(record))


if __name__ == "__main__":
    main()
