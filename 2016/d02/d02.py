#!/usr/bin/python3 -u

import sys
sys.path.append('../../lib')
import dirutils  # noqa: E402

keypad_part1 = ['00000',
                '01230',
                '04560',
                '07890',
                '00000']

keypad_part2 = ['0000000',
                '0001000',
                '0023400',
                '0567890',
                '00ABC00',
                '000D000',
                '0000000']


def part1(inp, keypad, r, c):
    code = []

    for seq in inp:
        for letter in seq:
            rn = r + dirutils.dirvecs[letter][0]
            cn = c + dirutils.dirvecs[letter][1]
            if keypad[rn][cn] == '0':
                continue  # ignore if this would take us off the keypad
            r, c = rn, cn
        code.append(keypad[r][c])

    return ''.join(code)


def part2(inp, keypad, r, c):
    return part1(inp, keypad, r, c)


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp, keypad_part1, 2, 2))
        print("Part 2 answer =", part2(inp, keypad_part2, 3, 1))
        print()


if __name__ == '__main__':
    main()
