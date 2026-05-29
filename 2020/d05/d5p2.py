#!/usr/bin/python3

seats = set()
with open('input.txt', 'r') as boarding_passes:
  for line in boarding_passes:
    bp = line.rstrip()
    row = int(bp[0:7].replace('B', '1').replace('F', '0'), base=2)
    col = int(bp[7:10].replace('R', '1').replace('L', '0'), base=2)
    seat_id = 8 * row + col
    seats.add(seat_id)

S = sorted(seats)
for x in S[:-1]:
  if (x + 1) not in seats:
    print(x + 1)
