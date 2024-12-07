#!/usr/bin/python3 -u

import re


def part1(rules: tuple, pagelists: tuple) -> int:
    middles_sum = 0

    for pages in pagelists:
        pset = set(pages)
        # code assumes no dups in each list of pages
        assert len(pages) == len(pset)

        # create hash of indexes
        pidx = dict([(b, a) for a, b in enumerate(pages)])

        prules = []  # rules for these pages
        for r in rules:
            if r[0] in pset and r[1] in pset:
                prules.append(r)

        correct = True
        for ra, rb in prules:
            if pidx[ra] > pidx[rb]:
                correct = False
                break

        if correct:
            assert len(pages) % 2 == 1
            middle = pages[len(pages) // 2]  # don't forget zero-based indexes
            middles_sum += middle

    return middles_sum


def part2():
    return None


def slurp(fname: str) -> tuple[str, ...]:
    with open(fname) as file:
        return tuple(line.rstrip() for line in file.readlines())


def parse_input(lines: tuple[str, ...]) -> tuple:
    rules = []
    pagelists = []
    for line in lines:
        if m := re.fullmatch(r'(\d+)\|(\d+)', line):
            rules.append((int(m.group(1)), int(m.group(2))))
        elif re.fullmatch(r'\d+(,\d+)*', line):
            pagelists.append(tuple(int(x) for x in line.split(',')))
        elif not line:
            pass
        else:
            raise ValueError(f'bad input: {line}')
    return tuple(rules), tuple(pagelists)


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        rules, pagelists = parse_input(inp)
        print("Part 1 answer =", part1(rules, pagelists))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
