#!/usr/bin/python3 -u

def part1(polymer: str, unitpairs: dict) -> int:
    p1 = list(polymer)
    p2 = []
    changed = True

    while changed:
        changed = False
        p2 = []
        i = 0
        i_limit = len(p1) - 1

        while i < i_limit:
            if p1[i + 1] != unitpairs[p1[i]]:
                p2.append(p1[i])
            else:
                changed = True
                i += 1
            i += 1

        # handle last unit
        if i == i_limit:
            p2.append(p1[i])

        p1 = p2

    return len(p2)


def part2():
    return None


def slurp(fname: str) -> list[str]:
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def make_up() -> dict:
    unitpairs = {}
    ai = ord('A')
    for i in range(ai, ai + 26):
        c_upper = chr(i)
        c_lower = c_upper.lower()
        unitpairs[c_upper] = c_lower
        unitpairs[c_lower] = c_upper
    return unitpairs


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    unitpairs = make_up()

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp[0], unitpairs))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
