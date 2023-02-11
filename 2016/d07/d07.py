#!/usr/bin/python3 -u

import re


def tokenize(ip):
    spec = r'([a-z]+|\[[a-z]+\])'
    idx = 0
    while mo := re.match(spec, ip[idx:]):
        tok = mo.group(0)
        idx += len(tok)
        yield mo.group(0)


def supports_tls(ip):
    abba = r'([a-z])([a-z])\2\1'
    st = False
    for token in tokenize(ip):
        if mo := re.search(abba, token):
            a, b = mo.groups()
            if a != b:
                if token[0] == '[':
                    # ABBA found in hypernet sequence, return immediately
                    return False
                else:
                    st = True
    return st


def part1(inp):
    tls_count = 0
    for ip in inp:
        if supports_tls(ip):
            tls_count += 1
    return tls_count


def part2():
    return None


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
