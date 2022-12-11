#!/usr/bin/python3 -u

import sys
sys.path.append('../../lib')
from multiline_record import multiline_data

import math
import re
import textwrap


class Monkey():
  # class vars to track the ultimate modulo divisor
  #
  # NOTE: I was stumped on part 2. It was obvious that the test divisors
  # were all prime, and that the "squaring" monkeys were blowing up the
  # problem. I tried to think of some practical way to track prime factors,
  # but it was clear that the "addition" monkeys would thwart any attempt
  # to smartly update prime factors. Ultimately I got the modulo hint from
  # https://www.reddit.com/r/adventofcode/comments/zim5o6/2022_day11_part2_python_brute_force/
  divs = {1}
  moddiv = 1

  def __init__(self, descriptor, monkeys, wdiv):
    self.monkeys = monkeys  # need to know all the other monkeys
    self.inspect_count = 0
    self.wdiv = wdiv
    for d in descriptor:
      match d.split():
        case ['Monkey', midstr]:
          self.mid = int(midstr[:-1])
        case ['Starting', 'items:', *items]:
          self.items = [int(x.removesuffix(',')) for x in items]
        case ['Operation:', 'new', '=', 'old', op, val2]:
          self.op = op
          if val2 == 'old':
            self.val2 = 0
          else:
            self.val2 = int(val2)
        case ['Test:', 'divisible', 'by', divisor]:
          self.divisor = int(divisor)
          Monkey.divs.add(self.divisor)
          Monkey.moddiv = math.prod(Monkey.divs)
        case ['If', ('true:' | 'false:') as b, 'throw', 'to', 'monkey', target]:
          if b == 'true:':
            self.throw_t = int(target)
          else:
            self.throw_f = int(target)
        case _:
          raise ValueError

  def show(self):
    print(f'{self.mid=} {self.items=} {self.op=} {self.val2=} '
          f'{self.divisor=} {self.throw_t=} {self.throw_f=}')

  def divtest(self, worry_level):
    return worry_level % self.divisor == 0

  def update_worry_level(self, worry_level):
    wl = worry_level

    if self.val2 == 0:
      x = wl
    else:
      x = self.val2

    if self.op == '+':
      wl = (wl + x) % Monkey.moddiv
    elif self.op == '*':
      wl = (wl * x) % Monkey.moddiv
    else:
      raise ValueError

    wl = wl // self.wdiv
    
    return wl

  def recv(self, item):
    self.items.append(item)

  def process(self):
    while self.items:
      item = self.items.pop(0)
      wl = item
      self.inspect_count += 1
      wl = self.update_worry_level(wl)
      if self.divtest(wl):
        target = self.throw_t
      else:
        target = self.throw_f
      self.monkeys[target].recv(wl)


def part1(monkeys, rounds):
  for round in range(rounds):
    for mid in monkeys:
      monkeys[mid].process()

  activity = []
  for mid in monkeys:
    activity.append(monkeys[mid].inspect_count)
  activity.sort(reverse=True)
  monkey_business = math.prod(activity[:2])

  return monkey_business


def part2(monkeys, rounds):
  return part1(monkeys, rounds)


def make_monkeys(inp, wdiv):
  monkeys = {}
  mid = None  # monkey id

  for descriptor in multiline_data(inp):
    match = re.fullmatch(r'Monkey (\d+):', descriptor[0])
    assert match
    mid = int(match.group(1))
    monkeys[mid] = Monkey(descriptor, monkeys, wdiv)

  return monkeys


def main():
  sample_input = textwrap.dedent('''\
      Monkey 0:
        Starting items: 79, 98
        Operation: new = old * 19
        Test: divisible by 23
          If true: throw to monkey 2
          If false: throw to monkey 3

      Monkey 1:
        Starting items: 54, 65, 75, 74
        Operation: new = old + 6
        Test: divisible by 19
          If true: throw to monkey 2
          If false: throw to monkey 0

      Monkey 2:
        Starting items: 79, 60, 97
        Operation: new = old * old
        Test: divisible by 13
          If true: throw to monkey 1
          If false: throw to monkey 3

      Monkey 3:
        Starting items: 74
        Operation: new = old + 3
        Test: divisible by 17
          If true: throw to monkey 0
          If false: throw to monkey 1
  ''').rstrip().split('\n')

  main_input = []
  with open('input.txt') as file:
    for line in file:
      line = line.rstrip()
      main_input.append(line)

  for inp in (sample_input, main_input):
    part1_monkeys = make_monkeys(inp, wdiv=3)
    part2_monkeys = make_monkeys(inp, wdiv=1)
    print("Part 1 answer =", part1(part1_monkeys, rounds=20))
    print("Part 2 answer =", part2(part2_monkeys, rounds=10000))


if __name__ == '__main__':
  main()
