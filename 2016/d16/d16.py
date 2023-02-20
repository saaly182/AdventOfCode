#!/usr/bin/python3 -u

def filldisk(disklen, init_data):
    data = list(init_data)

    while len(data) < disklen:
        b = list(reversed(data))
        for i, c in enumerate(b):
            b[i] = '0' if c == '1' else '1'
        data.append('0')
        data.extend(b)

    return ''.join(data[:disklen])


def checksum(s):
    csum = list(s)
    while len(csum) % 2 == 0:
        next_csum = []
        for a, b in zip(csum[::2], csum[1::2]):
            bit = '1' if a == b else '0'
            next_csum.append(bit)
        csum = next_csum
    return ''.join(csum)


def part1(disklen, init_data):
    return checksum(filldisk(disklen, init_data))


def part2(disklen, init_data):
    # part 2 changes the disklen
    disklen = 35_651_584
    return checksum(filldisk(disklen, init_data))


def main():
    sample_input = (20, '10000')
    main_input = (272, '10011111011011001')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(*inp))
        print("Part 2 answer =", part2(*inp))
        print()


if __name__ == '__main__':
    main()
