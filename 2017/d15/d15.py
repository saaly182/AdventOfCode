#!/usr/bin/python3 -u

def generator(gid: str, prev_value: int) -> int:
    gid2factor = {'A': 16807, 'B': 48271}
    mprime = 2147483647
    if gid not in gid2factor:
        raise ValueError(f'id not found: {gid}')
    return (prev_value * gid2factor[gid]) % mprime


def judge(a, b):
    return a & 0b1111111111111111 == b & 0b1111111111111111


def part1(a_init: int, b_init: int) -> int:
    judge_count = 0
    a_prev, b_prev = a_init, b_init
    for i in range(40_000_000):
        a_now, b_now = generator('A', a_prev), generator('B', b_prev)
        judge_count += judge(a_now, b_now)
        a_prev, b_prev = a_now, b_now
    return judge_count


def part2():
    return None


def main():
    sample_input = (65, 8921)
    main_input = (516, 190)
    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(*inp))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
