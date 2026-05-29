#!/usr/bin/python3

with open('input.txt', 'r') as f:
  t_avail = int(f.readline())
  buses = [int(a) for a in f.readline().rstrip().split(',') if a != 'x']

t = 0
while True:
  b_now = []
  for b in buses:
    if t % b == 0:
      b_now.append(b)
  if t >= t_avail and b_now:
    break
  t += 1

print('t_avail = {}, t_now = {}, buses leaving = {}'.format(t_avail, t, b_now))
answer = b_now[0] * (t - t_avail)
print('answer =', answer)
