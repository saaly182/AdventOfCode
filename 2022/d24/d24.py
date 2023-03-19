#!/usr/bin/python3 -u

import sys
sys.path.append('../../lib')

import dirutils
import functools
import math


class Valley:
    # class vars
    drdc = dirutils.dirvecs

    def __init__(self, inp):
        self.maxrow = len(inp) - 1
        self.maxcol = len(inp[0]) - 1
        self.start = (0, inp[0].index('.'))
        self.end = (self.maxrow, inp[-1].index('.'))
        self.blizzards = self._gen_blizzards(inp)
        self._tstart = 0
        self._visited_states = set()
        self._lcm = math.lcm(self.maxrow - 1, self.maxcol - 1)  # least common multiple of row & col data sizes

    def go_back(self, t):
        """Reverse the start/end points in preparation for another bfs search."""
        self.start, self.end = self.end, self.start
        self._visited_states.clear()
        self._tstart = t

    @staticmethod
    def _gen_blizzards(inp):
        blizlist = []
        for r0, line in enumerate(inp):
            for c0, sym in enumerate(line):
                if sym in set('<>^v'):
                    blizlist.append((sym, r0, c0))
        return tuple(blizlist)

    def _blizpos(self, b, t):
        """Return the row, col position of blizzard b at time t"""
        # This was a pain to work out correctly.
        if t < 0:
            raise ValueError
        sym, r0, c0 = b
        t_rmod = t % (self.maxrow - 1)
        t_cmod = t % (self.maxcol - 1)
        r = (r0 - 1 + (t_rmod * Valley.drdc[sym][0])) % (self.maxrow - 1) + 1
        c = (c0 - 1 + (t_cmod * Valley.drdc[sym][1])) % (self.maxcol - 1) + 1
        return r, c

    @functools.cache
    def _blizlocs(self, t):
        """Return the set of cells occupied by blizzards at time t."""
        blizcells = set()
        for b in self.blizzards:
            blizcells.add(self._blizpos(b, t))
        return blizcells

    def _visited(self, eloc, t):
        """Return true if we've visited this state before."""
        # The state of the blizzards is the same every self._lcm minutes, so if we see that state with the same
        # expedition location again, we have already visited this configuration.
        tmod = t % self._lcm
        if (eloc, tmod) in self._visited_states:
            return True
        else:
            self._visited_states.add((eloc, tmod))
        return False

    def bfs(self):
        """Search for self.end and return the time it took."""
        bq = [(self.start, self._tstart)]  # bfs queue; elements are (expedition location, time)
        while bq:
            eloc, t1 = bq.pop(0)
            er, ec = eloc
            if eloc == self.end:
                return t1 - self._tstart
            t2 = t1 + 1
            bcells = self._blizlocs(t2)
            for d in list(Valley.drdc.values()) + [(0, 0)]:
                r = er + d[0]
                c = ec + d[1]
                if c < 1 or c == self.maxcol:
                    continue
                if (r < 1 or r == self.maxrow) and ((r, c) not in (self.start, self.end)):
                    continue
                if (r, c) not in bcells and not self._visited((r, c), t2):
                    bq.append(((r, c), t2))


def part1(inp):
    valley = Valley(inp)
    return valley.bfs()


def part2(inp):
    valley = Valley(inp)
    t1 = valley.bfs()
    valley.go_back(t1)
    t2 = valley.bfs()
    valley.go_back(t1 + t2)
    t3 = valley.bfs()
    return t1 + t2 + t3


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    sample_input = slurp('sample_input.txt')
    main_input = slurp('input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
