#!/usr/bin/python3
"""
Valid passports contain all these fields:
byr (Birth Year)
iyr (Issue Year)
eyr (Expiration Year)
hgt (Height)
hcl (Hair Color)
ecl (Eye Color)
pid (Passport ID)
cid (Country ID) [OPTIONAL]
"""

valid_count = 0

def isvalidpp(fields):
  required_fields = set(('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'))
  return required_fields.issubset(fields)

with open('input.txt', 'r') as ppdb:
  found_fields = set()

  for line in ppdb:
    if line == '\n':
      if isvalidpp(found_fields):
        valid_count += 1
      found_fields = set()
    else:
      line = line.rstrip()
      kvs = line.split()
      for i in kvs:
        f = i.partition(':')[0]
        found_fields.add(f)

# process the possible last record
if isvalidpp(found_fields):
  valid_count += 1

print(valid_count)
