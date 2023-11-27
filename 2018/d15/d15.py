#!/usr/bin/python3 -u

import collections
import sys
sys.path.append('../../lib')
import dirutils  # noqa: E402


class Unit:
    UNIT_TYPES = ('E', 'G')
    unit_id_source = 100
    
    def __init__(self, unit_type: str, row: int, col: int):
        if unit_type not in Unit.UNIT_TYPES:
            raise ValueError(f'bad unit type: {unit_type}')
        self.unit_type = unit_type
        self.hp = 200
        self.attack_power = 3
        self.r = row
        self.c = col

        self.unit_id = Unit.unit_id_source
        Unit.unit_id_source += 1

    def show(self) -> None:
        details = (f'id={self.unit_id} type={self.unit_type} hp={self.hp} '
                   f'attack_power={self.attack_power} '
                   f'location=({self.r}, {self.c})')
        print(details)

    def is_alive(self) -> bool:
        return self.hp > 0

    def is_dead(self) -> bool:
        return not self.is_alive()

    def is_elf(self) -> bool:
        return self.unit_type == 'E'

    def is_goblin(self) -> bool:
        return self.unit_type == 'G'

    def __str__(self) -> str:
        return self.unit_type


class Grid:
    def __init__(self, lines: list):
        self.combat_active = True
        self.grid = []
        r = 0
        for line in lines:
            row = []
            c = 0
            for char in line:
                if char in Unit.UNIT_TYPES:
                    unit = Unit(char, r, c)
                    row.append(unit)
                else:
                    row.append(char)
                c += 1
            self.grid.append(row)
            r += 1

    def __str__(self) -> str:
        row_strings = []
        for row in self.grid:
            row_strings.append(''.join([str(i) for i in row]))
        return '\n'.join(row_strings)

    def set(self, row: int, col: int, val: str | Unit) -> None:
        self.grid[row][col] = val

    def get(self, row: int, col: int):
        return self.grid[row][col]

    def units_in_reading_order(self) -> tuple:
        """Return tuple of alive units in grid, in reading order."""
        unitlist = []
        for row in self.grid:
            for item in row:
                if isinstance(item, Unit):
                    assert item.is_alive()
                    unitlist.append(item)
        return tuple(unitlist)

    def total_hp(self):
        thp = 0
        for row in self.grid:
            for item in row:
                if isinstance(item, Unit):
                    assert item.is_alive()
                    thp += item.hp
        return thp


def attack(unit: Unit, grid: Grid) -> bool:
    """Attack the appropriate in-range target, if it exists.
    Return True if the attack happened.
    """
    min_hp = float('inf')
    target = None
    # Important that we process the possible targets in reading-order (NWES),
    # which neighbor_coords() does.
    for r, c in neighbor_coords(unit):
        item = grid.get(r, c)
        if isinstance(item, Unit) and item.unit_type != unit.unit_type:
            if item.hp < min_hp:
                target = item
                min_hp = target.hp

    if target:
        target.hp -= unit.attack_power
        if target.is_dead():
            grid.set(target.r, target.c, '.')
        return True

    return False


def neighbor_coords(unit: Unit):
    n = []
    for d in 'NWES':
        r = unit.r + dirutils.dirvecs[d][0]
        c = unit.c + dirutils.dirvecs[d][1]
        n.append((r, c))
    return tuple(n)


def move(unit: Unit, grid: Grid, targets: tuple) -> None:
    """
    We need to do a specialized BFS that keeps track of the best first step,
    because in the end we're just going to take that first step.
    """
    dest_cells = set()  # open cells adjacent to enemy targets
    for t in targets:
        for r, c in neighbor_coords(t):
            item = grid.get(r, c)
            if item == '.':
                dest_cells.add((r, c))

    bfsq = collections.deque()
    for r, c in neighbor_coords(unit):
        item = grid.get(r, c)
        if item == '.':
            origin = (r, c)
            bfsq.append((origin, 1, origin))

    reached = {}
    seen = {}
    while bfsq:
        cell, steps, origin = bfsq.popleft()
        seen[(cell, origin)] = 1
        if cell in dest_cells:
            if cell not in reached:
                reached[cell] = (steps, origin)
            else:
                steps_r, origin_r = reached[cell]
                if steps < steps_r or (steps == steps_r and origin < origin_r):
                    reached[cell] = (steps, origin)
        else:
            for d in 'NWES':
                r = cell[0] + dirutils.dirvecs[d][0]
                c = cell[1] + dirutils.dirvecs[d][1]
                item = grid.get(r, c)
                if item == '.' and ((r, c), origin) not in seen:
                    bfsq.append(((r, c), steps + 1, origin))

    # Now "reached" contains values that are step counts and the "origin" (or
    # first cell on that path) according to reading-order. So the unit should
    # move to the reached value that has the min steps, and for ties, the min
    # origin.
    if not reached:
        return

    move_to_cell = min(reached.values())[1]
    mr = move_to_cell[0]
    mc = move_to_cell[1]
    grid.set(unit.r, unit.c, '.')
    grid.set(mr, mc, unit)
    unit.r = mr
    unit.c = mc


def take_turn(unit: Unit, grid: Grid) -> None:
    targets = tuple(u for u in grid.units_in_reading_order() if
                    u.unit_type != unit.unit_type)

    # if no targets are left, then combat ends
    if not targets:
        grid.combat_active = False
        return

    # if unit can successfully attack already, do that then end turn
    if attack(unit, grid):
        return

    # move, then try an attack
    move(unit, grid, targets)
    attack(unit, grid)


def combat_round(grid: Grid) -> None:
    for unit in grid.units_in_reading_order():
        if unit.is_alive():  # it could have died in earlier turns
            take_turn(unit, grid)
            if not grid.combat_active:
                break


def battle(grid: Grid) -> int:
    """Return the outcome of the battle given the initial grid."""
    print(grid)
    fulls_rounds = 0
    while True:
        combat_round(grid)
        print()
        print(grid)
        if grid.combat_active:
            fulls_rounds += 1
        else:
            break
    outcome = fulls_rounds * grid.total_hp()
    return outcome


def part1(grid: Grid) -> int:
    return battle(grid)


def part2():
    return None


def slurp(fname: str) -> list[str]:
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    sample_input = slurp('input/sample_input_3.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, ):
        grid = Grid(inp)
        print("Part 1 answer =", part1(grid))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
