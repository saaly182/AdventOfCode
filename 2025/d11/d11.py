#!/usr/bin/python3 -u

from collections import defaultdict


def dfs_path_count(graph: defaultdict[str, tuple], this_node: str, dst: str,
                   path: list = None, cache: dict = None) -> int:
    if path is None:
        path = []

    if cache is None:
        cache = {}

    cache_key = (this_node, dst)

    if cache_key in cache:
        return cache[cache_key]

    path_count = 0
    path.append(this_node)

    if this_node == dst:
        path_count = 1
    else:
        for next_node in graph[this_node]:
            if next_node not in path:
                path_count += dfs_path_count(graph, next_node, dst, path, cache)
                if path:
                    path.pop()

    cache[cache_key] = path_count
    return path_count


def part1(g: defaultdict[str, tuple]) -> int:
    return dfs_path_count(g, 'you', 'out')


def part2(g: defaultdict[str, tuple]) -> int:
    # svr -> dac -> fft -> out
    x1 = dfs_path_count(g, "svr", "dac")
    x2 = dfs_path_count(g, "dac", "fft")
    x3 = dfs_path_count(g, "fft", "out")

    # svr -> fft -> dac -> out
    y1 = dfs_path_count(g, "svr", "fft")
    y2 = dfs_path_count(g, "fft", "dac")
    y3 = dfs_path_count(g, "dac", "out")

    z = (x1 * x2 * x3) + (y1 * y2 * y3)

    return z


def parse_input(fname: str) -> defaultdict[str, tuple]:
    graph = defaultdict(tuple)
    with open(fname) as file:
        for line in file:
            toks = line.rstrip().replace(':', '').split()
            graph[toks[0]] = tuple(toks[1:])
    return graph


def main():
    sample_input = parse_input('input/sample_input.txt')
    sample_input2 = parse_input('input/sample_input2.txt')
    main_input = parse_input('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))

    for inp in (sample_input2, main_input):
        print("Part 2 answer =", part2(inp))


if __name__ == '__main__':
    main()
