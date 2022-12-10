#!/usr/bin/python3 -u

import textwrap


def sign(n):
  if n == 0: return 0
  return n // abs(n)


def tailmove(h, t):
  hx, hy = h
  tx, ty = t
  dx = hx - tx
  dy = hy - ty

  if max(abs(dx), abs(dy)) < 2:
    t_next = t
  else:
    t_next = (tx + sign(dx) * 1, ty + sign(dy) * 1)

  return t_next


def part1(moves):
  h = [0, 0]
  t = (0, 0)
  tvisit = set()
  tvisit.add(t)

  delta = {'L': (-1,  0), 'R': ( 1,  0), 'U': ( 0,  1), 'D': ( 0, -1)}

  for dcmd, steps in moves:
    for i in range(steps):
      h[0] += delta[dcmd][0]
      h[1] += delta[dcmd][1]
      t = tailmove(h, t)
      tvisit.add(t)

  return len(tvisit)


def part2(moves):
  return None


def main():
  sample_input = textwrap.dedent('''\
      R 4
      U 4
      L 3
      D 1
      R 4
      D 1
      L 5
      R 2
  ''').rstrip().split('\n')

  main_input = []
  with open('input.txt') as file:
    for line in file:
      line = line.rstrip()
      main_input.append(line)

  for inp in (sample_input, main_input):
    moves = tuple([(x[0], int(x[1])) for x in [y.split() for y in inp]])
    print("Part 1 answer =", part1(moves))
    print("Part 2 answer =", part2(moves))


if __name__ == '__main__':
  main()
