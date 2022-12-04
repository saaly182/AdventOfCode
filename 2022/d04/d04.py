#!/usr/bin/python3 -u

import re

debug = False
use_sample = False
SAMPLE_INPUTFILE = './sample_input.txt'
INPUTFILE = './input.txt'


def fully_contains(ranges):
  a, b, c, d = ranges
  if (a >= c and b <= d) or (c >= a and d <= b):
    return True
  return False


def overlaps(ranges):
  a, b, c, d = ranges
  if b < c or d < a:
    return False
  return True


def part1(assignment_pairs):
  count = 0
  for ap in assignment_pairs:
    if fully_contains(ap):
      count += 1
  return count


def part2(assignment_pairs):
  count = 0
  for ap in assignment_pairs:
    if overlaps(ap):
      count += 1
  return count


def main():
  fname = INPUTFILE
  if use_sample:
    fname = SAMPLE_INPUTFILE

  assignment_pairs = []
  with open(fname) as file:
    for line in file:
      line = line.rstrip()
      match = re.fullmatch(r'(\d+)-(\d+),(\d+)-(\d+)', line)
      assert match
      section_ranges = tuple(int(x) for x in match.group(1, 2, 3, 4))
      assignment_pairs.append(section_ranges)

  print("Part 1 answer =", part1(assignment_pairs))
  print("Part 2 answer =", part2(assignment_pairs))


if __name__ == '__main__':
  main()
