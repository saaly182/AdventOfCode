#!/usr/bin/python3 -u

import json
import re


def part1(inp):
    s = inp[0]
    all_num_sum = sum([int(x) for x in re.findall(r'-?\d+', s)])
    return all_num_sum


def clear_red(x):
    """Recursively examine all elements and clear any dict with a value 'red'"""
    tx = type(x)

    if tx not in (int, str, list, dict):
        raise ValueError(x)

    if tx in (int, str):
        return

    if tx == list:
        for y in x:
            clear_red(y)
        return

    # dict handling
    if 'red' in x.values():
        x.clear()
    for y in x:
        clear_red(x[y])


def part2(inp):
    jdata = json.loads(inp[0])
    clear_red(jdata)
    all_num_sum = sum([int(x) for x in re.findall(r'-?\d+', str(jdata))])
    return all_num_sum


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
