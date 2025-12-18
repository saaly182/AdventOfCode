#!/usr/bin/python3 -u

import collections


class Machine:
    def __init__(self, spec: dict) -> None:
        self.spec = spec
        self.light_diagram = spec['light_diagram']
        self.buttons = spec['buttons']
        self.jolts = spec['jolts']
        self.lights = [False] * len(self.light_diagram)

    def is_startable(self) -> bool:
        return self.light_diagram == tuple(self.lights)

    def push_button(self, button: tuple[int, ...]) -> None:
        # Note that pushing a sequence of buttons and then pushing that sequence
        # in reverse returns the lights to the same state.
        if button not in self.buttons:
            raise ValueError(f'Invalid button: {button}')
        for pos in button:
            self.lights[pos] = not self.lights[pos]


def min_start_pushes(m: Machine) -> int:
    q = collections.deque()
    starting_lights = tuple([False] * len(m.light_diagram))
    parent = {}
    final_step = None

    for b in m.buttons:
        k = (b, starting_lights)
        parent[k] = None
        q.append(k)

    def bfs():
        nonlocal final_step
        while q:
            button1, lights1 = q.popleft()
            lights_next = list(lights1)
            for pos in button1:
                lights_next[pos] = not lights_next[pos]
            lights2 = tuple(lights_next)

            if lights2 == m.light_diagram:
                final_step = (button1, lights1)
                return
            for b in m.buttons:
                k = (b, lights2)
                if k not in parent:
                    parent[k] = (button1, lights1)
                    q.append(k)

    bfs()

    # now reconstruct the button sequence
    bseq = []
    step = final_step
    while True:
        if step is None:
            break
        bu, li = step
        bseq.append(bu)
        step = parent[step]
    bseq.reverse()

    return len(bseq)


def part1(machines) -> int:
    pushcount = 0
    for m in machines:
        pushcount += min_start_pushes(m)
    return pushcount


def part2() -> int:
    return -99


def parse_input(fname: str) -> tuple[Machine, ...]:
    mlist = []
    with open(fname) as file:
        for line in file:
            light_diagram = None
            buttons = []
            jolts = None

            line = line.strip()
            # sample line: [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
            for tok in line.split():
                if tok.startswith('[') and tok.endswith(']'):
                    light_diagram = tuple([x == '#' for x in tok[1:-1]])
                elif tok.startswith('(') and tok.endswith(')'):
                    buttons.append(
                        tuple([int(x) for x in tok[1:-1].split(',')]))
                elif tok.startswith('{') and tok.endswith('}'):
                    jolts = tuple([int(x) for x in tok[1:-1].split(',')])
                else:
                    raise ValueError(f'Invalid input: {line}')
            spec = {'light_diagram': light_diagram,
                    'buttons': frozenset(buttons),
                    'jolts': jolts}
            mlist.append(Machine(spec))
    return tuple(mlist)


def main():
    sample_input = parse_input('input/sample_input.txt')
    main_input = parse_input('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
