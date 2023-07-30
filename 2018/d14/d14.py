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


def part1(rcount: int) -> str:
    scores = [3, 7]
    elf1 = 0
    elf2 = 1

    while len(scores) < rcount + 10:
        scores.extend([int(d) for d in str(scores[elf1] + scores[elf2])])
        elf1 = (elf1 + 1 + scores[elf1]) % len(scores)
        elf2 = (elf2 + 1 + scores[elf2]) % len(scores)

    return ''.join([str(d) for d in scores[rcount:rcount + 10]])


def part2(seq: str) -> int:
    seqlen = len(seq)
    found = False
    scores = [3, 7]
    elf1 = 0
    elf2 = 1

    while not found:
        for d in [int(d) for d in str(scores[elf1] + scores[elf2])]:
            scores.append(d)
            if len(scores) >= seqlen:
                tail = ''.join([str(d) for d in scores[-seqlen:]])
                if tail == seq:
                    found = True
                    break
        elf1 = (elf1 + 1 + scores[elf1]) % len(scores)
        elf2 = (elf2 + 1 + scores[elf2]) % len(scores)

    return len(scores) - seqlen


def main():
    rcounts = (9, 5, 18, 2018, 30121)
    for rcount in rcounts:
        print(f"Part 1 answer for {rcount} =", part1(rcount))
        print()

    seqs = ('51589', '01245', '92510', '59414', '030121')
    for seq in seqs:
        print(f"Part 2 answer for {seq} =", part2(seq))
        print()


if __name__ == '__main__':
    main()
