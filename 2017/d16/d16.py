#!/usr/bin/python3 -u

ALPHA16 = 'abcdefghijklmnop'


def dance(progs: list[str], dance_moves: tuple[tuple]) -> list[str]:
    plen = len(progs)
    for dm in dance_moves:
        match dm[0]:
            case 's':
                spin = dm[1]
                progs = progs[-spin:] + progs[:plen - spin]
            case 'x':
                i1, i2 = dm[1], dm[2]
                progs[i1], progs[i2] = progs[i2], progs[i1]
            case 'p':
                n1, n2 = dm[1], dm[2]
                i1 = progs.index(n1)
                i2 = progs.index(n2)
                progs[i1], progs[i2] = progs[i2], progs[i1]
            case _:
                assert ValueError(f'bad move: {dm}')

    return progs


def part1(dance_moves: tuple[tuple]) -> str:
    progs = list(ALPHA16)
    return ''.join(dance(progs, dance_moves))


def part2(dance_moves: tuple[tuple]) -> str:
    progs = list(ALPHA16)

    # This is only gonna work if there's a cycle. Let's see if we can find a
    # cycle that returns to the original list. If there's not a cycle this code
    # will just do a billion loops (and take forever).
    cycle_count = -1
    needed_loops = 1_000_000_000
    for i in range(needed_loops):
        progs = dance(progs, dance_moves)
        if ''.join(progs) == ALPHA16:
            cycle_count = i + 1
            print(f'FOUND CYCLE: {cycle_count=}')
            break
    if cycle_count == -1:
        print('Never found a cycle, and you probably did not let this run.')
        return ''.join(progs)
    # Now just run the number of loops to get to the right part of the cycle
    progs = list(ALPHA16)
    for i in range(needed_loops % cycle_count):
        progs = dance(progs, dance_moves)

    return ''.join(progs)


def slurp(fname: str) -> list[str]:
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp: str) -> tuple:
    dance_moves = []
    for move in inp.split(','):
        match move[0]:
            case 's':
                dance_moves.append(('s', int(move[1:])))
            case 'x':
                i1, i2 = [int(x) for x in move[1:].split('/')]
                dance_moves.append(('x', i1, i2))
            case 'p':
                n1, n2 = move[1:].split('/')
                dance_moves.append(('p', n1, n2))
            case _:
                raise ValueError(f'bad move: {move}')

    return tuple(dance_moves)


def main():
    main_input = slurp('input/input.txt')

    for inp in (main_input,):
        dance_moves = parse(inp[0])
        print("Part 1 answer =", part1(dance_moves))
        print("Part 2 answer =", part2(dance_moves))
        print()


if __name__ == '__main__':
    main()
