#!/usr/bin/python3 -u

def look_and_say(num):
    if not num.isnumeric():
        raise ValueError(num)

    lsnum = []
    curr_digit = num[0]
    curr_count = 1
    for digit in list(num[1:]):
        if digit == curr_digit:
            curr_count += 1
        else:
            lsnum.extend([str(curr_count), curr_digit])
            curr_digit = digit
            curr_count = 1
    lsnum.extend([str(curr_count), curr_digit])

    return ''.join(lsnum)


def part1(num, rotations):
    lsnum = num
    for r in range(rotations):
        lsnum = look_and_say(lsnum)
    return len(lsnum)


def part2(num, rotations):
    return part1(num, rotations)


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    assert look_and_say('111221') == '312211'
    print("Part 1 answer =", part1('3113322113', 40))
    print("Part 2 answer =", part2('3113322113', 50))
    print()


if __name__ == '__main__':
    main()
