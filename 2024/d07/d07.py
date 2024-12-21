#!/usr/bin/python3 -u

import itertools
import operator


def part1(equations: tuple) -> int:
    calibration_result = 0
    valid_ops = {'+': operator.add, '*': operator.mul}
    for e in equations:
        target = e[0]
        nums = e[1:]
        for ops in itertools.product(valid_ops.keys(), repeat=len(nums) - 1):
            res = nums[0]
            for op, num in zip(ops, nums[1:], strict=True):
                res = valid_ops[op](res, num)
            if res == target:
                calibration_result += res
                # print(f'{calibration_result} {res=} {target=} {nums=} {ops=}')
                break
    return calibration_result


def part2():
    return None


def slurp(fname: str) -> tuple[tuple[int, ...], ...]:
    a = []
    with open(fname) as file:
        for line in file:
            b = tuple(int(x) for x in line.replace(':', '').split())
            a.append(b)
    return tuple(a)


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
