#!/usr/bin/python3

import logging
import sys


OUTPUT_LEVEL=logging.INFO
logging.basicConfig(stream=sys.stdout, level=OUTPUT_LEVEL)


def game(p1, p2):
  "Return when the game is over, with p1 and p2 in their final state."

  gstate = set()
  first_state = (tuple(p1), tuple(p2))
  gstate.add(first_state)

  logging.debug('Starting game with %s %s', p1, p2)

  while len(p1) > 0 and len(p2) > 0:
    c1 = p1.pop(0)
    c2 = p2.pop(0)

    logging.debug('c1 = %s, c2 = %s, %s %s', c1, c2, p1, p2)

    if len(p1) < c1 or len(p2) < c2:
      logging.debug('Playing normal round')
      if c1 > c2:
        p1.extend((c1, c2))
      else:
        p2.extend((c2, c1))
    else:
      logging.debug('Playing subgame')
      subp1 = p1[:c1]
      subp2 = p2[:c2]
      game(subp1, subp2)
      # if subp1 is empty, then p2 won, otherwise p1 won normally or
      # because of a repeated state
      if len(subp1) == 0:
        p2.extend((c2, c1))
      else:
        p1.extend((c1, c2))

    this_state = (tuple(p1), tuple(p2))
    if this_state in gstate:
      logging.debug('Repeat state! p1 wins.')
      return
    else:
      gstate.add(this_state)

  logging.debug('Ending game with final decks %s %s', p1, p2)


top_p1 = [14, 6, 21, 10, 1, 33, 7, 13, 25, 8, 17, 11, 28, 27, 50, 2, 35, 49, 19, 46, 3, 38, 23, 5, 43]
top_p2 = [18, 9, 12, 39, 48, 24, 32, 45, 47, 41, 40, 15, 22, 36, 30, 26, 42, 34, 20, 16, 4, 31, 37, 44, 29]

game(top_p1, top_p2)

if top_p1:
  winner = top_p1
else:
  winner = top_p2

winner.reverse()

answer = 0

for i in range(len(winner)):
  answer += (i + 1) * winner[i]

print(answer)
