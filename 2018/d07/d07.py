#!/usr/bin/python3 -u

from collections import defaultdict
import copy
import re


def part1(presteps: dict, poststeps: dict) -> str:
    # don't alter inputs
    pr = copy.deepcopy(presteps)
    po = copy.deepcopy(poststeps)

    order = []
    nodes = set(list(pr.keys()) + list(po.keys()))

    while unblocked := [n for n in nodes if n not in pr.keys()]:
        # unblocked nodes are not in the presteps dict
        step = sorted(unblocked)[0]  # rules of the puzzle, alphabetically
        order.append(step)
        nodes.remove(step)
        for n in po[step]:
            pr[n].remove(step)
            if not pr[n]:
                del pr[n]

    return ''.join(order)


def part2(presteps: dict, poststeps: dict, num_workers=5, fixed_time=60) -> int:
    pr = copy.deepcopy(presteps)
    po = copy.deepcopy(poststeps)
    nodes = set(list(pr.keys()) + list(po.keys()))
    nodetimer = defaultdict(int)
    workslots = set()

    t = 0  # seconds
    while nodes:
        if openslots := num_workers - len(workslots):
            unblocked = sorted(nodes - set(pr.keys()) - workslots)
            start_nodes = unblocked[:openslots]
            workslots.update(start_nodes)
            for sn in start_nodes:
                nodetimer[sn] = fixed_time + ord(sn) - ord('A') + 1

        for node in list(nodetimer.keys()):
            nodetimer[node] -= 1
            if nodetimer[node] == 0:
                del nodetimer[node]
                nodes.remove(node)
                workslots.remove(node)
                for n in po[node]:
                    pr[n].remove(node)
                    if not pr[n]:
                        del pr[n]

        t += 1

    return t


def slurp(fname: str) -> list[str]:
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp: list) -> tuple[dict, dict]:
    presteps = defaultdict(set)
    poststeps = defaultdict(set)
    regex = r'Step ([A-Z]) must be finished before step ([A-Z]) can begin\.'
    for line in inp:
        if mo := re.fullmatch(regex, line):
            node1 = mo.group(1)
            node2 = mo.group(2)
            presteps[node2].add(node1)
            poststeps[node1].add(node2)
        else:
            raise ValueError(f'bad input: {line}')
    return presteps, poststeps


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        presteps, poststeps = parse(inp)
        print("Part 1 answer =", part1(presteps, poststeps))
        print("Part 2 answer =", part2(presteps, poststeps))
        print()


if __name__ == '__main__':
    main()
