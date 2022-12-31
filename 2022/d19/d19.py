#!/usr/bin/python3 -u

import re


class Blueprint:
  def __init__(self, bpraw):
    (self.bpid,
     self.orebot_ore_cost,
     self.clabot_ore_cost,
     self.obsbot_ore_cost,
     self.obsbot_cla_cost,
     self.geobot_ore_cost,
     self.geobot_obs_cost) = bpraw
    self.set_max_bots()

  def set_max_bots(self):
    # There's no point in building more bots of a given type than the max
    # amount of their resource that can be used in one robot build.
    self.orebot_max = max(self.orebot_ore_cost, self.clabot_ore_cost,
                          self.obsbot_ore_cost, self.geobot_ore_cost)
    self.clabot_max = self.obsbot_cla_cost
    self.obsbot_max = self.geobot_obs_cost

  def __str__(self):
    return str(self.__class__) + ": " + str(self.__dict__)


class State:
  def __init__(self, ttl, orebots, clabots, obsbots, geobots,
               ore, cla, obs, geo):
    (self.ttl, self.orebots, self.clabots, self.obsbots, self.geobots,
     self.ore, self.cla, self.obs, self.geo) = (ttl, orebots, clabots,
     obsbots, geobots, ore, cla, obs, geo)

  def dup(self):
    'Return a duplicate of this instance.'
    return State(self.ttl, self.orebots, self.clabots, self.obsbots,
    self.geobots, self.ore, self.cla, self.obs, self.geo)

  def produce_resources(self):
    self.ore += self.orebots
    self.cla += self.clabots
    self.obs += self.obsbots
    self.geo += self.geobots

  def __str__(self):
    return str(self.__class__) + ": " + str(self.__dict__)


class SearchTracker:
  def __init__(self):
    self.best_score = 0
    self.nodes_visited = 0


def dfs_explore(bp, state1, tracker):
  # NOTE: A lot of DRY problems with this version, but I didn't want to
  # rework this to add abstractions for the robots and resources to
  # get rid of the repetition.
  tracker.nodes_visited += 1

  if state1.ttl == 1:
    state1.produce_resources()  # one last production run
    score = state1.geo
    if score > tracker.best_score:
      tracker.best_score = score
    return

  # build orebot next
  if state1.orebots < bp.orebot_max:
    state2 = state1.dup()
    while state2.ore < bp.orebot_ore_cost and state2.ttl > 1:
      state2.produce_resources()
      state2.ttl -= 1
    if state2.ttl > 1:
      state2.ore -= bp.orebot_ore_cost
      state2.produce_resources()
      state2.orebots += 1
      state2.ttl -= 1
    dfs_explore(bp, state2, tracker)

  # build clabot next
  if state1.clabots < bp.clabot_max:
    state2 = state1.dup()
    while state2.ore < bp.clabot_ore_cost and state2.ttl > 1:
      state2.produce_resources()
      state2.ttl -= 1
    if state2.ttl > 1:
      state2.ore -= bp.clabot_ore_cost
      state2.produce_resources()
      state2.clabots += 1
      state2.ttl -= 1
    dfs_explore(bp, state2, tracker)

  # build obsbot next
  if state1.obsbots < bp.obsbot_max:
    state2 = state1.dup()
    while ((state2.ore < bp.obsbot_ore_cost or state2.cla < bp.obsbot_cla_cost)
           and state2.ttl > 1):
      state2.produce_resources()
      state2.ttl -= 1
    if state2.ttl > 1:
      state2.ore -= bp.obsbot_ore_cost
      state2.cla -= bp.obsbot_cla_cost
      state2.produce_resources()
      state2.obsbots += 1
      state2.ttl -= 1
    dfs_explore(bp, state2, tracker)

  # build geobot next
  state2 = state1.dup()
  while ((state2.ore < bp.geobot_ore_cost or state2.obs < bp.geobot_obs_cost)
         and state2.ttl > 1):
    state2.produce_resources()
    state2.ttl -= 1
  if state2.ttl > 1:
    state2.ore -= bp.geobot_ore_cost
    state2.obs -= bp.geobot_obs_cost
    state2.produce_resources()
    state2.geobots += 1
    state2.ttl -= 1
  dfs_explore(bp, state2, tracker)


def part1(blueprints):
  ttl = 24
  answer = 0

  for bp in blueprints:
    init_state = State(ttl, 1, *([0] * 7))
    tracker = SearchTracker()
    dfs_explore(bp, init_state, tracker)
    answer += bp.bpid * tracker.best_score

  return answer


def part2(blueprints):
  ttl = 32
  answer = 1

  for bp in blueprints[:3]:
    init_state = State(ttl, 1, *([0] * 7))
    tracker = SearchTracker()
    dfs_explore(bp, init_state, tracker)
    answer *= tracker.best_score

  return answer


def slurp(fname):
  with open(fname) as file:
    return [line.rstrip() for line in file.readlines()]


def process(inp):
  spec = (r'Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot '
          r'costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) '
          r'clay. Each geode robot costs (\d+) ore and (\d+) obsidian.')

  blueprints = []
  for line in inp:
    match = re.fullmatch(spec, line)
    assert match
    data = tuple([int(x) for x in match.groups()])
    blueprints.append(Blueprint(data))

  return tuple(blueprints)


def main():
  sample_input = slurp('sample_input.txt')
  main_input = slurp('input.txt')

  for inp in (sample_input, main_input):
    blueprints = process(inp)
    print("Part 1 answer =", part1(blueprints))
    print("Part 2 answer =", part2(blueprints))
    print()


if __name__ == '__main__':
  main()
