#!/usr/bin/python3 -u

import collections


def part1(num_players: int, hi_marble: int) -> int:
    circle = collections.deque([0])
    scores = [0] * (num_players + 1)
    player = 1

    for marble in range(1, hi_marble + 1):
        if marble % 23 == 0:
            circle.rotate(7)
            scores[player] += marble + circle.popleft()
        else:
            circle.rotate(-2)
            circle.appendleft(marble)

        player = player % num_players + 1

    return max(scores)


def part2(num_players: int, hi_marble: int) -> int:
    return part1(num_players, hi_marble * 100)


def main():
    inputs = ((9, 25), (10, 1618), (13, 7999), (17, 1104), (21, 6111),
              (30, 5807), (446, 71522))

    for num_players, hi_marble in inputs:
        print("Part 1 answer =", part1(num_players, hi_marble))
        print("Part 2 answer =", part2(num_players, hi_marble))
        print()


if __name__ == '__main__':
    main()
