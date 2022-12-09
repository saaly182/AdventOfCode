#!/usr/bin/python3 -u

def part1():
  return None


def part2():
  return None


def main():
  sample_input = '''\
  '''.split('\n')

  main_input = []
  with open('input.txt') as file:
    for line in file:
      line = line.rstrip()
      main_input.append(line)

  for inp in (sample_input, main_input):
    print("Part 1 answer =", part1())
    print("Part 2 answer =", part2())


if __name__ == '__main__':
  main()
