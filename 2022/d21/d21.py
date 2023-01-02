#!/usr/bin/python3 -u

import operator


opfnc = {
  '+': operator.add,
  '-': operator.sub,
  '*': operator.mul,
  '/': operator.floordiv,
}


def evaluate(exptree, node):
  "Recursively evaluate and return the node's value in exptree."
  e = exptree[node]
  if isinstance(e, int):
    return e

  left, op, right = e
  return opfnc[op](evaluate(exptree, left), evaluate(exptree, right))


def part1(exptree):
  return evaluate(exptree, 'root')


def part2(exptree):
  return None


def slurp(fname):
  with open(fname) as file:
    return [line.rstrip() for line in file.readlines()]


def parse(inp):
  et = {}
  for line in inp:
    a = line.split()
    a[0] = a[0][:-1]  # chop off the ':'
    if len(a) == 2:
      et[a[0]] = int(a[1])
    else:
      et[a[0]] = a[1:]
  return et


def main():
  sample_input = slurp('sample_input.txt')
  main_input = slurp('input.txt')

  for inp in (sample_input, main_input):
    exptree = parse(inp)
    print("Part 1 answer =", part1(exptree))
    print("Part 2 answer =", part2(exptree))
    print()


if __name__ == '__main__':
  main()
