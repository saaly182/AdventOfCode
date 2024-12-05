#!/usr/bin/python3 -u

import re


def part1(memory: str) -> int:
    answer = 0
    for mult in re.findall(r'mul\((\d+),(\d+)\)', memory):
        answer += int(mult[0]) * int(mult[1])
    return answer


def part2(memory: str) -> int:
    answer = 0
    domul = True
    opmatch = r"mul\((\d+),(\d+)\)|(do\(\))|(don't\(\))"
    for op in re.findall(opmatch, memory):
        if op[2]:
            domul = True
            continue
        if op[3]:
            domul = False
            continue
        if domul:
            answer += int(op[0]) * int(op[1])
    return answer


def slurp(fname: str) -> str:
    with open(fname) as file:
        return file.read()


def main():
    sample_input = slurp('input/sample_input_2.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
