#!/usr/bin/python3 -u

import re


class Screen:
    def __init__(self):
        self.rows = 6
        self.cols = 50
        self.pixels = [['.' for _ in range(self.cols)]
                       for _ in range(self.rows)]

    def show(self):
        print('v' * 75)
        for row in self.pixels:
            print(''.join(row))
        print('^' * 75)

    def litcount(self):
        return sum([r.count('#') for r in self.pixels])

    def run(self, prog):
        for line in prog:
            if mo := re.match(r'rect (\d+)x(\d+)', line):
                self._rect(int(mo.group(1)), int(mo.group(2)))
            elif mo := re.match(r'rotate (row|column) ([xy])=(\d+) by (\d+)',
                                line):
                self._rotate(mo.group(2), int(mo.group(3)), int(mo.group(4)))
            else:
                raise ValueError(f'bad prog line: {line}')

    def _rect(self, w, h):
        for row in range(h):
            for col in range(w):
                self.pixels[row][col] = '#'

    def _rotate(self, rc, idx, amount):
        if rc == 'y':
            self.pixels[idx] = rotate_right(self.pixels[idx], amount)
        elif rc == 'x':
            col = [self.pixels[r][idx] for r in range(self.rows)]
            col = rotate_right(col, amount)
            for row in range(self.rows):
                self.pixels[row][idx] = col[row]
        else:
            raise ValueError(f'bad prog input: {rc=}')


def rotate_right(lst, amount):
    """Return a right-shifted list, with wrap-around."""
    llen = len(lst)
    amount = amount % llen
    return lst[-amount:] + lst[:llen - amount]


def part1(inp):
    screen = Screen()
    screen.run(inp)
    return screen.litcount()


def part2(inp):
    screen = Screen()
    screen.run(inp)
    screen.show()
    return None


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
