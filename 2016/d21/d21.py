#!/usr/bin/python3 -u

def rotate_by_steps(a, direction, steps):
    """Return list "a" rotated left or right n steps."""
    # make both cases a left shift
    if direction == 'right':
        steps = len(a) - steps
    return a[steps:len(a)] + a[0:steps]


def rotate_by_position(a, b):
    """
    Return list "a" rotated based on the letter b, per problem rules.

    "rotate based on position of letter X means that the whole string should
    be rotated to the right based on the index of letter X (counting from 0)
    as determined before this instruction does any rotations. Once the index
    is determined, rotate the string to the right one time, plus a number of
    times equal to that index, plus one additional time if the index was at
    least 4."
    """
    bi = a.index(b)
    rotations = bi + 1
    if bi >= 4:
        rotations += 1
    return rotate_by_steps(a, 'right', rotations)


def scramble(pwstr, ops):
    # Note that the description doesn't explicitly call this out, but it
    # implies that the pwstr does not have any repeat letters.
    pw = list(pwstr)
    for op in ops:
        match op.split():
            case ('swap', 'position', x, 'with', 'position', y):
                x = int(x)
                y = int(y)
                pw[x], pw[y] = pw[y], pw[x]
            case ('swap', 'letter', x, 'with', 'letter', y):
                xi = pw.index(x)
                yi = pw.index(y)
                pw[xi], pw[yi] = pw[yi], pw[xi]
            case ('rotate', direction, x, ('step' | 'steps')):
                pw = rotate_by_steps(pw, direction, int(x))
            case ('rotate', 'based', 'on', 'position', 'of', 'letter', x):
                pw = rotate_by_position(pw, x)
            case ('reverse', 'positions', x, 'through', y):
                x = int(x)
                y = int(y)
                pw[x:y + 1] = reversed(pw[x:y + 1])
            case ('move', 'position', x, 'to', 'position', y):
                x = int(x)
                y = int(y)
                z = pw[x]
                del pw[x]
                pw.insert(y, z)
            case _:
                raise ValueError(op)

    return ''.join(pw)


def part1(password, operations):
    return scramble(password, operations)


def part2():
    return None


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    sample_input = ('abcde', slurp('input/sample_input.txt'))
    main_input = ('abcdefgh', slurp('input/input.txt'))

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(*inp))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
