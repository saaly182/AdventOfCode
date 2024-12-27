#!/usr/bin/python3 -u

import functools


@functools.cache
def blinkstones(stone: int, blink_count: int) -> int:
    """Dynamic Programming approach."""

    # end of recursion
    if blink_count == 0:
        return 1

    bcm1 = blink_count - 1

    # rule 1
    if stone == 0:
        return blinkstones(1, bcm1)

    # rule 2
    sstr = str(stone)
    sl = len(sstr)
    if sl % 2 == 0:
        mid_idx = sl // 2
        sleft = int(sstr[:mid_idx])
        sright = int(sstr[mid_idx:])
        return blinkstones(sleft, bcm1) + blinkstones(sright, bcm1)

    # rule 3
    return blinkstones(stone * 2024, bcm1)


def part1(stones: list, blink_count: int) -> int:
    final_stone_count = 0
    for st in stones:
        final_stone_count += blinkstones(st, blink_count)
    return final_stone_count


def slurp(fname: str) -> tuple[str, ...]:
    with open(fname) as file:
        return tuple(line.rstrip() for line in file.readlines())


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        stones = [int(x) for x in inp[0].split()]
        print("Part 1 answer =", part1(stones[:], 25))
        print("Part 2 answer =", part1(stones[:], 75))
        print()


if __name__ == '__main__':
    main()
