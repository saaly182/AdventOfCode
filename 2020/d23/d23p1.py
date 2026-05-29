#!/usr/bin/python3

import logging
import sys

OUTPUT_LEVEL=logging.INFO
logging.basicConfig(stream=sys.stdout, level=OUTPUT_LEVEL)

input='716892543'

cups = [int(x) for x in input]

for i in range(100):
  logging.debug('Start round, cups: %s', cups)
  cur_cup = cups[0]
  cups3 = cups[1:4]
  cups = cups[0:1] + cups[4:]
  logging.debug('cur_cup = %s, cups3 = %s, cups = %s', cur_cup, cups3, cups)
  dest_cup = cur_cup - 1
  while dest_cup not in cups:
    dest_cup -= 1
    if dest_cup < min(cups):
      dest_cup = max(cups)
  logging.debug('dest_cup = %s', dest_cup)
  dest_cup_idx = cups.index(dest_cup)
  ins = dest_cup_idx + 1
  cups[ins:ins] = cups3
  cups = cups[1:] + [cups[0]]
  logging.debug('final cups = %s', cups)

idx_1 = cups.index(1)
cups = cups[idx_1:] + cups[0:idx_1]
answer = ''.join([str(x) for x in cups[1:]])
print(answer)
