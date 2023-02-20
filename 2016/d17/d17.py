#!/usr/bin/python3 -u

import collections
import hashlib


def md5hex(msg):
    m = hashlib.md5()
    m.update(msg.encode('UTF-8'))
    return m.hexdigest()


def open_doors(passcode, path):
    """Return the tuple of open doors under the input conditions."""
    s = passcode + ''.join(path)
    od = []  # open doors
    h = md5hex(s)[:4]
    opencodes = 'bcdef'
    dirs = 'UDLR'
    for i in range(4):
        if h[i] in opencodes:
            od.append(dirs[i])
    return tuple(od)


def bfs(passcode, find_shortest=True):
    """
    Return shortest or longest path to the destination room.
    Given the nature of this problem (dynamically using md5 hashes), I'm
    assuming that it's pointless to track any sort of "visited" state in
    this BFS.
    """
    tgt = (3, 3)
    longest_path = []
    q = collections.deque([(0, 0, [], open_doors(passcode, []))])
    while q:
        r, c, path, od = q.popleft()
        if (r, c) == tgt:
            if find_shortest:
                return ''.join(path)
            else:
                if len(path) > len(longest_path):
                    longest_path = path
                continue

        for door in od:
            npath = nr = nc = None
            match door:
                case 'U':
                    if r > 0:
                        npath = 'U'
                        nr, nc = r - 1, c
                case 'D':
                    if r < 3:
                        npath = 'D'
                        nr, nc = r + 1, c
                case 'L':
                    if c > 0:
                        npath = 'L'
                        nr, nc = r, c - 1
                case 'R':
                    if c < 3:
                        npath = 'R'
                        nr, nc = r, c + 1
            if npath:
                newpath = path.copy() + [npath]
                q.append((nr, nc, newpath, open_doors(passcode, newpath)))

    # if we got here, then we are looking for the longest path
    assert find_shortest is False
    return ''.join(longest_path)


def part1(passcode):
    return bfs(passcode)


def part2(passcode):
    return len(bfs(passcode, find_shortest=False))


def main():
    for inp in ('ihgpwlah', 'kglvqrro', 'ulqzkmiv', 'dmypynyp'):
        print(f'{inp=}')
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
