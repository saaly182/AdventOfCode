#!/usr/bin/python3 -u

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


def part1(lengths):
    x = list(range(256))
    pos = 0
    skip = 0
    for length in lengths:
        twist(x, pos, length)
        pos += length + skip
        skip += 1
    return x[0] * x[1]


def part2():
    return None


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    main_input = slurp('input/input.txt')
    for inp in (main_input, ):
        lengths = tuple([int(a) for a in inp[0].split(',')])
        print("Part 1 answer =", part1(lengths))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
