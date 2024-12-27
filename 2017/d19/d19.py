#!/usr/bin/python3 -u

import sys
sys.path.append('../../lib')
import dirutils  # noqa: E402 F401

SPACE = ' '
BOUNDARY = '@'


def travel_path(diagram: tuple) -> tuple[str, int]:
    r1 = 1
    c1 = diagram[1].index('|')
    dirvec = dirutils.dirvecs['S']
    letters = []
    step_count = 1
    at_end = False

    while not at_end:
        r2 = r1 + dirvec[0]
        c2 = c1 + dirvec[1]
        x = diagram[r2][c2]
        if x == BOUNDARY or x == SPACE:
            at_end = True
            continue

        step_count += 1

        if x == '|' or x == '-':
            pass

        elif x.isalpha():
            letters.append(x)

        elif x == '+':
            new_dirvec = None
            for uv in dirutils.unitvecs:
                r3 = r2 + uv[0]
                c3 = c2 + uv[1]
                y = diagram[r3][c3]
                if y == BOUNDARY or y == SPACE:
                    continue
                if dirvec[0] + uv[0] == 0 and dirvec[1] + uv[1] == 0:
                    # this is going back from where we came, so ignore
                    continue
                assert new_dirvec is None  # otherwise there are multiple exits
                new_dirvec = uv
            if new_dirvec is None:
                at_end = True
            else:
                dirvec = new_dirvec

        else:
            raise ValueError(f'invalid char at {r2}, {c2}: {x}')
        r1, c1 = r2, c2

    return ''.join(letters), step_count


def part1(diagram: tuple) -> str:
    return travel_path(diagram)[0]


def part2(diagram: tuple) -> int:
    return travel_path(diagram)[1]


def slurp(fname: str) -> list[str]:
    with open(fname) as file:
        return [line.rstrip('\n') for line in file.readlines()]


def parse(inp: list) -> tuple:
    # include ghost points around all edges
    ghostrow = tuple(BOUNDARY * (len(inp[0]) + 2))
    diagram = [ghostrow]
    for line in inp:
        diagram.append(tuple(BOUNDARY + line + BOUNDARY))
    diagram.append(ghostrow)
    return tuple(diagram)


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        diagram = parse(inp)
        print("Part 1 answer =", part1(diagram))
        print("Part 2 answer =", part2(diagram))
        print()


if __name__ == '__main__':
    main()
