#include <stdio.h>

void show(int line, int a, int b, int c, int e, int f) {
    printf("line %3d, a=%d b=%d c=%d e=%d f=%d\n",
            line, a, b, c, e, f);
    return;
}

int main(void) {
/***
 
Implement this pseudo code:

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
***/
    int a, b, c, e, f;

    setvbuf(stdout, NULL, _IONBF, 0);

    a = 0;
    b = c = e = f = 0;

    e = 123;
L01:
    e = e & 456;
    if (e == 72) {
        show(__LINE__, a, b, c, e, f);
        goto L05;
    }
    show(__LINE__, a, b, c, e, f);
    goto L01;
L05:
    e = 0;
L06:
    b = e | 65536;
    e = 678134;
L08:
    f = b & 255;
    e = e + f;
    e = e & 16777215;
    e = e * 65899;
    e = e & 16777215;
    if (b < 256) {
        show(__LINE__, a, b, c, e, f);
        goto L16;
    }
    show(__LINE__, a, b, c, e, f);
    goto L17;
L16:
    show(__LINE__, a, b, c, e, f);
    goto L28;
L17:
    f = 0;
L18:
    c = f + 1;
    c = c * 256;
    if (c > b) {
        show(__LINE__, a, b, c, e, f);
        goto L23;
    }
    show(__LINE__, a, b, c, e, f);
    goto L24;
L23:
    show(__LINE__, a, b, c, e, f);
    goto L26;
L24:
    f = f + 1;
    show(__LINE__, a, b, c, e, f);
    goto L18;
L26:
    b = f;
    show(__LINE__, a, b, c, e, f);
    goto L08;
L28:
    if (e == a) {
        show(__LINE__, a, b, c, e, f);
        goto LHALT;
    }
    show(__LINE__, a, b, c, e, f);
    goto L06;

LHALT:
    printf("HALTED!\n");
    return 0;
}

