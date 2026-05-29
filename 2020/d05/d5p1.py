#!/usr/bin/python3

max_seat_id = 0
with open('input.txt', 'r') as boarding_passes:
  for line in boarding_passes:
    bp = line.rstrip()
    row = int(bp[0:7].replace('B', '1').replace('F', '0'), base=2)
    col = int(bp[7:10].replace('R', '1').replace('L', '0'), base=2)
    seat_id = 8 * row + col
    if seat_id > max_seat_id:
      max_seat_id = seat_id

print(max_seat_id)
