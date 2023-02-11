#!/usr/bin/python3 -u

import hashlib


def genhashes(s):
    i = 0
    prefix_target = '0' * 5
    while True:
        m = hashlib.md5()
        msg = s + str(i)
        m.update(msg.encode('UTF-8'))
        h = m.hexdigest()
        if h.startswith(prefix_target):
            yield h
        i += 1


def part1(doorid):
    password = []
    for h in genhashes(doorid):
        password.append(h[5])
        if len(password) == 8:
            break
    return ''.join(password)


def part2(doorid):
    blank = '_'
    password = [blank] * 8
    for h in genhashes(doorid):
        pos = h[5]
        if pos not in '01234567':
            continue
        pos = int(pos)
        val = h[6]
        if password[pos] == blank:
            password[pos] = val
        if blank not in password:
            break
    return ''.join(password)


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    print("Part 1 answer =", part1('wtnhxymk'))
    print("Part 2 answer =", part2('wtnhxymk'))
    print()


if __name__ == '__main__':
    main()
