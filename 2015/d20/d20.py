#!/usr/bin/python3 -u

def factors(n):
    facs = set()
    for i in range(1, int(n ** 0.5) + 1):
        if n % i == 0:
            facs.update((i, n // i))
    return facs


def present_count_p1(house_number):
    return 10 * sum(factors(house_number))


def present_count_p2(house_number):
    pcount = 0
    for fac in factors(house_number):
        if house_number // fac <= 50:
            pcount += 11 * fac
    return pcount


def part1(pcount):
    # I _think_ this has to be brute-force search because the present count for
    # houses is not sorted by house number
    house_number = 1
    while present_count_p1(house_number) < pcount:
        house_number += 1
    return house_number


def part2(pcount):
    house_number = 1
    while present_count_p2(house_number) < pcount:
        house_number += 1
    return house_number


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    pcount = 29_000_000
    print("Part 1 answer =", part1(pcount))
    print("Part 2 answer =", part2(pcount))
    print()


if __name__ == '__main__':
    main()
