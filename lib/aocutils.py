#!/usr/bin/python3
"""
Various utility functions for AoC
"""

import collections
import copy
import heapq


def drange(a, b):
    """
    Return a range between a and b inclusive regardless
    of which is larger.
    """
    if a <= b:
        dr = range(a, b + 1)
    else:
        dr = range(a, b - 1, -1)
    return dr


def merge_intervals(input_intervals):
    """
    Return a list of the merged set of the input intervals.

    Input: an iterable of [a, b] intervals, where a & b are ints and a <= b
    Based on https://www.geeksforgeeks.org/merging-intervals/
    """
    intervals = list(copy.deepcopy(input_intervals))  # don't change the input
    for i in intervals:
        assert len(i) == 2 and (i[0] <= i[1])
    intervals.sort()
    stack = [list(intervals[0])]
    for i in intervals[1:]:
        if stack[-1][0] <= i[0] <= stack[-1][1]:
            stack[-1][1] = max(stack[-1][1], i[1])
        else:
            stack.append(list(i))
    return stack


def shortest_paths(g, src):
    """
    Return distance and path info from src to all other vertices in the graph.

    Uses the "lazy" Dijkstra algorithm, which basically means the
    min-priority-queue does not have a decrease-key method. This is not space
    efficient, but AoC problems don't tend to have *huge* graphs.

    G structure: dict with vertex key and value of adjacency list with
    (vertex, edge length) elements.

    reference: https://nilmamano.com/blog/implementing-dijkstra
    """
    dist = collections.defaultdict(lambda: float('inf'))
    seen = collections.defaultdict(bool)
    prev = {}
    minq = []
    dist[src] = 0
    heapq.heappush(minq, (0, src))

    while minq:
        _, u = heapq.heappop(minq)
        if seen[u]:
            continue  # already seen this vertex
        seen[u] = True

        for v, e in g[u]:
            alt = dist[u] + e
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                if v in g:
                    heapq.heappush(minq, (alt, v))

    return dist, prev


def topo_sort(g: dict) -> list:
    """
    Return a topological sorted list of vertices in the graph.
    Raises ValueError if the input is not a well-formed DAG.

    G structure: dict with vertex key and value of adjacency list with
    (vertex, edge length) elements.

    reference:
    https://en.wikipedia.org/wiki/Topological_sorting#Kahn%27s_algorithm
    """
    tsort = []
    indegree = collections.defaultdict(int)

    # compute indegree
    for u in g:
        if u not in indegree:
            indegree[u] = 0
        for v, e in g[u]:
            indegree[v] += 1

    no_incoming = {u for u in indegree if indegree[u] == 0}
    while no_incoming:
        u = no_incoming.pop()
        tsort.append(u)
        if u in g:
            for v, e in g[u]:
                indegree[v] -= 1
                if indegree[v] == 0:
                    no_incoming.add(v)

    if any(indegree[u] != 0 for u in g):
        raise ValueError('Input is not a well-formed DAG')

    return tsort


def rotate_2darray(grid: list, direction='cw') -> tuple:
    """Return a tuple copy of the input 2d array, rotated 90 degrees."""
    if direction == 'cw':
        return tuple(zip(*reversed(grid)))
    elif direction == 'ccw':
        return tuple(zip(*[reversed(row) for row in grid]))
    else:
        raise ValueError('Direction must be cw or ccw')
