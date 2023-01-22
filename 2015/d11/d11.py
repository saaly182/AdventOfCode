#!/usr/bin/python3 -u

def string_incr(s):
    """Return incremented 8-char string, with wrapping."""
    if not s.islower() and len(s) != 8:
        raise ValueError(s)

    # brute force approach
    c = list(reversed(list(s)))
    i = 0
    while i < 8:
        c[i] = chr(ord(c[i]) + 1)
        if c[i] == '{':  # '{' is the ascii char after 'z'
            c[i] = 'a'
            i += 1
        else:
            break
    c.reverse()
    return ''.join(c)


def is_valid_pw(s):
    """
    1 Passwords must include one increasing straight of at least three letters,
      like abc, bcd, cde, and so on, up to xyz. They cannot skip letters; abd
      doesn't count.
    2 Passwords may not contain the letters i, o, or l, as these letters can be
      mistaken for other characters and are therefore confusing.
    3 Passwords must contain at least two different, non-overlapping pairs of
      letters, like aa, bb, or zz.
    """
    # rule 2
    for prohibited_char in 'iol':
        if prohibited_char in s:
            return False

    # rule 1
    found = False
    for i in range(len(s) - 2):
        c1, c2, c3 = (ord(c) for c in s[i:i + 3])
        if c1 + 1 == c2 and c2 + 1 == c3:
            found = True
            break
    if not found:
        return False

    # rule 3
    unique_pairs = set()
    for adjletters in zip(s, s[1:]):
        if adjletters[0] == adjletters[1]:
            unique_pairs.add(adjletters)
    if len(unique_pairs) < 2:
        return False

    # all rules passed, so this pw is valid
    return True


def find_next_pw(pw):
    while True:
        pw = string_incr(pw)
        if is_valid_pw(pw):
            break
    return pw


def part1(pw):
    return find_next_pw(pw)


def part2(pw):
    return find_next_pw(find_next_pw(pw))


def main():
    print("Part 1 answer =", part1('vzbxkghb'))
    print("Part 2 answer =", part2('vzbxkghb'))
    print()


if __name__ == '__main__':
    main()
