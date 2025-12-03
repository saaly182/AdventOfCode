#!/usr/bin/python3 -u

def is_valid(i: int, chunkcount=None) -> bool:
    # If chunkcount is specified, then just consider that chunkcount.
    # If chunkcount is None, the consider all possible chunkcounts in turn.

    s = str(i)

    if chunkcount is None:
        for n in range(2, len(s) + 1):
            if not is_valid(i, n):
                return False
        return True

    if len(s) % chunkcount != 0:
        return True

    unique_chunks = set()
    chunksize = len(s) // chunkcount
    for x in range(0, len(s), chunksize):
        chunk = s[x:x + chunksize]
        unique_chunks.add(chunk)

    if len(unique_chunks) == 1:
        return False

    return True


def part1(ranges: tuple, chunkcount=2) -> int:
    invalids_sum = 0
    for r in ranges:
        for i in range(r[0], r[1] + 1):
            if not is_valid(i, chunkcount):
                invalids_sum += i
    return invalids_sum


def part2(ranges: tuple) -> int:
    return part1(ranges, None)


def parse_input(fname: str) -> tuple:
    ranges = []
    with open(fname) as file:
        line = file.readline()
    for rangestr in line.split(','):
        x1, x2 = rangestr.split('-')
        ranges.append((int(x1), int(x2)))
    return tuple(ranges)


def main():
    sample_input = parse_input('input/sample_input.txt')
    main_input = parse_input('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
