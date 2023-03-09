#!/usr/bin/python3 -u

import functools


def twist(lst, pos, length):
    """Reverse the slice at pos with length in list lst.
    Treat lst as circular. Modifies lst in place."""
    len_lst = len(lst)

    if length > len_lst:
        raise ValueError(f'length param longer than lst: {length}')

    pos = pos % len_lst

    # easy case with no circular index wrapping
    if pos + length <= len_lst:
        lst[pos:pos + length] = reversed(lst[pos:pos + length])
        return

    # complex case with circular wrap-around
    rev_tail_head = list(reversed(lst[pos:] + lst[:length + pos - len_lst]))
    lst[pos:] = rev_tail_head[:len_lst - pos]
    lst[:length + pos - len_lst] = rev_tail_head[len_lst - pos:]


def densify(sparse_hash):
    dense_hash = []
    for i in range(0, 256, 16):
        dense_hash.append(functools.reduce(lambda x, y: x ^ y,
                                           sparse_hash[i:i + 16]))
    return dense_hash


def hexify(lst):
    return ''.join([f'{a:02x}' for a in lst])


def knot_hash(s):
    lengths = [ord(a) for a in s] + [17, 31, 73, 47, 23]
    sparse_hash = list(range(256))
    pos = 0
    skip = 0
    for _ in range(64):
        for length in lengths:
            twist(sparse_hash, pos, length)
            pos += length + skip
            skip += 1

    return hexify(densify(sparse_hash))


def part1(lengths_str):
    lengths = tuple([int(a) for a in lengths_str.split(',')])
    x = list(range(256))
    pos = 0
    skip = 0
    for length in lengths:
        twist(x, pos, length)
        pos += length + skip
        skip += 1
    return x[0] * x[1]


def part2(s):
    return knot_hash(s)


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    main_input = slurp('input/input.txt')
    for inp in (main_input, ):
        print("Part 1 answer =", part1(inp[0]))
        print("Part 2 answer =", part2(inp[0]))
        print()


if __name__ == '__main__':
    main()
