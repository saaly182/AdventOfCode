#!/usr/bin/python3
"""
- It is a six-digit number.
- The value is within the range given in your puzzle input.
- Two adjacent digits are the same (like 22 in 122345).
- Going from left to right, the digits never decrease; they only ever
  increase or stay the same (like 111123 or 135679).
- Within range 254032-789860
- The two adjacent matching digits are not part of a larger group
  of matching digits.
"""

pmin = 254032
pmax = 789860

def adjcheck(s):
  """Return True if s has two adj digits that are not part of a larger group."""
  d = s[0]
  groupsize = 1
  i = 1
  while i < len(s):
    if s[i] == d:
      groupsize += 1
    else:
      if groupsize == 2:
        return True
      else:
        d = s[i]
        groupsize = 1
    i += 1

  # handles the last two digits
  if groupsize == 2:
    return True

  return False


def is_valid_pw(p):
  s = str(p)

  if len(s) != 6:
    return False

  if p < pmin or p > pmax:
    return False

  for i in range(len(s) - 1):
    if s[i] > s[i + 1]:
      return False

  if not adjcheck(s):
    return False

  return True


valid_count = 0
for p in range(pmin, pmax + 1):
  if is_valid_pw(p):
    valid_count += 1

answer = valid_count
print(answer)
