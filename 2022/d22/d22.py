#!/usr/bin/python3 -u

from collections import namedtuple
import sys
sys.path.append('../../lib')
from multiline_record import multiline_file  # noqa: E402 F401
import dirutils  # noqa: E402 F401


class Walker:
  def __init__(self, row, col, direction):
    self.row = row
    self.col = col
    self.dir = direction

  def __str__(self):
    return str(self.__class__) + ": " + str(self.__dict__)

  def __repr__(self):
    return str(self)


class Walker2(Walker):
  def __init__(self, face, row, col, direction):
    self.face = face
    super().__init__(row, col, direction)


class Board:
  def __init__(self, boardstr):
    rows = boardstr.split('\n')
    # adding a border of spaces to make zero-based counting easier
    maxrlen = max([len(r) for r in rows])
    for i, r in enumerate(rows):
      r_mod = list(' ' + r + ' ' * (maxrlen - len(r)) + ' ')
      rows[i] = r_mod
    spacerow = [sp for sp in ' ' * (maxrlen + 2)]
    rows[:0] = [spacerow]
    rows.append(spacerow)
    self.board = rows
    self._set_dir_vars()
    self.walker = Walker(1, self.board[1].index('.'), 'E')
    self._mark_walker_tile()

  def _set_dir_vars(self):
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
    self.move = dirutils.dirvecs

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
    return (1000 * self.walker.row + 4 * self.walker.col
            + dirvals.index(self.walker.dir))

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
      

