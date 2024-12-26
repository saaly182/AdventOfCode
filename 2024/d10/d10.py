#!/usr/bin/python3 -u

import sys
sys.path.append('../../lib')
import dirutils  # noqa


def hike(topomap: tuple, rthis: int, cthis: int, r9s: set) -> None:
    # DFS - do not have to track "visited" nodes, b/c we can only "climb"
    cur_height = topomap[rthis][cthis]
    if cur_height == 9:
        r9s.add((rthis, cthis))
        return

    for d in 'ESWN':  # east, south, west, north
        dr, dc = dirutils.dirvecs[d]
        rn = rthis + dr
        cn = cthis + dc
        if rn < 0 or cn < 0:
            continue
        try:
            neighbor_height = topomap[rn][cn]
        except IndexError:
            continue
        if neighbor_height == (cur_height + 1):
            hike(topomap, rn, cn, r9s)

    return


def score_trailhead(topomap: tuple, rt: int, ct: int) -> int:
    reachable_nines = set()
    hike(topomap, rt, ct, reachable_nines)
    return len(reachable_nines)


def part1(topomap: tuple) -> int:
    total_score = 0
    for r, row in enumerate(topomap):
        for c, square in enumerate(row):
            if square == 0:
                score = score_trailhead(topomap, r, c)
                total_score += score
    return total_score


def part2():
    return None


def create_topomap(lines: tuple) -> tuple:
    tmap = tuple(tuple([int(y) for y in x]) for x in lines)
    return tmap


def slurp(fname: str) -> tuple[str, ...]:
    with open(fname) as file:
        return tuple(line.rstrip() for line in file.readlines())


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        topomap = create_topomap(inp)
        print("Part 1 answer =", part1(topomap))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
