#include <stdio.h>
#include <stddef.h>
#include <string.h>
// you can write to stdout for debugging purposes, e.g.
// printf("this is a debug message\n");

//this elimination is regardless of how the original string looks and how you choose which to eliminate, the end result is allways the same. Since if you use any of the rules when possible the other options dosn't disappere it may only create more use cases of the elimination rules. An example of logical elimination in AI if I don't miss remember.

char *solution(char *S)
{
    // write your code in C99 (gcc 6.2.0)
    char *needles[3] = {"AA", "BB", "CC"};
    int keeprunning = 1, i;
    char *ptr;

    while (keeprunning) {
        for (i = 0; i < 3; i++) {
            if ((ptr = strstr(S, needles[i]))){
                break;
                 }
        }

        if (ptr == NULL)
            return S;

        if (*ptr == 'A' || *ptr == 'B' || *ptr == 'C') {
            ptr[0] = 0;
            ptr[1] = 0;
            strcpy(ptr, ptr + 2);
        } else
            keeprunning = 0;
    }
}
