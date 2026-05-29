#!/usr/bin/python3

with open('input.txt') as f:
  line = f.readline()

line = line.rstrip()

mem_image = [int(x) for x in line.split(',')]
target_output = 19690720

def find_inp():
  for inp1 in range(100):
    for inp2 in range(100):

      # reset the machine
      mem = mem_image[:]
      pc = 0

      mem[1] = inp1
      mem[2] = inp2

      while mem[pc] != 99:
        op = mem[pc]

        a, b, loc = mem[mem[pc + 1]], mem[mem[pc + 2]], mem[pc + 3]

        if op == 1:
          result = a + b
        elif op == 2:
          result = a * b
        else:
          raise BadOp

        mem[loc] = result

        pc += 4

      output = mem[0]

      if output == target_output:
        return (inp1, inp2)

  return None

i1, i2 = find_inp()
answer = 100 * i1 + i2
print(answer)
