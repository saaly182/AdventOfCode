#!/usr/bin/python3

prog = []

with open('input.txt', 'r') as instructions:
  for line in instructions:
    line = line.rstrip()
    op, val = line.split()
    prog.append([op, int(val), False]) # last items is False if the line has not been executed yet

# Introduce a 'trm' op to terminate the program, and put it on a new last line
prog.append(['trm', 0, False])

for fixaddr in range(len(prog)):
  fixop = prog[fixaddr][0]
  if fixop not in ('jmp', 'nop'):
    continue

  # switch the op
  if fixop == 'jmp':
    prog[fixaddr][0] = 'nop'
  else:
    prog[fixaddr][0] = 'jmp'

  # reset the state
  acc = 0
  pc = 0
  for i in prog:
    i[2] = False

  while True:
    inst = prog[pc]
    op, val, already_executed = inst

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
    elif op == 'trm':
      break
    else:
      raise InvalidOpCode

  # if we broke out because of an infinite loop, then restore the program
  # to its original state and try the next repair
  if already_executed == True:
    # un-switch the op
    if fixop == 'jmp':
      prog[fixaddr][0] = 'jmp'
    else:
      prog[fixaddr][0] = 'nop'

  # if we broke because we got to 'trm', then print the acc
  if op == 'trm':
    print(acc)
    break
