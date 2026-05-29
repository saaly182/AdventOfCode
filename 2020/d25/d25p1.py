#!/usr/bin/python3

def transform(snum, smax, loops):
  T = 1
  for i in range(loops):
    T = (T * snum) % smax
  return T

pk1 = 2084668
pk2 = 3704642
snum = 7
smax = 20201227

secloops1 = 0
secloops2 = 0
loops = 1
T = 1

while secloops1 == 0 or secloops2 == 0:
  T = (T * snum) % smax
  if T == pk1:
    secloops1 = loops
  if T == pk2:
    secloops2 = loops

  loops += 1

x1 = transform(pk1, smax, secloops2)
x2 = transform(pk2, smax, secloops1)
assert x1 == x2

answer = x1
print(answer)
