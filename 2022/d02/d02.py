#!/usr/bin/python3 -u

debug = False
use_sample = False
SAMPLE_INPUTFILE = './sample_input.txt'
INPUTFILE = './input.txt'

_score_move = {'X': 1, 'Y': 2, 'Z': 3}
_score_outcome = {
  'AX': 3,
  'AY': 6,
  'AZ': 0,

  'BX': 0,
  'BY': 3,
  'BZ': 6,

  'CX': 6,
  'CY': 0,
  'CZ': 3,
}

# X = lose, Y = draw, Z = win
_my_move = {
  #R
  'AX': 'Z',
  'AY': 'X',
  'AZ': 'Y',

  #P
  'BX': 'X',
  'BY': 'Y',
  'BZ': 'Z',

  #S
  'CX': 'Y',
  'CY': 'Z',
  'CZ': 'X',
}


def score(p1, p2):
  s = 0
  s += _score_move[p2]
  s += _score_outcome[p1 + p2]
  return s


def part1(moves):
  total_score = 0
  for m in moves:
    total_score += score(m[0], m[1])

  return total_score


def part2(moves):
  total_score = 0
  for m in moves:
    mymove = _my_move[m[0] + m[1]]
    total_score += score(m[0], mymove)

  return total_score


def main():
  fname = INPUTFILE
  if use_sample:
    fname = SAMPLE_INPUTFILE

  moves = []
  with open(fname) as file:
    for line in file:
      line = line.rstrip()
      moves.append(tuple(line.split()))

  print("Part 1 answer =", part1(moves))
  print("Part 2 answer =", part2(moves))


if __name__ == '__main__':
  main()
