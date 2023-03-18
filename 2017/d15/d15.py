#!/usr/bin/python3 -u

from typing import Iterator


def generator(gid: str, init_value: int, divisor: int = 1) -> Iterator[int]:
    gid2factor = {'A': 16807, 'B': 48271}
    if gid not in gid2factor:
        raise ValueError(f'id not found: {gid}')
    factor = gid2factor[gid]
    mprime = 2147483647
    prev_value = init_value
    while True:
        this_value = (prev_value * factor) % mprime
        if this_value % divisor == 0:
            yield this_value
        prev_value = this_value


def judgecmp(a, b):
    return a & 0b1111111111111111 == b & 0b1111111111111111


def judge_count(a_init: int, b_init: int, comparisons: int,
                a_div: int = 1, b_div: int = 1) -> int:
    count = 0
    i = 0
    for a, b in zip(generator('A', a_init, a_div),
                    generator('B', b_init, b_div)):
        count += judgecmp(a, b)
        i += 1
        if i >= comparisons:
            break
    return count


def part1(a_init: int, b_init: int) -> int:
    return judge_count(a_init, b_init, 40_000_000)


def part2(a_init: int, b_init: int) -> int:
    return judge_count(a_init, b_init, 5_000_000, 4, 8)


def main():
    sample_input = (65, 8921)
    main_input = (516, 190)
    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(*inp))
        print("Part 2 answer =", part2(*inp))
        print()


if __name__ == '__main__':
    main()
