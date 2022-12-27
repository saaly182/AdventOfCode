#!/usr/bin/python3 -u

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


def part1(cubes):
  cg = make_graph(cubes)
  surf_area = 0
  for cube in cg:
    surf_area += (6 - len(cg[cube]))
    
  return surf_area


def part2():
  return None


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
    print("Part 2 answer =", part2())
    print()


if __name__ == '__main__':
  main()
