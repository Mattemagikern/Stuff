#include <stdio.h>
#include <string.h>

struct pos {
    char x, y;
};

int possible_moves(char **B, int N, struct pos jafar,
                   struct pos *possible_moves)
{
    int i = 0, j = 0;

    if (!(jafar.x < N - 1 || jafar.y < N - 1))
        return 0;

    if (jafar.x - 2 > 0 && jafar.y - 2 > 0 && B[jafar.x - 2][jafar.y - 2] == '.' &&
        B[jafar.x - 1][jafar.y - 1] == 'X') {
        possible_moves[i].x = jafar.x - 2;
        possible_moves[i++].y = jafar.y - 2;
    }

    if (jafar.x - 2 > 0 && jafar.y + 2 < N && B[jafar.x - 2][jafar.y + 2] == '.' &&
        B[jafar.x - 1][jafar.y + 1] == 'X') {
        possible_moves[i].x = jafar.x - 2;
        possible_moves[i++].y = jafar.y + 2;
    }

    return i;
}

int  recursion(char **B, int N, struct pos jafar)
{
    int temp1, temp2, nbr_move = 0;
    struct pos moves[N];

    if ((nbr_move = possible_moves(B, N, jafar, moves))) {
        if (nbr_move > 1) {
            temp1 = recursion(B, N, moves[0]);
            temp2 = recursion(B, N, moves[1]);
            return temp1 > temp2 ? temp1 + 1 : temp2 + 1;
        } else
            return recursion(B, N, moves[0]) + 1;
    } else
        return 0;
}
int solution(char *B[], int N)
{
    // write your code in C99 (gcc 6.2.0)
    int i, index, nbr_move, max_moves = 0;
    char *ptr;
    struct pos jafar;

    for (i = 0; i < N; i++) {
        ptr = strstr(B[i], "O");

        if (ptr)
            break;
    }

    if (!ptr || i < 2)
        return 0;

    jafar.x = i;
    jafar.y = ptr - B[i];
    return recursion(B, N, jafar);
}


int main(int argc, char const *argv[])
{
    char *B[6];
    B[0] = "..X...";
    B[1] = "......";
    B[2] = "....X.";
    B[3] = ".X....";
    B[4] = "..X.X.";
    B[5] = "...O..";
    printf("%d\n", solution(B, 6));
    return 0;
}
