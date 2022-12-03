#!/usr/bin/python3 -u

import sys
sys.path.append('../../lib')

from multiline_record import multiline_file

debug = False
use_sample = False
SAMPLE_INPUTFILE = './sample_input.txt'
INPUTFILE = './input.txt'

def make_cal_list(fname):
  elfcalories = []
  for record in multiline_file('input.txt'):
    cals = sum([int(x) for x in record.split()])
    elfcalories.append(cals)
  return elfcalories


def part1(fname):
  return max(make_cal_list(fname))


def part2(fname):
  cal_list = make_cal_list(fname)
  cal_list.sort(reverse=True)
  return sum(cal_list[:3])


def main():
  fname = INPUTFILE
  if use_sample:
    fname = SAMPLE_INPUTFILE

  print("Part 1 answer =", part1(fname))
  print("Part 2 answer =", part2(fname))


if __name__ == '__main__':
  main()
