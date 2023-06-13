#!/usr/bin/python3 -u


def manhattan(cell1: tuple[int, int], cell2: tuple[int, int]) -> int:
    """Return the manhattan distance between the two cells."""
    return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])


def closest_coord(r: int, c: int, coords: tuple) -> int:
    """
    By the rules of the problem, if there is more than one coord with the min
    distance, then ignore this case. This program indicates that by returning
    -1.
    """
    more_than_one_closest = -1
    distances = [manhattan((r, c), coord) for coord in coords]
    mindist = min(distances)
    if distances.count(mindist) != 1:
        return more_than_one_closest
    return distances.index(mindist)


def bounding_box(coords: tuple) -> tuple:
    row_vals = [x[0] for x in coords]
    col_vals = [x[1] for x in coords]
    return min(row_vals), max(row_vals), min(col_vals), max(col_vals)


def part1(coords: tuple) -> int:
    """
    The approach for part 1 is that all coordinates that "reach" the edge of the
    overall bounding box result in an infinite area, because at least the
    straight line from that edge point extends infinitely. So we just need to
    compute the closest coordinate for all the points in the bounding box
    and consider just the largest area that does not reach the edge.
    """
    grid = {}
    r1, r2, c1, c2 = bounding_box(coords)
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            grid[(r, c)] = closest_coord(r, c, coords)

    # determine which coords are *not* associated with the edge
    cids = set(range(len(coords)))
    for r in (r1, r2):
        for c in range(c1, c2 + 1):
            cids.discard(grid[(r, c)])
    for c in (c1, c2):
        for r in range(r1, r2 + 1):
            cids.discard(grid[(r, c)])

    # determine the largest area of the remaining cids
    gv = list(grid.values())
    return max([gv.count(x) for x in cids])


def part2(coords: tuple) -> int:
    """
    What is the size of the region containing all locations which have a
    total distance to all given coordinates of less than 10000?
    """
    limit = 10_000
    grid = {}
    r1, r2, c1, c2 = bounding_box(coords)
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            total_dist = sum([manhattan((r, c), coord) for coord in coords])
            if total_dist < limit:
                grid[(r, c)] = True
    return len(grid)


def slurp(fname: str) -> list[str]:
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp: list) -> tuple:
    coords = []
    for line in inp:
        x, y = line.split(',')
        r, c = int(y), int(x)
        coords.append((r, c))
    return tuple(coords)


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        coords = parse(inp)
        print("Part 1 answer =", part1(coords))
        print("Part 2 answer =", part2(coords))
        print()


if __name__ == '__main__':
    main()
