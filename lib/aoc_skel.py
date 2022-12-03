#!/usr/bin/python3 -u

debug = False
use_sample = True
SAMPLE_INPUTFILE = './sample_input.txt'
INPUTFILE = './input.txt'

def part1():
  return None


def part2():
  return None


def main():
  fname = INPUTFILE
  if use_sample:
    fname = SAMPLE_INPUTFILE

  with open(fname) as file:
    for line in file:
      line = line.rstrip()
      # do something with input

  print("Part 1 answer =", part1())
  print("Part 2 answer =", part2())


if __name__ == '__main__':
  main()
