#!/usr/bin/python3

with open('input.txt') as f:
  line = f.readline()

line = line.rstrip()

prg = [int(x) for x in line.split(',')]
prg[1] = 12
prg[2] = 2

pc = 0

while prg[pc] != 99:
  op = prg[pc]

  a, b, loc = prg[prg[pc + 1]], prg[prg[pc + 2]], prg[pc + 3]

  if op == 1:
    result = a + b
  elif op == 2:
    result = a * b
  else:
    raise BadOp

  prg[loc] = result

  pc += 4

answer = prg[0]
print(answer)
