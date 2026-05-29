#!/usr/bin/python3

prog = []

with open('input.txt', 'r') as instructions:
  for line in instructions:
    line = line.rstrip()
    op, val = line.split()
    prog.append([op, int(val), False]) # last items is False if the line has not been executed yet


acc = 0
pc = 0

while True:
  inst = prog[pc]
  op, val, already_executed = inst
  print(pc, acc, op, val, already_executed)

  if already_executed == True:
    break

  inst[2] = True

  if op == 'acc':
    acc += val
    pc += 1
  elif op == 'jmp':
    pc += val
  elif op == 'nop':
    pc += 1
  else:
    raise InvalidOpCode

print(acc)
