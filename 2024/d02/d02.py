#!/usr/bin/python3 -u

def cmp(a, b):
    return (a > b) - (a < b)


def monotonic(x) -> bool:
    """Return True if elements are stricly increasing or decreasing"""
    if len(x) < 2:
        return True

    direction = 0
    for a, b in zip(x, x[1:]):
        if a == b:
            return False
        if not direction:
            direction = cmp(a, b)
        else:
            if cmp(a, b) != direction:
                return False

    return True


def safe_steps(x) -> bool:
    """Return True if all step sizes are between 1 and 3 inclusive"""
    if len(x) < 2:
        return True

    for a, b in zip(x, x[1:]):
        if not 1 <= abs(a - b) <= 3:
            return False

    return True


def is_safe(x) -> bool:
    return monotonic(x) and safe_steps(x)


def part1(reports: tuple) -> int:
    safe_count = 0
    for r in reports:
        if is_safe(r):
            safe_count += 1
    return safe_count


def part2(reports: tuple) -> int:
    safe_count = 0
    for r in reports:
        if is_safe(r):
            safe_count += 1
        else:
            # just brute force check all possible removals
            for i in range(len(r)):
                r2 = r[:i] + r[i + 1:]
                if is_safe(r2):
                    safe_count += 1
                    break
    return safe_count


def slurp(fname: str) -> tuple:
    reports = []
    with open(fname) as file:
        for line in file.readlines():
            reports.append(tuple(int(x) for x in line.split()))
    return tuple(reports)


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
