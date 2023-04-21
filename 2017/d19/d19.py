#!/usr/bin/python3 -u

import sys
sys.path.append('../../lib')
import dirutils

SPACE = ' '


def part1(diagram: tuple) -> str:
    r1 = 0
    c1 = diagram[0].index('|')
    dirvec = dirutils.dirvecs['S']
    letters = []
    at_end = False

    while not at_end:
        r2 = r1 + dirvec[0]
        c2 = c1 + dirvec[1]
        try:
            x = diagram[r2][c2]
        except IndexError:
            # this can happen if the path ends with a letter
            if diagram[r1][c1].isalpha():
                at_end = True
                continue
            else:
                raise

        if x == '|' or x == '-':
            pass

        elif x.isalpha():
            letters.append(x)

            # peek at the next cell to check for end-of-path
            r3 = r2 + dirvec[0]
            c3 = c2 + dirvec[1]
            try:
                y = diagram[r3][c3]
                if y == SPACE:
                    at_end = True
            except IndexError:
                at_end = True

        elif x == '+':
            new_dirvec = None
            for uv in dirutils.unitvecs:
                r3 = r2 + uv[0]
                c3 = c2 + uv[1]
                try:
                    y = diagram[r3][c3]
                except IndexError:
                    continue
                if y == SPACE:
                    continue
                if dirvec[0] + uv[0] == 0 and dirvec[1] + uv[1] == 0:
                    # this is going back from where we came, so ignore
                    continue
                assert new_dirvec is None  # otherwise there are two exits
                new_dirvec = uv
            if new_dirvec is None:
                at_end = True
            else:
                dirvec = new_dirvec

        else:
            raise ValueError(f'invalid char at {r2}, {c2}: {x}')
        r1, c1 = r2, c2

    return ''.join(letters)


def part2():
    return None


def slurp(fname: str) -> list[str]:
    with open(fname) as file:
        return [line.rstrip('\n') for line in file.readlines()]


def parse(inp: list) -> tuple:
    diagram = []
    for line in inp:
        diagram.append(tuple(line))
    return tuple(diagram)


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        diagram = parse(inp)
        print("Part 1 answer =", part1(diagram))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
