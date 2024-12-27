#!/usr/bin/python3 -u

import sys
sys.path.append('../../lib')
from multiline_record import multiline_file  # noqa: E402 F401

debug = False
use_sample = False
SAMPLE_INPUTFILE = './sample_input.txt'
INPUTFILE = './input.txt'


def make_cal_list(fname):
  elfcalories = []
  for record in multiline_file(fname):
    cals = sum([int(x) for x in record.split()])
    elfcalories.append(cals)
  return elfcalories


def part1(cal_list):
  return max(cal_list)


def part2(cal_list):
  return sum(sorted(cal_list, reverse=True)[:3])


def main():
  fname = INPUTFILE
  if use_sample:
    fname = SAMPLE_INPUTFILE

  cal_list = make_cal_list(fname)
  print("Part 1 answer =", part1(cal_list))
  print("Part 2 answer =", part2(cal_list))


if __name__ == '__main__':
  main()
