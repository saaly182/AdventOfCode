#!/usr/bin/python3 -u

import functools


def snafu2decimal(sna):
    dec = 0
    place_val = 1
    for digit in sna[::-1]:
        match digit:
            case '0' | '1' | '2' as multiplier:
                dec += int(multiplier) * place_val
            case '-':
                dec -= 1 * place_val
            case '=':
                dec -= 2 * place_val
            case _ as d:
                raise ValueError(f'bad input = "{d}"')
        place_val *= 5
    return dec


@functools.lru_cache(maxsize=None)
def _boundary(place_val):
    b = 0
    while place_val > 0:
        b += 2 * place_val
        place_val //= 5
    return b


def decimal2snafu(dec):
    sna = []
    place_val = 1
    while dec > _boundary(place_val):
        place_val *= 5
    pv = place_val

    while pv > 0:
        pv_next = pv // 5
        for digit in range(-2, 3):
            dec_next = dec - digit * pv
            if abs(dec_next) <= _boundary(pv_next):
                sna.append(digit)
                pv = pv_next
                dec = dec_next
                break
        assert pv == pv_next  # it's required that one of the digits worked

    # now dec contains the remaining one's value
    # sna.append(dec)

    snaval = ''.join(['012=-'[i] for i in sna])

    return snaval


def part1(inp):
    return decimal2snafu(sum([snafu2decimal(snafu_num) for snafu_num in inp]))


def part2():
    return None


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    sample_input = slurp('sample_input.txt')
    main_input = slurp('input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
