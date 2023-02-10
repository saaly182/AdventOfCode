#!/usr/bin/python3 -u

def is_triangle(a, b, c):
    return a + b > c and b + c > a and a + c > b


def part1(tdata):
    tri_count = 0
    for t in tdata:
        if is_triangle(*t):
            tri_count += 1
    return tri_count


def part2(tdata):
    tri_count = 0
    for t3 in zip(tdata[::3], tdata[1::3], tdata[2::3]):
        for t in zip(*t3):
            if is_triangle(*t):
                tri_count += 1
    return tri_count


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    main_input = slurp('input/input.txt')

    for inp in (main_input,):
        tdata = tuple(tuple(map(int, line.split())) for line in inp)
        print("Part 1 answer =", part1(tdata))
        print("Part 2 answer =", part2(tdata))
        print()


if __name__ == '__main__':
    main()
