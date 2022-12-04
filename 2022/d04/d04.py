#!/usr/bin/python3 -u

import re

debug = False
use_sample = False
SAMPLE_INPUTFILE = './sample_input.txt'
INPUTFILE = './input.txt'


def fully_contains(r1, r2):
  "Return True if r1 or r2 is fully contained within the other."
  a, b, c, d = r1 + r2
  if (a >= c and b <= d) or (c >= a and d <= b):
    return True
  return False


def part1(assignment_pairs):
  count = 0

  for ap in assignment_pairs:
    if fully_contains((ap[0], ap[1]), (ap[2], ap[3])):
      count += 1
  
  return count


def part2():
  return None


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
  print("Part 2 answer =", part2())


if __name__ == '__main__':
  main()
