#!/usr/bin/python3 -u

import math
import re


class Game:
    def __init__(self, game_line):
        m = re.match(r'Game (\d+): ', game_line)
        self.id = int(m.group(1))
        self.reveals = []
        for cset in game_line[m.end():].split(';'):
            cset = cset.strip()
            reveal = {'red': 0, 'green': 0, 'blue': 0}
            for cubecount in cset.split(','):
                count, color = cubecount.split()
                count = int(count)
                reveal[color] = count
            self.reveals.append(reveal)

    def __repr__(self):
        return f'Game(id={self.id}, reveals={self.reveals})'

    def is_possible(self, r: int, g: int, b: int) -> bool:
        for rev in self.reveals:
            if rev['red'] > r or rev['green'] > g or rev['blue'] > b:
                return False
        return True

    def mincounts(self) -> dict:
        mins = {'red': 0, 'green': 0, 'blue': 0}
        for rev in self.reveals:
            for color in rev:
                if rev[color] > mins[color]:
                    mins[color] = rev[color]
        return mins


def part1(games: list) -> int:
    idsum = 0
    for g in games:
        if g.is_possible(12, 13, 14):
            idsum += g.id
    return idsum


def part2(games: list) -> int:
    powersum = 0
    for g in games:
        power = math.prod(g.mincounts().values())
        powersum += power
    return powersum


def slurp(fname: str) -> tuple[str, ...]:
    with open(fname) as file:
        return tuple(line.rstrip() for line in file.readlines())


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        games = []
        for line in inp:
            games.append(Game(line))
        print("Part 1 answer =", part1(games))
        print("Part 2 answer =", part2(games))
        print()


if __name__ == '__main__':
    main()
