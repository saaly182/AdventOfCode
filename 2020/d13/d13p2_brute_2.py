#!/usr/bin/python3
#
# ALSO TOO SLOW...
#

with open('sample-input.txt', 'r') as f:
  t_avail_ignored = int(f.readline())
  sched = [a for a in f.readline().rstrip().split(',')]

# change sched to be int, with 'x' changed to 0
new_sched = []
for s in sched:
  if s == 'x':
    i = 0
  else:
    i = int(s)
  new_sched.append(i)
sched = tuple(new_sched)
buses = tuple([b for b in sched if b != 0])

t_min = 100000000000000
t_min = 0

# find t_start
t = t_min
while t % buses[0] != 0:
  t += 1
t_start = t
t_delta = buses[0]

t = t_start
while True:
  solved = True
  for x in range(1, len(sched)):
    if sched[x] != 0:
      if (t + x) % sched[x] != 0:
        solved = False
        break
  if solved:
    break
  t += t_delta

print(t)
