#!/usr/bin/python3 -u

def part1(inp):
    paper_needed = 0
    for dims in inp:
        l, w, h = (int(x) for x in dims.split('x'))
        areas = l * w, l * h, w * h
        paper_needed += 2 * (sum(areas)) + min(areas)
    return paper_needed


def part2(inp):
    ribbon_needed = 0
    for dims in inp:
        l, w, h = (int(x) for x in dims.split('x'))
        perims = 2 * (l + w), 2 * (l + h), 2 * (w + h)
        volume = l * w * h
        ribbon_needed += min(perims) + volume
    return ribbon_needed


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
