#!/usr/bin/python3 -u

import sys
sys.path.append('../../lib')
from aocutils import shortest_paths

from collections import defaultdict
import functools
import re

# globals
_flowrates = None
_time_from = None
_time_limit = None


# DP version
@functools.lru_cache(maxsize=None)
def moving_score(path):
  'Return the score and time left as of right when the last valve opened.'
  if path == ('AA',):
    return 0, _time_limit

  tail1 = path[-1]
  tail2 = path[-2]
  prevpath = tuple(list(path[:-1]))
  dt = _time_from[tail2][tail1] + 1  # time to move + open valve

  score, time_left = moving_score(prevpath)
  score += static_score(prevpath, dt)
  time_left -= dt

  return score, time_left


def static_score(path, duration):
  'Return score for the open valves in the path for the duration.'
  score = 0
  for v in path:
    if v != 'AA':
      score += duration * _flowrates[v]
  return score


def score(path):
  m_score, time_left = moving_score(path)
  s_score = static_score(path, time_left)
  return m_score + s_score


def pathgen(curr_path, time_left, closed_v):
  # scenario 1: we opened every valve within time
  if not closed_v:
    yield curr_path
    return

  out_of_time = True
  for v in sorted(closed_v):
    dt = _time_from[curr_path[-1]][v]
    if time_left - dt < 2:  # no point in moving there
      continue
    else:
      out_of_time = False 
      new_curr_path = curr_path + (v,)
      new_time_left = time_left - dt - 1
      new_closed_v = closed_v - set([v])
      yield from pathgen(new_curr_path, new_time_left, new_closed_v)

  # scenario 2: ran out of time
  if out_of_time:
    yield curr_path


def max_press_release(start_v, t_limit, valves):
  mpr = 0

  for path in pathgen(start_v, t_limit, valves):
    pr = score(path)
    if pr > mpr:
      mpr = pr
  
  return mpr


def part1():
  # NOTE: I could not see how to make this problem tractable with
  # a 30-step lookahead and a branching factor of 3-5. The hint I
  # eventually took from reddit was to only pay attention to the
  # non-zero valves and only ever visit-and-open a valve.
  valves = set(_flowrates)
  return max_press_release(('AA',), _time_limit, valves)


def part2():
  return None


def parse(inp):
  global _flowrates, _time_from

  G = defaultdict(set)
  _flowrates = {}
  spec = r'Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z ,]+)'
  for line in inp:
    match = re.fullmatch(spec, line)
    assert match
    v = match.group(1)
    _flowrates[v] = int(match.group(2))
    for u in match.group(3).split(', '):
      G[v].add((u, 1))
      G[u].add((v, 1))

  # we only care about valves with non-zero flow rates
  _flowrates = {k: v for k, v in _flowrates.items() if v > 0}

  valves = set(_flowrates)
  _time_from = {'AA': shortest_paths(G, 'AA')[0]}
  for v in valves:
    _time_from[v] = shortest_paths(G, v)[0]


def slurp(fname):
  with open(fname) as file:
    return [line.rstrip() for line in file.readlines()]


def main():
  global _time_limit
  sample_input = slurp('sample_input.txt')
  main_input = slurp('input.txt')

  for inp in (sample_input, main_input):
    parse(inp)
    _time_limit = 30
    print("Part 1 answer =", part1())
    _time_limit = 26
    print("Part 2 answer =", part2())
    print()


if __name__ == '__main__':
  main()
