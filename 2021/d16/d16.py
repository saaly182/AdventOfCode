#!/usr/bin/python3 -u
"""
AOC 2021 Day 16

(Took lots of hints from https://github.com/viliampucik/adventofcode/blob/master/2021/16.py)

Literal values (type ID 4) represent a single number as described above. The remaining type IDs are more interesting:

Packets with type ID 0 are sum packets - their value is the sum of
the values of their sub-packets. If they only have a single sub-packet,
their value is the value of the sub-packet.

Packets with type ID 1 are product packets - their value is the
result of multiplying together the values of their sub-packets. If
they only have a single sub-packet, their value is the value of the
sub-packet.

Packets with type ID 2 are minimum packets - their value is the
minimum of the values of their sub-packets.

Packets with type ID 3 are maximum packets - their value is the
maximum of the values of their sub-packets.

Packets with type ID 5 are greater than packets - their value is 1
if the value of the first sub-packet is greater than the value of
the second sub-packet; otherwise, their value is 0. These packets
always have exactly two sub-packets.

Packets with type ID 6 are less than packets - their value is 1 if
the value of the first sub-packet is less than the value of the
second sub-packet; otherwise, their value is 0. These packets always
have exactly two sub-packets.

Packets with type ID 7 are equal to packets - their value is 1 if
the value of the first sub-packet is equal to the value of the
second sub-packet; otherwise, their value is 0. These packets always
have exactly two sub-packets.
"""

debug = False 


def hex2bin(h):
  """
  Convert hex string to binary string.

  Needed because regular bin() does not maintain leading zeros
  """
  hb = {
      '0': '0000', '1': '0001', '2': '0010', '3': '0011',
      '4': '0100', '5': '0101', '6': '0110', '7': '0111',
      '8': '1000', '9': '1001', 'A': '1010', 'B': '1011',
      'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111',
  }
  return ''.join([hb[x] for x in h])


def getbits(m):
  return list(hex2bin(m))


def read_bint(b, count):
  "Pop count bits from the front of b and return the value of that binary int."
  val = int(''.join(b[:count]), 2)
  del b[:count]
  return val


def applyop(ptype, vals):
  if ptype == 0:
    return sum(vals)
  elif ptype == 1:
    r = 1
    for x in vals:
      r *= x
    return r
  elif ptype == 2:
    return min(vals)
  elif ptype == 3:
    return max(vals)
  elif ptype == 5:
    if vals[0] > vals[1]:
      return 1
    return 0
  elif ptype == 6:
    if vals[0] < vals[1]:
      return 1
    return 0
  elif ptype == 7:
    if vals[0] == vals[1]:
      return 1
    return 0
  else:
    raise ValueError(ptype)


def packet(b):
  if debug:
    print('In packet(), bits =', ''.join(b))

  ver = read_bint(b, 3)
  versum = ver
  ptype = read_bint(b, 3)
  val = -1

  if ptype == 4:
    more = read_bint(b, 1)
    val = read_bint(b, 4)
    while more:
      more = read_bint(b, 1)
      val = val << 4 | read_bint(b, 4)
  else:
    length_type_id = read_bint(b, 1)
    subvals = []
    if length_type_id == 0:
      pkt_bits = read_bint(b, 15)
      # keep parsing new pkts until we've consumed the correct number of bits
      blen1 = len(b)
      while (blen1 - len(b)) != pkt_bits:
        subversum, subval = packet(b)
        versum += subversum
        subvals.append(subval)
    elif length_type_id == 1:
      pkt_cnt = read_bint(b, 11)
      for _ in range(pkt_cnt):
        subversum, subval = packet(b)
        versum += subversum
        subvals.append(subval)
    else:
      raise ValueError(length_type_id)
    val = applyop(ptype, subvals)

  return versum, val


def main():
  with open('input.txt') as transmissions:
    for line in transmissions:
      msg = line.rstrip()
      bits = getbits(msg)
      if debug:
        print('--\nNew Case', msg, bits)
      versum, value = packet(bits)
      print('part 1, versum =', versum)
      print('part 2, value =', value)


if __name__ == '__main__':
  main()
