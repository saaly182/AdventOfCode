#!/usr/bin/python3
"""
- It is a six-digit number.
- The value is within the range given in your puzzle input.
- Two adjacent digits are the same (like 22 in 122345).
- Going from left to right, the digits never decrease; they only ever
  increase or stay the same (like 111123 or 135679).
- Within range 254032-789860
"""

pmin = 254032
pmax = 789860

def is_valid_pw(p):
  s = str(p)

  if len(s) != 6:
    return False

  if p < pmin or p > pmax:
    return False

  # Check both adjacency and increasing criteria during the same loop
  adjfound = False
  for i in range(len(s) - 1):
    if s[i] > s[i + 1]:
      return False
    if s[i] == s[i + 1]:
      adjfound = True
  if not adjfound:
    return False

  return True


valid_count = 0
for p in range(pmin, pmax + 1):
  if is_valid_pw(p):
    valid_count += 1

answer = valid_count
print(answer)
