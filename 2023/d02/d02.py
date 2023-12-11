#!/usr/bin/python3 -u

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


def part1(inp: tuple[str, ...]) -> int:
    games = []
    for line in inp:
        games.append(Game(line))
    idsum = 0
    for g in games:
        if g.is_possible(12, 13, 14):
            idsum += g.id
    return idsum


def part2():
    return None


def slurp(fname: str) -> tuple[str, ...]:
    with open(fname) as file:
        return tuple(line.rstrip() for line in file.readlines())


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
