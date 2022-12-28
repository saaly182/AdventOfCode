#!/usr/bin/python3 -u

from collections import defaultdict
import itertools


def make_graph(cubes):
  'Return an adjacency graph of the input cubes.'
  # neighbor offsets
  offsets = (
  #  dx, dy, dz
    ( 0,  0,  1),  # front facing
    ( 1,  0,  0),  # right facing
    ( 0,  0, -1),  # back facing
    (-1,  0,  0),  # left facing
    ( 0,  1,  0),  # top facing
    ( 0, -1,  0),  # bottom facing
  )

  cset = set(cubes)
  cube_graph = {}
  for cube in cubes:
    cube_graph[cube] = set()
    x1, y1, z1 = cube
    for face in range(6):
      neighbor = (x1 + offsets[face][0],
                  y1 + offsets[face][1],
                  z1 + offsets[face][2])
      if neighbor in cset:
        cube_graph[cube].add(neighbor)

  return cube_graph


def surface_area(cube_graph):
  surf_area = 0
  for cube in cube_graph:
    surf_area += (6 - len(cube_graph[cube]))
  return surf_area


def cminmax(cubes):
  'Return min/max pairs of the input cubes.'
  # return format: (xmin, xmax, ymin, ymax, zmin, zmax)
  ret = []
  for i in range(3):
    ret.append(min(a[i] for a in cubes))
    ret.append(max(a[i] for a in cubes))
  return tuple(ret)


def make_enclosing_graph(cubes):
  'Return a graph that encloses the lava drop, including internal cavities.'
  x1, x2, y1, y2, z1, z2 = cminmax(cubes)
  cset = set(cubes)
  eset = set()
  for cube in itertools.product(range(x1 - 1, x2 + 2), range(y1 - 1, y2 + 2), range(z1 - 1, z2 + 2)):
    if cube not in cset:
      eset.add(cube)
  return make_graph(eset)


def get_cavities(g):
  'Return internal disconnected subgraphs of g.'
  # Specialized for this particular problem, because we assume g is an
  # enclosing graph with zero or more internal cavities.

  # flood fill each separate subgraph using BFS
  uncolored_cubes = set(g)
  subgraphs = defaultdict(list)
  visited = set()
  color = 100
  while uncolored_cubes:
    c = next(iter(uncolored_cubes))
    q = [c]
    # BFS
    while q:
      c = q.pop(0)
      visited.add(c)
      uncolored_cubes.remove(c)
      subgraphs[color].append(c)
      unvisited_neighbors = [n for n in g[c] if n not in visited]
      for n in unvisited_neighbors:
        visited.add(n)
        q.append(n)
    color += 1

  # identify and delete the outer graph
  mm = cminmax(g)
  xmin = mm[0]
  for cube in g:
    if cube[0] == xmin:
      outer_cube = cube
      break
  for color in subgraphs:
    if outer_cube in subgraphs[color]:
      del subgraphs[color]
      break

  # make the cavity graphs
  cavities = []
  for color in subgraphs:
    cavities.append(make_graph(subgraphs[color]))

  return cavities


def part1(cubes):
  cg = make_graph(cubes)
  return surface_area(cg)


def part2(cubes):
  cg = make_graph(cubes)
  eg = make_enclosing_graph(cubes)
  surf_area = surface_area(cg)
  # now subtract away s.a. of internal cavities
  for cavity in get_cavities(eg):
    surf_area -= surface_area(cavity)
  return surf_area


def slurp(fname):
  with open(fname) as file:
    return [line.rstrip() for line in file.readlines()]


def main():
  sample_input = slurp('sample_input.txt')
  main_input = slurp('input.txt')

  for inp in (sample_input, main_input):
    cubes = []
    for line in inp:
      x, y , z = line.split(',')
      cubes.append((int(x), int(y), int(z)))
    cubes = tuple(cubes)

    print("Part 1 answer =", part1(cubes))
    print("Part 2 answer =", part2(cubes))
    print()


if __name__ == '__main__':
  main()
