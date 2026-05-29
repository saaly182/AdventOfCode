#!/usr/bin/python3
#
# TOO SLOW...
#

def soln(s, tw):
  for ts in range(len(s)):
    b = s[ts]
    if b != 0:
      if b not in tw[ts][1]:
        return False
  return True
      

with open('input.txt', 'r') as f:
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

# Create a time window (tw) of len(sched) which is a list
# of tuples of buses leaving each time

# prime the list
offset = 100000000000000
tw = []
for t in range(offset, len(sched) + offset):
  blist = []
  for b in buses:
    if t % b == 0:
      blist.append(b)
  tw.append((t, tuple(blist)))

t += 1
while True:
  if t % 1000000 == 0:
    print(t)
  if soln(sched, tw):
    break
  tw.pop(0)
  blist = []
  for b in buses:
    if t % b == 0:
      blist.append(b)
  tw.append((t, tuple(blist)))
  t += 1

print('SOLN')
print(tw)
print('answer =',tw[0][0])
