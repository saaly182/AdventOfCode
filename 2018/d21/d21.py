#!/usr/bin/python3 -u

def part1() -> int:
    """
    I started with the naive approach of running the input program with
    increasing values of register[0] on the off chance that this specific
    halting-problem might be simple for part 1. But it's quickly obvious
    that this is not a "toy" halting-problem. So I've switched to
    hand-decompling the input code using the decompile() function in Day 19's
    program.

    Here's the output of decompile() for my input:

     0 (seti 123  0  4):      e = 123
     1 (bani  4 456  4):      e = e & 456
     2 (eqri  4 72  4):       e = 1 if e == 72 else 0
     3 (addr  4  3  3):       ip = e + ip
     4 (seti  0  0  3):       ip = 0
     5 (seti  0  6  4):       e = 0
     6 (bori  4 65536  1):    b = e | 65536
     7 (seti 678134  1  4):   e = 678134
     8 (bani  1 255  5):      f = b & 255
     9 (addr  4  5  4):       e = e + f
    10 (bani  4 16777215  4): e = e & 16777215
    11 (muli  4 65899  4):    e = e * 65899
    12 (bani  4 16777215  4): e = e & 16777215
    13 (gtir 256  1  5):      f = 1 if 256 > b else 0
    14 (addr  5  3  3):       ip = f + ip
    15 (addi  3  1  3):       ip = ip + 1
    16 (seti 27  8  3):       ip = 27
    17 (seti  0  1  5):       f = 0
    18 (addi  5  1  2):       c = f + 1
    19 (muli  2 256  2):      c = c * 256
    20 (gtrr  2  1  2):       c = 1 if c > b else 0
    21 (addr  2  3  3):       ip = c + ip
    22 (addi  3  1  3):       ip = ip + 1
    23 (seti 25  7  3):       ip = 25
    24 (addi  5  1  5):       f = f + 1
    25 (seti 17  1  3):       ip = 17
    26 (setr  5  3  1):       b = f
    27 (seti  7  8  3):       ip = 7
    28 (eqrr  4  0  5):       f = 1 if e == a else 0
    29 (addr  5  3  3):       ip = f + ip
    30 (seti  5  4  3):       ip = 5

    ====================================================================

    Hand-manipulated decompiled code, phase 1:

     0 (seti 123  0  4):      e = 123
L01  1 (bani  4 456  4):      e = e & 456
     2 (eqri  4 72  4):       IF e == 72:
     3 (addr  4  3  3):         GOTO L05
     4 (seti  0  0  3):       GOTO L01
L05  5 (seti  0  6  4):       e = 0
L06  6 (bori  4 65536  1):    b = e | 65536
     7 (seti 678134  1  4):   e = 678134
L08  8 (bani  1 255  5):      f = b & 255
     9 (addr  4  5  4):       e = e + f
    10 (bani  4 16777215  4): e = e & 16777215
    11 (muli  4 65899  4):    e = e * 65899
    12 (bani  4 16777215  4): e = e & 16777215
    13 (gtir 256  1  5):      IF b < 256:
    14 (addr  5  3  3):           GOTO L16
    15 (addi  3  1  3):       GOTO L17
L16 16 (seti 27  8  3):       GOTO L28
L17 17 (seti  0  1  5):       f = 0
L18 18 (addi  5  1  2):       c = f + 1
    19 (muli  2 256  2):      c = c * 256
    20 (gtrr  2  1  2):       IF c > b:
    21 (addr  2  3  3):           GOTO L23
    22 (addi  3  1  3):       GOTO L24
L23 23 (seti 25  7  3):       GOTO L26
L24 24 (addi  5  1  5):       f = f + 1
    25 (seti 17  1  3):       GOTO L18
L26 26 (setr  5  3  1):       b = f
    27 (seti  7  8  3):       GOTO L08
L28 28 (eqrr  4  0  5):       IF e == a:
    29 (addr  5  3  3):           GOTO LHALT
    30 (seti  5  4  3):       GOTO L06
LHALT

    ====================================================================
    I created some iterations of the code above in C. See the part1_1.c
    and part1_2.c files in this directory. From there I produced this
    Python code as a "decompiled" version of my input:

    a = 0
    b = c = e = f = 0
    while True:
        b = e | 65536
        e = 678134
        while True:
            f = b & 255
            e = e + f
            e = e & 16777215
            e = e * 65899
            e = e & 16777215
            if b < 256:
                if e == a:
                    assert False  # HALT
                else:
                    break
            f = 0
            c = (f + 1) * 256
            while c <= b:
                f += 1
                c = (f + 1) * 256
            b = f

    ====================================================================
    The python above ultimately simplifies down to:

    a = 0
    b = c = e = f = 0
    done = False
    while not done:
        b = e | 65536
        e = 678134
        while True:
            f = b & 255
            e = e + f
            e = e & 16777215
            e = e * 65899
            e = e & 16777215
            if b < 256:
                if e == a:
                    done = True
                break
            b //= 256

    """
    e = 0
    b = e | 65536
    e = 678134
    while True:
        f = b & 255
        e = e + f
        e = e & 16777215
        e = e * 65899
        e = e & 16777215
        if b < 256:
            answer = e
            break
        b //= 256    
    return answer


def part2() -> int:
    """
    The outer while loop state is only dependent on `e`, so once we see
    a repeated value of `e` we'll be in an infinite loop. So we want the `e`
    value that occurs immediately before the first repeat value.

    Note that the logic here is guaranteed to terminate because e is bounded
    by the "e = e & 16777215" lines. An eventual repeat of e is guaranteed by
    the pigeonhole principle.
    """
    e = 0
    seen = set()
    repeat_found = False
    answer = -99
    while not repeat_found:
        b = e | 65536  # 2**16
        e = 678134
        while True:
            f = b & 255
            e = e + f
            e = e & 16777215
            e = e * 65899
            e = e & 16777215  # 2**24 - 1
            if b < 256:
                if e in seen:
                    repeat_found = True
                else:
                    answer = e  # continuously track the previous `e`
                seen.add(e)
                break
            b //= 256
    return answer


def main():
    print("Part 1 answer =", part1())
    print("Part 2 answer =", part2())
    print()


if __name__ == '__main__':
    main()
