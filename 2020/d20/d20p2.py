#!/usr/bin/python3 -u

import math

def ostr(S):
  "Return rev(S) if it's sorted before S, or S otherwise."
  Srev = S[::-1]
  if Srev < S:
    return Srev
  return S


def borders(T):
  "Return the four borders of T in canonical representation."
  N = ostr(get_border(T, 'N'))
  S = ostr(get_border(T, 'S'))
  E = ostr(get_border(T, 'E'))
  W = ostr(get_border(T, 'W'))

  return((N, S, E, W))


def get_border(T, side):
  "Return given border in its current order."
  if side == 'N':
    return ''.join(T[0])
  elif side == 'S':
    return ''.join(T[-1])
  elif side == 'E':
    return ''.join([x[-1] for x in T])
  elif side == 'W':
    return ''.join([x[0] for x in T])
  else:
    raise SideError


tilenum = None
tiles = {}
t2b = {}
b2t = {}

with open('input.txt', 'r') as f:
  for line in f:
    line = line.rstrip()

    if not line:
      continue

    if line.startswith('Tile '):
      tilenum = int(line.split()[1].replace(':', ''))
      tiles[tilenum] = []
    else:
      tiles[tilenum].append(line)

for t in tiles:
  bs = borders(tiles[t])
  t2b[t] = bs
  for b in bs:
    if b not in b2t:
      b2t[b] = [t]
    else:
      b2t[b].append(t)

# tuple-ize these data structures, because they should not be changed at this point
for t in t2b:
  t2b[t] = tuple(t2b[t])
for b in b2t:
  b2t[b] = tuple(b2t[b])

# From doing part 1 we know that each border pairing is unique, so we'll
# use that fact to assemble the image.

def tflip(T):
  "Flip a tile in place. Arbitrarily flip vertically."
  T.reverse()


def trotate(T):
  "Rotate a tile 90 degrees clockwise."
  u = []
  for i in range(len(T)):
    u.append(''.join([x[i] for x in reversed(T)]))

  T[:] = u


# From part 1 we know that tile 1367 is a corner tile, so we'll arbitrarily
# start with it in position (0, 0) and build onto the image from it.
t0 = 1367
# Rotate it untils its unpaired borders are N and W.
nb, sb, eb, wb = borders(tiles[t0])
nbc = len(b2t[nb])
wbc = len(b2t[wb])
while not (nbc == 1 and wbc == 1):
  trotate(tiles[t0])
  nb, sb, eb, wb = borders(tiles[t0])
  nbc = len(b2t[nb])
  wbc = len(b2t[wb])

n = int(math.sqrt(len(tiles)))
assert n * n == len(tiles)
# Image Tiles
it = [[0] * n for i in range(n)]

def print_it():
  for x in it:
    for y in x:
      if y == 0:
        print('   0', end=' ')
      else:
        print(y, end=' ')
    print()
  print()


def print_t(T):
  for x in T:
    print(x)
  print()


def print_image():
  for x in image:
    print(x)
  print()


