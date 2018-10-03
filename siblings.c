#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char str[6];
char temp[6];
char *end;
unsigned i;
int walker;

int solution(int N)
{
    sprintf(str, "%d", N);
    printf("str:%s\n", str);
    int nbr = 10;
    walker = 0;

    while (nbr--) {
        for (i = 0; i < strlen(str); i++)
            if (*(str + i) == (char)(nbr + '0')) {
                strcpy(str + i, str + i + 1);
                temp[walker++] = (char)(nbr + '0');
                i--;
            }
    }

    return strtol(temp, &end, 10);
}


int main(int argc, char const *argv[])
{
    printf("%d\n", solution(3065));
    return 0;
}
