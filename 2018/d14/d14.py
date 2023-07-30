#!/usr/bin/python3 -u

def show(scores: list, e1: int, e2: int) -> None:
    for i, s in enumerate(scores):
        if i == e1:
            print(f'({s})', end='')
        elif i == e2:
            print(f'[{s}]', end='')
        else:
            print(f' {s} ', end='')
    print()


def part1(rcount: int):
    scores = [3, 7]
    elf1 = 0
    elf2 = 1

    while len(scores) < rcount + 10:
        scores.extend([int(d) for d in str(scores[elf1] + scores[elf2])])
        elf1 = (elf1 + 1 + scores[elf1]) % len(scores)
        elf2 = (elf2 + 1 + scores[elf2]) % len(scores)

    return ''.join([str(d) for d in scores[rcount:rcount + 10]])


def part2():
    return None


def main():
    rcounts = (9, 5, 18, 2018, 30121)
    for rcount in rcounts:
        print(f"Part 1 answer for {rcount} =", part1(rcount))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
