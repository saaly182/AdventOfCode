#!/usr/bin/python3 -u


def part1(prog):
  cycle = 0
  regx = 1
  sigsum = 0
  cycchecks = set(range(20, 221, 40))

  for inst in prog:
    cycle += 1

    if cycle in cycchecks:
      sigsum += cycle * regx

    if inst[0] == 'addx':
      cycle += 1
      if cycle in cycchecks:
        sigsum += cycle * regx
      regx += inst[1]

  return sigsum


def part2(prog):
  return None


def main():
  prog = []
  with open('input.txt') as file:
    for line in file:
      line = line.rstrip()
      toks = line.split()
      if toks[0] == 'noop':
        prog.append(tuple(toks))
      else:
        prog.append((toks[0], int(toks[1])))


  print("Part 1 answer =", part1(prog))
  print("Part 2 answer =", part2(prog))


if __name__ == '__main__':
  main()
