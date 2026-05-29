#!/usr/bin/python3
# See https://www.geeksforgeeks.org/expression-evaluation/

def applyop(a, b, op):
  if op == '*':
    return a * b
  elif op == '+':
    return a + b
  else:
    raise InvalidOp

def evaluate(e):
  val_stack = []
  op_stack = []
  
  for t in e:
    if t.isdigit():
      val_stack.append(int(t))
    elif t == '(':
      op_stack.append(t)
    elif t == ')':
      while op_stack[-1] != '(':
        a = val_stack.pop()
        b = val_stack.pop()
        op = op_stack.pop()
        val_stack.append(applyop(a, b, op))
      op_stack.pop()  # pop the left-paren
    elif t in ('*', '+'):
      while op_stack and op_stack[-1] != '(':
        a = val_stack.pop()
        b = val_stack.pop()
        op = op_stack.pop()
        val_stack.append(applyop(a, b, op))
      op_stack.append(t)
    else:
      raise InvalideToken

  while op_stack:
    a = val_stack.pop()
    b = val_stack.pop()
    op = op_stack.pop()
    val_stack.append(applyop(a, b, op))

  assert len(val_stack) == 1

  return val_stack[0]


expressions = []

with open('input.txt', 'r') as f:
  for line in f:
    line = line.rstrip()
    line = line.replace('(', ' ( ').replace(')', ' ) ')
    expressions.append(tuple(line.split()))

expressions = tuple(expressions)

print(sum([evaluate(e) for e in expressions]))
