#!/usr/bin/python3 -u

def make_cbuf(step_size: int, lastval: int) -> list[int]:
    cbuf = [0]
    pos = 0
    for i in range(1, lastval + 1):
        pos = (pos + step_size) % len(cbuf)
        if pos == len(cbuf) - 1:
            cbuf.append(i)
        else:
            cbuf.insert(pos + 1, i)
        pos += 1
        if i % 100_000 == 0:
            print(f'insertions left = {lastval - i:,}')
    return cbuf


def part1(step_size: int) -> int:
    lastval = 2017
    cbuf = make_cbuf(step_size, lastval)
    idx = (cbuf.index(lastval) + 1) % len(cbuf)
    return cbuf[idx]


def part2(step_size: int) -> int:
    lastval = 50_000_000
    cbuf = make_cbuf(step_size, lastval)
    idx = (cbuf.index(0) + 1) % len(cbuf)
    return cbuf[idx]


def slurp(fname: str) -> list[str]:
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    for inp in (3, 366):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
