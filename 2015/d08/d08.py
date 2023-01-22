#!/usr/bin/python3 -u

def charcount(s):
    x = list(s)

    # first get rid of the enclosing double quotes
    x.pop()
    x.pop(0)

    # now un-escape backslashes until no more escapes exist
    try:
        while True:
            bi0 = x.index('\\')
            bi1 = bi0 + 1
            if x[bi1] == '\\':
                del x[bi1]
                x[bi0] = '\\\\'
            elif x[bi1] == '"':
                del x[bi0]
            elif x[bi1] == 'x':
                # just replace \xhh with "X" since we only care about final len
                x[bi0] = 'X'
                del x[bi1:bi1 + 3]
    except ValueError:
        pass
    return len(x)


def part1(inp):
    literals_len = 0
    memory_len = 0

    for line in inp:
        assert line[0] == '"' and line[-1] == '"'
        literals_len += len(line)
        memory_len += charcount(line)
    return literals_len - memory_len


def part2():
    return None


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
