#!/usr/bin/python3 -u

import copy


class GroveMessage:
  def __init__(self, init_msg):
    self.init_msg = init_msg.copy()
    self.mlen = len(init_msg)
    # need unique id for each elem because init_msg elems are not unique
    self.msg_elems = list(enumerate(init_msg))
    self.msg = self.msg_elems.copy()
    self._mix()

  def _val_index(self, value):
    'Return first index of value in msg.'
    return [a[1] for a in self.msg].index(value)

  def _eid_index(self, eid):
    'Return first index of element id in msg.'
    return [a[0] for a in self.msg].index(eid)

  def vals_from_zero(self, offsets):
    'Return a list of values at the offsets from the zero element.'
    ret = []
    idx0 = self._val_index(0)
    for offset in offsets:
      ret.append(self.msg[(idx0 + offset) % self.mlen][1])
    return ret

  def getmsg(self):
    return [a[1] for a in self.msg]

  def show(self):
    print('---\n', self)
    print('msg: ', [a[1] for a in self.msg], '\n---')

  def __str__(self):
    return str(self.__class__) + ": " + str(self.__dict__)

  def _insert_idx(self, idx, value):
    'Return insertion point for the input idx and value.'
    return (idx + value) % (self.mlen - 1)

  def _mix(self):
    for eid, value in self.msg_elems:
      idx = self._eid_index(eid)
      del self.msg[idx]
      ins_idx = self._insert_idx(idx, value)
      self.msg[ins_idx:ins_idx] = [(eid, value)]


def part1(encrypted_msg):
  grovemsg = GroveMessage(encrypted_msg)
  return sum(grovemsg.vals_from_zero([1000, 2000, 3000]))


def part2():
  return None


def slurp(fname):
  with open(fname) as file:
    return [line.rstrip() for line in file.readlines()]


def main():
  sample_input = slurp('sample_input.txt')
  main_input = slurp('input.txt')

  for inp in (sample_input, main_input):
    encrypted_msg = [int(x) for x in inp]
    print("Part 1 answer =", part1(encrypted_msg))
    print("Part 2 answer =", part2())
    print()


if __name__ == '__main__':
  main()
