#!/usr/bin/python3

debug = False

class LanternFish:
  def __init__(self, timer):
    self.timer = timer

  def process(self):
    newfish = None
    if self.timer == 0:
      self.timer = 6
      newfish = LanternFish(8)
    else:
      self.timer -= 1

    return newfish

istates = []

with open('input.txt') as fishfile:
  for line in fishfile:
    line = line.rstrip()
    istates.extend([int(x) for x in line.split(',')])

fish = []

for i in istates:
  fish.append(LanternFish(i))

for day in range(1, 81):
  newfish = []
  for f in fish:
    result = f.process()
    if result is not None:
      newfish.append(result)
  fish.extend(newfish)

  if debug:
    print(f'After day {day}:')
    for f in fish:
      print(f.timer, end=' ')
    print()
    print(f'Fish count: {len(fish)}')

answer = len(fish)
print(answer)
