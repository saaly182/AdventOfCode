#!/usr/bin/python3 -u

from collections import namedtuple

Instruction = namedtuple('Instruction', "opcode operand nticks")


def part1(prog):
  cycle = 0
  regx = 1
  sigsum = 0

  for inst in prog:
    for tick in range(inst.nticks):
      cycle += 1
      if (cycle - 20) % 40 == 0:
        sigsum += cycle * regx

    if inst.opcode == 'addx':
      regx += inst.operand

  return sigsum


def pixel(cycle):
  row = cycle // 40
  col = cycle % 40
  return row, col


def part2(prog):
  cycle = 0
  regx = 1
  crt = [[' '] * 40 for _ in range(6)]

  for inst in prog:
    for tick in range(inst.nticks):
      row, col = pixel(cycle)
      sprite = (regx - 1, regx, regx + 1)
      if col in sprite:
        crt[row][col] = '#'
      cycle += 1

    if inst.opcode == 'addx':
      regx += inst.operand

  final_display = '\n'.join([''.join(row) for row in crt])

  return final_display


def main():
  prog = []
  with open('input.txt') as file:
    for line in file:
      line = line.rstrip()
      toks = line.split()
      if toks[0] == 'noop':
        prog.append(Instruction('noop', None, 1))
      elif toks[0] == 'addx':
        prog.append(Instruction('addx', int(toks[1]), 2))
      else:
        raise ValueError

  print("Part 1 answer =", part1(prog))
  print("Part 2 answer =\n", part2(prog))


if __name__ == '__main__':
  main()