class Board2(Board):
  """Part 2, which folds the map into a cube.

  I'm not gonna write code that will accept and parse arbitrary input. That's
  too much effort. Instead I'm gonna hardcode the topology for the sample
  input and my main input.

  sample input is this form:
      00
  112233
      4455

  main input is this form:
    0011
    22
  3344
  55
  """
  def __init__(self, boardstr):
    self.board = [list(r) for r in boardstr.split('\n')]
    self._set_dir_vars()
    self.score = None
    if len(self.board[0]) == 12:
      # SAMPLE INPUT
      self.fsize = 4
      self.fconn = {
        # face:
        #   edge headed off:
        #     (new face, new dir)
        # (made a physical cube to keep this all straight...)
        0: {'N': (1, 'S'), 'S': (3, 'S'), 'E': (5, 'W'), 'W': (2, 'S')},
        1: {'N': (0, 'S'), 'S': (4, 'N'), 'E': (2, 'E'), 'W': (5, 'N')},
        2: {'N': (0, 'E'), 'S': (4, 'E'), 'E': (3, 'E'), 'W': (1, 'W')},
        3: {'N': (0, 'N'), 'S': (4, 'S'), 'E': (5, 'S'), 'W': (2, 'W')},
        4: {'N': (3, 'N'), 'S': (1, 'N'), 'E': (5, 'E'), 'W': (2, 'N')},
        5: {'N': (3, 'W'), 'S': (1, 'E'), 'E': (0, 'W'), 'W': (4, 'W')},
      }
      self.facemap = ((0,  4,  8, 12),  # face 0
                      (4,  8,  0,  4),  # face 1
                      (4,  8,  4,  8),  # face 2
                      (4,  8,  8, 12),  # face 3
                      (8, 12,  8, 12),  # face 4
                      (8, 12, 12, 16),  # face 5
                     )
    else:
      # MAIN INPUT
      self.fsize = 50
      self.fconn = {
        # face:
        #   edge headed off:
        #     (new face, new dir)
        # (made a physical cube to keep this all straight...)
        0: {'N': (5, 'E'), 'S': (2, 'S'), 'E': (1, 'E'), 'W': (3, 'E')},
        1: {'N': (5, 'N'), 'S': (2, 'W'), 'E': (4, 'W'), 'W': (0, 'W')},
        2: {'N': (0, 'N'), 'S': (4, 'S'), 'E': (1, 'N'), 'W': (3, 'S')},
        3: {'N': (2, 'E'), 'S': (5, 'S'), 'E': (4, 'E'), 'W': (0, 'E')},
        4: {'N': (2, 'N'), 'S': (5, 'W'), 'E': (1, 'W'), 'W': (3, 'W')},
        5: {'N': (3, 'N'), 'S': (1, 'S'), 'E': (4, 'N'), 'W': (0, 'S')},
      }
      self.facemap = ((  0,  50,  50, 100),  # face 0
                      (  0,  50, 100, 150),  # face 1
                      ( 50, 100,  50, 100),  # face 2
                      (100, 150,   0,  50),  # face 3
                      (100, 150,  50, 100),  # face 4
                      (150, 200,   0,  50),  # face 5
                      )

    self.faces = self._make_faces()
    self.walker = Walker2(0, 0, self.faces[0][0].index('.'), 'E')
    self._mark_walker_tile()

  def _mark_walker_tile(self):
    face = self.walker.face
    w_r = self.walker.row
    w_c = self.walker.col
    self.faces[face][w_r][w_c] = self.dirsyms[self.walker.dir]

    b_r = w_r + self.facemap[face][0]
    b_c = w_c + self.facemap[face][2]
    self.board[b_r][b_c] = self.dirsyms[self.walker.dir]

    # maintain an updated score here
    dirvals = 'ESWN'
    self.score = (1000 * (b_r + 1) + 4 * (b_c + 1)
            + dirvals.index(self.walker.dir))

  def show(self):
    print('--')
    print('\n'.join([''.join(r) for r in self.board]))
    print()
    print(f'{self.walker=}')
    for i in range(6):
      print(f'face {i}:')
      for r in self.faces[i]:
        print(''.join(r))
    print('--')

  def _make_faces(self):
    fr = self.facemap
    f = [[] for i in range(6)]
    for i in range(6):
      for r in self.board[fr[i][0]:fr[i][1]]:
        f[i].append(list(r[fr[i][2]:fr[i][3]]))
    return f

  def _next_tile(self):
    'Return the next tile on the path.'
    row1, col1 = self.walker.row, self.walker.col
    face1, dir1 = self.walker.face, self.walker.dir
    dr, dc = self.move[self.walker.dir]
    maxr = maxc = self.fsize - 1
    row2, col2 = row1 + dr, col1 + dc

    if 0 <= row2 <= maxr and 0 <= col2 <= maxc:  # path remained on face
      return face1, row2, col2, dir1
    else:  # path moved to new face
      face2, dir2 = self.fconn[face1][dir1]
      match (dir1, dir2):
        # N
        case ('N', 'N'):
          row2, col2 = maxr, col1
        case ('N', 'S'):
          row2, col2 = 0, maxc - col1
        case ('N', 'E'):
          row2, col2 = col1, 0
        case ('N', 'W'):
          row2, col2 = maxr - col1, maxc
        # S
        case ('S', 'N'):
          row2, col2 = maxr, maxc - col1
        case ('S', 'S'):
          row2, col2 = 0, col1
        case ('S', 'E'):
          row2, col2 = maxr - col1, 0
        case ('S', 'W'):
          row2, col2 = col1, maxc
        # E
        case ('E', 'N'):
          row2, col2 = maxr, row1
        case ('E', 'S'):
          row2, col2 = 0, maxc - row1
        case ('E', 'E'):
          row2, col2 = row1, 0
        case ('E', 'W'):
          row2, col2 = maxr - row1, maxc
        # W
        case ('W', 'N'):
          row2, col2 = maxr, maxc - row1
        case ('W', 'S'):
          row2, col2 = 0, row1
        case ('W', 'E'):
          row2, col2 = maxr - row1, 0
        case ('W', 'W'):
          row2, col2 = row1, maxc

        case _:
          print(dir1, dir2)
          assert False  # should not get here

    return face2, row2, col2, dir2

  def _forward(self, steps):
    maxr = self.fsize - 1
    maxc = maxr  # faces are square

    for i in range(steps):
      face2, row2, col2, dir2 = self._next_tile()
      if self.faces[face2][row2][col2] == '#':
        break
      else:
        self._mark_walker_tile()
        self.walker.row = row2
        self.walker.col = col2
        self.walker.dir = dir2
        self.walker.face = face2

    self._mark_walker_tile()


def part1(boardstr, path):
  board = Board(boardstr)
  board.walk_path(path)
  return board.score()


def part2(boardstr, path):
  board = Board2(boardstr)
  board.walk_path(path)
  return board.score


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
    print("Part 2 answer =", part2(boardstr, path))
    print()


if __name__ == '__main__':
  main()
