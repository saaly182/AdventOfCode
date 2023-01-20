#!/usr/bin/python3 -u

import hashlib


def part1(secret_key, leading_zeros):
    i = 0
    prefix_target = '0' * leading_zeros
    while True:
        m = hashlib.md5()
        msg = secret_key + str(i)
        m.update(msg.encode('UTF-8'))
        h = m.hexdigest()
        if h.startswith(prefix_target):
            break
        i += 1
    return i


def part2(secret_key):
    return part1(secret_key, 6)


def main():
    assert part1('abcdef', 5) == 609043
    assert part1('pqrstuv', 5) == 1048970
    print("Part 1 answer =", part1('bgvyzdsv', 5))
    print("Part 2 answer =", part2('bgvyzdsv'))
    print()


if __name__ == '__main__':
    main()
