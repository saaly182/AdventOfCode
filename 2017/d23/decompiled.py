#!/usr/bin/pypy3 -u
"""
     0	set b 67
     1	set c b
     2	jnz a 2
     3	jnz 1 5
     4	mul b 100
     5	sub b -100000
     6	set c b
     7	sub c -17000
     8	set f 1
     9	set d 2
    10	set e 2

    11	set g d
    12	mul g e
    13	sub g b
    14	jnz g 2
    15	set f 0
    16	sub e -1
    17	set g e
    18	sub g b
    19	jnz g -8

    20	sub d -1
    21	set g d
    22	sub g b
    23	jnz g -13

    24	jnz f 2
    25	sub h -1
    26	set g b
    27	sub g c
    28	jnz g 2
    29	jnz 1 3
    30	sub b -17
    31	jnz 1 -23
"""

a = 1
b = c = d = e = f = g1 = g2 = g3 = g4 = h = 0
b = 67
c = b
if a != 0:
    b = b * 100 + 100000
    c = b + 17000

print(f'{a=} {b=} {c=} {d=} {e=} {f=} {g1=} {g2=} {g3=} {g4=} {h=}')
while True:  #L31
    f = 1
    d = 2
    while True:  #L23
        e = 2

        while True:  #L19
            g1 = d * e - b
            if g1 == 0:
                f = 0
            e += 1
            g2 = e - b
            if g2 == 0:
                break

        d += 1
        g3 = d - b
        if g3 == 0:
            break

    if f == 0:
        h += 1
    g4 = b - c
    if g4 == 0:
        break
    b += 17

    print(f'{a=} {b=} {c=} {d=} {e=} {f=} {g1=} {g2=} {g3=} {g4=} {h=}')

print(f'DONE: {a=} {b=} {c=} {d=} {e=} {f=} {g1=} {g2=} {g3=} {g4=} {h=}')
