#!/usr/bin/python3 -u

def show(circle, pos):
    for i, c in enumerate(circle):
        if i == pos:
            print(f'({c}) ', end='')
        else:
            print(f'{c} ', end='')
    print()


def part1(num_players: int, hi_marble: int) -> int:
    circle = [0]
    scores = [0] * (num_players + 1)
    player = 1
    pos = 0

    for marble in range(1, hi_marble + 1):
        if marble % 23 == 0:
            delidx = pos - 7
            scores[player] += marble + circle[delidx]
            pos = delidx if delidx >= 0 else len(circle) + delidx
            del circle[delidx]
        else:
            ins = (pos + 2) % len(circle)
            if ins == 0:
                ins = len(circle)
            circle.insert(ins, marble)
            pos = ins

        player += 1
        if player > num_players:
            player = 1

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
