#!/usr/bin/python3
"""
Valid passports:
byr (Birth Year) - four digits; at least 1920 and at most 2002.
iyr (Issue Year) - four digits; at least 2010 and at most 2020.
eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
hgt (Height) - a number followed by either cm or in:
  If cm, the number must be at least 150 and at most 193.
  If in, the number must be at least 59 and at most 76.
hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
pid (Passport ID) - a nine-digit number, including leading zeroes.
cid (Country ID) - ignored, missing or not.
"""

import re

valid_count = 0

def is_in_range(n, lo, hi):
  if not n.isnumeric():
    return False
  n = int(n)
  if n < lo or n > hi:
    return False
  return True

def isvalidpp(fields):
  required_fields = set(('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'))
  fnames = set(fields.keys())
  if not required_fields.issubset(fnames):
    return False

  if not is_in_range(fields['byr'], 1920, 2002):
    return False

  if not is_in_range(fields['iyr'], 2010, 2020):
    return False

  if not is_in_range(fields['eyr'], 2020, 2030):
    return False

  hgt = fields['hgt']
  if hgt.endswith('cm'):
    hgt = hgt[:-2]
    if not is_in_range(hgt, 150, 193):
      return False
  elif hgt.endswith('in'):
    hgt = hgt[:-2]
    if not is_in_range(hgt, 59, 76):
      return False
  else:
    return False

  if not re.match(r'^#[0-9a-f]{6}$', fields['hcl']):
    return False

  if fields['ecl'] not in set(('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')):
    return False

  if not re.match(r'^\d{9}$', fields['pid']):
    return False

  return True


with open('input.txt', 'r') as ppdb:
  found_fields = {}

  for line in ppdb:
    if line == '\n':
      if isvalidpp(found_fields):
        valid_count += 1
      found_fields = {}
    else:
      line = line.rstrip()
      kvs = line.split()
      for i in kvs:
        k, sep, v = i.partition(':')
        found_fields[k] = v

# process the possible last record
if isvalidpp(found_fields):
  valid_count += 1

print(valid_count)
