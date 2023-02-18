#!/usr/bin/python3 -u

import hashlib
import re


class HashList:
    def __init__(self, salt):
        self.salt = salt
        self.hlist = []

    def get(self, i):
        if not isinstance(i, int):
            raise TypeError(f'i must be type int; {i=}')
        if i < 0:
            raise ValueError(f'i must be > 0; {i=}')
        if i >= len(self.hlist):
            for j in range(len(self.hlist), i + 1):
                self.hlist.append(md5(self.salt + str(i)))
        return self.hlist[i]


def md5(msg):
    m = hashlib.md5()
    m.update(msg.encode('UTF-8'))
    return m.hexdigest()


def part1(salt):
    hlist = HashList(salt)
    keylist = []
    i = -1

    while len(keylist) < 64:
        i += 1
        h = hlist.get(i)
        if mo1 := re.search(r'(.)\1\1', h):
            c = mo1.group(1)
            fwd_re = c * 5
            for j in range(i + 1, i + 1002):
                if fwd_re in hlist.get(j):
                    keylist.append(h)

    return i


def part2():
    return None


def main():
    for inp in ('abc', 'yjdafjpo'):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
