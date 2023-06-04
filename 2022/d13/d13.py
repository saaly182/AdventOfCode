#!/usr/bin/python3 -u

import functools
import sys
sys.path.append('../../lib')
from multiline_record import multiline_data  # noqa: E402


def make_pairs(inp):
  allowed_chars = set('[],0123456789')
  pairs = []

  for pair_strs in multiline_data(inp):
    # validate data since we're going to eval() it
    for pkt in pair_strs:
      assert set(pkt).issubset(allowed_chars)

    pairs.append((eval(pair_strs[0]), eval(pair_strs[1])))

  return pairs


def mycmp(a, b):
  'Classic cmp behavior: return -1, 0, 1 if a<b,a==b,a>b'
  try:
    return (a > b) - (a < b)
  except TypeError:
    # if a and b are different lengths, I'll handle that after
    # the zip loop.
    for x, y in zip(a, b):
      xint = isinstance(x, int)
      xlst = isinstance(x, list)
      yint = isinstance(y, int)
      ylst = isinstance(y, list)

      # both same type
      if (xint and yint) or (xlst and ylst):
        order = mycmp(x, y)
        if order != 0:
          return order
        else:
          continue

      # one int and one list
      if xint:
        order = mycmp([x], y)
      else:
        order = mycmp(x, [y])
      if order != 0:
        return order

    # if we got here, a and b are equal up through their common length,
    # so the shorter one is less than the longer one
    return mycmp(len(a), len(b))


def part1(pairs):
  isum = 0
  for i, pair in enumerate(pairs, start=1):
    order = mycmp(pair[0], pair[1])
    if order == -1:
      isum += i

  return isum


def part2(pairs):
  pkts = [[[2]], [[6]]]
  for p in pairs:
    pkts.extend(p)
  pkts.sort(key=functools.cmp_to_key(mycmp))
  answer = (pkts.index([[2]]) + 1) * (pkts.index([[6]]) + 1)

  return answer


def slurp(fname):
  lines = []
  with open(fname) as file:
    for line in file:
      lines.append(line.rstrip())
  return lines


def main():
  sample_input = slurp('sample_input.txt')
  main_input = slurp('input.txt')

  for inp in (sample_input, main_input):
    pairs = make_pairs(inp)
    print("Part 1 answer =", part1(pairs))
    print("Part 2 answer =", part2(pairs))
    print()


if __name__ == '__main__':
  main()
