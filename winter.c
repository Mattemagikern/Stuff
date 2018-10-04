//after winter comes summer,
//Find the shortest winter,
//Def winter: all subsecuently numbers are higher than this number.
unsigned indx;
unsigned i;
int solution(int T[], int N)
{
    unsigned walker = N;
    indx = N-1;

    while (walker--) {
        int max = T[0], min = T[N - 1];

        for (i = 1 ; i < walker; i++) {
            if (max < T[i])
                max = T[i];
        }

        for (i = walker; i < N; i++) {
            if (min > T[i])
                min = T[i];
        }

        if (!(T[walker] < max) && !(min < T[walker]))
            indx = walker;
    }

    return indx;
}

int main(int argc, char const *argv[])
{
    int T[8] = {-5, -5, -5, -42, 6, -5 , 6, 12};
    printf("sol: %d\n", solution(T, 8));
    return 0;
}
