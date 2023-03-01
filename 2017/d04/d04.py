#!/usr/bin/python3 -u

def is_valid(passphrase, allow_anagrams=True):
    if len(passphrase) != len(set(passphrase)):
        return False
    if not allow_anagrams:
        elems = set([tuple(sorted(p)) for p in passphrase])
        if len(passphrase) != len(elems):
            return False
    return True


def part1(passphrases):
    return sum([1 for p in passphrases if is_valid(p)])


def part2(passphrases):
    return sum([1 for p in passphrases if is_valid(p, allow_anagrams=False)])


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp):
    passphrases = []
    for line in inp:
        passphrases.append(tuple(line.split()))
    return tuple(passphrases)


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        passphrases = parse(inp)
        print("Part 1 answer =", part1(passphrases))
        print("Part 2 answer =", part2(passphrases))
        print()


if __name__ == '__main__':
    main()
