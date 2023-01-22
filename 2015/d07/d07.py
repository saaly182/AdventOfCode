#!/usr/bin/python3 -u

def evaluate(item, connection):
    # seems I didn't need to account for input being 16-bit
    if isinstance(item, int):
        return item

    c = connection
    match c[item]:
        case tok if not isinstance(tok, tuple):
            if isinstance(tok, int):
                return tok
            else:
                n = evaluate(tok, c)
                c[item] = n
                return c[item]
        case ('NOT', var1):
            n = ~ evaluate(var1, c)
            c[item] = n
            return c[item]
        case ('LSHIFT', var1, num):
            n = evaluate(var1, c) << num
            c[item] = n
            return c[item]
        case ('RSHIFT', var1, num):
            n = evaluate(var1, c) >> num
            c[item] = n
            return c[item]
        case ('AND', tok, var2):
            n1 = evaluate(tok, c)
            n2 = evaluate(var2, c)
            c[item] = n1 & n2
            return c[item]
        case('OR', tok, var2):
            n1 = evaluate(tok, c)
            n2 = evaluate(var2, c)
            c[item] = n1 | n2
            return c[item]
        case _:
            raise ValueError(c[item])


def part1(connection):
    return evaluate('a', connection)


def part2():
    return None


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp):
    connection = {}
    for conn in inp:
        match conn.split():
            case [tok, '->', var1]:
                if tok.isnumeric():
                    tok = int(tok)
                connection[var1] = tok
            case ['NOT', var1, '->', var2]:
                connection[var2] = ('NOT', var1)
            case [tok, ('AND' | 'OR') as op, var1, '->', var2]:
                if tok.isnumeric():
                    tok = int(tok)
                connection[var2] = (op, tok, var1)
            case [var1, ('LSHIFT' | 'RSHIFT') as op, num, '->', var2] \
                    if num.isnumeric():
                connection[var2] = (op, var1, int(num))
            case _:
                raise ValueError(conn)
    return connection


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(parse(inp)))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
