#!/usr/bin/python3 -u

import dataclasses
import re


@dataclasses.dataclass
class Point:
    px: int
    py: int
    vx: int
    vy: int


def bounding_box(points: tuple[Point]) -> tuple[int]:
    minx = miny = float('inf')
    maxx = maxy = float('-inf')
    for p in points:
        if p.px < minx:
            minx = p.px
        if p.py < miny:
            miny = p.py
        if p.px > maxx:
            maxx = p.px
        if p.py > maxy:
            maxy = p.py
    return minx, miny, maxx, maxy


def showpoints(points: tuple[Point]) -> None:
    minx, miny, maxx, maxy = bounding_box(points)
    msg = [['.'] * (maxx - minx + 1) for _ in range(maxy - miny + 1)]
    for p in points:
        msg[p.py - miny][p.px - minx] = '#'
    msgstr = '\n'.join([''.join(x) for x in msg])
    print(msgstr)
    print()


def part1(points: tuple[Point]) -> None:
    print('Searching...')
    bb = bounding_box(points)
    # 100 x 100 is just a practical hueristic upper bound on msg size
    bbarea_min = min(100 * 100, (bb[2] - bb[0] + 1) * (bb[3] - bb[1] + 1))
    for t in range(20000):
        for p in points:
            p.px += p.vx
            p.py += p.vy
        bb = bounding_box(points)
        bbarea = (bb[2] - bb[0] + 1) * (bb[3] - bb[1] + 1)
        if bbarea < bbarea_min:
            bbarea_min = bbarea
            print(f'New potential answer at time {t + 1} seconds:')
            showpoints(points)


def slurp(fname: str) -> list[str]:
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp: list) -> tuple[Point]:
    points = []

    restr = r'position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>'
    for line in inp:
        mo = re.fullmatch(restr, line)
        if not mo:
            raise ValueError(f'bad input: {line}')
        points.append(Point(*[int(x) for x in mo.group(1, 2, 3, 4)]))

    return tuple(points)


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        points = parse(inp)
        print("Part 1 answer =", part1(points))
        print()


if __name__ == '__main__':
    main()
