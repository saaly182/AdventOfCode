#!/usr/bin/python3 -u

import copy
import re

debug = False
use_sample = False
SAMPLE_INPUTFILE = './sample_input.txt'
INPUTFILE = './input.txt'


def genstacks(slines):
  # info is easier to parse in transposed form with a stack on each line
  tlines = [''.join(chars).strip() for chars in zip(*reversed(slines))]
  stacks = {}
  for s in tlines:
    if re.search('[A-Z]', s):
      stacks[int(s[0])] = list(s[1:])

  return stacks


def genmoves(mlines):
  moves = []
  for m in mlines:
    moves.append(tuple(int(x) for x in m.split()[1::2]))
  return tuple(moves)


def parse_input(fname):
  "Return the stacks and moves in the input file."
  stacklines = []
  movelines = []
  stackmode = True
  with open(fname) as file:
    for line in file:

      # blank line separates stack and move data
      if line == '\n':
        stackmode = False
        continue

      if stackmode == True:
        stacklines.append(line)
      else:
        movelines.append(line)

  return genstacks(stacklines), genmoves(movelines)


def part1(stacks, moves):
  for count, src, dst in moves:
    for i in range(count):
      stacks[dst].append(stacks[src].pop())
  msg = []
  for sk in sorted(stacks.keys()):
    msg.append(stacks[sk][-1])
  return ''.join(msg)


def part2(stacks, moves):
  for count, src, dst in moves:
    crates = reversed([stacks[src].pop() for _ in range(count)])
    stacks[dst].extend(crates)
  msg = []
  for sk in sorted(stacks.keys()):
    msg.append(stacks[sk][-1])
  return ''.join(msg)


def main():
  fname = INPUTFILE
  if use_sample:
    fname = SAMPLE_INPUTFILE

  stacks, moves = parse_input(fname)

  print("Part 1 answer =", part1(copy.deepcopy(stacks), moves))
  print("Part 2 answer =", part2(copy.deepcopy(stacks), moves))


if __name__ == '__main__':
  main()
