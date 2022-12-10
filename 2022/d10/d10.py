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


def pixel(cycle):
  row = cycle // 40
  col = cycle % 40
  return row, col


def showcrt(crt):
  for line in crt:
    print(''.join(line))


def part2(prog):
  cycle = 0
  regx = 1
  crt = [[' '] * 40 for _ in range(6)]

  def updatecrt():
    nonlocal cycle
    row, col = pixel(cycle)
    sprite = (regx - 1, regx, regx + 1)
    if col in sprite:
      crt[row][col] = '#'
    cycle += 1

  for inst in prog:
    updatecrt()

    if inst[0] == 'addx':
      updatecrt()
      regx += inst[1]

  showcrt(crt)

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
