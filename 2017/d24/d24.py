#!/usr/bin/python3 -u

from typing import Generator


def strength(bridge: list) -> int:
    return sum([a + b for _, (a, b) in bridge])


def _createbin(components: tuple) -> dict:
    ports = set([p for c in components for p in c[1]])
    portbin = {}
    for p in ports:
        for c in components:
            if p in c[1]:
                if p in portbin:
                    portbin[p].append(c)
                else:
                    portbin[p] = [c]
    return portbin


def gen_bridges(components: tuple, portbin: dict = None, idx: int = 0,
                b: list = None, endtype: int = 0) -> \
                Generator[list, None, None]:
    if not portbin:
        portbin = _createbin(components)
    if idx == 0:
        for c in portbin[0]:
            b = [c]
            endtype = c[1][0] if c[1][0] != 0 else c[1][1]
            yield b
            yield from gen_bridges(components, portbin, idx + 1, b, endtype)
    else:
        cids = set([x[0] for x in b])
        for c in portbin[endtype]:
            if c[0] in cids:
                continue
            else:
                b.append(c)
                next_endtype = c[1][0] if c[1][0] != endtype else c[1][1]
                yield b
                yield from gen_bridges(components, portbin, idx + 1, b,
                                       next_endtype)
                b.pop()
    return


def print_bridge(b: list) -> None:
    print('--'.join(f'({c[1][0]}/{c[1][1]})' for c in b))


def part1(components: tuple) -> int:
    max_st = 0
    for b in gen_bridges(components):
        max_st = max(max_st, strength(b))
    return max_st


def part2():
    return None


def slurp(fname: str) -> list[str]:
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp: list[str]) -> tuple:
    components = []
    cid = 1000
    for line in inp:
        a, b = line.split('/')
        components.append((cid, (int(a), int(b))))
        cid += 1
    return tuple(components)


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        components = parse(inp)
        print("Part 1 answer =", part1(components))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
