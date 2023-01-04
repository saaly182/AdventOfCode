#!/usr/bin/python3 -u

import sys
sys.path.append('../../lib')

from collections import namedtuple
from multiline_record import multiline_file


class Walker:
  def __init__(self, row, col, direction):
    self.row = row
    self.col = col
    self.dir = direction

  def __str__(self):
    return str(self.__class__) + ": " + str(self.__dict__)


class Board:
  def __init__(self, boardstr):
    rows = boardstr.split('\n')
    # adding a border of spaces to make zero-based counting easier
    maxrlen = max([len(r) for r in rows])
    for i, r in enumerate(rows):
      r_mod = list(' ' + r + ' ' * (maxrlen - len(r)) + ' ')
      rows[i] = r_mod
    spacerow = ' ' * (maxrlen + 2)
    rows[:0] = [spacerow]
    rows.append(spacerow)
    self.board = rows

    self.dirsyms = {
        'N': '⇧',
        'S': '⇩',
        'E': '⇨',
        'W': '⇦',
    }
    self.turn = {
      'L': {'N': 'W', 'S': 'E', 'E': 'N', 'W': 'S'},
      'R': {'N': 'E', 'S': 'W', 'E': 'S', 'W': 'N'},
    }
    self.move = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}

    self.walker = Walker(1, rows[1].index('.'), 'E')
    self._mark_walker_tile()

  def _mark_walker_tile(self):
    self.board[self.walker.row][self.walker.col] = self.dirsyms[self.walker.dir]

  def show(self):
    print('--')
    print('\n'.join([''.join(r) for r in self.board]))
    print()
    print(self.walker)
    print('--')

  def score(self):
    dirvals = 'ESWN'
    return 1000 * self.walker.row + 4 * self.walker.col + dirvals.index(self.walker.dir)

  def _pathgen(self, path):
    numstr = []
    for c in path:
      if c in ('L', 'R'):
        if numstr:
          yield int(''.join(numstr))
          numstr = []
        yield c
      else:
        numstr.append(c)
    if numstr:
      yield int(''.join(numstr))
        
  def _forward(self, steps):
    sp = ' '
    maxr = len(self.board) - 1
    maxc = len(self.board[0]) - 1

    row1, col1 = self.walker.row, self.walker.col
    dr, dc = self.move[self.walker.dir]
    for i in range(steps):
      canstep = False
      row2, col2 = row1 + dr, col1 + dc
      if self.board[row2][col2] == '#':
        break
      elif self.board[row2][col2] == sp:
        # Advance row2, col2 until we wrap around to an open tile or a '#'
        while True:
          row2, col2 = row2 + dr, col2 + dc
          if row2 < 0: row2 = maxr
          if row2 > maxr: row2 = 0
          if col2 < 0: col2 = maxc
          if col2 > maxc: col2 = 0

          if self.board[row2][col2] == '#':
            break
          elif self.board[row2][col2] == sp:
            pass
          else:
            canstep = True
            break
      else:
        canstep = True

      if canstep:
        self._mark_walker_tile()
        self.walker.row = row2
        self.walker.col = col2
        row1, col1 = row2, col2

    self._mark_walker_tile()
      
  def walk_path(self, path):
    for cmd in self._pathgen(path):
      if cmd in ('L', 'R'):
        self.walker.dir = self.turn[cmd][self.walker.dir]
        self._mark_walker_tile()
      elif isinstance(cmd, int):
        self._forward(cmd)
      else:
        raise ValueError
      

def part1(boardstr, path):
  board = Board(boardstr)
  board.walk_path(path)
  return board.score()


def part2():
  return None


def parse(fname):
  records = []
  for record in multiline_file(fname):
    records.append(record.rstrip())
  return records


def main():
  sample_input = parse('sample_input.txt')
  main_input = parse('input.txt')

  for inp in (sample_input, main_input):
    boardstr, path = inp
    print("Part 1 answer =", part1(boardstr, path))
    print("Part 2 answer =", part2())
    print()


if __name__ == '__main__':
  main()
