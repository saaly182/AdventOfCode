#!/usr/bin/python3 -u

import math
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
  colmax = len(trees) - 1
  scenic_score_max = 0
  tcol = []

  # precompute all the tree columns
  for c in range(colmax + 1):
    tcol.append([x[c] for x in trees])

  for r, trow in enumerate(trees):
    for c, t in enumerate(trow):
      tree_view = []

      trees_L = reversed(trow[:c])
      trees_R = trow[c + 1:]
      trees_U = reversed(tcol[c][:r])
      trees_D = tcol[c][r + 1:]

      for tree_list in (trees_L, trees_R, trees_U, trees_D):
        tree_count = 0
        for tn in tree_list:
          tree_count += 1
          if tn >= t:
            break
        tree_view.append(tree_count)

      scenic_score = math.prod(tree_view)

      if scenic_score > scenic_score_max:
        scenic_score_max = scenic_score

  return scenic_score_max


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
