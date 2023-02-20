#!/usr/bin/python3 -u

trap = '^'
safe = '.'


def next_row(prev_row):
    """Return next row based on the prev row rules."""
    # Tile is a trap if:
    # Its left and center tiles are traps, but its right tile is not.
    # Its center and right tiles are traps, but its left tile is not.
    # Only its left tile is a trap.
    # Only its right tile is a trap.

    trapvals = {(trap, trap, safe), (safe, trap, trap),
                (trap, safe, safe), (safe, safe, trap)}

    pr = [safe] + list(prev_row) + [safe]  # add boundary points
    nr = ['X'] * len(pr)  # next row
    for i in range(1, len(pr) - 1):
        prvals = tuple(pr[i - 1:i + 2])
        nr[i] = trap if prvals in trapvals else safe

    return ''.join(nr[1:len(pr) - 1])


def count_safe(first_row, rsize):
    rows = [first_row]
    for i in range(rsize - 1):  # -1 to account for 1st row already existing
        nr = next_row(rows[-1])
        rows.append(nr)

    return ''.join(rows).count(safe)


def part1(first_row):
    return count_safe(first_row, 40)


def part2(first_row):
    return count_safe(first_row, 400_000)


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp[0]))
        print("Part 2 answer =", part2(inp[0]))
        print()


if __name__ == '__main__':
    main()
