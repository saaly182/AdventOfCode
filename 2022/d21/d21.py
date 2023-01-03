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


def humn_evaluate(exptree, node, humn):
  exptree['humn'] = humn
  return evaluate(exptree, node)


def h_bounds(exptree, node, target_val):
  'Return suitable initial bounds for a binary search.'
  h1 = 1000
  h2 = 2000
  slope = (humn_evaluate(exptree, node, h2) -
           humn_evaluate(exptree, node, h1)) / (h2 - h1)
  slope_sign = int(slope/abs(slope))

  v1 = slope_sign * humn_evaluate(exptree, node, h1)
  while v1 > target_val:
    h1 -= 2*abs(h1)
    v1 = slope_sign * humn_evaluate(exptree, node, h1)

  v2 = slope_sign * humn_evaluate(exptree, node, h2)
  while v2 < target_val:
    h2 += 2*abs(h2)
    v2 = slope_sign * humn_evaluate(exptree, node, h2)

  assert (v1 < target_val < v2) or (v1 > target_val > v2)
  return h1, h2, slope_sign


def h_search(exptree, node, target_val):
  'Return the value of "humn" that makes the node == target.'

  # NOTE: Using slope_sign to flip negative slopes to positive ones
  # to make the bounds handling simpler.

  h1, h2, slope_sign = h_bounds(exptree, node, target_val)
  while h1 != h2:
    h_mid = (h1 + h2) // 2
    v_mid = slope_sign * humn_evaluate(exptree, node, h_mid)
    if v_mid == slope_sign * target_val:
      return h_mid

    if v_mid < slope_sign * target_val:
      h1 = h_mid + 1
    else:
      h2 = h_mid - 1

  assert humn_evaluate(exptree, node, h1) == target_val
  return h1


def part1(exptree):
  return evaluate(exptree, 'root')


def part2(exptree):
  rootchild1, rootchild2 = exptree['root'][0], exptree['root'][2]
  # figure out which child depends on 'humn'
  rc1a = humn_evaluate(exptree, rootchild1, 5)
  rc2a = humn_evaluate(exptree, rootchild2, 5)
  rc1b = humn_evaluate(exptree, rootchild1, 8)
  rc2b = humn_evaluate(exptree, rootchild2, 8)
  if rc1a == rc1b and rc2a != rc2b:
    rc_change = rootchild2
    target_val = rc1a
  if rc1a != rc1b and rc2a == rc2b:
    rc_change = rootchild1
    target_val = rc2a
  else:
    assert False  # we're assuming only one child depends on humn

  return h_search(exptree, rc_change, target_val)


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
