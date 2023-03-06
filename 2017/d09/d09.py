#!/usr/bin/python3 -u

def score(cstream):
    """Return the score for the chr stream."""
    sc = 0
    grplevel = 0
    in_garbage = False

    i = 0
    while i < len(cstream):
        c = cstream[i]
        i += 1
        match c:
            case '!':
                i += 1
            case '<':
                if not in_garbage:
                    in_garbage = True
            case '>':
                if in_garbage:
                    in_garbage = False
            case '{':
                if not in_garbage:
                    grplevel += 1
                    sc += grplevel
            case '}':
                if not in_garbage:
                    grplevel -= 1

    return sc


def garbage_count(cstream):
    """Return the count of garbage chars per part2 rules."""
    gc = 0
    in_garbage = False

    i = 0
    while i < len(cstream):
        c = cstream[i]
        i += 1
        match c:
            case '!':
                i += 1
            case '<':
                if not in_garbage:
                    in_garbage = True
                else:
                    gc += 1
            case '>':
                if in_garbage:
                    in_garbage = False
            case _:
                if in_garbage:
                    gc += 1

    return gc


def part1(cstream):
    return score(cstream)


def part2(cstream):
    return garbage_count(cstream)


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp[0]))
        print("Part 2 answer =", part2(inp[0]))
        print()


if __name__ == '__main__':
    main()
