#include <stdio.h>

void show(int line, int a, int b, int c, int e, int f) {
    printf("line %3d, a=%d b=%d c=%d e=%d f=%d\n",
            line, a, b, c, e, f);
    return;
}

int main(void) {
    int a, b, c, e, f;

    setvbuf(stdout, NULL, _IONBF, 0);

    a = 0;
    b = c = e = f = 0;

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
        goto L28;  /* FORWARD */
    }
    f = 0;
L18:
    c = f + 1;
    c = c * 256;
    if (c > b) {
        show(__LINE__, a, b, c, e, f);
        goto L26;  /* FORWARD */
    }
    f = f + 1;
    show(__LINE__, a, b, c, e, f);
    goto L18;  /* BACK */
L26:
    b = f;
    show(__LINE__, a, b, c, e, f);
    goto L08;  /* BACK */
L28:
    if (e == a) {
        show(__LINE__, a, b, c, e, f);
        goto LHALT;  /* FORWARD */
    }
    show(__LINE__, a, b, c, e, f);
    goto L06;  /* BACK */

LHALT:
    printf("HALTED!\n");
    return 0;
}

