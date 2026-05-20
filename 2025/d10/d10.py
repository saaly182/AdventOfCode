#!/usr/bin/python3 -u

# TODO: The current Part 2 BFS solution in this version blows up.
# The internet says to switch to a linear algebra approach.

import collections
import dataclasses


@dataclasses.dataclass
class Machine:
    light_diagram: tuple
    buttons: frozenset
    jolts: tuple


def min_start_pushes_lights(m: Machine) -> int:
    def bfs():  # inner function
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
            for b2 in m.buttons:
                k2 = (b2, lights2)
                if k2 not in parent:
                    parent[k2] = (button1, lights1)
                    q.append(k2)

    q = collections.deque()
    starting_lights = tuple([False] * len(m.light_diagram))
    parent = {}
    final_step = None

    for b1 in m.buttons:
        k1 = (b1, starting_lights)
        parent[k1] = None
        q.append(k1)

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


def min_start_pushes_jolts(m: Machine) -> int:
    def bfs():  # inner function
        nonlocal final_step
        while q:
            button1, jolts1 = q.popleft()
            jolts_next = list(jolts1)
            for pos in button1:
                jolts_next[pos] += 1
            jolts2 = tuple(jolts_next)

            if jolts2 == m.jolts:
                final_step = (button1, jolts1)
                return

            # stop exploring this path if any jolt is now too large
            jolts_ok = True
            for i in range(len(m.jolts)):
                if jolts2[i] > m.jolts[i]:
                    jolts_ok = False
                    break
            if not jolts_ok:
                continue

            for b2 in m.buttons:
                k2 = (b2, jolts2)
                if k2 not in parent:
                    parent[k2] = (button1, jolts1)
                    q.append(k2)

    q = collections.deque()
    starting_jolts = tuple([0] * len(m.jolts))
    parent = {}
    final_step = None

    for b1 in m.buttons:
        k1 = (b1, starting_jolts)
        parent[k1] = None
        q.append(k1)

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
        pushcount += min_start_pushes_lights(m)
    return pushcount


def part2(machines) -> int:
    pushcount = 0
    for m in machines:
        pushcount += min_start_pushes_jolts(m)
    return pushcount


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
            mlist.append(Machine(light_diagram=light_diagram,
                                 buttons=frozenset(buttons),
                                 jolts=jolts))
    return tuple(mlist)


def main():
    sample_input = parse_input('input/sample_input.txt')
    main_input = parse_input('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
