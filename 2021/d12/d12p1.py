#!/usr/bin/python3 -u

import collections

ifile='input.txt'
pathcount = 0

def traverse(G, stack, node):
  global pathcount
  stack.append(node)
  if node == 'end':
    pathcount += 1
    return
  for n in G[node]:
    if n.isupper() or n not in stack:
      traverse(G, stack, n)
      stack.pop()


def main():
  G = collections.defaultdict(set)

  with open(ifile) as graphfile:
    for line in graphfile:
      line = line.rstrip()
      a, b = line.split('-')
      G[a].add(b)
      G[b].add(a)

  # Convert G values to sorted tuples
  Gtups = {}
  for a, b in G.items():
    Gtups[a] = tuple(sorted(b))
  G = Gtups

  stack = []

  traverse(G, stack, 'start')

  answer = pathcount
  print(answer)

if __name__ == '__main__':
  main()
