#!/usr/bin/python3 -u

debug = False
use_sample = False
SAMPLE_INPUTFILE = './sample_input.txt'
INPUTFILE = './input.txt'


def priority(c):
  v = ord(c)
  if v >= 97:
    return v - ord('a') + 1
  else:
    return v - ord('A') + 26 + 1


def part1(rs):
  psum = 0
  for s in rs:
    midpoint = len(s) // 2
    a, b = s[:midpoint], s[midpoint:]
    common = tuple(set(a).intersection(set(b)))[0]
    pc = priority(common)
    psum += pc

  return psum


def part2(rs):
  psum = 0
  for sackgroup in zip(rs[0::3], rs[1::3], rs[2::3]):
    badge = tuple(set.intersection(*[set(x) for x in sackgroup]))[0]
    pb = priority(badge)
    psum += pb

  return psum


def main():
  fname = INPUTFILE
  if use_sample:
    fname = SAMPLE_INPUTFILE

  rucksacks = []
  with open(fname) as file:
    for line in file:
      line = line.rstrip()
      rucksacks.append(line)

  print("Part 1 answer =", part1(rucksacks))
  print("Part 2 answer =", part2(rucksacks))


if __name__ == '__main__':
  main()
