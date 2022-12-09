#!/usr/bin/python3 -u

import textwrap


def part1(trees):
  rowmin = colmin = 0
  rowmax = len(trees[0]) - 1
  colmax = len(trees) - 1
  visible_trees = 0
  tcol = []

  # precompute all the tree columns
  for c in range(colmax + 1):
    tcol.append([x[c] for x in trees])

  for r, trow in enumerate(trees):
    for c, t in enumerate(trow):

      # if tree is on edge...
      if r in (rowmin, rowmax) or c in (colmin, colmax):
        visible_trees += 1
        continue

      # if interior tree is taller than all trees to its
      # left or all trees to its right...
      if max(trow[:c]) < t or max(trow[c + 1:]) < t:
        visible_trees += 1
        continue

      # if interior tree is taller than all trees above it
      # or all trees below it...
      if max(tcol[c][:r]) < t or max(tcol[c][r + 1:]) < t:
        visible_trees += 1
        continue

  return visible_trees


def part2(trees):
  return None


def main():
  sample_input = textwrap.dedent('''\
      30373
      25512
      65332
      33549
      35390
  ''').rstrip().split('\n')

  main_input = []
  with open('input.txt') as file:
    for line in file:
      line = line.rstrip()
      main_input.append(line)

  for inp in (sample_input, main_input):
    trees = []
    for row in inp:
      trees.append([int(x) for x in row])
    print("Part 1 answer =", part1(trees))
    print("Part 2 answer =", part2(trees))


if __name__ == '__main__':
  main()
