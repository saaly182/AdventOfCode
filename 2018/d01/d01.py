#!/usr/bin/python3 -u

def part1(nums: tuple) -> int:
    return sum(nums)


def part2(nums: tuple) -> int:
    freq = 0
    fset = {freq}
    while True:
        for delta in nums:
            freq += delta
            if freq in fset:
                return freq
            else:
                fset.add(freq)


def slurp(fname: str) -> list[str]:
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp: list) -> tuple:
    return tuple([int(x) for x in inp])


def main():
    main_input = slurp('input/input.txt')

    for inp in (main_input,):
        nums = parse(inp)
        print("Part 1 answer =", part1(nums))
        print("Part 2 answer =", part2(nums))
        print()


if __name__ == '__main__':
    main()
