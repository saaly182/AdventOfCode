#!/usr/bin/python3 -u

import collections
import itertools
import sys
sys.path.append('../../lib')
import dirutils  # noqa: E402 F40


def part1(cells: tuple) -> int:
    max_area = 0
    for a, b in itertools.combinations(cells, 2):
        area = (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)
        if area > max_area:
            max_area = area
    return max_area


def drange(a: int, b: int, inclusive=True) -> range:
    """Return a range between a and b."""
    if inclusive:
        if a == b:
            dr = range(0)
        elif a < b:
            dr = range(a, b + 1)
        else:
            dr = range(b, a + 1)
    else:
        if abs(a - b) < 2:
            dr = range(0)
        elif a < b:
            dr = range(a + 1, b)
        else:
            dr = range(b + 1, a)
    return dr


def compressed_grid(cells: tuple) -> list:
    """
    Given a set of (x, y) cells, return a list of
    [cgrid, c2r_map, r2c_map].
    cgrid: 2d compressed array of cells.
    c2r_map: a dict mapping the compressed cells to their real cells.
    r2c_map: a dict mapping the real cells to their compressed cells.
    Notes:
    * For easy flood-filling, the edge rows & cols of compressd_grid are
    empty exterior cells
    * Using the "+1" approach to 2d compression
    * '#' = red, 'X' = green, '.' = exterior, '*' = unassigned
    """

    cgrid = []
    c2r_map = {}
    r2c_map = {}
    xs_input = set()
    ys_input = set()
    xs = set()
    ys = set()

    for x, y in cells:
        assert x > 0 and y > 0
        xs_input.add(x)
        ys_input.add(y)
        xs.update((x, x + 1))
        ys.update((y, y + 1))

    xvals = [0] + sorted(xs)
    yvals = [0] + sorted(ys)
    rowsize = len(xvals) + 1
    for i in range(len(yvals) + 1):
        cgrid.append(['*'] * rowsize)

    # Place the red cells in cgrid
    for x, y in cells:
        xc = xvals.index(x)
        yc = yvals.index(y)
        c2r_map[(xc, yc)] = (x, y)
        r2c_map[(x, y)] = (xc, yc)
        cgrid[yc][xc] = '#'

    # Place green lines in cgrid between sequential red cells
    wrapped_cells = list(cells) + [cells[0]]
    for i in range(len(wrapped_cells) - 1):
        xc1, yc1 = r2c_map[wrapped_cells[i]]
        xc2, yc2 = r2c_map[wrapped_cells[i + 1]]
        assert xc1 == xc2 or yc1 == yc2
        if xc1 == xc2:
            for j in drange(yc1, yc2, inclusive=False):
                cgrid[j][xc1] = 'X'
        elif yc1 == yc2:
            for j in drange(xc1, xc2, inclusive=False):
                cgrid[yc1][j] = 'X'

    # Flood-fill the exterior cells. Remember that we explicitly put an empty
    # border around all the points, so (0, 0) is guaranteed to be an exterior
    # cell that can reach all the way around the polygon.
    q = collections.deque()
    visited = set()
    q.append((0, 0))
    visited.add((0, 0))
    while q:
        xc, yc = q.popleft()
        cgrid[yc][xc] = '.'
        for dx, dy in dirutils.unitvecs:
            neighbor_x = xc + dx
            neighbor_y = yc + dy
            if 0 <= neighbor_x <= len(xvals) and 0 <= neighbor_y <= len(yvals):
                if cgrid[neighbor_y][neighbor_x] == '*':
                    if (neighbor_x, neighbor_y) not in visited:
                        q.append((neighbor_x, neighbor_y))
                        visited.add((neighbor_x, neighbor_y))

    # Place interior green cells. Any '*' left is interior green.
    for row in cgrid:
        for n, c in enumerate(row):
            if c == '*':
                row[n] = 'X'

    return [cgrid, c2r_map, r2c_map]


def rect_area(x1: int, y1: int, x2: int, y2: int) -> int:
    return (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)


def part2(cells: tuple) -> int:
    """
    This part could be quite complicated if the red points and green lines
    between them were in adjacent cells. For example, that could result in
    interior pockets of "dot" cells. My particular input data does not have that
    characteristic, and reddit comments indicate that the AoC designer avoided
    this with everyone's input. So my code here does not try to deal with that
    general, complicated case. Instead, it assumes (and verifies) that the input
    does not have "touching" lines, making the algorithm simpler.
    """
    cgrid, c2r_map, r2c_map = compressed_grid(cells)

    max_area = 0

    for c1, c2 in itertools.combinations(c2r_map, 2):
        xc1, yc1 = c1
        xc2, yc2 = c2
        x1, y1 = c2r_map[c1]
        x2, y2 = c2r_map[c2]
        area = rect_area(x1, y1, x2, y2)
        if area <= max_area:
            continue

        # check that all enclosed cells are red or green
        valid_rect = True
        for yc in drange(yc1, yc2):
            for xc in drange(xc1, xc2):
                if cgrid[yc][xc] == '.':
                    valid_rect = False
                    break

        if valid_rect:
            max_area = area

    return max_area


def parse_input(fname: str) -> tuple[tuple]:
    cells = []
    with open(fname) as file:
        for line in file:
            a, b = line.split(',')
            cells.append((int(a), int(b)))
    return tuple(cells)


def main():
    sample_input = parse_input('input/sample_input.txt')
    main_input = parse_input('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
