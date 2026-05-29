#!/usr/bin/python3

import sys
sys.path.append('../../lib')

from multiline_record import multiline_file


class BingoBoard:
  def __init__(self, board):
    self.board = board
    self.bsize = len(self.board[0])
    self.state = [[0] * self.bsize for x in self.board]

  def show(self):
    print(f"self.board = {self.board}")
    print(f"self.bsize = {self.bsize}")
    print(f"self.state = {self.state}")

  def process(self, n):
    for row in range(self.bsize):
      for col in range(self.bsize):
        if self.board[row][col] == n:
          self.state[row][col] = 1

  def has_bingo(self):
    for row in self.state:
      if row.count(1) == self.bsize:
        return True

    for c in range(self.bsize):
      col = [row[c] for row in self.state]
      if col.count(1) == self.bsize:
        return True

    return False

  def umarked_sum(self):
    um_sum = 0
    for row in range(self.bsize):
      for col in range(self.bsize):
        if self.state[row][col] == 0:
          um_sum += self.board[row][col]

    return um_sum


boards = []

record_num = 0
for record in multiline_file('input.txt'):
  record_num += 1
  record = record.rstrip('\n')
  if record_num == 1:
    nums = tuple(int(x) for x in record.split(','))
    continue

  board = []
  for row in record.split('\n'):
    board.append(tuple([int(n) for n in row.split()]))
  board = tuple(board)

  boards.append(BingoBoard(board))

winning_boards = set()
try:
  for n in nums:
    for b in boards:
      b.process(n)
      if b.has_bingo():
        if b in winning_boards:
          continue
        if len(boards) - len(winning_boards) == 1:
          # ... then this is the last winning board
          um_sum = b.umarked_sum()
          answer = um_sum * n
          raise StopIteration
        winning_boards.add(b)
except StopIteration:
  pass

print(answer)
