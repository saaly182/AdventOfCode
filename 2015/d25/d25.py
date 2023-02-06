#!/usr/bin/python3 -u

def seqnum(row, col):
    """Return the sequence number at the given row, col."""
    d = row + col - 1  # diagonal number
    n = d * (d - 1) // 2 + col
    return n


def part1(row_t, col_t):
    s = seqnum(row_t, col_t)
    code = 20151125
    for i in range(2, s + 1):
        code = (code * 252533) % 33554393
    return code


def main():
    # Input: "To continue, please consult the code grid in the manual.
    # Enter the code at row 2947, column 3029."

    print("Part 1 answer =", part1(2947, 3029))
    print()


if __name__ == '__main__':
    main()
