#!/usr/bin/python3 -u

debug = False
use_sample = False
SAMPLE_INPUTFILE = './sample_input.txt'
INPUTFILE = './input.txt'


# Confession: I just did crappy throw-away code + vim to get the actual answers
# to this day quickly. Then I wrote this code.


def part1(stream, marker_size):
  found = False
  for i in range(marker_size - 1, len(stream)):
    if len(set(stream[i - marker_size + 1:i + 1])) == marker_size:
      found = True
      break
  if found:
    return i + 1
  return None


def part2(stream, marker_size):
  return part1(stream, 14)


def main():
  fname = INPUTFILE
  if use_sample:
    fname = SAMPLE_INPUTFILE

  with open(fname) as file:
    for line in file:
      line = line.rstrip()
  stream = line

  print("Part 1 answer =", part1(stream, 4))
  print("Part 2 answer =", part2(stream, 14))


if __name__ == '__main__':
  main()
