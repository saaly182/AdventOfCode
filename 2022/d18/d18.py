#!/usr/bin/python3 -u

def part1(cubes):
  # cd is the cubes dict. The key is the cube coords, and the value is a list
  # of the six cube faces where True means the face is exposed and False means
  # the face is covered.
  #
  # face 0: front facing
  # face 1: right facing
  # face 2: back facing
  # face 3: left facing
  # face 4: top facing
  # face 5: bottom facing
  cd = {}
  for cube in cubes:
    cd[cube] = [True] * 6

  # offsets for neighbor checking
  offsets = (
    ( 0,  0,  1),  # front facing
    ( 1,  0,  0),  # right facing
    ( 0,  0, -1),  # back facing
    (-1,  0,  0),  # left facing
    ( 0,  1,  0),  # top facing
    ( 0, -1,  0),  # bottom facing
  )

  for cube in cd:
    x1, y1, z1 = cube
    exposed = cd[cube]

    for f in range(6):
      neighbor = (x1 + offsets[f][0],
                  y1 + offsets[f][1],
                  z1 + offsets[f][2])
      if neighbor in cd:
        exposed[f] = False

  surf_area = 0
  for cube in cd:
    surf_area += sum([x for x in cd[cube] if x])
    
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
