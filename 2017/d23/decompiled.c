#include <stdio.h>

long a, b, c, d, e, f, g1, g2, g3, g4, h;

int main() {
    a = 1;
    b = c = d = e = f = g1 = g2 = g3 = g4 = h = 0;
    b = 67;
    c = b;
    if (a != 0) {
        b = b * 100 + 100000;
        c = b + 17000;
    }

    printf("a=%ld b=%ld c=%ld d=%ld e=%ld f=%ld g1=%ld g2=%ld g3=%ld g4=%ld h=%ld\n", a, b, c, d, e, f, g1, g2, g3, g4, h);
    while (1) {
        f = 1;
        d = 2;
        while (1) {
            e = 2;

            while (1) {
                g1 = d * e - b;
                if (g1 == 0) {
                    f = 0;
                }
                e += 1;
                g2 = e - b;
                if (g2 == 0) {
                    break;
                }
            }  // end-while

            d += 1;
            g3 = d - b;
            if (g3 == 0) {
                break;
            }
        }  // end-while

        if (f == 0) {
            h += 1;
        }

        g4 = b - c;
        if (g4 == 0) {
            break;
        }
        b += 17;

        printf("a=%ld b=%ld c=%ld d=%ld e=%ld f=%ld g1=%ld g2=%ld g3=%ld g4=%ld h=%ld\n", a, b, c, d, e, f, g1, g2, g3, g4, h);
    }  // end-while

    printf("DONE: a=%ld b=%ld c=%ld d=%ld e=%ld f=%ld g1=%ld g2=%ld g3=%ld g4=%ld h=%ld\n", a, b, c, d, e, f, g1, g2, g3, g4, h);
    return 0;
}
