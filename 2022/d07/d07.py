#!/usr/bin/python3 -u

def part1(rd):
  limit = 100000
  dsum = 0

  q = [rd]
  while q:
    d = q.pop(0)
    tsd = d.treesize()
    if tsd <= limit:
      dsum  += tsd
    q.extend(d.getsubdirs())
  return dsum


def part2(rd):
  disk_size = 70000000
  free_target = 30000000
  free_current = disk_size - rd.treesize()
  must_delete = free_target - free_current

  best_dir_size = disk_size
  q = [rd]
  while q:
    d = q.pop(0)
    tsd = d.treesize()
    if tsd >= must_delete and tsd < best_dir_size:
      best_dir_size = tsd
    q.extend(d.getsubdirs())
  return best_dir_size


class Directory:
  def __init__(self, path, parent):
    self.path = path
    self.parent = parent
    self.files = []
    self.subdirs = {}
    self.filebytes = 0

  def addfile(self, filerecord):
    assert filerecord not in self.files
    self.files.append(filerecord)
    self.filebytes += filerecord[2]

  def addsubdir(self, dirrecord):
    assert dirrecord not in self.subdirs
    self.subdirs[dirrecord[1]] = Directory(f'{self.path}/{dirrecord[1]}', self)

  def show(self, indent):
    print(f'{" " * indent}- {self.path} (dir)')
    for d in self.subdirs:
      self.subdirs[d].show(indent + 2)
    for f in self.files:
      name = f[1]
      size = f[2]
      print(f'{" " * (indent + 2)}- {name} {size}')

  def treesize(self):
    'Return total subdirectory tree size for this dir.'
    ts = self.filebytes + sum([d.treesize() for d in self.getsubdirs()])
    return ts

  def getsubdirs(self):
    return [self.subdirs[d] for d in self.subdirs]


def buildfs(fname):
  term = []
  with open(fname) as file:
    for line in file:
      line = line.rstrip()
      tokens = line.split()
      if tokens[0] == '$':
        term.append(tuple(tokens[1:]))
      elif tokens[0] == 'dir':
        term.append(tuple(tokens))
      else:
        term.append(('file', tokens[1], int(tokens[0])))

  rootdir = Directory('/', None)
  curdir = rootdir
  # the input pretty much has to begin with "$ cd /",
  # so just don't parse the first line
  for t in term[1:]:
    if t[0] == 'ls':
      pass
    elif t[0] == 'file':
      curdir.addfile(t)
    elif t[0] == 'dir':
      curdir.addsubdir(t)
    elif t[0] == 'cd':
      if t[1] == '..':
        curdir = curdir.parent
      else:
        curdir = curdir.subdirs[t[1]]
    else:
      raise ValueError

  return rootdir
      

def main():
  rootdir = buildfs('input.txt')

  print("Part 1 answer =", part1(rootdir))
  print("Part 2 answer =", part2(rootdir))


if __name__ == '__main__':
  main()
