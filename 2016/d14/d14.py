#!/usr/bin/python3 -u

import hashlib
import re


class HashList:
    def __init__(self, salt, stretches=0):
        self.salt = salt
        self.hlist = []
        self.stretches = stretches

    def get(self, i):
        if not isinstance(i, int):
            raise TypeError(f'i must be type int; {i=}')
        if i < 0:
            raise ValueError(f'i must be > 0; {i=}')
        if i >= len(self.hlist):
            for j in range(len(self.hlist), i + 1):
                h = md5hex(self.salt + str(i))
                for k in range(self.stretches):
                    h = md5hex(h)
                self.hlist.append(h)
        return self.hlist[i]


def md5hex(msg):
    m = hashlib.md5()
    m.update(msg.encode('UTF-8'))
    return m.hexdigest()


def findkeys(salt, stretches):
    """Return the index when the 64th key is found."""
    hlist = HashList(salt, stretches)
    keylist = []
    i = -1

    while len(keylist) < 64:
        i += 1
        h = hlist.get(i)
        if mo1 := re.search(r'(.)\1\1', h):
            c = mo1.group(1)
            fwd_re = c * 5
            for j in range(i + 1, i + 1001):
                if fwd_re in hlist.get(j):
                    keylist.append(h)

    return i


def part1(salt):
    return findkeys(salt, 0)


def part2(salt):
    return findkeys(salt, 2016)


def main():
    for inp in ('abc', 'yjdafjpo'):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