for r in range(n):
  for c in range(n):

    # upper-left tile already declared and oriented
    if r == 0 and c == 0:
      it[r][c] = t0
      continue

    # In column 0 we must match on the tile to our north
    if c == 0:
      # 1 = canonical border order
      # 2 = actual border order
      t_north = it[r - 1][c]
      bmatch1 = borders(tiles[t_north])[1]
      bmatch2 = get_border(tiles[t_north], 'S')
      t = list(b2t[bmatch1])
      t.remove(t_north)
      t = t[0]
      nb1, sb1, eb1, wb1 = borders(tiles[t])
      nb2 = get_border(tiles[t], 'N')
      sb2 = get_border(tiles[t], 'S')
      eb2 = get_border(tiles[t], 'E')
      wb2 = get_border(tiles[t], 'W')

      # now orient the tile properly
      if nb1 == bmatch1:
        if nb2 != bmatch2:
          trotate(tiles[t])
          tflip(tiles[t])
          trotate(tiles[t])
          trotate(tiles[t])
          trotate(tiles[t])
      elif sb1 == bmatch1:
        trotate(tiles[t])
        if sb2 == bmatch2:
          tflip(tiles[t])
        trotate(tiles[t])
      elif eb1 == bmatch1:
        if eb2 != bmatch2:
          tflip(tiles[t])
        trotate(tiles[t])
        trotate(tiles[t])
        trotate(tiles[t])
      elif wb1 == bmatch1:
        if wb2 == bmatch2:
          tflip(tiles[t])
        trotate(tiles[t])
      else:
        raise BorderError

      # finally record the tile num in "it"
      it[r][c] = t

      continue

    # All other tiles are matched on the tile to our west
    # 1 = canonical border order
    # 2 = actual border order
    t_west = it[r][c - 1]
    bmatch1 = borders(tiles[t_west])[2]
    bmatch2 = get_border(tiles[t_west], 'E')
    t = list(b2t[bmatch1])
    t.remove(t_west)
    t = t[0]
    nb1, sb1, eb1, wb1 = borders(tiles[t])
    nb2 = get_border(tiles[t], 'N')
    sb2 = get_border(tiles[t], 'S')
    eb2 = get_border(tiles[t], 'E')
    wb2 = get_border(tiles[t], 'W')

    # now orient the tile properly
    if nb1 == bmatch1:
      trotate(tiles[t])
      if nb2 == bmatch2:
        tflip(tiles[t])
      trotate(tiles[t])
      trotate(tiles[t])
    elif sb1 == bmatch1:
      trotate(tiles[t])
      if sb2 != bmatch2:
        tflip(tiles[t])
    elif eb1 == bmatch1:
      if eb2 == bmatch2:
        tflip(tiles[t])
      trotate(tiles[t])
      trotate(tiles[t])
    elif wb1 == bmatch1:
      if wb2 != bmatch2:
        tflip(tiles[t])
    else:
      raise BorderError

    # finally record the tile num in "it"
    it[r][c] = t

# "it" now contains the tile numbers in the right order, and
# the tiles have been oriented properly.
# print_it()

tsize = len(tiles[t0]) - 2
image = [[] for i in range(tsize * len(it))]
r_img = 0

# create image according to the problem statement
for a in it:
  for r_tile in range(1, tsize + 1):
    for t in a:
      S = tiles[t][r_tile][1:-1]
      image[r_img].append(S)
    r_img += 1

# refactor image to be a list of strings
image2 = []
for x in image:
  image2.append(''.join(x))
image = image2
print('Original Image')
print_image()

# The problem statement suggests that there's only
# one orientation of the image that will find any
# monsters.
monster = [
    '                  # ',
    '#    ##    ##    ###',
    ' #  #  #  #  #  #   ',
]

mcoords = []
monw = len(monster[0])  # monster width
monh = len(monster)     # monster height
for r in range(monh):
  for c in range(monw):
    if monster[r][c] == '#':
      mcoords.append((r, c))
mcoords = tuple(mcoords)

def monsearch():
  found_monsters = False
  for r in range(len(image) - monh + 1):
    for c in range(len(image[0]) - monw + 1):
      # create a window into the image that is the same size as the monster
      iwin = []
      for wr in range(monh):
        iwin.append(image[r + wr][c:c + monw])
      found = True
      for x, y in mcoords:
        if iwin[x][y] == '.':
          found = False
          break
      if found:
        found_monsters = True
        # convert the monsters to Os
        for x, y in mcoords:
          # super inefficient...
          z = list(image[r + x])
          z[c + y] = 'O'
          image[r + x ] = ''.join(z)

  return found_monsters

rotate_count = 0

while not monsearch():
  trotate(image)
  rotate_count += 1
  if rotate_count == 4:
    tflip(image)
  if rotate_count > 7:
    raise MonsterProblems

print('Monster Image')
print_image()

# Now just need to count up the remaining #s in the image
remaining_hashes = sum([x.count('#') for x in image])
print('ANSWER:', remaining_hashes)
