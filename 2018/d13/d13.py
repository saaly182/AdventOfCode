#!/usr/bin/python3 -u

class Cart:
    turnmap = {
        '^\\': '<',
        'v\\': '>',
        '<\\': '^',
        '>\\': 'v',
        '^/': '>',
        'v/': '<',
        '</': 'v',
        '>/': '^'
    }
    turnleft = {'^': '<', 'v': '>', '<': 'v', '>': '^'}
    turnright = {'^': '>', 'v': '<', '<': '^', '>': 'v'}

    def __init__(self, cid, direction, row, col):
        self.cid = cid
        self.direction = direction
        self.row = row
        self.col = col
        self.turn_count = 0
        self.crashed = False

    def __repr__(self):
        return (f'Cart({self.cid=} {self.direction=} {self.row=} {self.col=} '
                f'{self.turn_count=} {self.crashed=})')

    def _handle_intersection(self):
        turntype = self.turn_count % 3
        if turntype == 0:
            self.direction = Cart.turnleft[self.direction]
        elif turntype == 2:
            self.direction = Cart.turnright[self.direction]
        self.turn_count += 1

    def move(self, tracks: tuple, carts: list) -> None:
        """
        The convention for this move fnc is that we always set the direction for
        the _next_ move at the end of the current move. That is, during a single
        move, we move in the direction already established, and then we adjust
        the direction if necessary.
        """
        # move to new position
        match self.direction:
            case '^':
                self.row -= 1
            case 'v':
                self.row += 1
            case '<':
                self.col -= 1
            case '>':
                self.col += 1
            case _:
                raise ValueError(f'bad internal direction: {self.direction}')

        # adjust direction if necessary
        track = tracks[self.row][self.col]
        if track in '\\/':
            self.direction = Cart.turnmap[self.direction + track]
        elif track == '+':
            self._handle_intersection()

        # check for crash
        for cart in carts:
            if self.cid != cart.cid:
                if self.row == cart.row and self.col == cart.col:
                    self.crashed = True


def show(tracks: tuple, carts: list) -> None:
    tracks_carts = [list(x) for x in tracks]
    for cart in carts:
        tracks_carts[cart.row][cart.col] = cart.direction
    print()
    for tc in tracks_carts:
        print(''.join(tc))
    print()


def tick(tracks: tuple, carts: list) -> tuple[int, int] | None:
    carts.sort(key=lambda c: (c.row, c.col))
    for cart in carts:
        cart.move(tracks, carts)
        if cart.crashed:
            return cart.col, cart.row
    return None


def part1(tracks: tuple, carts: list) -> str:
    while True:
        crash_location = tick(tracks, carts)
        if crash_location:
            x, y = crash_location
            return f'{x},{y}'


def part2():
    return None


def slurp(fname: str) -> list[str]:
    with open(fname) as file:
        return [line.rstrip('\n') for line in file.readlines()]


def parse(inp: list) -> tuple[tuple, list]:
    tracks = []
    carts = []
    cid = 100
    for r, line in enumerate(inp):
        this_row = list(line)
        for c, val in enumerate(this_row):
            if val in '^v<>':
                carts.append(Cart(cid, val, r, c))
                cid += 1
                this_row[c] = '-' if val in '<>' else '|'
        tracks.append(tuple(this_row))

    return tuple(tracks), carts


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        tracks, carts = parse(inp)
        print("Part 1 answer =", part1(tracks, carts))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
