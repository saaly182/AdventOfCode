#!/usr/bin/python3 -u

import sys
sys.path.append('../../lib')
import dirutils  # noqa


def hike(topomap: tuple, rthis: int, cthis: int,
         r9s: set, rating: list) -> None:
    # DFS - do not have to track "visited" nodes, b/c we can only "climb"
    cur_height = topomap[rthis][cthis]
    if cur_height == 9:
        summit = (rthis, cthis)
        r9s.add(summit)
        # every time we reach a 9 it was a unique path to get here
        rating[0] += 1
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
            hike(topomap, rn, cn, r9s, rating)

    return


def eval_trailhead(topomap: tuple, rt: int, ct: int) -> tuple[int, int]:
    """Return score and rating of trailhead."""
    reachable_nines = set()
    rating = [0]
    hike(topomap, rt, ct, reachable_nines, rating)
    return len(reachable_nines), rating[0]


def part1(topomap: tuple) -> tuple[int, int]:
    total_score = 0
    total_rating = 0
    for r, row in enumerate(topomap):
        for c, square in enumerate(row):
            if square == 0:
                score, rating = eval_trailhead(topomap, r, c)
                total_score += score
                total_rating += rating
    return total_score, total_rating


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
        ts, tr = part1(topomap)
        print(f"Part 1 answer = {ts}")
        print(f"Part 2 answer = {tr}")
        print()


if __name__ == '__main__':
    main()
