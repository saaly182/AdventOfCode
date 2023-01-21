#!/usr/bin/python3 -u

import re


def is_nice1(s):
    """
    A nice string is one with all of the following properties:
    * It contains at least three vowels (aeiou only), like aei, xazegov, or
      aeiouaeiouaeiou.
    * It contains at least one letter that appears twice in a row, like xx,
      abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
    * It does not contain the strings ab, cd, pq, or xy, even if they are part
      of one of the other requirements.
    """
    if re.search('ab|cd|pq|xy', s):
        return False
    if not re.search('.*[aeiou].*[aeiou].*[aeiou]', s):
        return False
    if not re.search(r'(.)\1', s):
        return False
    return True


def is_nice2(s):
    """
    Now, a nice string is one with all of the following properties:
    * It contains a pair of any two letters that appears at least twice in the
      string without overlapping, like xyxy (xy) or aabcdefgaa (aa), but not
      like aaa (aa, but it overlaps).
    * It contains at least one letter which repeats with exactly one letter
      between them, like xyx, abcdefeghi (efe), or even aaa.
    """
    if re.search(r'(..).*\1', s) and re.search(r'(.).\1', s):
        return True
    return False


def part1(inp):
    return len([s for s in inp if is_nice1(s)])


def part2(inp):
    return len([s for s in inp if is_nice2(s)])


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    main_input = slurp('input/input.txt')

    for inp in (main_input, ):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
