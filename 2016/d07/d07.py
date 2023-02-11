#!/usr/bin/python3 -u

import re


def tokenize(ip):
    spec = r'([a-z]+|\[[a-z]+\])'
    idx = 0
    while mo := re.match(spec, ip[idx:]):
        tok = mo.group(0)
        idx += len(tok)
        yield tok


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


def supports_ssl(ip):
    # need to use lookahead assertion (?=) to find overlapping results
    aba = r'(?=(([a-z]).\2))'
    supernet_abas = set()
    hypernet_abas = set()

    for token in tokenize(ip):
        mos = re.finditer(aba, token)
        for mo in mos:
            s = mo.group(1)
            if s[0] == s[1]:  # this is an 'aaa' not an 'aba'
                continue
            if token[0] == '[':
                hypernet_abas.add(s)
            else:
                supernet_abas.add(s)

    for aba in supernet_abas:
        x, y = aba[:2]
        if ''.join((y, x, y)) in hypernet_abas:
            return True

    return False


def part1(inp):
    tls_count = 0
    for ip in inp:
        if supports_tls(ip):
            tls_count += 1
    return tls_count


def part2(inp):
    ssl_count = 0
    for ip in inp:
        if supports_ssl(ip):
            ssl_count += 1
    return ssl_count


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
