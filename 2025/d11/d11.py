#!/usr/bin/python3 -u

from typing import Iterator


def dfs(graph: dict, this_node: str, dst: str, path=None) -> Iterator[tuple]:
    if path is None:
        path = []

    path.append(this_node)

    if this_node == dst:
        yield tuple(path)
    else:
        for next_node in graph[this_node]:
            if next_node not in path:
                yield from dfs(graph, next_node, dst, path)
                if path:
                    path.pop()


def part1(g: dict) -> int:
    all_paths = tuple(dfs(g, 'you', 'out'))
    return len(all_paths)


def part2() -> int:
    return -99


def parse_input(fname: str) -> dict:
    graph = {}
    with open(fname) as file:
        for line in file:
            toks = line.rstrip().replace(':', '').split()
            graph[toks[0]] = tuple(toks[1:])
    return graph


def main():
    sample_input = parse_input('input/sample_input.txt')
    main_input = parse_input('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
