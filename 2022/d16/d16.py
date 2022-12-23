#!/usr/bin/python3 -u

import sys
sys.path.append('../../lib')
from aocutils import shortest_paths

from collections import defaultdict
import re


def score(path):
  # TODO: implement using DP
  return 1


def pathgen(curr_path, time_left, closed_v, time_from, flowmap):
  # scenario 1: we opened every valve within time
  if not closed_v:
    yield curr_path
    return

  out_of_time = True
  for v in sorted(closed_v):
    dt = time_from[curr_path[-1]][v]
    if time_left - dt < 2:  # no point in moving there
      continue
    else:
      out_of_time = False 
      new_curr_path = curr_path + (v,)
      new_time_left = time_left - dt - 1
      new_closed_v = closed_v - set([v])
      yield from pathgen(new_curr_path, new_time_left, new_closed_v, time_from, flowmap)

  # scenario 2: ran out of time
  if out_of_time:
    yield curr_path


def max_press_release(start_v, t_limit, valves, time_from, flowmap):
  mpr = 0

  for path in pathgen(start_v, t_limit, valves, time_from, flowmap):
    print(f'{path=}')
    pr = score(path)
    if pr > mpr:
      mpr = pr
  
  return mpr


def part1(G, flowmap):
  # we only care about valves with non-zero flow rates
  flowmap = {k: v for k, v in flowmap.items() if v > 0}

  valves = set(flowmap)
  time_from = {'AA': shortest_paths(G, 'AA')[0]}
  for v in valves:
    time_from[v] = shortest_paths(G, v)[0]

  return max_press_release(('AA',), 30, valves, time_from, flowmap)


def part2():
  return None


def parse(inp):
  G = defaultdict(set)
  flowmap = {}
  spec = r'Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z ,]+)'
  for line in inp:
    match = re.fullmatch(spec, line)
    assert match
    v = match.group(1)
    flowmap[v] = int(match.group(2))
    for u in match.group(3).split(', '):
      G[v].add((u, 1))
      G[u].add((v, 1))

  return G, flowmap


def slurp(fname):
  with open(fname) as file:
    return [line.rstrip() for line in file.readlines()]


def main():
  sample_input = slurp('sample_input.txt')
  main_input = slurp('input.txt')

  for inp in (sample_input, main_input):
    G, flowmap = parse(inp)
    print("Part 1 answer =", part1(G, flowmap))
    print("Part 2 answer =", part2())
    print()


if __name__ == '__main__':
  main()
